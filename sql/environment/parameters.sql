/*
    Query Name : parameters
    Category   : environment
    Purpose    : Collect key Oracle initialization parameters
    Source     : V$PARAMETER
    Version    : Oracle 19c+
*/

SELECT
    name,
    value,
    isdefault,
    issys_modifiable
FROM v$parameter
WHERE name IN (
    'memory_target',
    'memory_max_target',
    'sga_target',
    'sga_max_size',
    'pga_aggregate_target',
    'pga_aggregate_limit',
    'processes',
    'sessions',
    'open_cursors'
)
ORDER BY name