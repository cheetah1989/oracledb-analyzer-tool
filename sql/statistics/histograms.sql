/*
    Query Name : histograms
    Category   : statistics
    Purpose    : Identify columns with optimizer histograms
    Source     : DBA_TAB_COL_STATISTICS
*/

SELECT
    owner,
    table_name,
    column_name,
    num_distinct,
    num_nulls,
    num_buckets,
    histogram,
    density,
    last_analyzed
FROM dba_tab_col_statistics
WHERE histogram <> 'NONE'
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
    table_name,
    column_name