# Existing linked CHStone artifacts: independent size check

All 24 ELF hashes match the previously executed fixed-vector checks. No compiler, linker or executable was run. Selection remains the frozen object-code rule.

| Linked metric | Reference sum | Selected sum | Saving | W/T/L |
|---|---:|---:|---:|---:|
| text_section_bytes | 34,907 | 34,513 | 1.129% | 5/7/0 |
| berkeley_text_bytes | 126,792 | 126,601 | 0.151% | 4/7/1 |
| berkeley_data_bytes | 6,784 | 6,784 | 0.000% | 0/12/0 |
| berkeley_bss_bytes | 46,464 | 46,464 | 0.000% | 0/12/0 |
| file_bytes | 274,152 | 274,016 | 0.050% | 5/7/0 |

These are dynamically linked, unstripped x86-64 ELF files linked with -no-pie. File bytes include metadata and padding; shared-library contents are not included. The object-code fallback gives no guarantee for these linked metrics. The existing fixed-vector checks are not a semantic proof or a runtime measurement.

Reproduce in the existing container:

```sh
docker exec cgym-audit python scripts/audit_linked_selector.py
```
