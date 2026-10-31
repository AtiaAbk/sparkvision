# CURZON HALL DEFECT CORRECTION & ITERATION LOG
**Project**: SparkVision — Level 1 University of Dhaka Digital Twin  
**Tracking Cycle**: Phase 1 Blockout $\rightarrow$ Phase 2 Architectural Analysis $\rightarrow$ Phase 3 Precision Reconstruction $\rightarrow$ Final Polish.

---

## 1. Defect Tracking Matrix

| Defect ID | Severity | Subsystem / Component | Defect Description (Legacy Implementation) | Root Cause Analysis | Corrective Action & Verification | Status |
|---|---|---|---|---|---|---|
| **DEF-CH-001** | CRITICAL | Geometry / Arches | Veranda openings were modeled as flat rectangular box extrusions with sharp $90^\circ$ corners. | Script used basic `bmesh.ops.create_cube` without profile curve subdivision. | Replaced with mathematical B-spline curve generators producing true Moorish horseshoe and 7-cusp multi-foil profiles. | **CLOSED** |
| **DEF-CH-002** | CRITICAL | Massing / Central Portal | Central entrance was an unarticulated flat box missing the 2-storey monumental archway and rooftop pavilions. | Over-simplification during early blockout phase. | Engineered dedicated `SM_Curzon_Entrance_Portal` with recessed porch, clock pediment, and paired chhatris. | **CLOSED** |
| **DEF-CH-003** | HIGH | Silhouette / Roofline | Parapet was completely flat and featureless; occasional concept drawings incorrectly placed a giant dome. | Lack of archival drawing verification. | Designed modular `SM_Curzon_Parapet_Merlons` with stepped Indo-Saracenic battlements; strictly removed all non-authentic central domes. | **CLOSED** |
| **DEF-CH-004** | HIGH | Architecture / Eaves | Walls lacked the characteristic projecting *chhajjas* (slanted eaves) and corbel support brackets. | Absence of eave geometry in modular bay meshes. | Integrated $1.2\text{ m}$ sloped terracotta chhajjas with carved brackets every $1.0\text{ m}$ into both upper and lower veranda modules. | **CLOSED** |
| **DEF-CH-005** | HIGH | Massing / Corner Towers | Corner towers were simple low octagonal cylinders lacking observation balconies and authentic Rajput cupolas. | Placeholder geometry used during preliminary layout. | Reconstructed full $25.2\text{ m}$ towers (`SM_Curzon_Tower_Octagon`) with tiered windows, corbelled balconies, and domed chhatris. | **CLOSED** |
| **DEF-CH-006** | MEDIUM | Gameplay / Collision | Player experienced snagging when walking through veranda corridors due to overlapping collision primitives. | Simple box colliders collided with door frames and column bases. | Enabled `CTF_UseComplexAsSimple` per-poly collision on veranda corridors, walkways, and stairs. Traversal verified 100% smooth. | **CLOSED** |
| **DEF-CH-007** | MEDIUM | Shading / Materials | Brick material appeared as uniform flat red paint with zero tonal variation or mortar depth. | Simple untextured constant RGB parameter shader. | Created multi-layered PBR materials with normal maps, roughness variation, chuna-surki mortar joints, and weathered dampness. | **CLOSED** |
| **DEF-CH-008** | LOW | Lighting / Shadowing | Under-arch shadows were unnaturally harsh or pitch black in Software Lumen mode. | Insufficient skylight bounce and lack of interior bounce geometry. | Adjusted Lumen Scene Detail to 2.0, boosted indirect lighting intensity, and added ambient fill point lights at colonial lanterns. | **CLOSED** |

---

## 2. Verification Sign-Off
All 8 identified defects from the preliminary audit have been systematically addressed, verified in 3D modeling DCC (Blender 5.2.3 LTS), imported into Unreal Engine 5.8, assembled into `/Game/SparkVision/Maps/Campus/LV_Campus_Blockout`, and validated via runtime Play-In-Editor (PIE) camera captures.
