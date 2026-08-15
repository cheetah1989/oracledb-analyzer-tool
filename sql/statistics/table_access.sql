/*
    Query Name : table_access
    Category   : statistics
    Purpose    : Identify frequently accessed tables from SQL execution plans
    Source     : V$SQL_PLAN
*/

SELECT
    object_owner AS owner,
    object_name AS table_name,
    COUNT(*) AS plan_operations,
    COUNT(DISTINCT sql_id) AS sql_count,
    MAX(timestamp) AS last_seen
FROM v$sql_plan
WHERE object_type LIKE 'TABLE%'
  AND object_owner IS NOT NULL
  AND object_name IS NOT NULL
  AND object_owner NOT IN (
    'SYS',
    'SYSTEM',
    'SYSMAN',
    'DBSNMP',
    'OUTLN',
    'CTXSYS',
    'MDSYS',
    'ORDSYS',
    'ORDDATA',
    'XDB',
    'WMSYS'
)
GROUP BY
    object_owner,
    object_name
ORDER BY
    sql_count DESC,
    plan_operations DESC
FETCH FIRST 100 ROWS ONLY