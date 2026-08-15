/*
    Query Name : parallelism
    Category   : configuration
    Purpose    : Collect Oracle parallel execution settings
    Source     : V$PARAMETER
    Version    : Oracle 19c+
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
    'parallel_degree_policy',
    'parallel_degree_limit',
    'parallel_min_servers',
    'parallel_max_servers',
    'parallel_servers_target',
    'parallel_min_percent',
    'parallel_threads_per_cpu'
)
ORDER BY name