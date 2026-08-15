/*
    Query Name : load
    Category   : server
    Purpose    : Collect current Oracle workload metrics
    Source     : V$SYSMETRIC
    Version    : Oracle 19c+
*/

SELECT
    metric_name,
    value,
    metric_unit,
    begin_time,
    end_time
FROM v$sysmetric
WHERE group_id = 2
ORDER BY metric_name