import sys
import os
import base64
import re
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QStackedWidget, QLineEdit, QMessageBox,QSizePolicy,QGraphicsOpacityEffect
from PyQt5.QtGui import QFont, QColor, QPalette,QPixmap,QLinearGradient
from PyQt5.QtCore import Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import webbrowser
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QDialog
from datetime import datetime
from PyQt5.QtWidgets import QScrollArea,QGridLayout
from PyQt5.QtWidgets import QFrame
from .config import GOOGLE_CLASSROOM_SCOPES as SCOPES
from . import link_service

class CustomWebEnginePage(QWebEnginePage):
    def __init__(self, parent=None):
        super().__init__(parent)

    def acceptNavigationRequest(self, url, _type, isMainFrame):
        if _type == QWebEnginePage.NavigationTypeLinkClicked:
            url_str = url.toString()
            print(f"Navigating to: {url_str}")

            # ตรวจสอบว่าลิงก์เป็นแบบแปลงหรือไม่
            if url_str.startswith('https://www.oems//'):
                self.prompt_for_code(url_str)  # เรียแร้ช้ฟังก์ชันเพื่อขอรหัส unique_code
                return False  # หยุดการทำงานของ QWebEngineView

            # เปิดลิงก์ใน QWebEngineView
            self.view().setUrl(url)
            return False

        return super().acceptNavigationRequest(url, _type, isMainFrame)

    def prompt_for_code(self, encoded_link):
        code_dialog = UniqueCodeDialog(encoded_link, self.view())  # ส่ง QWebEngineView
        code_dialog.exec_()

    def decode_custom_link(self, url_str):
        encoded_str = url_str[len('https://www.oems//'):]
        decoded_bytes = base64.urlsafe_b64decode(encoded_str)
        decoded_link = decoded_bytes.decode('utf-8')
        print(f"Decoded link: {decoded_link}")
        return decoded_link

class UniqueCodeDialog(QDialog):
    def __init__(self, encoded_link, web_view, parent=None):
        super().__init__(parent)
        self.encoded_link = encoded_link
        self.web_view = web_view
        self.setWindowTitle("กรุณาใส่รหัส")
        self.setGeometry(100, 100, 300, 150)

        # ตั้งค่า dialog ให้เป็น modal และอยู่ด้านบนสุดเสมอ
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        # เลเอาต์
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # ช่องกรอกสำหรับรหัส unique code
        self.code_input = QLineEdit(self)
        self.code_input.setPlaceholderText("กรุณาใส่รหัส")
        self.code_input.setStyleSheet("padding: 10px; border: 1px solid #007BFF; border-radius: 5px; font-size: 14px;")
        self.layout.addWidget(self.code_input)

        # ปุ่มสำหรับตรวจสอบรหัส
        validate_button = QPushButton("ตรวจสอบรหัส")
        validate_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px; font-size: 16px; border: none;")
        validate_button.setCursor(Qt.PointingHandCursor)
        validate_button.clicked.connect(self.validate_code)
        self.layout.addWidget(validate_button)

        # ทำเลเอาต์ dialog แสดงอยู่ด้านบนและได้รับการโฟกัส
        self.raise_()
        self.activateWindow()

    def validate_code(self):
        unique_code = self.code_input.text()
        if unique_code:
            if self.check_code_in_database(unique_code):
                original_link = self.decode_link(self.encoded_link)
                self.web_view.setUrl(QUrl(original_link))
                self.close()
            else:
                QMessageBox.warning(self, "รหัสไม่ถูกต้อง", "รหัส unique code ไม่ถูกต้อง กรุณาลองอีกครั้ง.")
        else:
            QMessageBox.warning(self, "ต้องกรอกข้อมูล", "กรุณาใส่รหัส unique code.")

    def check_code_in_database(self, unique_code):
        try:
            return link_service.check_code_exists(unique_code)
        except Exception as err:
            QMessageBox.critical(self, "ข้อผิดพลาด", f"เกิดข้อผิดพลาดในการเชื่อมต่อฐานข้อมูล: {err}")
            return False

    def decode_link(self, encoded_link):
        return link_service.decode_link(encoded_link)
    
class AssignmentDetails(QWidget):
    def __init__(self, assignment, service, parent=None):
        super().__init__(parent)
        self.assignment = assignment
        self.service = service
        self.parent = parent

        # ตั้งค่าเลเอาต์
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # WebView สำหรับแสดงรายละเอียดของการบ้าน
        self.web_view = QWebEngineView()
        self.web_page = CustomWebEnginePage(self.web_view)
        self.web_view.setPage(self.web_page)
        self.layout.addWidget(self.web_view)

        # โหลดรายละเอียดหรือลิงก์ในรูปแบบ HTML
        description = assignment.get('description', 'No Description')
        description = self.convert_links_to_html(description)

        html_content = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 20px;
                    background-color: #f0f0f0;
                    color: #333;
                }}
                h2 {{
                    color: #ffffff;
                    font-size: 36px;
                    border: 3px solid #45A049;
                    text-align: center;
                    background-color: #45A049;
                    border-radius: 15px;
                    padding: 20px;
                    margin-bottom: 30px;
                    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
                }}
                p {{
                    font-size: 20px;
                    line-height: 1.6;
                    background-color: #ffffff;
                    padding: 20px;
                    border: 2px solid #ddd;
                    border-radius: 10px;
                    box-shadow: 0 5px 10px rgba(0, 0, 0, 0.1);
                    margin-bottom: 20px;
                    height:800px;
                }}
                a {{
                    color: #007BFF;
                    text-decoration: none;
                    font-weight: bold;
                    transition: color 0.3s, transform 0.3s;
                }}
                a:hover {{
                    color: #004085;
                    text-decoration: underline;
                    transform: scale(1.05);
                }}
                .link-section {{
                    margin-top: 30px;
                    background-color: #ffffff;
                    border: 2px solid #45A049;
                    border-radius: 10px;
                    padding: 15px;
                    box-shadow: 0 5px 10px rgba(0, 0, 0, 0.1);
            }}
        </style>
        </head>
        <body>
            <h2>{assignment.get('title', 'No Title')}</h2>
            <p>{description}</p>
        """

        # ตรวจสอบว่ามีสื่อเพิ่มเติมและเพิ่มเป็นลิงก์ที่คลิกได้
        materials = assignment.get('materials', [])
        if materials:
            html_content += '<div class="link-section"><h3>Links:</h3>'
            for material in materials:
                link_info = material.get('link', {})
                original_link = link_info.get('url')
                if original_link:
                    decoded_link = self.decode_custom_link(original_link)
                    html_content += f'<p><a href="{decoded_link}" target="_blank">{decoded_link}</a></p>'
            html_content += '</div>'

        html_content += "</body></html>"
        self.web_view.setHtml(html_content)

        # ปุ่มกลับไปยังรายละเอียดของคอร์ส
        self.back_button = QPushButton('Back To Course')
        self.back_button.setStyleSheet("""
            background-color: #4CAF50; 
            color: white; 
            padding: 10px; 
            border-radius: 5px; 
            font-size: 16px; 
            border: none;
        """)
        self.back_button.setCursor(Qt.PointingHandCursor)
        self.back_button.clicked.connect(self.go_back)
        self.layout.addWidget(self.back_button)

    def convert_links_to_html(self, text):
        url_pattern = r'(https?://[^\s]+|www\.[^|\s]+)'
        return re.sub(url_pattern, r'<a href="\1">\1</a>', text)

    def decode_custom_link(self, link):
        prefix = 'www.oems://'
        if link.startswith(prefix):
            try:
                encoded_str = link[len(prefix):]
                decoded_bytes = base64.urlsafe_b64decode(encoded_str)
                decoded_link = decoded_bytes.decode('utf-8')
                print(f"Original encoded link: {link}")
                print(f"Decoded link: {decoded_link}")
                return decoded_link
            except Exception as e:
                print(f"Error decoding link: {str(e)}")
                return link  # Return original link if decoding fails
        else:
            print(f"Non-encoded link: {link}")
        return link

    def go_back(self):
        if self.parent:
            self.layout.addWidget(self.back_button)
            self.parent.set_current_widget('course_details')


            
class CourseDetails(QWidget):
    def __init__(self, course_id, service, parent=None):
        super().__init__(parent)
        self.service = service
        self.course_id = course_id
        self.parent = parent

        # ตั้งค่าเลเอาต์
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)

        # โลดรายละเอียดของคอร์ส
        self.load_course_details()

        # ปิ่มกลับไปยังห้องเรียน
        self.back_button = QPushButton('Back To Classroom')
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: #45A049;
                color: white;
                padding: 15px;
                border-radius: 10px;
                font-size: 18px;
                font-weight: bold;
                border: none;
                margin-top: 30px;
                box-shadow: 0 5px 10px rgba(0, 0, 0, 0.3);
            }
            QPushButton:hover {
                background-color: #3D8C40;
                box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4);
                transform: scale(1.05);
            }
        """)
        self.back_button.setCursor(Qt.PointingHandCursor)
        self.back_button.clicked.connect(self.go_back)

        self.layout.addStretch()  # Push the button to the bottom
        self.layout.addWidget(self.back_button)

    def load_course_details(self):
        try:
            course = self.service.courses().get(id=self.course_id).execute()
            course_name = course.get('name', 'No Name')

            # แสดงชื่อคอรฌส
            course_name_label = QLabel(f'Course: {course_name}')
            course_name_label.setAlignment(Qt.AlignCenter)
            course_name_label.setStyleSheet("""
                font-size: 36px;
                font-weight: bold;
                color: #000000;
                background-color: #f0f0f0;
                padding: 20px;
                border-radius: 15px;
                margin-bottom: 30px;
                box-shadow: 0 5px 10px rgba(0, 0, 0, 0.2);
            """)
            self.layout.addWidget(course_name_label)

            course_work = self.service.courses().courseWork().list(courseId=self.course_id).execute()
            assignments = course_work.get('courseWork', [])

            if not assignments:
                no_assignments_label = QLabel('ไม่มี Assignment ที่พฦ')
                no_assignments_label.setAlignment(Qt.AlignCenter)
                no_assignments_label.setStyleSheet("""
                    font-size: 28px;
                    color: #333333;
                """)
                self.layout.addWidget(no_assignments_label)
            else:
                assignments_label = QLabel('Assignments:')
                assignments_label.setAlignment(Qt.AlignLeft)
                assignments_label.setStyleSheet("""
                    font-size: 30px;
                    color: #000000;
                    margin-bottom: 20px;
                """)
                self.layout.addWidget(assignments_label)

                for assignment in assignments:
                    title = assignment.get('title', 'No Title')
                    button = QPushButton(title)
                    button.setStyleSheet("""
                        QPushButton {
                            background-color: white;
                            color: black;
                            padding: 15px;
                            border: 2px solid #45A049;
                            border-radius: 10px;
                            font-size: 20px;
                            font-weight: bold;
                            margin: 10px 0;
                            transition: all 0.3s;
                        }
                        QPushButton:hover {
                            background-color: #45A049;
                            color: white;
                            transform: scale(1.03);
                            box-shadow: 0 5px 10px rgba(0, 0, 0, 0.2);
                        }
                    """)
                    button.setCursor(Qt.PointingHandCursor)
                    button.clicked.connect(lambda _, a=assignment: self.show_assignment_details(a))
                    self.layout.addWidget(button)
        except Exception as e:
            QMessageBox.critical(self, "ข้อผิดพลาด", f'เกิดข้อผิดพลาด: {str(e)}')

    def show_assignment_details(self, assignment):
        if self.parent:
            self.parent.set_current_widget('assignment_details', assignment)

    def go_back(self):
        if self.parent:
            self.parent.set_current_widget('main')






class ClassroomApp(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('Google Classroom')
        self.setGeometry(100, 100, 1200, 800)
        self.pressed_keys = {}
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint)
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Set background color
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor("#57ff9e"))  # ฟ้าอ่อน
        gradient.setColorAt(0.5, QColor("#6e9b7b"))  # เทาเข้ม
        gradient.setColorAt(1, QColor("#ebfef0")) 
        palette = self.palette()
        palette.setBrush(QPalette.Background, gradient)  # ญช้ gradient แทนสีพื้นหลังธรรมดา
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        

        self.header_label = QLabel('ONLINE EXAMINATION MANAGEMENT SYSTEM VIA GOOGLE FORMS')
        self.header_label.setFont(QFont('Arial', 24, QFont.Bold))
        self.header_label.setAlignment(Qt.AlignCenter)
        self.header_label.setStyleSheet("background-color: black; color: #FFF; padding: 20px; border:solid 3px #FFF; border-radius:10px;")
        opacity_effect = QGraphicsOpacityEffect()
        opacity_effect.setOpacity(0.8)
        self.header_label.setGraphicsEffect(opacity_effect)
        self.main_layout.addWidget(self.header_label)
        
        # Create a scroll area for courses
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)  # Enable resizing
        self.main_layout.addWidget(self.scroll_area)

        # Create a widget to hold the courses
        self.courses_widget = QWidget()
        self.courses_layout = QGridLayout()  # Use QGridLayout for multiple columns
        self.courses_widget.setLayout(self.courses_layout)

        # Set the scroll area's widget
        self.scroll_area.setWidget(self.courses_widget)
        
        self.stack = QStackedWidget()  # QStackedWidget สหรับจัดการหน้าตจางแบบซ้อนกัน
        self.main_layout.addWidget(self.stack) # แบ่งพื้นที่สำหรัธ header_label
        self.stack.addWidget(self.scroll_area)
        
        self.course_details_widget = None
        self.assignment_details_widget = None
        # Refresh button
        self.refresh_button = QPushButton('Refresh')
        self.refresh_button.setStyleSheet('background-color: #28B463; color: white; padding: 10px; border: none; font-size: 20px; border-radius:10px;')
        self.refresh_button.setCursor(Qt.PointingHandCursor)
        self.refresh_button.clicked.connect(self.load_classroom_data)
        self.main_layout.addWidget(self.refresh_button, alignment=Qt.AlignCenter)

        # Status label
        self.status_label = QLabel('Fetching Classroom data...')
        self.status_label.setFont(QFont('Arial', 12))
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: black;")
        self.main_layout.addWidget(self.status_label)

        self.load_classroom_data()

        # Exit button
        self.exit_button = QPushButton('Exit')
        self.exit_button.setStyleSheet('background-color: #E74C3C; color: white; padding: 10px; border: none; font-size: 20px; border-radius:10px;')
        self.exit_button.setCursor(Qt.PointingHandCursor)
        self.exit_button.clicked.connect(self.close)
        self.main_layout.addWidget(self.exit_button, alignment=Qt.AlignCenter)

    def load_classroom_data(self):
        self.status_label.setText('Fetching Classroom data...')
        self.clear_courses()

        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            try:
                self.service = build('classroom', 'v1', credentials=creds)
                results = self.service.courses().list(pageSize=10).execute()
                courses = results.get('courses', [])

                if not courses:
                    self.status_label.setText('No courses found.')
                else:
                    for index, course in enumerate(courses):
                        course_name = course.get('name', 'No Name')
                        course_id = course.get('id')

                        # Create a card for each course
                        card_widget = QWidget()
                        card_layout = QVBoxLayout()
                        card_widget.setLayout(card_layout)
                        card_widget.setFixedSize(600, 300)  # Set fixed size for equal width

                        # Set card styles
                        card_widget.setStyleSheet("""
                            background-color: white;
                            border-radius: 10px;
                            border: 1px solid black;
                            padding: 10px;
                            margin: 10px;
                            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
                        """)

                        # Course title
                        course_label = QLabel(course_name)
                        course_label.setFont(QFont('Arial', 16, QFont.Bold))
                        course_label.setStyleSheet("color: #0000;")
                        course_label.setWordWrap(True)  # Enable word wrap
                        card_layout.addWidget(course_label)

                        # Course button to show details
                        course_button = QPushButton('View Course Details')
                        course_button.setFont(QFont('Arial', 12))
                        course_button.setStyleSheet('background-color: #28B463; color: white; border: none; padding: 5px; border-radius: 5px;')
                        course_button.setCursor(Qt.PointingHandCursor)
                        course_button.clicked.connect(lambda checked, c_id=course_id: self.show_course_details(c_id))
                        card_layout.addWidget(course_button)

                        # Add the card to the courses layout
                        row = index // 3  # Calculate row index
                        column = index % 3  # Calculate column index
                        self.courses_layout.addWidget(card_widget, row, column)  # Place in grid
                        self.status_label.setText('Courses loaded successfully.')
            except Exception as e:
                self.status_label.setText(f"Error: {str(e)}")
        else:
            self.status_label.setText("Please login first in the Login app.")

    def clear_courses(self):
        for i in reversed(range(self.courses_layout.count())):
            widget = self.courses_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

    # Remaining methods...

    def set_current_widget(self, widget_name, course_id=None):
        if widget_name == 'main':
            # ลบ widget หน้าเก่าก่อน และแสดงหน้า Main
            if self.course_details_widget:
                self.stack.removeWidget(self.course_details_widget)
                self.course_details_widget.deleteLater()
                self.course_details_widget = None

            self.stack.setCurrentWidget(self.scroll_area)  # กลับไปที่หน้า Main

        elif widget_name == 'course_details':
            # ลบ widget หน้าเก่าก่อน และแสดงหน้า CourseDetails
            if self.course_details_widget:
                self.stack.removeWidget(self.course_details_widget)
                self.course_details_widget.deleteLater()

            self.course_details_widget = CourseDetails(course_id, self.service, parent=self)
            self.stack.addWidget(self.course_details_widget)
            self.stack.setCurrentWidget(self.course_details_widget)  # แสดง CourseDetails แบบเต็มจอ

    def go_back(self):
        """ เมื่อกดปุ่มกลับไปยังห้องเรีน """
        self.set_current_widget('main')  # กลับไปที่หน้าหลักแสดงรายวิชา
        # แสดงปุ่ม Refresh และ Exit อีกครั้ง
        self.refresh_button.show()
        self.exit_button.show()
            
    def show_course_details(self, course_id):
        if self.course_details_widget is None or self.course_details_widget.course_id != course_id:
            self.course_details_widget = CourseDetails(course_id, self.service, self)
            self.stack.addWidget(self.course_details_widget)
            self.stack.setCurrentWidget(self.course_details_widget)

            # Hide Exit and Refresh buttons
            self.refresh_button.hide()
            self.exit_button.hide()

    def set_current_widget(self, widget_name, assignment=None):
        if widget_name == 'course_details' and self.course_details_widget:
            self.stack.setCurrentWidget(self.course_details_widget)
        elif widget_name == 'assignment_details' and assignment:
            self.assignment_details_widget = AssignmentDetails(assignment, self.service, self)
            self.stack.addWidget(self.assignment_details_widget)
            self.stack.setCurrentWidget(self.assignment_details_widget)
        elif widget_name == 'main':
            self.stack.setCurrentWidget(self.scroll_area)  
            self.refresh_button.show()  # แสดงปุ่ม Refresh
            self.exit_button.show()


   
    def keyPressEvent(self, event):
        key = event.key()  # ใช้ event.key() แทน event.text() สำหรับปุ่มพิเศษ
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if event.text():  # เช็คว่ามีการกดปุ่มที่มีค่าตัวอักษร
            key = event.text()
        else:  # ถ้าเป็นปุ่มพิเศษ ให้แสดงชื่อปุ่ม
            key = self.get_key_name(key)

        self.log_keypress_to_file(key, timestamp)

        self.log_keypress_to_file(key, timestamp)
    
    def log_keypress_to_file(self, key, timestamp):
        # เขียน log ลงไฟล์ 'keypress_log.log' โดยใช้การเข้ารหัส utf-8
        with open("keypress_log.log", "a", encoding="utf-8") as log_file:
            log_file.write(f"{timestamp} - Key pressed: {key}\n")
            
    def get_key_name(self, key):
        # สร้างฟังก์ชันเพื่อแปลงโค้ดปุ่มเป็นชื่อ
        if key == Qt.Key_F1:
            return "F1"
        elif key == Qt.Key_F2:
            return "F2"
        elif key == Qt.Key_F3:
            return "F3"
        elif key == Qt.Key_F4:
            return "F4"
        elif key == Qt.Key_F5:
            return "F5"
        elif key == Qt.Key_F6:
            return "F6"
        elif key == Qt.Key_F7:
            return "F7"
        elif key == Qt.Key_F8:
            return "F8"
        elif key == Qt.Key_F9:
            return "F9"
        elif key == Qt.Key_F10:
            return "F10"
        elif key == Qt.Key_F11:
            return "F11"
        elif key == Qt.Key_F12:
            return "F12"
        elif key == Qt.Key_Escape:
            return "Esc"
        elif key == Qt.Key_Tab:
            return "Tab"
        elif key == Qt.Key_Backspace:
            return "Backspace"
        elif key == Qt.Key_Space:
            return "Space"
        elif key == Qt.Key_Return or key == Qt.Key_Enter:
            return "Enter"
        elif key == Qt.Key_Shift:
            return "Shift"
        elif key == Qt.Key_Control:
            return "Ctrl"
        elif key == Qt.Key_Alt:
            return "Alt"
        elif key == Qt.Key_Left:
            return "Left Arrow"
        elif key == Qt.Key_Right:
            return "Right Arrow"
        elif key == Qt.Key_Up:
            return "Up Arrow"
        elif key == Qt.Key_Down:
            return "Down Arrow"
        elif key == Qt.Key_Home:
            return "Home"
        elif key == Qt.Key_End:
            return "End"
        elif key == Qt.Key_PageUp:
            return "Page Up"
        elif key == Qt.Key_PageDown:
            return "Page Down"
        elif key == Qt.Key_Insert:
            return "Insert"
        elif key == Qt.Key_Delete:
            return "Delete"
        # เพิ่มปุ่มอื่นๆ ที่ต้องการเช็คได้ที่นี่
        return f"Key code: {key}" 
    
    def closeEvent(self, event):
        """ลบไฟล์ token.json เมื่อปิดแอปพลิเคชัน"""
        if os.path.exists('token.json'):
            os.remove('token.json')
            print("ไฟล์ token.json ถูกลบเรียบร้อยแล้ว")
        event.accept()  # ให้ปิดแอปพลิเคชันได้ตามปกติ
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ClassroomApp()
    window.showFullScreen()
    window.show()
    sys.exit(app.exec_())
