/*
    Query Name : top_io
    Category   : performance
    Purpose    : Identify SQL generating the most physical I/O
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
    disk_reads,
    direct_reads,
    direct_writes,
    ROUND(
        CASE
            WHEN executions = 0 THEN 0
            ELSE disk_reads / executions
        END,
        2
    ) AS disk_reads_per_exec,
    ROUND(elapsed_time / 1000000, 2) AS elapsed_seconds,
    ROUND(cpu_time / 1000000, 2) AS cpu_seconds,
    last_active_time,
    SUBSTR(sql_text, 1, 1000) AS sql_text
FROM v$sql
WHERE executions > 0
ORDER BY disk_reads DESC
FETCH FIRST 20 ROWS ONLY