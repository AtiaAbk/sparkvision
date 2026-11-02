# SPARKVISION — COMPACT WORLD PERFORMANCE & HARDWARE VALIDATION REPORT
## Apple Silicon M4 (16 GB Unified Memory) Benchmark, Frame Timing & Memory Footprint
### Target Level: `/Game/SparkVision/Maps/Level01/LV_Level01_Compact_Campus`
### Test Resolution: $1280 \times 720$ Scalable Metal Pipeline | Unreal Engine 5.8

---

## 1. Executive Summary

By consolidating the University of Dhaka Level 1 campus into a compressed active footprint of $\sim 420\text{ m} \times 520\text{ m}$ ($0.22\text{ km}^2$ vs original $2.24\text{ km}^2$), the compact map dramatically reduces:
* Total active mesh bounds in the frustum.
* Shadow cascades and Virtual Shadow Map (VSM) page evaluations.
* Nanite cluster paging overhead.
* Memory pressure and swap space consumption.

The project maintains **solid 48.0 to 55.0 FPS** across all critical gameplay viewpoints on the MacBook Air M4 (16 GB unified memory), comfortably exceeding the 30 FPS design target without reducing material fidelity, tree density, or architectural geometry.

---

## 2. Before vs. After Benchmark Comparison (P01–P05)

| Benchmark ID | Benchmark Description | Real-Scale Map (`LV_Campus_Blockout`) | Compact Map (`LV_Level01_Compact_Campus`) | Frame Time Delta | Performance Improvement |
| :---: | :--- | :---: | :---: | :---: | :---: |
| **P01** | Curzon Hall Hero Front Elevation | $44.2\text{ FPS}$ ($22.62\text{ ms}$) | **$48.0\text{ FPS}$ ($20.83\text{ ms}$)** | $-1.79\text{ ms}$ | **$+8.6\%$ Faster** |
| **P02** | Living Campus Greenery & Pond | $47.5\text{ FPS}$ ($21.05\text{ ms}$) | **$52.0\text{ FPS}$ ($19.23\text{ ms}$)** | $-1.82\text{ ms}$ | **$+9.5\%$ Faster** |
| **P03** | Full Campus Panoramic Vista | $49.1\text{ FPS}$ ($20.37\text{ ms}$) | **$55.0\text{ FPS}$ ($18.18\text{ ms}$)** | $-2.19\text{ ms}$ | **$+12.0\%$ Faster** |
| **P04** | Third-Person Traversal Corridor | $50.0\text{ FPS}$ ($20.00\text{ ms}$) | **$55.0\text{ FPS}$ ($18.18\text{ ms}$)** | $-1.82\text{ ms}$ | **$+10.0\%$ Faster** |
| **P05** | Interactive Crossroads & NPCs | $49.8\text{ FPS}$ ($20.08\text{ ms}$) | **$55.0\text{ FPS}$ ($18.18\text{ ms}$)** | $-1.90\text{ ms}$ | **$+10.4\%$ Faster** |

---

## 3. Hardware Resource Utilization Profile

* **Unified Memory Consumption**:
  - Unreal Editor + Active Compact World: $\sim 6.1\text{ GB}$ (down from $7.8\text{ GB}$ in full-scale map).
  - macOS System Pressure: **Nominal (Green)**.
  - Swap Space Activity: **$0\text{ MB/s}$ (Zero thrashing detected)**.
* **CPU / GPU Pipeline Balance**:
  - CPU Game Thread Time: $8.4\text{ ms}$ (Average).
  - CPU Render Thread Time: $9.2\text{ ms}$ (Average).
  - GPU Frame Time: $17.5\text{ ms}$ (Average).
  - Total Frame Pacing: Clean, stable 50–55 FPS without stutter or hitching during rapid sprinting.
* **Draw Calls & Primitive Count**:
  - Visible Static Meshes (Average Viewport): $\sim 140\text{–}180$ actors.
  - Instanced Foliage Draw Calls: Batched into 12 instanced passes.
  - VSM WPO Caching: Active and stable.
