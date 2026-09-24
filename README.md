# Online Examination Management System

This project is a merged Windows application package for the Online Examination Management System, and now also includes the recovered and refactored Python application source under `src/`.

## Included applications

- `Student.exe`
- `Teacher.exe`
- `src/student_app.py` — student-facing app (recovered from `form2.py` / `ClassroomApp`)
- `src/teacher_app.py` — teacher-facing app (recovered from `form3.py` / `MainGUI`)

Both executables depend on the bundled `_internal` runtime folder and must be launched from this project directory. The `src/` package is the maintainable source these executables were originally built from; it can be run directly with Python (see "Run from source" below) or repackaged with PyInstaller.

## Project Structure

- `Student.exe`, `Teacher.exe` — PyInstaller-built entry points (stored via Git LFS)
- `_internal/` — bundled Python runtime and dependencies (PyQt5, Firebase/Google API client libraries, etc.) required by both executables
- `src/` — recovered and refactored Python application source:
  - `config.py` — environment-variable-driven configuration (database credentials, Google Classroom OAuth scopes, exam-link prefix). No secrets are hardcoded here.
  - `db.py` — MySQL connection helpers built on `config.DatabaseConfig`
  - `link_service.py` — shared exam-link encode/decode and login-history/link-log database access, used by both apps
  - `student_app.py` — student-facing PyQt5 application
  - `teacher_app.py` — teacher-facing PyQt5 application
- `requirements.txt` — Python dependencies for running `src/` directly
- `.env.example` — template for the local `.env` file (copy to `.env` and fill in your MySQL password)
- `credentials.example.json`, `firebase-service-account.example.json` — shape references for the real credential files (not committed)
- `verify-run.ps1` — PowerShell script that launches both executables and captures logs to `test-logs/`
- `TEST_REPORT.md` — test report for this build
- `OEMS_LOGO.png`, `oems_icon.ico` — branding assets

## Security note

The original recovered source had the MySQL root password hardcoded in plaintext in multiple places. That has been removed during refactoring: all database access now goes through `src/config.py` / `src/db.py`, which read credentials from environment variables (via `.env`, loaded with `python-dotenv`). **No database password is committed to this repository.** If you find any other copy of this project with a hardcoded password, treat that copy as compromised and rotate the MySQL password.

## Required local files

The real credential files are intentionally ignored by Git:

- `credentials.json` (Google OAuth client secret)
- `oems-702ce-firebase-adminsdk-fbsvc-a498d0281d.json` (Firebase service account key)
- `.env` (local database credentials — copy `.env.example` to `.env` and fill in `OEMS_DB_PASSWORD`)
- `token.json` (Google OAuth token cache, created at runtime)

Use the included example files as shape references only. Do not commit real private keys, OAuth secrets, or database passwords to this repository.

## Run

### From the compiled executables (PowerShell)

```powershell
.\Student.exe
.\Teacher.exe
```

To capture launch results:

```powershell
powershell -ExecutionPolicy Bypass -File .\verify-run.ps1
```

Logs are written to `test-logs/`.

### From source

```powershell
pip install -r requirements.txt
copy .env.example .env
# edit .env and set OEMS_DB_PASSWORD (and other values if needed)
python -m src.student_app
python -m src.teacher_app
```

You'll also need `credentials.json` (Google OAuth) in the project directory, and a running MySQL server with the `oems` database (tables used: `login_log`, `link_log`).

## Known limitation

The MySQL schema (`login_log`, `link_log` table definitions) is not yet included in this repository; it will need to be recreated to match the columns referenced in `src/link_service.py`, or added here if the original schema/dump is located.
