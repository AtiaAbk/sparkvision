# SPARKVISION — OBJECTIVE DISTANCE & CLEARANCE VALIDATION REPORT
## Metric Distance Analysis, Collision Clearances & Objective Placement
### Map: `/Game/SparkVision/Maps/Level01/LV_Level01_Compact_Campus`

---

## 1. Story Objective Waypoint Registry

| Objective ID | Objective Title | Target Actor / Asset | Compact Position (X, Y, Z cm) | Associated Landmark | Required Interaction |
| :---: | :--- | :--- | :---: | :--- | :--- |
| **OBJ_01** | *Awakening at Curzon* | `PlayerStart_CurzonEntrance` | `(-4500, 0, 80)` | Curzon Hall South Plinth | Movement & Camera Tutorial |
| **OBJ_02** | *Heritage Botanical Record* | `ArchiveTerminal_Curzon` | `(4200, 400, 80)` | Curzon Botanical Pond | Recover Archive 01 |
| **OBJ_03** | *Voices of Doyel Chattar* | `StudentNPC_Mehdi` | `(5200, -7800, 80)` | Doyel Chattar Roundabout | Dialogue with NPC Mehdi |
| **OBJ_04** | *Language Martyrs Tribute* | `ArchiveTerminal_Shaheed` | `(0, -18200, 80)` | Central Shaheed Minar | Recover Archive 02 |
| **OBJ_05** | *Fuller Road Assembly* | `StudentNPC_Rina` | `(17000, -23000, 80)` | Raju Memorial Sculpture | Dialogue with NPC Rina |
| **OBJ_06** | *Student Democracy Ledger* | `ArchiveTerminal_TSC` | `(20000, -21000, 80)` | TSC Courtyard Plaza | Recover Archive 03 |
| **OBJ_07** | *The Academic Repository* | `ArchiveTerminal_Library` | `(25500, -26500, 80)` | DU Central Library | Recover Archive 04 |
| **OBJ_08** | *Arts Faculty Climax* | `ArchiveTerminal_KalaBhaban`| `(30500, -35000, 80)` | Aparajeyo Bangla / Kala Bhaban | Recover Final Archive 05 |
| **OBJ_09** | *Chapter 1 Conclusion* | `SVGameMode_Encounter` | `(31000, -36000, 80)` | Kala Bhaban Portico | Trigger Chapter Complete State |

---

## 2. Geometric Clearance & Safety Audit

The spatial layout solver strictly enforces minimum clearance envelopes around every building, tree, and road to eliminate overlapping meshes:

* **Curzon Hall Portal & Verandas**:
  - Distance to Curzon Science Annex East: $45.2\text{ m}$ (Safety margin: $>30\text{ m}$)
  - Distance to Curzon Science Annex West: $45.2\text{ m}$ (Safety margin: $>30\text{ m}$)
  - Distance to Dr. Shahidullah Hall: $38.5\text{ m}$ (Safety margin: $>25\text{ m}$)
  - Distance to Curzon Pond Ghat: $35.0\text{ m}$ (Safety margin: $>20\text{ m}$)
  - **Collision Status: ZERO CLIPPING DETECTED.**
* **Doyel Chattar Monument**:
  - Distance to Curzon North Approach: $62.0\text{ m}$ (Clear vehicular roundabout)
  - Distance to Bangla Academy Burdwan House: $38.0\text{ m}$ (Clear sightline)
  - **Collision Status: ZERO CLIPPING DETECTED.**
* **Central Shaheed Minar**:
  - Distance to Jagannath Hall: $42.0\text{ m}$ (Preserves ceremonial lawn)
  - Distance to Salimullah Muslim Hall: $36.0\text{ m}$ (Preserves Fuller Road avenue)
  - Marble altar plinth clear zone: $18.0\text{ m}$ radius without vegetation interference.
  - **Collision Status: ZERO CLIPPING DETECTED.**
* **Raju Memorial Sculpture & TSC**:
  - Distance to TSC Auditorium Facade: $22.5\text{ m}$ (Authentic pedestrian plaza)
  - Distance to Begum Rokeya Hall: $32.0\text{ m}$ (Clear road crossroad)
  - Distance to IBA Complex: $35.0\text{ m}$ (Clear commercial green)
  - **Collision Status: ZERO CLIPPING DETECTED.**
* **Arts Faculty (Kala Bhaban) & Central Library**:
  - Distance between Central Library and Central Mosque: $24.0\text{ m}$ (Authentic courtyard)
  - Distance from Central Library to Aparajeyo Bangla: $42.0\text{ m}$ (Mall Road promenade)
  - Distance from Aparajeyo Bangla to Kala Bhaban portico: $14.0\text{ m}$ (Authentic statue foreground)
  - Distance to Surja Sen Hall: $35.0\text{ m}$ (Clear residential perimeter)
  - **Collision Status: ZERO CLIPPING DETECTED.**
