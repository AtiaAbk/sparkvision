# SPARKVISION — WHERE WINDS MEET RESEARCH & DEVELOPMENT BENCHMARK
## Comprehensive Architectural, Gameplay, Visual & Interaction Design Framework for University of Dhaka Open-World Adaptation

---

## 1. Executive Research Overview

* **Reference Title**: *Where Winds Meet* (燕云十六声 - *Yān Yún Shí Liù Shēng*)
* **Developer**: Everstone Studio (Subsidiary of NetEase Games)
* **Engine**: Proprietary Messiah Engine
* **Genre**: Open-World Wuxia Action-Adventure RPG
* **Historical Setting**: Ten Kingdoms & Early Northern Song Dynasty (10th-century China)
* **Creative Adaptation Target**: **University of Dhaka (DU) Historical Campus, Bangladesh**
* **Core Philosophy**: *"Cinematic Poetic Realism meets Responsive Fluid Action"*. Recreating the sweeping, wind-swept, contemplative, and martial intensity of *Where Winds Meet* while anchoring the physical geography, architecture, cultural identity, and narrative in the authentic, real-world University of Dhaka campus.

---

## 2. In-Depth Systemic Research & Deconstruction

### 2.1 Art Direction, World Aesthetics & Poetic Realism
* **Visual Philosophy**: *Where Winds Meet* balances hyper-realistic rendering with the philosophical elegance of traditional Chinese ink-wash painting (*Shuimohua*). Landscapes are not merely backdrops; they convey philosophical mood (*Yijing* - 意境), nostalgia, historical turbulence, and solitude.
* **Color Harmonization**:
  * **Dominant Palette**: Grounded organic earth tones—charcoals, weathered river slates, raw terracotta, muted sandstone ochres, moss greens, and deep walnut browns.
  * **Strategic Focal Accents**: Intentional, high-contrast splashes of saturated color—vivid crimson flags, scarlet silk banners, golden sunlight rimming architectural silhouettes, and soft cerulean waters.
* **University of Dhaka Adaptation**:
  * British Raj red brickwork of Curzon Hall, aged ivory sandstone cornices, terracotta paving, tropical rain-washed plaster of Kala Bhaban, and weathered marble of the Central Shaheed Minar.
  * Contrast vivid crimson from the Shaheed Minar Sun Disc and Bangladeshi flags against the deep verdant greens of banyan shade trees (*Ficus benghalensis*).

### 2.2 Environmental Storytelling & Atmosphere
* **The Living Wind**: In *Where Winds Meet*, wind is an active character. Foliage bends dynamically, roadside banners whip in gusts, dust motes drift through light beams, and autumn leaves swirl across stone pathways.
* **Atmospheric Volumetrics**:
  * Low-altitude morning mist rising from water basins and grass lawns.
  * High-density volumetric sun shafts (God rays) filtering through mature tree canopies and cusped archways.
  * Distinct golden-hour warmth contrasting with cool slate-blue shadows.
* **University of Dhaka Adaptation**:
  * Tropical afternoon haze over University Avenue; leaves from mature raintrees (*Samanea saman*) and banyans drifting across red brick walkways; reflection of clouds in the Curzon botanical pond and Doyel Chattar fountain.

### 2.3 Traversal, Locomotion & Qinggong Flow
* **Wuxia Traversal Mechanics**:
  * *Qinggong* (Lightness Skills): Fluid momentum-preserving sprinting, roof vaults, low-friction slides, wall runs, and water skimming.
  * Weight & Momentum: Characters exhibit tangible physical mass on initial acceleration, transitioning into weightless, graceful parkour at peak velocity.
  * Verticality: Fluid transitions from street-level navigation up colonnades, porticos, and rooftops without rigid climbing grid interruptions.
* **SparkVision Implementation**:
  * Fluid sprint with responsive acceleration curve (`MaxWalkSpeed = 600.0`, sprinting up to `950.0 cm/s`).
  * Dynamic slide/roll mechanic (`Crouch/Slide` preserving forward momentum).
  * Ledge vaulting over campus balustrades, Curzon veranda parapets, and stepped plinths.

### 2.4 Dynamic Third-Person Camera & Cinematic Framing
* **Exploration Framing**:
  * Generous spring-arm distance (`TargetArmLength = 380.0 cm` to `420.0 cm`) with slight camera lag (`bEnableCameraLag = True`, `CameraLagSpeed = 8.0`).
  * Low-angle pitch framing player pawn in the lower third, allowing majestic monumental architecture (Curzon towers, Shaheed Minar pillars, TSC folded roof) to dominate the upper two-thirds of the frame.
  * Wide Field-of-View (`FOV = 75°` default, dynamically expanding to `85°` during high-speed sprint).
* **Combat & Tension Framing**:
  * Tight shoulder-offset perspective (`TargetArmLength = 260.0 cm`, `SocketOffset = (0, 50, 20)`).
  * Target lock-on focusing on opponent telegraphs and parry timings.
  * Dynamic micro-shake on heavy impacts and deflects.

### 2.5 Combat Mechanics & Martial Flow
* **Core Combat Triad**:
  1. **Light & Heavy Chains**: Responsive martial strikes with weapon trails and distinct impact stops (*hitstop* / frame freeze of 0.05s).
  2. **Deflection / Parry System**: High-risk, high-reward deflection window (within 150ms of incoming strike) yielding metallic sparks, posture damage, and staggering counters.
  3. **Internal Energy / Qi Resource**: Mana/stamina gauge depleted by dodges, special techniques, and sprint leaps; replenished by successful parries and rhythmic basic attacks.
* **SparkVision Level 1 Encounter (Curzon Hall Quadrangles)**:
  * Adaptation from Wuxia duels into historical Bangladeshi resistance / athletic martial defense: Quarterstaff / baton (*Lathi*) defense against colonial / oppressive security automatons or rival challengers.
  * Clean deflection windows, directional dodges, and tactical posture breaks.

### 2.6 Minimalist Calligraphic UI/UX Design
* **Exploration Immersion**: All non-essential HUD elements auto-fade during uninterrupted exploration.
* **Top Compass / Horizon Ribbon**: Ultra-thin minimalist cardinal bar at the top screen border, highlighting objective markers (distance in meters), landmark waypoints, and discovery alerts.
* **Bottom-Left Status Arc**:
  * Curved vital health bar wrapping an inner circular Qi/Stamina gauge.
  * Stylized brush-stroke filigree accents reminiscent of ink calligraphy / Bengali woodcut typography.
* **Contextual Interaction Reticle**:
  * Sleek circular indicator with button prompt (e.g. `[E] Investigate Historical Archive`, `[F] Converse with Scholar`).
* **Cinematic Dialogue Interface**:
  * Cinematic letterbox masking (2.35:1 aspect ratio bars slide in).
  * Clean serif typography, subtle speaker title card, and branching dialogue choices presented as minimalist horizontal cards.

### 2.7 Environmental Interactivity & Archive Discovery
* **Living Sandbox Interactions**:
  * Sitting on campus stone benches, drinking tea at street stalls, meditating/reflecting before historic memorials.
  * Contextual examination of primary documents, historical manifestos, and architectural tablets.
* **SparkVision Level 1 Five Primary Archives**:
  1. *Curzon Hall Foundation Tablet (1904)* — Indo-Saracenic synthesis.
  2. *Language Movement Bulletin (February 21, 1952)* — Shaheed Minar sacrifice.
  3. *Muzharul Islam Modernist Architecture Manifesto (1953)* — Central Library pilotis.
  4. *Raju Anti-Terrorism Declaration (March 1992)* — TSC Mor student solidarity.
  5. *Aparajeyo Bangla Freedom Fighters Proclamation (1979)* — Liberation War memory.

---

## 3. Measurable Evaluation Matrix

| Category | Where Winds Meet Benchmark Standard | SparkVision DU Campus Target | Evaluation Method |
| :--- | :--- | :--- | :--- |
| **1. Architecture** | Meticulous timber/stone historical joinery, weathered textures, modular consistency. | 1:1 metric Indo-Saracenic & Modernist campus landmarks with authentic PBR material slots. | Vertex inspection, texture density, historic alignment. |
| **2. Atmosphere** | Volumetric fog, dynamic god rays, wind rustling through foliage, poetic weather. | Exponential height fog, volumetric directional light shafts, banyan leaf wind drift. | Visual comparison captures, viewport histogram. |
| **3. Camera** | Dynamic spring arm (380cm travel, 260cm combat), smooth lag, dynamic FOV. | SpringArm with custom lag interpolation, sprint FOV blend, collision probe. | Camera runtime tracing, framerate stability. |
| **4. Locomotion** | Fluid sprint, parkour vaulting, momentum conservation, agile recovery. | Responsive character pawn with sprint acceleration, slide/roll, and obstacle vault. | Input responsiveness test, animation blend evaluation. |
| **5. Combat** | Precise parry window, spark VFX, posture break, weapon swapping. | Tight 150ms parry window, particle clash, opponent posture bar, impact freeze. | PIE combat duel test, combat log latency. |
| **6. UI/UX** | Minimalist ink-wash HUD, auto-fading elements, clean compass ribbon, letterbox dialogue. | WWM-style HUD with compass ribbon, health/stamina arc, interactive prompts, letterboxing. | UI rendering overhead, legibility test. |
| **7. Audio** | Dynamic wind hum, rustling leaves, resonant footfalls on stone/wood, subtle guzheng/flute. | Ambient wind, tropical bird calls (*Doyel*), gravel/marble footstep cues, traditional ektara/flute motif. | Audio cue verification, distance attenuation. |
| **8. Performance** | Scalable rendering architecture, seamless streaming, stable 30-60 FPS. | Scalable rendering for Apple Silicon M4 (16GB unified), memory capped <10GB, stable 30 FPS. | Activity Monitor RSS, UE engine profiling (`stat fps`, `stat unit`). |

---

## 4. Hardware Budget for Apple Silicon (MacBook Air M4, 16GB)

* **Maximum Editor Process RSS**: **≤ 6.5 GB** (Preventing macOS yellow memory pressure and disk swap).
* **Texture Streaming Pool**: **1000 MB** (`r.Streaming.PoolSize = 1000`).
* **Rendering Path**: **Lumen Software Ray Tracing** (Mesh Distance Fields + Screen Traces; Hardware Ray Tracing disabled).
* **Shadow Architecture**: Optimized Virtual Shadow Maps with clamped page address bits (`r.Shadow.Virtual.MaxPhysicalPages = 2048`).
* **Resolution Scaling**: Temporal Super Resolution (TSR) with `r.ScreenPercentage = 80%`.
