/*
    Query Name : datafiles
    Category   : storage
    Purpose    : Analyze individual datafiles
    Source     : DBA_DATA_FILES
    Version    : Oracle 19c+
*/

SELECT
    file_id,
    tablespace_name,
    file_name,
    ROUND(bytes / 1024 / 1024 / 1024, 2) AS size_gb,
    autoextensible,
    ROUND(maxbytes / 1024 / 1024 / 1024, 2) AS max_size_gb,
    increment_by,
    ROUND(
        increment_by * blocks / 1024 / 1024,
        2
    ) AS autoextend_increment_mb
FROM dba_data_files
ORDER BY
    tablespace_name,
    file_id