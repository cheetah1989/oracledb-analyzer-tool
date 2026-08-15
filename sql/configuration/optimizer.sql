/*
    Query Name : optimizer
    Category   : configuration
    Purpose    : Collect optimizer-related configuration
    Source     : V$PARAMETER
    Version    : Oracle 19c+

    Purpose:
    Used to assess optimizer behavior and identify
    configuration that may influence SQL execution plans.
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
    'optimizer_mode',
    'optimizer_features_enable',
    'optimizer_dynamic_sampling',
    'optimizer_adaptive_plans',
    'optimizer_adaptive_statistics',
    'optimizer_use_sql_plan_baselines',
    'optimizer_capture_sql_plan_baselines',
    'optimizer_use_invisible_indexes'
)
ORDER BY name