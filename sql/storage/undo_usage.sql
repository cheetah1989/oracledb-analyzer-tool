/*
    Query Name : undo_usage
    Category   : storage
    Purpose    : Analyze UNDO tablespace utilization
    Source     : DBA_DATA_FILES, DBA_FREE_SPACE, V$PARAMETER
    Version    : Oracle 19c+
*/

SELECT
    df.tablespace_name,
    ROUND(
        SUM(df.bytes) / 1024 / 1024 / 1024,
        2
    ) AS allocated_gb,
    ROUND(
        (
            SUM(df.bytes)
            - NVL(fs.free_bytes, 0)
        ) / 1024 / 1024 / 1024,
        2
    ) AS used_gb,
    ROUND(
        NVL(fs.free_bytes, 0) / 1024 / 1024 / 1024,
        2
    ) AS free_gb,
    ROUND(
        (
            (
                SUM(df.bytes)
                - NVL(fs.free_bytes, 0)
            )
            / SUM(df.bytes)
        ) * 100,
        2
    ) AS used_percent
FROM dba_data_files df
LEFT JOIN (
    SELECT
        tablespace_name,
        SUM(bytes) AS free_bytes
    FROM dba_free_space
    GROUP BY tablespace_name
) fs
    ON df.tablespace_name = fs.tablespace_name
WHERE df.tablespace_name IN (
    SELECT value
    FROM v$parameter
    WHERE name = 'undo_tablespace'
)
GROUP BY
    df.tablespace_name,
    fs.free_bytes