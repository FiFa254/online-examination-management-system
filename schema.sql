-- OEMS (Online Examination Management System) database schema
-- Microsoft SQL Server (T-SQL) version.
--
-- This schema was reconstructed from the SQL queries used in src/link_service.py
-- and src/teacher_app.py (the original login/link-log tables' CREATE statements
-- were not found in the recovered source, so no original schema/dump exists to
-- restore from). Adjust column types/sizes as needed for your data.
--
-- Usage (sqlcmd):
--   sqlcmd -S localhost -U sa -P <password> -i schema.sql
-- or open this file in SQL Server Management Studio / Azure Data Studio and
-- execute it against your target server.

IF DB_ID(N'oems') IS NULL
BEGIN
    CREATE DATABASE oems;
END
GO

USE oems;
GO

-- Records each exam login (who signed in, in what role, and when).
-- Populated by the exam login flow; read by MainGUI.show_login_history()
-- via src/link_service.py:fetch_login_history().
IF OBJECT_ID(N'dbo.login_log', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.login_log (
        ID     INT IDENTITY(1,1) PRIMARY KEY,
        NAME   NVARCHAR(255) NOT NULL,
        Email  NVARCHAR(255) NOT NULL,
        Role   NVARCHAR(50)  NOT NULL,
        Time   DATETIME2     NOT NULL CONSTRAINT DF_login_log_Time DEFAULT SYSDATETIME()
    );
END
GO

-- Maps each obfuscated exam link (https://www.oems://<base64>) to its real
-- destination and the 6-character unique code required to unlock it.
-- Written by src/link_service.py:save_converted_link() (via encode_link());
-- looked up by is_code_unique() / check_code_exists() / decode flows.
IF OBJECT_ID(N'dbo.link_log', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.link_log (
        id                INT IDENTITY(1,1) PRIMARY KEY,
        original_link     NVARCHAR(MAX) NOT NULL,
        transformed_link  NVARCHAR(MAX) NOT NULL,
        unique_code       NVARCHAR(10)  NOT NULL,
        created_at        DATETIME2     NOT NULL CONSTRAINT DF_link_log_created_at DEFAULT SYSDATETIME(),
        CONSTRAINT UQ_link_log_unique_code UNIQUE (unique_code)
    );
END
GO
