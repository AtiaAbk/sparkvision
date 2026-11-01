# SparkVision — Recommended Graphics Settings
## Optimized Hardware Profiles for Apple Silicon and PC Targets

---

## 1. Apple Silicon M4 / 16 GB Tier (MacBook Air / Pro) — Primary Target

This profile is configured by default in `Config/DefaultEngine.ini`:

| Setting Category | Recommended Setting | Rationale |
| :--- | :--- | :--- |
| **Global Illumination** | Lumen (Software Ray Tracing / Mesh SDF) | Fast signed distance field ray marching; avoids heavy BLAS rebuilds on Metal |
| **Reflections** | Lumen (Screen Traces + Surface Cache) | High visual accuracy for water, glass, and wet marble with zero RT stalls |
| **Anti-Aliasing** | Temporal Super Resolution (TSR, `r.AntiAliasingMethod=4`) | Superior subpixel detail and temporal stability on architectural geometry |
| **Resolution Scale** | 80% – 85% (`r.ScreenPercentage=85`) | Native-like clarity with TSR upsampling, saving 30% fillrate |
| **Shadows** | Virtual Shadow Maps (VSM) with CSM Caching | Razor-sharp contact shadows, clamped to 2,048 pages for memory stability |
| **Texture Streaming Pool** | 1,000 MB (`r.Streaming.PoolSize=1000`) | Prevents unified memory blowout on 16 GB system memory |
| **Substrate** | Disabled (`r.Substrate=False`) | Uses standard 16 bytes/pixel deferred GBuffer for optimal memory bandwidth |

---

## 2. Low-Power / Battery Saver Profile (M1 / M2 8GB)

For older Apple Silicon laptops or battery-saver play:

```ini
[SystemSettings]
r.ScreenPercentage=70
r.Shadow.Virtual.ResolutionLodBiasDirectional=2
r.Shadow.Virtual.MaxPhysicalPages=1024
r.Streaming.PoolSize=600
r.Lumen.DiffuseFilter.Quality=0
r.Lumen.Reflections.SmoothBias=1
```

---

## 3. High-End Desktop Tier (Apple M4 Max / Discrete PC GPU)

For high-memory workstations:

```ini
[SystemSettings]
r.ScreenPercentage=100
r.Shadow.Virtual.MaxPhysicalPages=4096
r.Streaming.PoolSize=3000
r.Lumen.HardwareRayTracing=1
r.Lumen.Reflections.HardwareRayTracing.Translucent.Refraction.EnableForProject=1
```
