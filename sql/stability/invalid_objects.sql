/*
    Query Name : invalid_objects
    Category   : stability
    Purpose    : Identify invalid database objects
*/

SELECT
    owner,
    object_type,
    object_name,
    status,
    created,
    last_ddl_time
FROM dba_objects
WHERE status <> 'VALID'
  AND owner NOT IN (
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
ORDER BY
    owner,
    object_type,
    object_name