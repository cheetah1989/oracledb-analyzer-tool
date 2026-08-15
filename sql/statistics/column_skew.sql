/*
    Query Name : column_skew
    Category   : statistics
    Purpose    : Identify columns with useful distribution statistics
    Source     : DBA_TAB_COL_STATISTICS
    Version    : Oracle 19c+

    Notes:
    - Only columns with histograms are collected.
    - Columns without histograms cannot provide histogram-based
      skew evidence.
    - This significantly reduces the result set.
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
    sample_size,
    last_analyzed
FROM dba_tab_col_statistics
WHERE histogram <> 'NONE'
  AND histogram IS NOT NULL
  AND num_distinct > 1
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
    num_buckets DESC,
    num_distinct DESC
FETCH FIRST 5000 ROWS ONLY