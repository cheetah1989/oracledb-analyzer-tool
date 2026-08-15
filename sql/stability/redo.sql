/*
    Query Name : redo
    Category   : stability
    Purpose    : Collect redo generation and log configuration
*/

SELECT
    thread#,
    COUNT(*) AS log_groups,
    SUM(bytes) / 1024 / 1024 / 1024 AS total_redo_gb,
    MIN(bytes) / 1024 / 1024 AS min_log_mb,
    MAX(bytes) / 1024 / 1024 AS max_log_mb
FROM v$log
GROUP BY
    thread#
ORDER BY
    thread#