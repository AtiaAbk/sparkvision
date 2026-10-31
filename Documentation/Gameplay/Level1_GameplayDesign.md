# SPARKVISION — CHAPTER 1 GAMEPLAY DESIGN SPECIFICATION

## 1. Title & Executive Purpose

* **Document**: `Level1_GameplayDesign.md`
* **Purpose**: Defines the narrative structure, quest beats, exploration sequence, and level boundaries for **Chapter 1: Voices of Curzon Hall**.

---

## 2. Narrative Premise & Historical Setting

In Chapter 1, the player enters the historic grounds of the **University of Dhaka** in the mid-20th century during a pivotal era of cultural reawakening. Historical secrets, intellectual manuscripts, and student political declarations have been dispersed across the campus into 5 protected Archive Terminals.

The player must navigate the campus grounds, converse with students, evade hostile campus authorities patrolling restricted science pavilions, and reconstruct the 5 primary historical archives to unlock Chapter 2.

---

## 3. Mission Objectives & Progression Sequence

### Objective 1: The Curzon Prelude (Spawn & Orientation)
* **Location**: Curzon Hall South Promenade (`X=-3500, Y=0, Z=107.65`).
* **Goal**: Approach the monumental entrance portico, speak to student informant `NPC_Student_Curzon`, and activate **Archive Terminal 01: The Founding Stones (1904)**.

### Objective 2: The Crossroads of Heritage (Doyel Chattar)
* **Location**: Doyel Chattar Roundabout (`X=7507, Y=-16487, Z=20`).
* **Goal**: Follow University Avenue north to Doyel Chattar. Locate and decode **Archive Terminal 02: The Folk Renaissance**.

### Objective 3: The Monument of Sacrifice (Shaheed Minar)
* **Location**: Shaheed Minar Memorial Square (`X=12600, Y=-52400, Z=20`).
* **Goal**: Evade or neutralize patrolling guards near the southern approach (`Opponent_Helmeted_01/02`). Ascend the marble podium to uncover **Archive Terminal 03: The Language Martyrs (1952)**.

### Objective 4: The Hub of Resistance (TSC & Raju Sculpture)
* **Location**: Teacher-Student Centre (`X=43000, Y=-149000, Z=20`).
* **Goal**: Meet `NPC_Student_Raju` beside the anti-terrorism sculpture to retrieve **Archive Terminal 04: The Anti-Imperialist Student Movement**.

### Objective 5: The Vanguard of Freedom (Arts Faculty & Aparajeyo Bangla)
* **Location**: Arts Faculty Quadrangle (`X=51000, Y=-160000, Z=20`).
* **Goal**: Reach the foot of Aparajeyo Bangla and interface with **Archive Terminal 05: The Charter of Liberation**.
* **Reward**: Java Mission Control confirms 5/5 archives gathered; triggers level transition unlocking **Chapter 2**.

---

## 4. Playable Boundary & Natural Environmental Barriers

To avoid immersion-breaking invisible walls, Level 1 employs authentic architectural and natural boundary elements:
* **East Boundary**: Supreme Court / High Court colonial wrought-iron fencing and dense tree lines.
* **South Boundary**: Historic Dhaka Medical College perimeter brick walls and military checkpoints.
* **North Boundary**: Shahbagh avenue intersection monitored by heavy traffic and police blockades.
* **Interior Restrictions**: Locked colonial padlocks on secondary chemistry labs and administration wing grilles (`Restricted_Curzon_ResearchLab_Gate`).

---

## 5. Current Status

* **Status**: `COMPLETED`
* **Evidence**:
  - All 5 Archive Terminals placed in level (`LV_Campus_Blockout`).
  - Terminal 01-05 verified in World Outliner and Java Mission Control tracking.
* **Remaining Tasks**:
  - Author localized Bengali/English text strings for each terminal lore inspect screen.
