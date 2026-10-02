import os
import subprocess
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QMessageBox, QPushButton, QVBoxLayout, QWidget

from src import theme

ROLES = [
    ("อาจารย์", "ดูประวัติการเข้าสอบ\nและสร้างลิงก์เข้ารหัส", "Teacher.exe", "src.teacher_app"),
    ("นักศึกษา", "ดูวิชาใน Google Classroom\nและเข้าทำข้อสอบด้วยรหัส", "Student.exe", "src.student_app"),
]


def is_frozen():
    return getattr(sys, "frozen", False)


def base_dir():
    if is_frozen():
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def app_command(exe_name, module):
    if is_frozen():
        return [os.path.join(base_dir(), exe_name)]
    return [sys.executable, "-m", module]


class RoleChooser(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OEMS")
        self.setMinimumSize(640, 400)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(16)

        title = theme.role(QLabel("เลือกประเภทผู้ใช้"), "title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        subtitle = theme.role(QLabel("เลือกโปรแกรมที่ต้องการเปิด"), "muted")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)

        cards = QHBoxLayout()
        cards.setSpacing(16)
        for name, detail, exe_name, module in ROLES:
            cards.addWidget(self.role_card(name, detail, exe_name, module))
        layout.addLayout(cards, 1)

        close_button = QPushButton("ปิด")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button, alignment=Qt.AlignCenter)

    def role_card(self, name, detail, exe_name, module):
        card = theme.role(QPushButton(), "choice")
        card.setAccessibleName(name)
        card.setCursor(Qt.PointingHandCursor)
        card.setMinimumHeight(160)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        for text, label_role in ((name, "heading"), (detail, "muted")):
            label = theme.role(QLabel(text), label_role)
            label.setAlignment(Qt.AlignCenter)
            label.setAttribute(Qt.WA_TransparentForMouseEvents)
            card_layout.addWidget(label)

        card.clicked.connect(lambda: self.open_app(exe_name, module))
        return card

    def open_app(self, exe_name, module):
        command = app_command(exe_name, module)
        if is_frozen() and not os.path.exists(command[0]):
            QMessageBox.critical(self, "ไม่พบโปรแกรม", f"ไม่พบไฟล์ {exe_name} ในโฟลเดอร์เดียวกับ OEMS.exe\n{base_dir()}")
            return
        try:
            subprocess.Popen(command, cwd=base_dir())
        except OSError as err:
            QMessageBox.critical(self, "เปิดโปรแกรมไม่สำเร็จ", f"เปิด {exe_name} ไม่สำเร็จ: {err}")
            return
        self.close()


def main():
    app = QApplication(sys.argv)
    theme.apply(app)
    window = RoleChooser()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
