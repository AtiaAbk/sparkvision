# SPARKVISION — ENVIRONMENT QUALITY AUDIT CHECKLIST

## 1. Title & Executive Purpose

* **Document**: `EnvironmentQualityChecklist.md`
* **Purpose**: A comprehensive 25-point visual and technical verification checklist required before promoting any landmark, environment module, or campus zone to approved status.

---

## 2. The 25-Point Environment Verification Matrix

### A. Architectural & Historical Fidelity (Points 1–5)
1. [ ] **Authentic Silhouette**: Does the building profile match real-world photographic evidence? (e.g. no fictional central dome on Curzon Hall).
2. [ ] **Metric Scale (1m = 100uu)**: Are door apertures, stair risers, railings, and ceilings anatomically plausible relative to the 180cm character?
3. [ ] **Ornamental Detailing**: Are characteristic regional features (chhatris, cusped arches, chhajja eaves, jali screens) present?
4. [ ] **Historical Grounding**: Does the landmark reflect its real mid-20th-century historical condition?
5. [ ] **Compound Boundaries**: Are perimeter boundaries realistic (wrought iron, low brick walls, hedge lines) rather than invisible forcefields?

### B. Visual Quality & Presentation (Points 6–10)
6. [ ] **3-Point Depth Layering**: Does the composition feature distinct foreground, middle-ground, and background visual elements?
7. [ ] **Atmospheric Depth**: Is exponential height fog balanced so distant areas softly fade without drowning foreground detail?
8. [ ] **Lighting Contrast**: Are sunlit surfaces cleanly contrasted against ambient shadows without pitch-black occlusion?
9. [ ] **Silhouette Legibility**: Are landmarks recognizable from distance as guiding beacons?
10. [ ] **Foliage Integration**: Are trees, shrubs, and lawns organically clustered around structures rather than floating in isolation?

### C. Material & Texturing Standards (Points 11–15)
11. [ ] **PBR Roughness Calibration**: Are brick, stone, and plaster materials appropriately matte ($0.70 - 0.95$) with zero unphysical glossiness?
12. [ ] **Metallic Discipline**: Is metallic set strictly to $0.0$ for non-metals (brick, wood, stone, glass) and $>0.8$ for iron fixtures?
13. [ ] **Texel Density**: Is texture resolution consistent across modular architectural modules (minimum $10.24\text{ px/cm}$)?
14. [ ] **Weathering & Wear**: Do lower plinths, corners, and rain channels show appropriate humidity staining and dust accumulation?
15. [ ] **No Texture Tiling Repetition**: Are micro/macro variation blending nodes used to hide repetitive tiling patterns?

### D. Collision & Player Traversal (Points 16–20)
16. [ ] **Solid Walkable Ground**: Does downward collision trace confirm continuous blocking hits without gaps or pitfalls?
17. [ ] **No Snagging on Stairs**: Are staircases covered with smooth invisible collision ramps ($35^\circ$ incline) to prevent camera jitter?
18. [ ] **Zero Encroaching Volumes**: Is the `PlayerStart` clear of all collision bounds (minimum $50\text{ cm}$ clearance)?
19. [ ] **Proper Pawn Profiles**: Do non-walkable ornamental railings and fences properly block player pawns while letting camera pass?
20. [ ] **Clean Doorway Clearances**: Are entrances at least $150\text{ cm}$ wide and $240\text{ cm}$ high for smooth camera clearance?

### E. Performance & Technical Optimization (Points 21–25)
21. [ ] **Nanite Enabled**: Are high-polygon static meshes converted to Nanite geometry?
22. [ ] **Lumen Compatibility**: Are two-sided materials and mesh cards properly configured for Lumen hardware ray-tracing?
23. [ ] **LOD Setup**: Do non-Nanite meshes possess clean 3-tier LOD decay reductions?
24. [ ] **Draw Call Budget**: Does the scene stay under 2,500 draw calls in dense courtyard views?
25. [ ] **Memory Footprint**: Does total VRAM usage remain comfortably within the 16 GB Apple Silicon unified memory ceiling?

---

## 3. Current Status

* **Status**: `COMPLETED`
* **Evidence**:
  - Curzon Hall Hero environment evaluated against all 25 points during Phase 2 Quality Gate; score: 25/25 verified.
* **Remaining Tasks**:
  - Apply checklist to Doyel Chattar and Shaheed Minar during Phase 3 review.
