/*
    Query Name : blocking_sessions
    Category   : stability
    Purpose    : Identify sessions involved in blocking
*/

SELECT
    w.inst_id AS waiting_inst_id,
    w.sid AS waiting_sid,
    w.serial# AS waiting_serial,
    w.username AS waiting_user,
    w.sql_id AS waiting_sql_id,
    w.event AS waiting_event,

    b.inst_id AS blocking_inst_id,
    b.sid AS blocking_sid,
    b.serial# AS blocking_serial,
    b.username AS blocking_user,
    b.sql_id AS blocking_sql_id,
    b.module AS blocking_module,
    b.machine AS blocking_machine,

    w.seconds_in_wait
FROM gv$session w
JOIN gv$session b
    ON w.blocking_instance = b.inst_id
   AND w.blocking_session = b.sid
WHERE w.blocking_session IS NOT NULL
ORDER BY
    w.seconds_in_wait DESC