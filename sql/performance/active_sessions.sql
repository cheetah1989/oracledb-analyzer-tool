/*
    Query Name : active_sessions
    Category   : performance
    Purpose    : Identify currently active database sessions
    Source     : V$SESSION, V$SQL
    Version    : Oracle 19c+
*/

SELECT
    s.sid,
    s.serial#,
    s.username,
    s.status,
    s.type,
    s.machine,
    s.program,
    s.module,
    s.action,

    s.sql_id,
    s.sql_child_number,

    s.event,
    s.wait_class,
    s.state,

    s.seconds_in_wait,
    s.last_call_et,

    ROUND(
        NVL(q.cpu_time, 0) / 1000000,
        2
    ) AS sql_cpu_seconds,

    ROUND(
        NVL(q.elapsed_time, 0) / 1000000,
        2
    ) AS sql_elapsed_seconds,

    SUBSTR(
        q.sql_text,
        1,
        1000
    ) AS sql_text

FROM v$session s

LEFT JOIN v$sql q
    ON s.sql_id = q.sql_id
    AND s.sql_child_number = q.child_number

WHERE s.status = 'ACTIVE'
  AND s.type = 'USER'

ORDER BY
    NVL(q.cpu_time, 0) DESC