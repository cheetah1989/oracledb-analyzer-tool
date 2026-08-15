/*
    Query Name : asm_diskgroups
    Category   : storage
    Purpose    : Analyze ASM diskgroup capacity
    Source     : V$ASM_DISKGROUP
    Version    : Oracle 19c+

    Notes:
    - Requires appropriate ASM privileges.
    - Query may return no rows when executed against
      a database instance without ASM visibility.
*/

SELECT
    name,
    type,
    total_mb,
    free_mb,
    usable_file_mb,
    required_mirror_free_mb,
    offline_disks,
    state
FROM v$asm_diskgroup
ORDER BY name