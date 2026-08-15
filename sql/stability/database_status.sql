/*
    Query Name : database_status
    Category   : stability
    Purpose    : Collect database and instance operational status
*/

SELECT
    d.name,
    d.db_unique_name,
    d.open_mode,
    d.database_role,
    d.log_mode,
    d.force_logging,
    d.flashback_on,
    i.instance_name,
    i.status AS instance_status,
    i.database_status,
    i.active_state,
    i.host_name
FROM v$database d
CROSS JOIN v$instance i