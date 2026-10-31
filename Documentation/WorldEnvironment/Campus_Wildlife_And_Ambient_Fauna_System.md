# CAMPUS WILDLIFE & AMBIENT FAUNA SYSTEM
**Project**: SparkVision — Level 1 University of Dhaka Digital Twin  
**Aesthetic Benchmark**: *Where Winds Meet* / *Ghost of Tsushima* Living World Ecology  
**Technical Implementation**: Niagara GPU particle emitters, lightweight vertex-animated mesh instances, and state-driven ambient AI.

---

## 1. Ambient Fauna Catalog & Behavior Patterns

| Species ID | Common Name (Bengali / English) | Model / Particle Type | Behavior Logic & State Machine | Spawn Location & Timing |
|---|---|---|---|---|
| **FAUNA-01** | **Bhat Shalik / Common Myna** | Skeletal Mesh / Vertex Anim | Ground foraging (pecking animation); when player sprints within $4.0\text{ m}$, triggers startle hop $\rightarrow$ wing flap take-off $\rightarrow$ perch on nearby branch. | Lawns, promenades, Curzon gardens; active during daylight. |
| **FAUNA-02** | **Kani Bok / Indian Pond Heron** | Skeletal Mesh / Static Perch | Motionless stalking on pond margin; occasional slow neck extension; flies low over water if approached within $6.0\text{ m}$. | Curzon Botanical Pond & Shahidullah Pond shoreline; early morning / dusk. |
| **FAUNA-03** | **Pati Kak / House Crow** | Lightweight Instanced Mesh | Perched on high colonial parapets and telephone wires; head-bobbing and cawing; circling thermals over open fields. | Rooflines, highest branches; all day. |
| **FAUNA-04** | **Ghash Foring / Dragonfly Swarm** | Niagara GPU Particle Emitter | Hover-and-dart motion vectors; iridescent specular reflections; responsive to wind gusts. | Over lily pads and pond surfaces; warm afternoons. |
| **FAUNA-05** | **Projapoti / Tropical Butterflies** | Niagara GPU Ribbon/Mesh | Fluttering chaotic trajectory with sinusoidal wing flapping; attracted to flowering Krishnachura flowerbeds. | Flower gardens, parterres; sunny hours. |
| **FAUNA-06** | **Badur / Flying Fox (Fruit Bat)** | Skeletal Mesh Flocking System | High-altitude silhouettes gliding between ancient Banyan crowns at dusk; slow, rhythmic wing beats. | Sky above Curzon Hall and Mall; twilight / night cycle. |

---

## 2. Interaction & Performance Optimization
* **Player Proximity Triggers**:
  - Wildlife uses simple spherical distance checks ($r = 400 - 800\text{ cm}$) to trigger state changes (Idle $\rightarrow$ Alert $\rightarrow$ Flee).
* **Niagara GPU Particles for Insects**:
  - Dragonflies and butterflies execute entirely on the GPU via Niagara simulation stages.
  - Zero CPU tick cost, maintaining 60 FPS on Apple Silicon M4.
* **Sound-Visual Coupling**:
  - When crows take flight from a tree, a subtle wing-flutter audio cue and falling leaf burst accompany the event, enhancing player immersion.
