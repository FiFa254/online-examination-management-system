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
  - `config.py` — environment-variable-driven configuration (database connection, Google Classroom OAuth scopes, exam-link prefix). No secrets are hardcoded here.
  - `db.py` — SQL Server connection helpers (via `pyodbc`) built on `config.DatabaseConfig`
  - `link_service.py` — shared exam-link encode/decode and login-history/link-log database access, used by both apps
  - `student_app.py` — student-facing PyQt5 application
  - `teacher_app.py` — teacher-facing PyQt5 application
- `schema.sql` — creates the `oems` SQL Server database and its tables
- `requirements.txt` — Python dependencies for running `src/` directly
- `.env.example` — template for the local `.env` file (copy to `.env` and fill in your database connection details)
- `credentials.example.json`, `firebase-service-account.example.json` — shape references for the real credential files (not committed)
- `verify-run.ps1` — PowerShell script that launches both executables and captures logs to `test-logs/`
- `TEST_REPORT.md` — test report for this build
- `OEMS_LOGO.png`, `oems_icon.ico` — branding assets

## Security note

The original recovered source had the database root password hardcoded in plaintext in multiple places (as a MySQL connection). That has been removed during refactoring: all database access now goes through `src/config.py` / `src/db.py`, which read connection details from environment variables (via `.env`, loaded with `python-dotenv`). **No database password is committed to this repository.** If you find any other copy of this project with a hardcoded password, treat that copy as compromised and rotate it.

## Database engine: Microsoft SQL Server

The original recovered source connected to **MySQL** (via `mysql.connector`, with a hardcoded `root` password). This project's `src/` has been migrated to **Microsoft SQL Server** instead, using `pyodbc`, to match the database actually available in this environment. If you'd rather run the original MySQL-based version, use an earlier commit of `src/` (before this migration) together with `mysql-connector-python`.

Requirements for the SQL Server version:

- SQL Server (Express is fine) reachable from this machine
- The **ODBC Driver for SQL Server** installed (e.g. "ODBC Driver 17 for SQL Server" — this is usually already present if SQL Server Management Studio is installed; otherwise install it from Microsoft's download page)

## Required local files

The real credential files are intentionally ignored by Git:

- `credentials.json` (Google OAuth client secret)
- `oems-702ce-firebase-adminsdk-fbsvc-a498d0281d.json` (Firebase service account key)
- `.env` (local database connection details — copy `.env.example` to `.env` and fill it in)
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
# edit .env: set OEMS_DB_SERVER / OEMS_DB_NAME, and either
#   OEMS_DB_USER + OEMS_DB_PASSWORD (SQL login), or
#   OEMS_DB_TRUSTED_CONNECTION=yes (Windows Authentication)
python -m src.student_app
python -m src.teacher_app
```

You'll also need `credentials.json` (Google OAuth) in the project directory, and the `oems` database set up on your SQL Server instance from `schema.sql`.

## Database schema

`schema.sql` (T-SQL) creates the `oems` database and its two tables. Run it against your SQL Server instance, e.g. with `sqlcmd`:

```powershell
sqlcmd -S localhost -U sa -P "<your-sa-password>" -i schema.sql
```

or open `schema.sql` in SQL Server Management Studio / Azure Data Studio, connect to your server, and execute it (F5).

Tables created:

- `login_log` — one row per exam login (`ID`, `NAME`, `Email`, `Role`, `Time`)
- `link_log` — maps each obfuscated exam link to its real destination and unique unlock code (`original_link`, `transformed_link`, `unique_code`)

> The original table-creation SQL was not among the recovered source files, so this schema was reconstructed from the columns and queries actually used in `src/link_service.py`. If you have the original schema or a data dump, replace `schema.sql` with it.
