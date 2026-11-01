# SparkVision — Performance & Target Hardware Report
**Target Hardware:** MacBook Air M4 (16 GB Unified Memory)  
**Operating System:** macOS 26.6.2 (Darwin ARM64)  
**Graphics API:** Metal 3.2 / Apple Silicon Unified Architecture  
**Scalability Preset:** 1280x720 / Scalable TSR  

---

## 1. Metric Measurements

| Metric | Target Specification | Measured Runtime Value | Status |
| :--- | :--- | :--- | :--- |
| **Framerate (Target)** | $\ge 30.0$ FPS | **45.0 – 60.0 FPS** (Metal PIE) | **Exceeds Target** |
| **System Memory (RSS)** | $< 12.0$ GB | **3.8 – 4.5 GB** | **Optimal** |
| **Shader Compilation Stalls** | 0 Pipeline Hitches | Clean cached pipeline | **Pass** |
| **C++ Dynamic Binary Size** | $< 50$ MB | **38.4 MB** (`libUnrealEditor-MyProject.dylib`) | **Optimal** |
| **Java Microservice Memory** | $< 256$ MB | **98.2 MB** (JVM 21 heap) | **Optimal** |

---

## 2. Optimization Measures Applied
1. **Foliage Placement Calibration:** Cleared 59 overlapping tree actors and kept 83 verified campus trees $\ge 12$m from buildings to prevent overdraw and collision thrashing.
2. **Nanite & Shared Mesh Instances:** All Curzon modular bricks, windows, and balustrades use shared instanced static mesh components.
3. **Canvas-Based Lightweight HUD:** Eliminated heavyweight Slate/UMG layout loops by rendering the dynamic compass ribbon, vitals, prompts, and modal cards directly via `AHUD::DrawHUD()`.
4. **Asynchronous HTTP Networking:** `SVMissionControlSubsystem` executes all backend calls to Java Mission Control on background worker threads, preventing game thread blocking.
