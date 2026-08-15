/*
    Query Name : unused_indexes
    Category   : indexes
    Purpose    : Identify indexes with no observed usage across the database
    Source     : DBA_OBJECT_USAGE + DBA_INDEXES
    Version    : Oracle 19c+

    Important:
    DBA_OBJECT_USAGE only reports usage for indexes where
    index monitoring has been enabled.

    Therefore this query identifies indexes that are:
        - monitored
        - currently showing no usage

    It does NOT mean the index is safe to drop.
*/

SELECT
    u.owner,
    u.index_name,
    i.table_owner,
    i.table_name,
    i.index_type,
    i.uniqueness,
    i.status,
    i.visibility,
    i.partitioned,
    i.num_rows,
    i.distinct_keys,
    i.leaf_blocks,
    i.clustering_factor,
    i.last_analyzed,
    u.monitoring,
    u.used,
    u.start_monitoring,
    u.end_monitoring
FROM dba_object_usage u  -- Changed from v$object_usage to look across all schemas
JOIN dba_indexes i
    ON i.owner = u.owner
   AND i.index_name = u.index_name
WHERE u.monitoring = 'YES'
  AND u.used = 'NO'
  AND u.owner NOT IN (
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
    i.leaf_blocks DESC,
    u.owner,
    u.index_name