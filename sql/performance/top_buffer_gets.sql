/*
    Query Name : top_buffer_gets
    Category   : performance
    Purpose    : Identify SQL generating the most logical I/O
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
    buffer_gets,
    ROUND(
        CASE
            WHEN executions = 0 THEN 0
            ELSE buffer_gets / executions
        END,
        2
    ) AS buffer_gets_per_exec,
    ROUND(cpu_time / 1000000, 2) AS cpu_seconds,
    ROUND(elapsed_time / 1000000, 2) AS elapsed_seconds,
    rows_processed,
    last_active_time,
    SUBSTR(sql_text, 1, 1000) AS sql_text
FROM v$sql
WHERE executions > 0
ORDER BY buffer_gets DESC
FETCH FIRST 20 ROWS ONLY