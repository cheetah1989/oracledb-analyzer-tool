/*
    Query Name : duplicate_indexes
    Category   : indexes
    Purpose    : Identify indexes with identical column definitions
    Source     : DBA_INDEXES + DBA_IND_COLUMNS
    Version    : Oracle 19c+

    Purpose:
    Identify potentially redundant indexes on the same table.

    Important:
    These are candidates for review, NOT automatic drop candidates.
*/

SELECT
    a.table_owner,
    a.table_name,
    a.index_name AS index_name_1,
    b.index_name AS index_name_2,
    a.uniqueness AS index_1_uniqueness,
    b.uniqueness AS index_2_uniqueness,
    a.status AS index_1_status,
    b.status AS index_2_status
FROM dba_indexes a
JOIN dba_indexes b
    ON a.table_owner = b.table_owner
   AND a.table_name = b.table_name
   AND a.index_name < b.index_name
WHERE a.owner NOT IN (
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
AND a.index_type = 'NORMAL'
AND b.index_type = 'NORMAL'
AND (
    SELECT LISTAGG(column_name, ',')
           WITHIN GROUP (ORDER BY column_position)
    FROM dba_ind_columns c1
    WHERE c1.index_owner = a.owner
      AND c1.index_name = a.index_name
) =
(
    SELECT LISTAGG(column_name, ',')
           WITHIN GROUP (ORDER BY column_position)
    FROM dba_ind_columns c2
    WHERE c2.index_owner = b.owner
      AND c2.index_name = b.index_name
)
ORDER BY
    a.table_owner,
    a.table_name,
    a.index_name