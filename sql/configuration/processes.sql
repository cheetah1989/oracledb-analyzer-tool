/*
    Query Name : processes
    Category   : configuration
    Purpose    : Collect Oracle process and session limits
    Source     : V$PARAMETER
    Version    : Oracle 19c+

    Purpose:
    Used to assess whether configured process/session capacity
    is appropriate for the observed application workload.
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
    'processes',
    'sessions',
    'transactions',
    'license_max_users',
    'resource_limit'
)
ORDER BY name