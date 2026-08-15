/*
    Query Name : long_transactions
    Category   : stability
    Purpose    : Identify long-running active transactions
*/

SELECT
    s.inst_id,
    s.sid,
    s.serial#,
    s.username,
    s.status,
    s.sql_id,
    s.module,
    s.machine,

    t.start_time,
    ROUND(
        (SYSDATE - TO_DATE(t.start_time, 'MM/DD/YY HH24:MI:SS')) * 24,
        2
    ) AS transaction_hours,

    t.used_ublk AS undo_blocks,
    t.used_urec AS undo_records

FROM gv$transaction t
JOIN gv$session s
    ON t.addr = s.taddr
   AND t.inst_id = s.inst_id

ORDER BY
    t.used_ublk DESC