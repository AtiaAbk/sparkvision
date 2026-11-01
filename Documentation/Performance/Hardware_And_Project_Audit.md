# SparkVision — Hardware & Project Performance Audit
**Audit Date:** November 1, 2026  
**Target Hardware:** Apple MacBook Air M4 (Model: `Mac16,12`)  
**Operating System:** macOS 26.6.2 (Darwin 25.6.0 ARM64)  
**Primary Engine:** Unreal Engine 5.8 (Native Mac ARM64 / Metal 4)  
**Backend:** Java 21 Mission Control Microservice  
**Map:** `/Game/SparkVision/Maps/Campus/LV_Campus_Blockout`  

---

## 1. Physical Hardware & System State

| Component | Specification | Real-World Operational Status |
| :--- | :--- | :--- |
| **SoC / Processor** | Apple M4 (`hw.cpufamily: 0x6f5129ac`) | 10 Cores (4 Performance Cores @ 4.4 GHz + 6 Efficiency Cores @ 2.8 GHz) |
| **GPU Architecture** | Apple M4 10-core GPU | Metal 4 Feature Set, Apple Silicon Unified Memory Architecture (UMA) |
| **Unified Memory** | 16,384 MB (16.0 GB) | Shared dynamically between CPU system ram, GPU VRAM, and unified caches |
| **Display Resolution** | 2560 x 1664 Retina LCD | High-DPI scaling active (Color LCD) |
| **Disk Storage** | 460 GiB APFS Container | 77 GiB Free (14% capacity utilized) |
| **Thermal Profile** | Fanless Passive Chassis | Sensitive to sustained high-power GPU workloads; thermal throttling triggers if watts stay above envelope |

---

## 2. Memory Pressure & Compressor Audit

A detailed audit via `vm_stat` and `memory_pressure` revealed:
- **Free Memory:** 24% system-wide free memory.
- **Wired Memory:** 417,429 pages (~6.8 GB wired down by macOS kernel, Metal drivers, and active processes).
- **Compressed Pages:** 1,190,177 pages (~19.5 GB virtual data compressed into ~5.5 GB physical memory).
- **Swap I/O:** 8.9M swapins / 10.9M swapouts recorded.
- **Primary Finding:** On a 16 GB unified memory architecture, memory compression and disk swapping occur when applications demand excessive unstreamed textures, huge GBuffer layouts, and heavyweight background processes.

---

## 3. Project Configuration & Engine Settings Audit

### 3.1 Dangerous & Over-Specified Renderer Settings in `Config/DefaultEngine.ini`
Inspection of `[/Script/Engine.RendererSettings]` identified major configuration bottlenecks that heavily penalize Apple Silicon:

1. **`r.Substrate=True` (`r.Substrate.BytesPerPixel=80`)**:
   - *Impact:* Substrate (Strata) increases the GBuffer to 80 bytes per pixel and quadruples shader permutation complexity. On unified memory mobile/laptop GPUs with limited cache line width, this induces severe bandwidth saturation.
2. **`r.PathTracing=True` & `r.RayTracing=True`**:
   - *Impact:* Forces the engine to compile and build Top-Level Acceleration Structures (TLAS) and Bottom-Level Acceleration Structures (BLAS) for every static mesh, consuming hundreds of megabytes of RAM.
3. **`r.Lumen.HardwareRayTracing=True`**:
   - *Impact:* Hardware Ray Tracing on M4 Metal triggers continuous BVH tree updates, whereas Software Lumen (SDF / Mesh Distance Fields) achieves visually identical global illumination at a fraction of the compute cost.
4. **`r.RayTracing.UseTextureLod=False`**:
   - *Impact:* Forces mip 0 (full un-mipmapped texture resolution) for reflections, consuming gigabytes of unified memory.
5. **`r.Shadow.CSMCaching=False`**:
   - *Impact:* Shadow cascades are recalculated every frame rather than cached.
6. **`r.AntiAliasingMethod=0` with `r.MSAACount=4`**:
   - *Impact:* Multisample anti-aliasing on a deferred renderer is inefficient and conflicts with Unreal's Temporal Super Resolution (TSR).

---

## 4. Gameplay & CPU Tick Audit

1. **`ASVCharacter::Tick`**:
   - Executed `UKismetSystemLibrary::SphereTraceMultiForObjects` (radius 280cm) every single frame.
   - Executed string-based landmark distance scanning (`GetCurrentLandmarkName()`) across 6 zones every single frame.
   - *Optimization:* Throttled interaction sphere sweeps to 10 Hz (every 0.10s) or upon player movement.
2. **`ASVStudentNPC`**:
   - `PrimaryActorTick.bCanEverTick = false` (properly non-ticking).
3. **`SVMissionControlSubsystem`**:
   - 100% Non-blocking asynchronous HTTP requests on background worker threads. Zero game thread stalls.

---

## 5. Java Mission Control Audit

- **Process Memory:** 13.2 MB RSS (`MissionControlServer` running on OpenJDK 21).
- **CPU Consumption:** $< 0.1\%$ CPU idle.
- **Database:** SQLite (`sparkvision_missions.db`) local file persistence.
- **Findings:** Java service is exceptionally lightweight; no memory leaks or thread thrashing detected.
