/*
    Query Name : instance
    Category   : environment
    Purpose    : Collect Oracle instance information
    Source     : V$INSTANCE
    Version    : Oracle 19c+
*/

SELECT
    instance_name,
    host_name,
    version,
    startup_time,
    status,
    parallel
FROM v$instance