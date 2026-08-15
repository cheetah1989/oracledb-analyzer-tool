/*
    Query Name : cursor
    Category   : configuration
    Purpose    : Collect Oracle cursor and parsing configuration
    Source     : V$PARAMETER
    Version    : Oracle 19c+

    Purpose:
    Used to assess cursor reuse, parsing behavior and
    potential application scalability issues.
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
    'open_cursors',
    'session_cached_cursors',
    'cursor_sharing',
    'cursor_space_for_time',
    'session_max_open_files'
)
ORDER BY name