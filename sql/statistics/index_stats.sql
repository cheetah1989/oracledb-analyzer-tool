/*
    Query Name : index_stats
    Category   : statistics
    Purpose    : Collect optimizer statistics for indexes
    Source     : DBA_INDEXES
*/

SELECT
    owner,
    index_name,
    table_owner,
    table_name,
    index_type,
    uniqueness,
    status,
    visibility,
    partitioned,
    num_rows,
    distinct_keys,
    leaf_blocks,
    clustering_factor,
    blevel,
    avg_leaf_blocks_per_key,
    avg_data_blocks_per_key,
    last_analyzed,
    global_stats,
    user_stats
FROM dba_indexes
WHERE owner NOT IN (
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
    index_name