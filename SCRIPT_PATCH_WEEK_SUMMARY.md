# Script Patch & Script Week Summary

This document summarizes the contents and structure of the `script_patch` and `script_week` directories. It complements the detailed function-level inventory in [revival project/FILE_ANALYSIS_SUMMARY.txt](revival%20project/FILE_ANALYSIS_SUMMARY.txt).

---

## Overview

| Directory | Purpose | File Count | Notes |
|---|---|---:|---|
| `revival project/script_patch/` | Main game scripts (patchable runtime modules) | 4,896 | Primary codebase used at runtime |
| `revival project/script_week/` | Weekly/rolling update scripts | 244 | Smaller, time-based patches |

> File counts were measured on **January 31, 2026**.

---

## script_patch (Primary Runtime Code)

### Structure

- Organized into numeric folders (`0`..`999`), each containing one or more Python files.
- Contains the main gameplay logic, UI systems, managers, scene logic, and data helpers.
- This is the **primary source of game behavior** in the revival project.

### Function Inventory (High-Level)

A full function listing is available in:
- [revival project/FILE_ANALYSIS_SUMMARY.txt](revival%20project/FILE_ANALYSIS_SUMMARY.txt)

Key types of systems observed in the inventory:

- **Core gameplay systems:** weapon handling, movement, combat, state machines
- **UI systems:** login UI, lobby, battle UI, widgets, dialogs
- **Managers:** resource loaders, patch utilities, data caches
- **Networking stubs:** client/server RPC wrappers (some unused in offline mode)
- **Utility layers:** math, file handling, configuration parsing

### Important Notes

- The offline system is integrated in [785_17524466876519882393.py](785_17524466876519882393.py).
- The bootstrap entry logic is in [revival project/script_patch/573/10076230044261121434.py](revival%20project/script_patch/573/10076230044261121434.py).
- The login scene is in [revival project/script_patch/609/11026820604907119192.py](revival%20project/script_patch/609/11026820604907119192.py).
- The Manager fix is in [revival project/script_patch/422/14606205992556332510.py](revival%20project/script_patch/422/14606205992556332510.py).

---

## script_week (Weekly Update Layer)

### Structure

- Mirrors the numeric folder structure seen in `script_patch`.
- Typically smaller in size, containing **weekly or incremental updates**.
- Used for rolling changes and adjustments without replacing the entire base.

### Observed Characteristics

- File count is significantly smaller than `script_patch` (244 vs 4,896).
- Intended for incremental update cadence, likely tied to weekly release cycles.
- Good candidate for tracking deltas over time if periodic diffs are needed.

---

## Recommendations for Future Analysis

If you want deeper analysis, the next best steps are:

1. **Diff weekly patches vs primary scripts** to identify changes:
   - Compare same numeric folders between `script_patch` and `script_week`.
2. **Generate function summaries** specifically for `script_week` for update analysis.
3. **Track weekly changes by date** to build a rolling changelog.

---

## Related Documentation

- [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)
- [CHANGELOG.md](CHANGELOG.md)
- [MODIFICATIONS.md](MODIFICATIONS.md)
- [ARCHITECTURE.md](ARCHITECTURE.md)
- [revival project/FILE_ANALYSIS_SUMMARY.txt](revival%20project/FILE_ANALYSIS_SUMMARY.txt)

---

*Last Updated: January 31, 2026*
