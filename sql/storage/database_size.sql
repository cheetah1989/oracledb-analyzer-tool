/*
    Query Name : database_size
    Category   : storage
    Purpose    : Calculate total allocated database storage
    Source     : DBA_DATA_FILES
    Version    : Oracle 19c+

    Notes:
    - Represents allocated permanent datafile space.
    - Does not include TEMP.
    - Does not represent ac.tual business data volume.
*/

SELECT
    ROUND(SUM(bytes) / 1024 / 1024 / 1024, 2) AS allocated_size_gb
FROM dba_data_files