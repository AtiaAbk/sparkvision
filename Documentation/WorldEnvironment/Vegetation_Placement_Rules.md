# SPARKVISION — VEGETATION PLACEMENT RULES & VALIDATION PROTOCOL
## Strict Architectural Protection, Traversal Envelopes & Automated Audit Criteria

---

### Executive Mandate

Under the **Open Campus & Natural Density Override**, every tree, shrub, hedge, and plant in SparkVision must have a validated, deliberate, and geometrically sound position. Random scattering and unverified placement are strictly prohibited.

---

### 1. Absolute Placement Prohibitions (Zero Tolerance)

The automated audit suite rejects any placement violating the following rules:

1. **Building Intersection**:
   * Zero tree trunks, branches, or leaf cards may intersect building exterior walls, parapets, chhajjas, colonnades, or roofs.
   * Zero foliage may enter interior veranda corridors, classrooms, or windows.
2. **Roadway & Traversal Obstruction**:
   * Zero tree trunks may be planted on asphalt roads, pedestrian sidewalks, paved plinths, or public staircases.
   * Lower branches overhanging roads must have at least $4.5\text{ m}$ ($450\text{ cm}$) vertical clearance.
3. **Monument Sightline Occlusion**:
   * Curzon Hall central entrance portal must remain 100% visible along its primary south approach axis (`Y: -1500 to +1500, X: -7500 to -2500`).
   * Central Shaheed Minar red sun disc must remain 100% visible from the south arrival courtyard.
   * Raju Memorial Sculpture must have a clear 15-meter circular clearance buffer.
4. **Signboard & Plaque Occlusion**:
   * Department of Physics blue signboard on Curzon East wing must have an unobstructed view from the walkway.
5. **Terrain Floating & Burial**:
   * Zero floating trees (root flare must intersect ground surface by exactly $5 - 15\text{ cm}$ to simulate natural root embedding).
   * Zero buried shrubs (foliage origin must rest on ground surface).
6. **Bamboo Placement**:
   * Bamboo clusters (*Bambusa tulda*) are restricted to designated botanical pocket groves. Never placed along main avenues or in front of heritage buildings.

---

### 2. Species-Specific Clearance & Setback Tolerances

```
+-----------------------------------+--------------------+--------------------+--------------------+
| Species Name                      | Min. Building Dist | Min. Road Kerb Dist| Vertical Clearance |
+-----------------------------------+--------------------+--------------------+--------------------+
| Ficus benghalensis (Banyan)       | 20.0 m (2000 UU)   | 8.0 m (800 UU)     | 5.5 m (550 UU)     |
| Albizia saman (Rain Tree)         | 14.0 m (1400 UU)   | 4.5 m (450 UU)     | 4.5 m (450 UU)     |
| Swietenia mahagoni (Mahogany)     | 12.0 m (1200 UU)   | 4.5 m (450 UU)     | 4.5 m (450 UU)     |
| Delonix regia (Krishnachura)      | 8.0 m (800 UU)     | 4.0 m (400 UU)     | 3.8 m (380 UU)     |
| Peltophorum pterocarpum (Radha)   | 8.0 m (800 UU)     | 4.0 m (400 UU)     | 3.8 m (380 UU)     |
| Lagerstroemia speciosa (Jarul)    | 7.0 m (700 UU)     | 3.5 m (350 UU)     | 3.2 m (320 UU)     |
| Azadirachta indica (Neem)         | 5.0 m (500 UU)     | 3.0 m (300 UU)     | 3.0 m (300 UU)     |
| Polyalthia longifolia (Debdaru)   | 4.5 m (450 UU)     | 3.0 m (300 UU)     | 3.0 m (300 UU)     |
| Roystonea regia (Royal Palm)      | 3.5 m (350 UU)     | 2.5 m (250 UU)     | 6.0 m (600 UU)     |
| Cocos nucifera (Coconut Palm)     | 3.5 m (350 UU)     | 2.5 m (250 UU)     | 5.0 m (500 UU)     |
| Bambusa tulda (Bamboo Thicket)    | 6.0 m (600 UU)     | 4.0 m (400 UU)     | N/A (Shrub buffer) |
| Duranta repens (Boxwood Hedge)    | 0.3 m (30 UU)      | 1.0 m (100 UU)     | 0.85 m (85 UU)     |
+-----------------------------------+--------------------+--------------------+--------------------+
```

---

### 3. Automated Geometric Audit Protocol

Every vegetation placement script must execute a two-pass algorithmic audit:

#### Pass 1: Ground Z-Raycast & Normal Alignment
```python
def ground_vegetation(actor_loc, mesh_height):
    start = {"x": actor_loc["x"], "y": actor_loc["y"], "z": actor_loc["z"] + 1000.0}
    end = {"x": actor_loc["x"], "y": actor_loc["y"], "z": actor_loc["z"] - 1000.0}
    hit = trace_world(start, end, channel="Visibility")
    if hit["bBlockingHit"]:
        ground_z = hit["location"]["z"]
        # Embed root flare by 8 cm for natural anchoring
        return {"x": actor_loc["x"], "y": actor_loc["y"], "z": ground_z - 8.0}
    return None
```

#### Pass 2: Bounding Box Building & Road Collision Query
```python
def validate_clearance(actor_loc, species_rules, building_boxes, road_splines):
    for b_box in building_boxes:
        dist = compute_horizontal_distance(actor_loc, b_box)
        if dist < species_rules["min_building_dist"]:
            return False, f"Too close to building: {dist:.1f}m < {species_rules['min_building_dist']}m"
    for r_segment in road_splines:
        dist = compute_distance_to_road(actor_loc, r_segment)
        if dist < species_rules["min_road_dist"]:
            return False, f"Too close to road: {dist:.1f}m < {species_rules['min_road_dist']}m"
    return True, "Clearance Validated"
```
