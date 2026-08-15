/*
    Query Name : top_cpu
    Category   : performance
    Purpose    : Identify SQL statements consuming the most CPU
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
    ROUND(cpu_time / 1000000, 2) AS cpu_seconds,
    ROUND(
        CASE
            WHEN executions = 0 THEN 0
            ELSE cpu_time / executions / 1000000
        END,
        4
    ) AS cpu_seconds_per_exec,
    ROUND(elapsed_time / 1000000, 2) AS elapsed_seconds,
    buffer_gets,
    disk_reads,
    rows_processed,
    last_active_time,
    SUBSTR(sql_text, 1, 1000) AS sql_text
FROM v$sql
WHERE executions > 0
ORDER BY cpu_time DESC
FETCH FIRST 20 ROWS ONLY