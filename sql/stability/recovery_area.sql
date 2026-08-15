/*
    Query Name : recovery_area
    Category   : stability
    Purpose    : Collect Fast Recovery Area utilization
*/

SELECT
    name,
    space_limit / 1024 / 1024 / 1024 AS space_limit_gb,
    space_used / 1024 / 1024 / 1024 AS space_used_gb,
    space_reclaimable / 1024 / 1024 / 1024 AS space_reclaimable_gb,
    ROUND(
        space_used / NULLIF(space_limit, 0) * 100,
        2
    ) AS used_percent,
    number_of_files
FROM v$recovery_file_dest