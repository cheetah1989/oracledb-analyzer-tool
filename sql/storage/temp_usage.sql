/* Query Name : temp_usage Category : storage Purpose : Collect current TEMP utilization Source : DBA_TEMP_FILES + DBA_TEMP_FREE_SPACE */
SELECT
    tf.tablespace_name,
    ROUND(tf.allocated_gb, 2) AS allocated_gb,
    ROUND(tf.max_size_gb, 2) AS max_size_gb,
    ROUND(tf.allocated_gb - NVL(dtf.free_gb, 0), 2) AS used_gb,
    ROUND(NVL(dtf.free_gb, 0), 2) AS free_gb,
    ROUND((tf.allocated_gb - NVL(dtf.free_gb, 0)) / NULLIF(tf.allocated_gb, 0) * 100, 2) AS used_percent
FROM
    (
        SELECT
            tablespace_name,
            SUM(bytes) / 1024 / 1024 / 1024 AS allocated_gb,
            SUM(maxbytes) / 1024 / 1024 / 1024 AS max_size_gb
        FROM dba_temp_files
        GROUP BY tablespace_name
    ) tf
LEFT JOIN
    (
        SELECT
            tablespace_name,
            SUM(free_space) / 1024 / 1024 / 1024 AS free_gb
        FROM dba_temp_free_space
        GROUP BY tablespace_name
    ) dtf
ON tf.tablespace_name = dtf.tablespace_name
ORDER BY used_percent DESC
