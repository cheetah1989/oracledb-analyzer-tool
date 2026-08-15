/*
    Query Name : cpu_memory
    Category   : server
    Purpose    : Collect host CPU and physical memory information
    Source     : V$OSSTAT
    Version    : Oracle 19c+
*/

SELECT
    stat_name,
    value
FROM v$osstat
WHERE stat_name IN (
    'NUM_CPUS',
    'NUM_CPU_CORES',
    'NUM_CPU_SOCKETS',
    'PHYSICAL_MEMORY_BYTES',
    'LOAD',
    'BUSY_TIME',
    'IDLE_TIME',
    'USER_TIME',
    'SYS_TIME',
    'IOWAIT_TIME'
)
ORDER BY stat_name