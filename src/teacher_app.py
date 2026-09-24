import sys 
import base64
import pandas as pd  # เพิ่มการนนนำเข้า pandas
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QSpacerItem, QSizePolicy, QLineEdit, QHBoxLayout, QMessageBox, QTableWidget, QTableWidgetItem
from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineView  # นำเข้า QWebEngineView และ QWebEnginePage
import openpyxl
import random
import string
import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from . import link_service
from . import db

# สร้างคลาสสำหรับหน้าต่างหลัก
class MainGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OEMS")
        self.setGeometry(100, 100, 600, 500)
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        
        # สร้าง layout แนวตั้ง
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # สร้างหน้าหลัก
        self.create_main_page()

    def create_main_page(self):
        # เคลียร์ layout ปัจจุบันแ่นเธ้ง
        self.clear_layout()

        # สร้าง label สำหรับข้อความต้อนรับ
        welcome_label = QLabel("ยินดีต้อนรับอาจารย์")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setFont(QFont("Arial", 22, QFont.Bold))
        welcome_label.setFixedSize(700, 80)
        welcome_label.setStyleSheet("""
            color: #FFF;
            border-radius: 10px;
            background-color:#6b6961;
            padding: 10px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
        """)
        self.layout.addWidget(welcome_label)

        # สร้างกรอบสำหรับปุ่มทั้งหมด
        button_frame = QFrame()
        button_frame.setFrameShape(QFrame.Box)  # กรอบเป็นแบบ Box
        button_frame.setFrameShadow(QFrame.Raised)  # เงาของกรอบ
        button_frame.setStyleSheet("border: 3px solid black; border-radius: 10px; padding: 20px;")
        
        # สร้าง layout แนวตั้งสำหรับปุ่มในกรอบ
        button_layout = QVBoxLayout()
        button_frame.setLayout(button_layout)
        
        # สร้างปุ่มสำหรับ "ประวัติการเข้าสอบ"
        history_button = QPushButton("ประวัติการเข้าสอบ")
        history_button.setFont(QFont("Arial", 14))
        history_button.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                padding: 15px;
                border-radius: 10px;
                margin: 10px 0;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        history_button.clicked.connect(self.show_login_history)  # เชื่อมต่อสัญญาณกับฟังก์ชัน
        button_layout.addWidget(history_button)

        # สร้างปุ่มสำหรับ "สร้างลิ้งค์เข้ารหัสสำหรับโปรแกรม"
        create_link_button = QPushButton("สร้างลิ้งค์เข้ารหัสสำหรับโปรแกรม")
        create_link_button.setFont(QFont("Arial", 14))
        create_link_button.setStyleSheet("""
            QPushButton {
                background-color: #e67e22;
                color: white;
                padding: 15px;
                border-radius: 10px;
                margin: 10px 0;
            }
            QPushButton:hover {
                background-color: #d35400;
            }
        """)
        create_link_button.clicked.connect(self.show_link_transformer)  # กดปุ่มแล้วแสดงหน้าจอการเข้ารหัส
        button_layout.addWidget(create_link_button)

        # สร้างปุ่ม Exit
        exit_button = QPushButton("Exit")
        exit_button.setFont(QFont("Arial", 14))
        exit_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                padding: 15px;
                border-radius: 10px;
                margin: 10px 0;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        exit_button.clicked.connect(close_app)
        button_layout.addWidget(exit_button)

        # เพิ่มกรอบที่บรรจุปุ่มเข้าใน layout หลัก
        self.layout.addWidget(button_frame)
    def closeEvent(self, event):
        """ลบไฟล์ token.json เมื่อปิดแอปพลิเคชัน"""
        if os.path.exists('token.json'):
            os.remove('token.json')
            print("ไฟล์ token.json ถูกลบเรียบร้อยแล้ว")
        event.accept() # ให้ปิดแอปพลิเคชัน
    def show_login_history(self):
        # เคลียร์ layout ก่อนแสดงประวัติ
        self.clear_layout()

        # สร้าง label หัวข้อ
        history_label = QLabel("ประวัติการเข้าสอบ")
        history_label.setFont(QFont("Arial", 18, QFont.Bold))
        history_label.setAlignment(Qt.AlignCenter)
        history_label.setStyleSheet("color: #3498db;")
        self.layout.addWidget(history_label)

        try:
            records = link_service.fetch_login_history()

            # สร้างตารางเพื่อแสดงข้อมูล
            table = QTableWidget()
            table.setRowCount(len(records))
            table.setColumnCount(5)
            table.setHorizontalHeaderLabels(["ID", "NAME", "Email", "Role", "Time"])

            for row_index, row_data in enumerate(records):
                for column_index, data in enumerate(row_data):
                    table.setItem(row_index, column_index, QTableWidgetItem(str(data)))

            self.layout.addWidget(table)

            # สร้างปุ่มส่งออกเป็น Excel
            export_button = QPushButton("ส่งออกเป็น Excel")
            export_button.setFont(QFont("Arial", 14))
            export_button.setStyleSheet(""" 
                QPushButton {
                    background-color: #3498db; 
                    color: white; 
                    padding: 10px; 
                    border-radius: 10px; 
                } 
                QPushButton:hover { 
                    background-color: #2980b9; 
                } 
            """)
            export_button.clicked.connect(lambda: self.export_to_excel(records))  # เชื่อมต่อกับฟังก์ชันส่งออก
            self.layout.addWidget(export_button)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not retrieve login history: {str(e)}")

        # สร้างปุ่มย้อนกลับ
        back_button = QPushButton("ย้อนกลับ")
        back_button.setFont(QFont("Arial", 14))
        back_button.setStyleSheet(""" 
            QPushButton {
                background-color: #3498db; 
                color: white; 
                padding: 10px; 
                border-radius: 10px; 
            } 
            QPushButton:hover { 
                background-color: black; 
            } 
        """)
        back_button.clicked.connect(self.create_main_page)
        self.layout.addWidget(back_button)

    # ฟังก์ชันส่งออกข้อมูลเป็น Excel
    def export_to_excel(self, records):
        df = pd.DataFrame(records, columns=["ID", "NAME", "Email", "Role", "Time"])
        try:
            df.to_excel('login_history.xlsx', index=False)  # ส่งออกไปยังไฟล์ Excel
            QMessageBox.information(self, "Export Successful", "ประวัติการเข้าสอบถูกส่งออกเป็นไฟล์ Excel สำเร็จแล้ว!")
        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Could not export to Excel: {str(e)}")

        # แสดงปุ่มสำหรับแสดงข้อความ
    def show_link_transformer(self):
        # เคลียร์ layout ปัจจุบันก่อน
        self.clear_layout()

        # สร้าง label หัวข้อ
        header_label = QLabel('OEMS Link Transformer')
        header_label.setFont(QFont('Arial', 18, QFont.Bold))
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("color: navy;")
        self.layout.addWidget(header_label)

        # สร้าง label สำหรับการป้อนลิงค์
        link_label = QLabel('Enter the link to encode or decode:')
        link_label.setFont(QFont('Arial', 12))
        self.layout.addWidget(link_label)

        # ช่องกรอกข้อมูลลิงก์
        self.link_input = QLineEdit(self)
        self.link_input.setFont(QFont('Arial', 12))
        self.link_input.setPlaceholderText('Enter link here...')
        self.layout.addWidget(self.link_input)

        # Layout สร้างปุ่ม encode และ decode
        button_layout = QHBoxLayout()

        # สร้างปุ่ม Encode
        encode_button = QPushButton("Encode Link")
        encode_button.setFont(QFont("Arial", 14))
        encode_button.setStyleSheet(""" 
            QPushButton {
                background-color: #2ecc71; 
                color: white; 
                padding: 10px; 
                border-radius: 10px; 
            } 
            QPushButton:hover { 
                background-color: #27ae60; 
            } 
        """)
        encode_button.clicked.connect(self.encode_link)
        button_layout.addWidget(encode_button)

        # สร้างปุ่ม Decode
        decode_button = QPushButton("Decode Link")
        decode_button.setFont(QFont("Arial", 14))
        decode_button.setStyleSheet(""" 
            QPushButton {
                background-color: #e67e22; 
                color: white; 
                padding: 10px; 
                border-radius: 10px; 
            } 
            QPushButton:hover { 
                background-color: #d35400; 
            } 
        """)
        decode_button.clicked.connect(self.decode_link)
        button_layout.addWidget(decode_button)

        self.layout.addLayout(button_layout)

        # สร้างปุ่มสร้างคัดลอกลิงก์และรหัส
        self.copy_link_button = QPushButton("Copy Encoded Link")
        self.copy_link_button.setFont(QFont("Arial", 14))
        self.copy_link_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db; 
                color: white; 
                padding: 10px; 
                border-radius: 10px; 
            }
            QPushButton:hover { 
                background-color: #2980b9;
            }
        """)
        self.copy_link_button.clicked.connect(self.copy_link_to_clipboard)
        self.layout.addWidget(self.copy_link_button)
        self.copy_link_button.setEnabled(False)  # ปิดปุ่มก่อนเพื่อเปิดใช้งานหลังจากแปลงลิงก์แล้ว

        self.copy_code_button = QPushButton("Copy Unique Code")
        self.copy_code_button.setFont(QFont("Arial", 14))
        self.copy_code_button.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6;
                color: white;
                padding: 10px; 
                border-radius: 10px; 
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
        """)
        self.copy_code_button.clicked.connect(self.copy_code_to_clipboard)
        self.layout.addWidget(self.copy_code_button)
        self.copy_code_button.setEnabled(False)  # ปิดปุ่มก่อนเพื่อเปิดใช้งานหลังจากแปลงลิงก์แล้ว

        # สร้างปุ่มย้อนกลับ
        back_button = QPushButton("ย้อนกลับ")
        back_button.setFont(QFont("Arial", 14))
        back_button.setStyleSheet(""" 
            QPushButton {
                background-color: #3498db; 
                color: white; 
                padding: 10px; 
                border-radius: 10px; 
            } 
            QPushButton:hover { 
                background-color: #2980b9; 
            } 
        """)
        back_button.clicked.connect(self.create_main_page)
        self.layout.addWidget(back_button)

    def is_code_unique(self, code):
        try:
            return link_service.is_code_unique(code)
        except Exception as e:
            self.show_message("Database Error", f"Could not check code uniqueness: {str(e)}")
            return False

    # ฟฅก์ชนสำหรับสางญฅะฉญญฉ 6 ตัวทึฉเฯพน๋งฉำฉะฉฉฉฉเฉฉนฉสฉจฉฌฉ
    def generate_unique_code(self, length=6):
        while True:
            code = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
            if self.is_code_unique(code):  # ตรวจสอบว่ารหัสนี้ไม่ซ้ำ
                return code

    def encode_link(self):
        original_link = self.link_input.text()
        if original_link:
            try:
                encoded_bytes = base64.urlsafe_b64encode(original_link.encode('utf-8'))
                encoded_str = encoded_bytes.decode('utf-8')
                transformed_link = f"https://www.oems://{encoded_str}"

                # สร้างรหัสส 6 ตัวทึ่ไม่ซ้ำ
                unique_code = self.generate_unique_code()

                # า๑นวณตรายคอและรสสในฐานข้อมูล
                self.save_converted_link(original_link, transformed_link, unique_code)

                # เก็บค่าลิงก์และรหัสไฟ้ในตัวแถรสฬรหัสการคัดลอก
                self.encoded_link = transformed_link
                self.unique_code = unique_code

                # เปิดใช้งานปุ่มคัดลอกลิงก์และรหัส
                self.copy_link_button.setEnabled(True)
                self.copy_code_button.setEnabled(True)

                # แสดงผลลัพธ์
                self.show_message('Encoded Link', f'Encoded Link: {transformed_link}\nUnique Code: {unique_code}')

            except Exception as e:
                self.show_message('Error', f'Error encoding link: {str(e)}')
        else:
            self.show_message('Error', 'Please enter a link to encode.')

    # ฟกญชนาญฉทญแญฅะญญฉฅญโญจญฅญแญฉชญฅญใญญญญญญญญญญญญญญญญญญญญญญญญญญญญญญญญญญ
    def save_converted_link(self, original_link, transformed_link, unique_code):
        try:
            link_service.save_converted_link(original_link, transformed_link, unique_code)
        except Exception as e:
            self.show_message("Database Error", f"Could not save link: {str(e)}")

    def decode_link(self):
        transformed_link = self.link_input.text()
        if transformed_link.startswith('https://www.oems://'):
            try:
                encoded_str = transformed_link[len('https://www.oems://'):]
                decoded_bytes = base64.urlsafe_b64decode(encoded_str)
                decoded_link = decoded_bytes.decode('utf-8')

                # บันทึกลิงค์ที่ถอดรสาสในฐานข้อมูล (ถ้าต้องการ)

                # แสดงผลลัพธ์และคัดลอกไปที่คลิปบอร์ด
                self.show_message('Decoded Link', f'Decoded Link: {decoded_link}', decoded_link)
                self.copy_to_clipboard(decoded_link)  # คัดลอกลิงก์ที่ถอดรหัสไปที่คลิปบอร์ด
            except Exception as e:
                self.show_message('Error', f'Error decoding link: {str(e)}')
        else:
            self.show_message('Error', 'The link does not start with the correct prefix.')

    # ฟังก์ชันสำหรับแสดงข้อความ
    def show_message(self, title, message, detailed_message=None):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        if detailed_message:
            msg_box.setDetailedText(detailed_message)
        msg_box.exec_()

    def copy_to_clipboard(self, text):
        clipboard = QApplication.clipboard()
        clipboard.setText(text)

    def copy_link_to_clipboard(self):
        if hasattr(self, 'encoded_link'):
            self.copy_to_clipboard(self.encoded_link)
            self.show_message("Copied", "Encoded link copied to clipboard!")

    def copy_code_to_clipboard(self):
        if hasattr(self, 'unique_code'):
            self.copy_to_clipboard(self.unique_code)
            self.show_message("Copied", "Unique code copied to clipboard!")

    def clear_layout(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget() is not None:
                item.widget().deleteLater()
            elif item.layout() is not None:
                self.clear_sub_layout(item.layout())

    def clear_sub_layout(self, layout):
        while layout.count():
            sub_item = layout.takeAt(0)
            if sub_item.widget() is not None:
                sub_item.widget().deleteLater()
            elif sub_item.layout() is not None:
                self.clear_sub_layout(sub_item.layout())


class CustomWebEnginePage(QWebEnginePage):
    def __init__(self, parent=None):
        super().__init__(parent)

    def acceptNavigationRequest(self, url, _type, isMainFrame):
        if _type == QWebEnginePage.NavigationTypeLinkClicked:
            url_str = url.toString()
            print(f"Navigating to: {url_str}")
            self.log_link_click(url_str)

            if url.isEmpty():
                print("Error: URL is empty.")
                return False

            if url_str.startswith('https://www.oems://'):
                decoded_link = self.decode_custom_link(url_str)
                return False

            self.view().setUrl(url)
            return False

        return super().acceptNavigationRequest(url, _type, isMainFrame)

    def decode_custom_link(self, url_str):
        encoded_str = url_str[len('https://www.oems://'):]
        decoded_bytes = base64.urlsafe_b64decode(encoded_str)
        decoded_link = decoded_bytes.decode('utf-8')
        print(f"Decoded link: {decoded_link}")
        return decoded_link


def close_app():
    try:
        if os.path.exists('token.json'):
            os.remove('token.json')
            print("token.json has been deleted.")
        else:
            print("token.json does not exist.")
    except Exception as e:
        print(f"Error deleting token.json: {str(e)}")
    app.quit()


app = QApplication(sys.argv)
main_gui = MainGUI()
main_gui.show()
sys.exit(app.exec_())
