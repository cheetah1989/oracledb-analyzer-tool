/*
    Query Name : top_elapsed
    Category   : performance
    Purpose    : Identify SQL statements consuming the most elapsed time
    Source     : V$SQL
    Version    : Oracle 19c+
*/

SELECT
    sql_id,
    plan_hash_value,
    parsing_schema_name,
    module,
    action,
    executions,
    ROUND(elapsed_time / 1000000, 2) AS elapsed_seconds,
    ROUND(
        CASE
            WHEN executions = 0 THEN 0
            ELSE elapsed_time / executions / 1000000
        END,
        4
    ) AS elapsed_seconds_per_exec,
    ROUND(cpu_time / 1000000, 2) AS cpu_seconds,
    buffer_gets,
    disk_reads,
    rows_processed,
    last_active_time,
    SUBSTR(sql_text, 1, 1000) AS sql_text
FROM v$sql
WHERE executions > 0
ORDER BY elapsed_time DESC
FETCH FIRST 20 ROWS ONLY