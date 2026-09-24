"""OEMS (Online Examination Management System) application package.

Modules:
    config       - environment-variable driven configuration (DB creds, OAuth scopes, link prefix)
    db           - MySQL connection helpers built on config.DatabaseConfig
    link_service - shared exam-link encode/decode + login-history/link-log database access
    student_app  - student-facing PyQt5 application (formerly form2.py / ClassroomApp)
    teacher_app  - teacher-facing PyQt5 application (formerly form3.py / MainGUI)
"""
