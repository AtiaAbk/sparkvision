# SparkVision — Mac M4 Memory Baseline Report

> **Project**: SparkVision — 2X12: Birth of 36 July  
> **Target Target Hardware**: Apple MacBook Air M4 (16 GB Unified Memory / Metal 3)  
> **Engine Version**: Unreal Engine 5.8 (Source/Development, Apple Silicon arm64)  
> **Date**: November 3, 2026  
> **Diagnostic Source**: Native `memreport -full`, macOS `vm_stat`, `sysctl vm.swapusage`, `top`, Activity Monitor API  
> **Raw Artifact**: `Saved/Profiling/MemReports/LV_Level01_Compact_Campus-MacEditor-11.03-22.25.05/Pid93414_LV_Level01_Compact_Campus-MacEditor-03-22.25.05.memreport`

---

## 1. Executive Summary & Core Diagnostic Findings

Diagnostic benchmarking reveals that SparkVision's primary memory bottleneck on Apple Silicon is **not traditional mesh or game-thread object bloat**, but rather **massive GPU buffer over-allocation within Apple Silicon Unified Memory**:

1. **Metal Unified Memory Over-Allocation (Pooled Render Targets: 1,147.43 MB)**:
   - On macOS Apple Silicon, GPU textures, render targets, and compute buffers share the same physical RAM as the CPU.
   - When allocated, Metal marks these buffers as **Unevictable Wired Memory** (`Pages wired down`).
   - The unoptimized configuration allocated **10 separate 4096×4096 Lumen Surface Cache & Radiosity atlases (64 MB each = 640 MB)** and **128 MB for Virtual Shadow Map Physical Page Pools**, causing the engine alone to wire over **1.15 GB of raw GPU render targets**.

2. **System Memory Exhaustion & Swap Pressure**:
   - In Situation A (Editor Idle): Swap usage was **4,474 MB**, with **5,124 MB wired**.
   - In Situation B (Play In Editor - PIE): Wired memory escalated to **8,939 MB**, forcing swap to jump immediately to **5,532 MB** (+1.05 GB spike).
   - In Situation C (Standalone Game Runtime): Physical memory reached **5,826.41 MB used (Peak: 5,826.41 MB)**, with total host physical RAM consumption reaching **14,740.84 MB / 16,384 MB (90% capacity)**, leaving only **1,643 MB free**.

3. **Indiscriminate Nanite Usage**:
   - All **105 static meshes** in the project currently have `naniteSettings.bEnabled=True`, including low-poly prototype cubes, cylinders, plants, and foliage props.
   - Nanite streaming reserve (`r.Nanite.Streaming.StreamingPoolSize=512`) commands an additional **512 MB fixed streaming pool** in memory.

---

## 2. Quantitative Baseline Across Three Situations

| Metric | Situation A: Editor Idle | Situation B: PIE Gameplay | Situation C: Standalone Runtime (`-game`) |
|---|---|---|---|
| **Primary Process RSS** | 415.6 MB (PID 90183) | 430.0 MB (Editor + PIE) | **1,224.6 MB** (Game Process) |
| **Process Physical Memory** | ~4.2 GB (Host allocated) | ~5.4 GB | **5,826.41 MB** (MemReport measured) |
| **Process Virtual Memory (VSZ)**| 435,080.8 MB (64-bit sparse) | 435,355.9 MB | **433,337.25 MB** |
| **System Wired Memory** | 5,124.5 MB | **8,939.7 MB** | 7,850.0 MB |
| **System Active Memory** | 3,110.1 MB | 1,346.3 MB | 3,517.3 MB |
| **System Inactive Memory** | 3,023.6 MB | 2,100.0 MB | 3,082.5 MB |
| **Compressed Memory** | 4,406.7 MB | 4,085.4 MB | 3,514.6 MB |
| **macOS Swap Used** | 4,474.38 MB | **5,532.69 MB** | **6,184.44 MB** |
| **Total Physical RAM Used** | 12,698 MB / 16 GB | 14,371 MB / 16 GB | **14,740.84 MB / 16,384 MB** (90%) |
| **Free Physical RAM** | 3,686 MB | 2,013 MB | **1,643.16 MB** |
| **CPU Usage** | 15.1% (Idle GUI) | 57.6% (1 Game Thread) | 211.4% (Multi-thread render/tick) |
| **Target Viewport Resolution** | 1280×720 (Editor UI scaled) | 1280×720 (In-viewport) | 1280×720 (Windowed) |

---

## 3. Top Memory Consumers (Ranked by Measured Impact)

### 3.1. Pooled Render Targets (Total: 1,147.43 MB)
*Source: `r.DumpRenderTargetPoolMemory` from MemReport*

| Rank | Render Target Name | Resolution & Format | Memory Allocation | Root Cause / Configuration |
|---|---|---|---|---|
| 1 | `Shadow.Virtual.PhysicalPagePool` | 16384×1024 (R32_UINT) | **128.00 MB** | `r.Shadow.Virtual.MaxPhysicalPages=2048` |
| 2 | `Lumen.RadianceCache.FinalRadianceAtlas` | 4352×4352 (FloatR11G11B10) | **72.25 MB** | Uncapped Radiance Cache probe updates |
| 3 | `Lumen.RadianceCache.RadianceProbeAtlasTextureSource` | 4096×4096 (FloatR11G11B10) | **64.00 MB** | `r.LumenScene.SurfaceCache.AtlasSize=4096` |
| 4 | `Lumen.Radiosity.FilteredTraceRadianceAtlas` | 4096×4096 (FloatR11G11B10) | **64.00 MB** | Full-res Radiosity filter pass |
| 5 | `Lumen.Radiosity.SceneIndirectLighting` | 4096×4096 (FloatR11G11B10) | **64.00 MB** | 4K Indirect Lighting Atlas |
| 6 | `Lumen.Radiosity.TraceRadianceAtlas` | 4096×4096 (FloatR11G11B10) | **64.00 MB** | 4K Radiance Trace Buffer |
| 7 | `Lumen.SceneAlbedo` | 4096×4096 (R8G8B8A8) | **64.00 MB** | 4K Surface Cache Albedo Card Atlas |
| 8 | `Lumen.SceneDirectLighting` | 4096×4096 (FloatR11G11B10) | **64.00 MB** | 4K Direct Lighting Card Atlas |
| 9 | `Lumen.SceneEmissive` | 4096×4096 (FloatR11G11B10) | **64.00 MB** | 4K Emissive Card Atlas |
| 10| `Lumen.SceneFinalLighting` | 4096×4096 (FloatR11G11B10) | **64.00 MB** | 4K Final Lighting Card Atlas |
| 11| `GlobalDistanceField.PageAtlas` | 1024×1024×56 (R8) | **56.00 MB** | 3D Global Distance Field Page Table |
| 12| `Lumen.RadianceCache.DepthProbeAtlasTexture` | 4096×4096 (R16_UINT) | **32.00 MB** | 4K Depth Probe Atlas |
| 13| `Lumen.SceneDepth` | 4096×4096 (G16) | **32.00 MB** | 4K Surface Cache Depth Atlas |
| 14| `Lumen.SceneNormal` | 4096×4096 (R8G8) | **32.00 MB** | 4K Surface Cache Normal Atlas |
| 15| `Shadow.Virtual.HZBPhysicalPagePool` | 8192×512 (R32_FLOAT) | **21.33 MB** | VSM Hierarchical Z-Buffer Pool |
| 16| `Lumen.RadianceCache.FinalRadianceAtlas (Mips)` | 2048×2048 (FloatR11G11B10) | **21.00 MB** | Downsampled Radiance Probe mip pyramid |
| 17| `TSR.History.Color` | 1280×720 (FloatR11G11B10) | **14.06 MB** | Temporal Super Resolution History |
| 18| `Lumen.RadianceCache.TempRadianceProbeAtlas` | 2048×1376 (FloatR11G11B10) | **10.75 MB** | Transient probe evaluation target |
| 19| `Shadow.Virtual.PageReceiverMasks` | 4608×384 (R32_UINT) | **9.00 MB** | VSM Receiver Mask bitfield |
| 20| `DistanceFields.DistanceFieldBrickTexture` | 1024×1024×8 (G8) | **8.00 MB** | Object Distance Field 3D volume |

> **Key Takeaway**: Lumen surface cache and radiosity atlases alone account for **641.25 MB** of pooled render targets. Virtual Shadow Maps consume **164.33 MB**.

---

### 3.2. Static & Skeletal Mesh Resources
*Source: `obj list -resourcesizesort` from MemReport*

- **Skeletal Meshes (Total: 25.91 MB NumKB / 6.75 MB Resource)**:
  - `/Game/Characters/Mannequins/Meshes/SKM_Manny_Simple`: 13.54 MB object size, 3.53 MB GPU resource.
  - `/Game/Characters/Mannequins/Meshes/SKM_Quinn_Simple`: 12.99 MB object size, 3.39 MB GPU resource.
- **Static Meshes (Total: 10.04 MB Resource across 102 loaded meshes)**:
  - `SM_Curzon_Entrance_Portal`: 423.23 KB resource
  - `SM_Natural_Raintree_Grand`: 347.41 KB resource
  - `SM_Natural_Krishnachura_Bloom`: 299.02 KB resource
  - `SM_Natural_Banyan_Heritage`: 284.16 KB resource
  - `SM_Garden_Flowerbed_Circular`: 279.28 KB resource
  - `SM_Tree_Krishnachura_Natural`: 205.31 KB resource
  - `SM_Tree_Banyan_Natural`: 191.50 KB resource

---

### 3.3. Textures & Streaming Pools
*Source: `ListTextures` & `texture_audit.json`*

- **Current Active In-Memory Texture Size**: **37.69 MB** (Disk Size: 173.68 MB across 166 textures).
- **Format Breakdown**:
  - `PF_FloatRGBA`: 17.09 MB in-memory (HDR cubemaps and cloud LUTs)
  - `PF_B8G8R8A8`: 15.13 MB in-memory (Uncompressed UI and cloud volume slices)
  - `PF_G8`: 2.75 MB in-memory
  - `PF_DXT1`: 2.19 MB in-memory
  - `PF_DXT5`: 0.32 MB in-memory
  - `PF_BC5`: 0.19 MB in-memory
- **Configured Pools (Cvars)**:
  - `r.Streaming.PoolSize`: Currently set to **750 MB** (was 1000 MB).
  - `r.Nanite.Streaming.StreamingPoolSize`: Set to **512 MB**.
  - `bNeverStream=True`: 1 texture detected (`/Game/Characters/Mannequins/Textures/Shared/T_UE_Logo_M`).
  - Large (2048×2048) Textures: 21 authored textures, including distant skyline towers (`T_ModernSkyline_Facade_CurtainWall_D/N`).

---

### 3.4. Level & Actor Population
*Source: Scene Actor Audit*

- **Active Map**: `/Game/SparkVision/Maps/Level01/LV_Level01_Compact_Campus`
- **Total Loaded Actors**: **439**
  - `StaticMeshActor`: 391
  - `SVStudentNPC`: 15
  - `SVHostileOpponent`: 7
  - `SVArchiveTerminal`: 6
  - `SkeletalMeshActor`: 3
  - Environment & Atmosphere actors: 6 (DirectionalLight, SkyLight, SkyAtmosphere, VolumetricCloud, Fog, PostProcessVolume)

---

## 4. Root Causes of Excessive Memory Consumption

1. **Inflated Lumen Surface Cache Resolution**:
   - `r.LumenScene.SurfaceCache.AtlasSize` configured at `4096` causes Unreal to allocate ten 4K 16-bit float / 32-bit textures.
   - On a 16 GB Apple Silicon machine, this single parameter forces over 640 MB of unevictable GPU memory allocation.
2. **Excessive Virtual Shadow Map Page Reservation**:
   - `r.Shadow.Virtual.MaxPhysicalPages=1024` (and formerly 2048) allocates a 16384×1024 page pool (128 MB) + HZB pool (21.33 MB) + page tables (20+ MB) = ~170 MB.
3. **Over-provisioned Nanite Streaming Pool**:
   - `r.Nanite.Streaming.StreamingPoolSize=512` reserves 512 MB of streaming buffer space regardless of scene complexity.
4. **Over-provisioned Texture Streaming Pool**:
   - `r.Streaming.PoolSize=750` commits 750 MB of RAM on a 16 GB unified system where OS + Editor already demand 8+ GB.
5. **Distant Horizon Assets Using 2K Textures & Nanite**:
   - Inaccessible modern skyline towers and perimeter walls share the same 2048 texture budgets as hero Curzon Hall assets.

---

## 5. Target Memory Budget for MacBook Air M4 (16 GB Unified RAM)

To guarantee that macOS memory pressure remains strictly **Green** and prevent disk swap expansion during gameplay, the following hardware budget is established:

```
Total Hardware RAM: 16,384 MB Unified Memory
├── macOS OS + WindowServer + Metal Core:  3,500 MB
├── Compressed Cache Headroom:             2,000 MB
└── SparkVision Game Target Budget:        5,500 MB (Down from 8,900 MB)
    ├── Executable & Engine Core:            800 MB
    ├── Game Thread & C++ State:             400 MB
    ├── Asset Registry & Name Table:         160 MB
    ├── Texture Streaming Pool:              400 MB (Calibrated from 750 MB)
    ├── Nanite Streaming Pool:               150 MB (Calibrated from 512 MB)
    ├── Lumen Surface Cache (Atlas 2048):    160 MB (Calibrated from 640 MB)
    ├── Virtual Shadow Map Pages (512 pgs):   45 MB (Calibrated from 170 MB)
    ├── Mesh & Static Buffers:               250 MB
    ├── Skeletal Animation & Rig:            150 MB
    └── Dynamic Render Targets (720p TSR):   285 MB
```

---

## 6. Optimization Roadmap

1. **Rendering & Lumen Calibration**:
   - Set `r.LumenScene.SurfaceCache.AtlasSize=2048` (saves ~480 MB VRAM).
   - Set `r.Shadow.Virtual.MaxPhysicalPages=512` (saves ~96 MB VRAM).
   - Set `r.Nanite.Streaming.StreamingPoolSize=150` (saves ~362 MB VRAM).
   - Set `r.Streaming.PoolSize=400` (saves ~350 MB RAM).
2. **Texture Clamping & Cleaning**:
   - Disable `neverStream` on `T_UE_Logo_M`.
   - Set `maxTextureSize=1024` on distant skyline and background backdrop textures.
3. **Foliage & Mesh Culling**:
   - Tune `foliage.MinimumScreenSize` and `grass.CullDistanceScale` to cull distant vegetation meshes.
   - Disable Nanite on non-complex primitive props (Cubes, Cylinders, Planes) and small foliage where overhead exceeds benefit.
4. **Validation & Packaging**:
   - Re-measure memory under all 3 situations.
   - Validate 10 gameplay scenarios and verify zero memory leak accumulation across mission transitions.
