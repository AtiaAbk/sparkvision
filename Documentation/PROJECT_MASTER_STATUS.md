# SPARKVISION — PROJECT MASTER STATUS

## 1. Project Overview & Environment
- **Project Name**: SparkVision (Historical Bangladesh 3D Game)
- **Engine Version**: Unreal Engine 5.8 Early Access
- **Target Platform**: macOS, Apple Silicon (arm64 / M4 MacBook Air, 16 GB Unified Memory)
- **Project Path**: `/Users/atiaoishi/Downloads/sparkvision/MyProject.uproject`
- **MCP Server Connection**: `http://127.0.0.1:8000/mcp` (Direct Streamable HTTP JSON-RPC 2.0)
- **Active Level**: `/Game/SparkVision/Maps/Level01/LV_Level01_Compact_Campus`

---

## 2. Unreal MCP Connection Status
- **Status**: **CONNECTED AND VERIFIED**
- **Endpoint**: `http://127.0.0.1:8000/mcp` (Localhost only)
- **Core Plugins**:
  - `ModelContextProtocol`: Active & Listening
  - `ToolsetRegistry`: Active
  - `EditorToolset`: Active
  - `AllToolsets`: Active (33 toolsets exposed, including SceneTools, ActorTools, BlueprintTools, MaterialTools, NiagaraToolsets, SlateInspectorToolset)
- **Configuration Path**: `~/.gemini/config/mcp_config.json` & `.agents/mcp_config.json`

---

## 3. Verified Progress & Milestones
- **Unreal MCP Setup & Live Verification**:
  - Environment inspection and engine plugin configuration complete.
  - Resolved preference location (registered under `Project Settings -> Plugins -> Model Context Protocol`).
  - Successfully performed live JSON-RPC session initialization and dynamic toolset queries.
  - Performed read-only scene actor inspection in active level `LV_Level01_Compact_Campus`.
  - Executed live spawn and property verification of temporary actor (`MCP_Connection_Test_Sphere`).
  - Executed safe removal and confirmed zero residual changes.
- **MCP-First Development Rules Standardized**:
  - Established 12 operational guidelines for MCP-first workflows.
  - Configured workspace rule at `.agents/rules/unreal_mcp.md`.
- **Audit Reconciliation & Memory Revalidation Completed**:
  - Documented in `Documentation/Performance/SPARKVISION_AUDIT_RECONCILIATION.md`.
  - Resolved Mission 6 discrepancy: L1_M06 in master story plan is peaceful solidarity pledge (*“আমিও থাকব।”*) concluding July 14, while combat encounter represents July 15 (Chapter 2) self-defense mechanics prototyped in Level 1.
  - Revalidated 3 SkeletalMeshActors via MCP: Confirmed as `Police_Officer_01`, `Police_Officer_02`, and `RAB_Tactical_01` perimeter sentries linked to police arrest flow (retention confirmed).
  - Confirmed render target memory reduction: Pooled render targets verified reduced from 1,149.46 MB down to 733.69 MB (-415.78 MB) via `DefaultDeviceProfiles.ini` clamping without visual degradation.
  - Isolated Java Mission Control process footprint: 6.8 MB - 13.4 MB RSS, zero GPU memory impact.

---

## 4. Current Issues & Limitations
- **Render Target Memory Footprint**: Pooled render targets clamped to 733.69 MB via device profile; must preserve this clamp to avoid macOS swap pressure.
- **Mission 6 Narrative Alignment**: Coordinate distance check to TSC Raju Sculpture requires an explicit trigger volume for the July 14 solidarity pledge.
- **Combat Polish for Chapter 2**: Hostile cadre combat mechanics function mathematically but require hit sound cues and stagger montages for full runtime presentation.

---

## 5. Latest Verified Commit
- **Latest Commit Hash**: `7ec5141`
- **Message**: `feat(characters): complete authentic character wardrobe, modular outfit system, and campus NPC integration`
- **Branch**: `main` (synced with `origin/main`)

---

## 6. Next Development Tasks
1. Execute **Milestone 1**: Implement dedicated trigger volume at Raju Memorial Plaza (TSC Mor) for the July 14 solidarity pledge and Chapter 2 transition.
2. Maintain existing validated `DefaultDeviceProfiles.ini` CVar clamps for M4 16GB memory stability.
3. Keep the 3 perimeter police/RAB sentries intact and operational.
4. Execute full automated mission validation pass via MCP.
