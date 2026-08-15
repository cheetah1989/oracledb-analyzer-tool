/*
    Query Name : stale_stats
    Category   : statistics
    Purpose    : Identify tables with stale optimizer statistics
    Source     : DBA_TAB_STATISTICS
*/

SELECT
    owner,
    table_name,
    partition_name,
    num_rows,
    blocks,
    last_analyzed,
    stale_stats
FROM dba_tab_statistics
WHERE stale_stats = 'YES'
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
    last_analyzed NULLS FIRST,
    owner,
    table_name