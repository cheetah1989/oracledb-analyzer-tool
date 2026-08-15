/*
    Query Name : top_executions
    Category   : performance
    Purpose    : Identify SQL statements with highest execution count
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
        6
    ) AS cpu_seconds_per_exec,
    ROUND(elapsed_time / 1000000, 2) AS elapsed_seconds,
    buffer_gets,
    disk_reads,
    last_active_time,
    SUBSTR(sql_text, 1, 1000) AS sql_text
FROM v$sql
WHERE executions > 0
ORDER BY executions DESC
FETCH FIRST 20 ROWS ONLY