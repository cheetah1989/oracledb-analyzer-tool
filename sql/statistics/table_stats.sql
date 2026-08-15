/*
    Query Name : table_stats
    Category   : statistics
    Purpose    : Collect table-level optimizer statistics
    Source     : DBA_TAB_STATISTICS
    Version    : Oracle 19c+

    Notes:
    - Excludes partition-level statistics.
    - Excludes Oracle/system schemas.
    - Focuses on table-level statistics required for assessment.
*/

SELECT
    owner,
    table_name,
    num_rows,
    blocks,
    empty_blocks,
    avg_row_len,
    sample_size,
    last_analyzed,
    stale_stats,
    stattype_locked,
    global_stats,
    user_stats
FROM dba_tab_statistics
WHERE partition_name IS NULL
  AND subpartition_name IS NULL
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
    table_name