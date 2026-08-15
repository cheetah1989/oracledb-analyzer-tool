/*
    Query Name : filesystem
    Category   : server
    Purpose    : Identify filesystem locations used by database files
    Source     : DBA_DATA_FILES, DBA_TEMP_FILES, V$LOGFILE, V$ARCHIVED_LOG
    Version    : Oracle 19c+

    Notes:
    This query identifies database storage paths.
    Actual filesystem capacity/utilization should later be
    collected from the operating system.
*/

SELECT
    'DATAFILE' AS file_type,
    file_name AS file_path
FROM dba_data_files

UNION ALL

SELECT
    'TEMPFILE' AS file_type,
    file_name AS file_path
FROM dba_temp_files

UNION ALL

SELECT
    'ONLINE_REDO' AS file_type,
    member AS file_path
FROM v$logfile

ORDER BY
    file_type,
    file_path