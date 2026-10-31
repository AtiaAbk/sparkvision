# SPARKVISION — COMPREHENSIVE TEST STRATEGY

## 1. Title & Executive Purpose

* **Document**: `TestStrategy.md`
* **Purpose**: Defines the multi-tiered quality assurance strategy for SparkVision, ensuring game stability, architectural fidelity, server synchronization, and 60 FPS performance.

---

## 2. Testing Levels & Execution Hierarchy

### Level 1: Java Subsystem Unit & Integration Tests
* **Tooling**: JUnit 5, Gradle Test Runner (`./gradlew test`).
* **Scope**: Health endpoint verification, SQLite CRUD operations, thread safety, and session isolation.
* **Gate Requirement**: 100% test pass rate required prior to any Git commit.

### Level 2: Metric Scale & Spatial Verification
* **Tooling**: Unreal MCP `ActorTools.get_actor_bounds` and `SceneTools.trace_world`.
* **Scope**: Validates that imported Blender models correspond to expected physical dimensions ($1\text{ uu} = 1\text{ cm}$) and verifies zero encroachment at `PlayerStart`.

### Level 3: Automated Play-In-Editor (PIE) Testing
* **Tooling**: Unreal MCP `EditorAppToolset.StartPIE` and `EditorAppToolset.StopPIE`.
* **Scope**: Spawns player pawn in-viewport, verifies camera attachment, logs subsystem handshakes, and executes collision traces across active paths.

### Level 4: Visual Regression & Framing Benchmarks
* **Tooling**: Unreal MCP `EditorAppToolset.CaptureViewport`.
* **Scope**: Fixed-coordinate camera captures evaluated against approved milestone baselines.

---

## 3. Defect Severity & Remediation SLAs

| Severity | Definition | Example | SLA |
| :---: | :--- | :--- | :---: |
| **P0 - Blocker** | Game crash, player falling through world, missing PlayerStart | Encroaching collision box preventing character spawn | Immediate hotfix |
| **P1 - Critical** | Backend mission failure, broken terminal interaction | Archive discovery not recorded in SQLite | 4 hours |
| **P2 - Major** | Inaccurate landmark proportions, texture stretching | Entrance portal scale off by $>10\%$ | 24 hours |
| **P3 - Minor** | Minor cosmetic gap, leaf clipping, foliage density | Misaligned lawn border curb | Next milestone |

---

## 4. Current Status

* **Status**: `COMPLETED`
* **Evidence**:
  - P0 blocker (PlayerStart collision encroachment by obsolete blockout box) successfully diagnosed and remediated via MCP.
  - Character grounded at Z=107.65 in active PIE.
* **Remaining Tasks**:
  - Add continuous integration hook running `./gradlew test` on pre-commit.
