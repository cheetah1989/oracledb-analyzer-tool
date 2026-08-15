/*
    Query Name : archive_log
    Category   : stability
    Purpose    : Collect archive log generation status
*/

SELECT
    thread#,
    sequence#,
    first_time,
    next_time,
    completion_time,
    blocks,
    block_size,
    archived
FROM v$archived_log
WHERE first_time >= SYSDATE - 1
ORDER BY
    first_time DESC
FETCH FIRST 100 ROWS ONLY