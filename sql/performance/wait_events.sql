/*
    Query Name : wait_events
    Category   : performance
    Purpose    : Identify significant database wait events
    Source     : V$SYSTEM_EVENT
    Version    : Oracle 19c+
*/

SELECT
    event,
    wait_class,
    total_waits,
    ROUND(
        time_waited_micro / 1000000,
        2
    ) AS total_wait_seconds,

    ROUND(
        CASE
            WHEN total_waits = 0 THEN 0
            ELSE time_waited_micro / total_waits / 1000
        END,
        2
    ) AS avg_wait_ms,

    ROUND(
        CASE
            WHEN total_waits = 0 THEN 0
            ELSE
                time_waited_micro
                / SUM(time_waited_micro)
                  OVER ()
                * 100
        END,
        2
    ) AS wait_percentage

FROM v$system_event

WHERE wait_class <> 'Idle'

ORDER BY
    time_waited_micro DESC
FETCH FIRST 30 ROWS ONLY