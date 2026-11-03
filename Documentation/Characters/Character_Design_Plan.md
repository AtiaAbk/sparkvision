# SparkVision — Character Design Plan
## Architecture, Modular Character Setup & Animation Compatibility Plan

### 1. Unified Skeletal Hierarchy & Modular Architecture
To ensure seamless animation compatibility, maximum gameplay responsiveness, and zero cloth-body clipping under rapid locomotion or high-flying Wuxia movement (double jumping, wall jumping, directional dodging), SparkVision adopts a **hybrid unified-skeletal model**:

```
                  ┌──────────────────────────────┐
                  │      SK_Mannequin            │
                  │   (UE5 Shared Humanoid)      │
                  └──────────────┬───────────────┘
                                 │
         ┌───────────────────────┴───────────────────────┐
         │                                               │
┌────────▼───────────────┐                     ┌─────────▼──────────────┐
│   SKM_Manny_Simple     │                     │    SKM_Quinn_Simple    │
│ (Male Proportions)     │                     │  (Female Proportions)  │
└────────┬───────────────┘                     └─────────┬──────────────┘
         │                                               │
   Slot 0: Legs / Trousers                         Slot 0: Full Ensemble
   Slot 1: Torso / Shirt / Panjabi                 Slot 1: Dupatta / Trim
```

### 2. Implementation Methodology: Skeletal Mesh Permutation vs Modular Merging
In accordance with Epic Games' *Working with Modular Characters in Unreal Engine* (UE 5.8 documentation), runtime assembly via `Set Leader Pose Component` incurs a separate render pass and bone-transform broadcast overhead per attached skeletal component. On Apple Silicon (MacBook Air M4, 16 GB unified RAM), having 40+ background NPCs each running 3–4 modular sub-meshes would generate excessive draw calls (160+ calls solely for characters) and strain memory bandwidth.

Therefore:
1. **Hero Character (`ASVCharacter`)**:
   - Supports dynamic gender and wardrobe swapping between Male (`SKM_Manny_Simple`) and Female (`SKM_Quinn_Simple`).
   - Driven by dual material slots mapped to fine-tuned authentic PBR fabric master instances.
2. **Background Student & Campus NPCs (`ASVStudentNPC`)**:
   - Pre-configured single-mesh humanoid actors categorized by role, department, and gender.
   - Dynamic procedural material assignment on spawn (`TorsoMat`, `LegsMat`) allowing infinite visual variety without additional mesh allocation.
3. **Mission 6 Hostiles (`ASVHostileOpponent`)**:
   - Specialized combat-ready setup with helmet/windbreaker material combinations and socket-attached defensive batons.
4. **Law Enforcement & Security**:
   - Dual-tone PBR police duty materials (`MI_Police_Uniform_BD`) and proctorial safari uniforms (`MI_Security_ProctorialKhaki`).

### 3. Animation State Machine Compatibility
All humanoid character classes link directly to `ABP_Unarmed` (`/Game/Characters/Mannequins/Anims/Unarmed/ABP_Unarmed.ABP_Unarmed_C`).
Verified animation sets supported across all outfits:
* `MM_Idle` — Natural breathing campus stance.
* `BS_Idle_Walk_Run` — Smooth velocity-driven directional blend space.
* `MM_Jump` / `MM_Fall_Loop` / `MM_Land` — Fluid jumping and landing physics.
* `MM_Dash` — Evasive directional roll / swift dodge.
* `MM_WallJump` — Vertical agility movement against campus architectural walls.
* `Rifle / Pistol Stance Sets` — Available for hostile / security weaponized scenarios.

### 4. Memory & Performance Guardrails (16 GB Unified Memory)
* Single master shader family (`M_Mannequin`) eliminates redundant shader permutation compiles.
* Shared 2K/1K PBR texture packing (MRA = Metallic, Roughness, Ambient Occlusion).
* LOD streaming: Distance-based tick throttling natively active via CharacterMovement optimization.
