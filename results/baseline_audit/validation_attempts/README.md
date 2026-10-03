# Incomplete development runs

These runs are retained for traceability and are excluded from all scientific totals.

- `llvm10_canonical_smoke`: bitcode serialization differed although full textual IR matched; the identity check was corrected.
- `llvm10_canonical_attempt1`: attribute insertion needed to follow `local_unnamed_addr`; covered by the regression fixture. Two concurrent launches briefly targeted this directory, so it must not be used. The runner now prevents concurrent writers with a directory lock.
- `llvm10_source_check_attempt1`: the bundled tool archive lacked llvm-objcopy; the completed source check uses system llvm-objcopy-14 solely for extracting section bytes.
