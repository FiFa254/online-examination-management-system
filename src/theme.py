ACCENT = "#15803d"
ACCENT_HOVER = "#166534"
ACCENT_SOFT = "#e7f6ec"
INK = "#14201a"
MUTED = "#55625a"
CANVAS = "#f4f6f3"
SURFACE = "#ffffff"
LINE = "#d3dcd5"
DISABLED = "#9aa59d"
DANGER = "#b42318"
DANGER_LINE = "#efb8b1"
DANGER_SOFT = "#fdecea"

STYLESHEET = f"""
QWidget {{
    background: {CANVAS};
    color: {INK};
}}
QLabel {{
    background: transparent;
}}
QLabel[role="title"] {{
    font-size: 24px;
    font-weight: 700;
    padding: 4px 0 8px 0;
}}
QLabel[role="heading"] {{
    font-size: 18px;
    font-weight: 700;
    padding-top: 8px;
}}
QLabel[role="muted"] {{
    color: {MUTED};
}}
QLabel[role="appbar"] {{
    background: {ACCENT};
    color: #ffffff;
    border-radius: 10px;
    padding: 16px;
    font-size: 20px;
    font-weight: 700;
}}
QFrame[role="card"], QWidget[role="card"] {{
    background: {SURFACE};
    border: 1px solid {LINE};
    border-radius: 12px;
}}
QPushButton {{
    background: {SURFACE};
    color: {INK};
    border: 1px solid {LINE};
    border-radius: 8px;
    padding: 10px 18px;
    font-size: 15px;
    font-weight: 600;
}}
QPushButton:hover {{
    border-color: {ACCENT};
    color: {ACCENT};
}}
QPushButton:focus {{
    border: 2px solid {ACCENT};
}}
QPushButton:disabled {{
    color: {DISABLED};
    border-color: #e3e8e4;
}}
QPushButton[role="primary"] {{
    background: {ACCENT};
    color: #ffffff;
    border: 1px solid {ACCENT};
}}
QPushButton[role="primary"]:hover {{
    background: {ACCENT_HOVER};
    border-color: {ACCENT_HOVER};
    color: #ffffff;
}}
QPushButton[role="primary"]:disabled {{
    background: #a7cdb3;
    border-color: #a7cdb3;
    color: #ffffff;
}}
QPushButton[role="danger"] {{
    color: {DANGER};
    border-color: {DANGER_LINE};
}}
QPushButton[role="danger"]:hover {{
    background: {DANGER_SOFT};
    border-color: {DANGER};
    color: {DANGER};
}}
QPushButton[role="menu"] {{
    padding: 16px 18px;
    font-size: 17px;
}}
QPushButton[role="menu"]:hover {{
    background: {ACCENT_SOFT};
}}
QPushButton[role="choice"] {{
    border-radius: 14px;
    padding: 0;
}}
QPushButton[role="choice"]:hover {{
    background: {ACCENT_SOFT};
    border: 2px solid {ACCENT};
}}
QLineEdit {{
    background: {SURFACE};
    border: 1px solid {LINE};
    border-radius: 8px;
    padding: 9px 12px;
    font-size: 15px;
    selection-background-color: {ACCENT};
}}
QLineEdit:focus {{
    border: 2px solid {ACCENT};
    padding: 8px 11px;
}}
QTableWidget {{
    background: {SURFACE};
    border: 1px solid {LINE};
    border-radius: 8px;
    gridline-color: #e6ebe7;
    selection-background-color: {ACCENT_SOFT};
    selection-color: {INK};
}}
QTableWidget::item {{
    padding: 6px 12px;
}}
QHeaderView::section {{
    background: #f7f9f7;
    color: {MUTED};
    border: none;
    border-bottom: 1px solid {LINE};
    padding: 8px;
    font-weight: 600;
}}
QScrollArea {{
    border: none;
}}
QDialog, QMessageBox {{
    background: {SURFACE};
}}
"""


def apply(app):
    app.setStyleSheet(STYLESHEET)


def role(widget, name):
    widget.setProperty("role", name)
    return widget
