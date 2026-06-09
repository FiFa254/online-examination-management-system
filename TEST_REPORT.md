# Test Report

Test date: 2026-06-09

## Verification command

```powershell
powershell -ExecutionPolicy Bypass -File .\verify-run.ps1
```

## Result

- `Student.exe` launched from the merged project directory and stayed running for the 12-second smoke test window.
- `Teacher.exe` launched from the merged project directory and stayed running for the 12-second smoke test window.
- No stderr output was captured for either executable.
- No `Student.exe` or `Teacher.exe` process remained after the verification script completed.

## Fixed issues

- Merged the missing shared `_internal` runtime folder with the executables.
- Added a verification script that launches each executable from the correct working directory.
- Fixed the verification script so empty stderr files do not cause a null-value error.
- Updated process cleanup so the smoke test does not leave app processes running.

## Remaining limitation

The package contains compiled binaries only. If a bug occurs inside application logic after startup, the original Python source code is required to patch and rebuild the executables.
