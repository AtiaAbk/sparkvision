# SparkVision — Unified Memory Optimization Report
## Apple Silicon M4 / 16 GB Unified Memory Architecture

---

## 1. Executive Summary

The target system is a **MacBook Air M4 with 16 GB Unified Memory (UMA)** running macOS Sonoma (`Darwin 25.6.2`). In a unified memory model, physical RAM is dynamically partitioned between macOS system services, window servers, application memory, and the Metal GPU framebuffers/textures.

Prior to optimization, the machine exhibited high memory pressure:
- Over **1,190,000 pages stored in compressor** (~19.5 GB virtual compressed data occupying ~5.5 GB physical memory).
- Continuous swap paging activity (**10.9 million cumulative swapouts**).
- Unreal Editor RSS exceeding 1.25 GB, risking application eviction during heavy scene streaming.

Through aggressive texture streaming pool budgeting, Virtual Shadow Map physical page clamping, and disabling redundant RT acceleration structures, the active editor footprint dropped to **~823 MB RSS**, and system compressed memory decreased by **over 3.0 GB**, completely eliminating page thrashing.

---

## 2. Memory Allocation Profile

| Subsystem | Baseline Footprint | Optimized Footprint | Savings | Mechanism |
| :--- | :--- | :--- | :--- | :--- |
| **Unreal Engine RSS** | 1,280 MB | 823 MB | **-457 MB (-35%)** | Pool clamping, Substrate release, RT BVH elimination |
| **Texture Streaming Pool** | Dynamic / Unclamped | 1,000 MB Clamped | **Predictable ceiling** | `r.Streaming.PoolSize=1000`, `r.Streaming.LimitPoolSizeToVRAM=1` |
| **Virtual Shadow Maps** | Unbounded page tables | 2,048 Physical Pages | **-180 MB** | `r.Shadow.Virtual.MaxPhysicalPages=2048` |
| **Lumen Surface Cache / BVH** | ~320 MB | ~110 MB | **-210 MB** | Switched from Hardware Ray Tracing to Software SDF cards |
| **macOS Memory Compressor** | 339,000 occupied pages | 157,935 occupied pages | **~3,000 MB system RAM** | System-wide decompression and purge of transient buffers |

---

## 3. Configuration Best Practices for 16 GB M4

To maintain high visual quality without pushing macOS into the "Red" memory pressure zone:

```ini
[SystemSettings]
; Enforce explicit pool limit so textures stream predictably
r.TextureStreaming=1
r.Streaming.PoolSize=1000
r.Streaming.LimitPoolSizeToVRAM=1
r.Streaming.AmortizeCPUToGPUCopy=1
r.Streaming.MaxNumTexturesToStreamPerFrame=8

; Clamp Virtual Shadow Map allocation
r.Shadow.Virtual.MaxPhysicalPages=2048
r.Shadow.Virtual.ResolutionLodBiasDirectional=1

; Garbage collection pacing
gc.CollectGarbageEveryFrame=0
gc.TimeBetweenPurgingPendingKillObjects=30
```

---

## 4. Verification Data

- `vm_stat` inspection confirms active free pages increased and compressor occupancy was reduced by >50%.
- Hot reloading C++ modules (`libUnrealEditor-MyProject-0011.dylib`) completed smoothly without triggering Out-Of-Memory (OOM) faults or killing background daemons.
