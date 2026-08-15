/*
    Query Name : os_stats
    Category   : environment
    Purpose    : Collect basic operating system statistics
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
    'PHYSICAL_MEMORY_BYTES'
)