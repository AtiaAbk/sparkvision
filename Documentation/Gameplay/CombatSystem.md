# SPARKVISION — COMBAT & DEFENSIVE SYSTEM DESIGN

## 1. Title & Executive Purpose

* **Document**: `CombatSystem.md`
* **Purpose**: Outlines the third-person martial combat framework, defensive posture, parry windows, and hit-reaction choreography inspired by the kinetic fluidity of *Where Winds Meet* and *Ghost of Tsushima*.

---

## 2. Combat Design Pillars

1. **Grounded & Deliberate**: Combat reflects authentic human athleticism and historical self-defense, avoiding supernatural magic or high-flying fantasy spells.
2. **Timing-Based Parrying**: Rewarding precision defensive timing rather than mindless button-mashing.
3. **Environmental Improvisation**: Using campus architecture, colonnades, trees, and stairs for line-of-sight breaking and tactical positioning.

---

## 3. Core Combat Mechanics & Input Schema

* **Light Strike (Left Mouse Button)**:
  - 3-hit unarmed / staff combo sequence: Jab -> Sweep -> Driving Push.
  - Generates mild stagger on opponents.
* **Heavy Strike (Hold Left Mouse Button / F-Key)**:
  - High-impact guard-breaking strike with longer windup.
  - Breaks opponent defensive blocks.
* **Parry / Deflect (Right Mouse Button Tap)**:
  - 200 ms active deflection window prior to incoming strike.
  - Successful parry triggers slow-motion cinematic camera pulse (0.2s duration) and exposes opponent to critical counter-strike.
* **Dodge / Evasion (Spacebar + Directional WASD)**:
  - Quick directional slip or tactical roll. Invulnerability frames (i-frames): 120 ms.

---

## 4. Hit Reactions & Damage Calculation

```text
Incoming Attack -> Check Defensive State:
├── [State: Perfect Parry Active] -> Deflect sound, Opponent Staggered (2.5s), Counter Available
├── [State: Guard Active]          -> Reduced stamina loss, zero health damage
├── [State: Dodging (i-frames)]    -> Attack misses cleanly
└── [State: Open / Exposed]        -> Full damage, directional hit reaction montage, camera shake
```

---

## 5. Current Status

* **Status**: `IN PROGRESS`
* **Evidence**:
  - `SVHostileOpponent` class compiled with basic health attributes and attack triggers.
* **Remaining Tasks**:
  - Integrate motion-matching animation sequences and notify-state collision traces on weapon/fist bones.
