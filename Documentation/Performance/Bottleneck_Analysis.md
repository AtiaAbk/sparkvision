# SparkVision — Real Bottleneck Analysis & Root Cause Diagnosis

## 1. Problem Classification Matrix

| Category | Primary Root Cause | Evidence | Severity | Proposed Fix |
| :--- | :--- | :--- | :--- | :--- |
| **GPU / Memory Bandwidth** | **Substrate (Strata) enabled** with 80 bytes/pixel GBuffer format | `Config/DefaultEngine.ini:161` (`r.Substrate=True`, `BytesPerPixel=80`) | **CRITICAL** | Disable Substrate in favor of standard UE5 Deferred GBuffer (16 bytes/pixel). |
| **GPU Compute & VRAM** | **Hardware Ray Tracing & Path Tracing** enabled in RendererSettings | `Config/DefaultEngine.ini:60,70,73` (`r.Lumen.HardwareRayTracing=True`, `r.PathTracing=True`) | **HIGH** | Switch to Software Lumen (SDF & Screen Tracing) which is native to Apple Silicon Metal. |
| **GPU Shadow Memory** | **CSM Caching Disabled & VSM Page Thrashing** | `Config/DefaultEngine.ini:116` (`r.Shadow.CSMCaching=False`) | **MEDIUM** | Enable Shadow Caching and clamp VSM Physical Pages to 2048 to prevent memory blowout. |
| **GPU Render Target** | **MSAA 4x enabled on Deferred Renderer** without Temporal Antialiasing | `Config/DefaultEngine.ini:103-104` (`r.AntiAliasingMethod=0`, `r.MSAACount=4`) | **MEDIUM** | Switch to Temporal Super Resolution (TSR, `r.AntiAliasingMethod=4`) for high temporal stability and dynamic resolution scaling. |
| **CPU Game Thread** | **Unthrottled Per-Frame Multi-Sphere Collision Sweeps & String Searches** | `ASVCharacter::Tick` running `SphereTraceMultiForObjects` & `GetCurrentLandmarkName` at 60 Hz | **MEDIUM** | Throttle interaction sweep to 10 Hz (every 0.10s) and cache landmark name. |
| **Unified Memory** | **Texture Streaming Pool Unclamped** | `Config/DefaultEngine.ini:208` set to 1000 MB; needs explicit pool budget enforcement on 16GB UMA | **LOW** | Enforce texture streaming pool size and amortize CPU-to-GPU copies. |
