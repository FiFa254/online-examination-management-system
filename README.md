# Online Examination Management System

This project is a merged Windows application package for the Online Examination Management System.

## Included applications

- `Student.exe`
- `Teacher.exe`

Both executables depend on the bundled `_internal` runtime folder and must be launched from this project directory.

## Required local files

The real credential files are intentionally ignored by Git:

- `credentials.json`
- `oems-702ce-firebase-adminsdk-fbsvc-a498d0281d.json`

Use the included example files as shape references only. Do not commit real private keys or OAuth secrets to a public repository.

## Run

From PowerShell:

```powershell
.\Student.exe
.\Teacher.exe
```

To capture launch results:

```powershell
powershell -ExecutionPolicy Bypass -File .\verify-run.ps1
```

Logs are written to `test-logs/`.

## Known limitation

Only compiled PyInstaller-style binaries are available in this package. Packaging, file placement, dependency, and configuration problems can be fixed here. Bugs inside the compiled application logic require the original Python source code.
