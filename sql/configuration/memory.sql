/*
    Query Name : memory
    Category   : configuration
    Purpose    : Collect Oracle memory configuration
    Source     : V$PARAMETER
    Version    : Oracle 19c+

    Purpose:
    Used later to assess whether Oracle memory configuration
    is appropriate for the database workload and server size.
*/

SELECT
    name,
    value,
    display_value,
    isdefault,
    ismodified,
    issys_modifiable
FROM v$parameter
WHERE name IN (
    'memory_target',
    'memory_max_target',
    'sga_target',
    'sga_max_size',
    'pga_aggregate_target',
    'pga_aggregate_limit',
    'use_large_pages'
)
ORDER BY name