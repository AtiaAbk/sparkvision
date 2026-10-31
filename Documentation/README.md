# SPARKVISION — COMPREHENSIVE PROJECT DOCUMENTATION SUITE

Welcome to the central technical and artistic documentation repository for **SparkVision: University of Dhaka**, a cinematic, scenic, semi-open-world third-person historical adventure game built in **Unreal Engine 5.8** paired with an autonomous **Java 21 Mission Control** subsystem.

---

## 1. Project Overview & Design Pillars

* **Engine**: Unreal Engine 5.8 (Apple Silicon Metal backend on macOS / M4 architecture)
* **Programming Languages**: C++20, Unreal Blueprints, Java 21, Python 3 (Unreal MCP tooling)
* **Backend Subsystem**: Java Mission Control (`JavaMissionControl/`) running as a standalone HTTP microservice with SQLite persistence
* **Editor Integration**: Direct Unreal Engine Model Context Protocol (MCP) server on `http://127.0.0.1:8000/mcp`
* **Visual Presentation Inspiration**: *Where Winds Meet* and *Ghost of Tsushima* (cinematic composition, atmospheric depth, scenic routes, natural sunlight, organic foliage layering)
* **Architectural Ground Truth**: Authentic heritage architecture of the University of Dhaka (Curzon Hall Indo-Saracenic Revival, Doyel Chattar, Shaheed Minar, TSC, Raju Sculpture, Central Library, Aparajeyo Bangla)

---

## 2. Master Documentation Directory Structure

```text
Documentation/
├── README.md                                  # Master index and documentation guide
│
├── VisualReferences/                          # Visual reference library and research
│   ├── README.md                              # 9-step visual reference and comparison workflow
│   ├── ReferenceSources.md                    # Audited source register with URLs and license status
│   ├── DU_Architecture/                       # Authentic DU building reference photos & guidelines
│   ├── DU_Environment/                        # Authentic DU landscape, greenery, lighting & atmosphere
│   ├── WhereWindsMeet/                        # Visual presentation & cinematic atmosphere references
│   ├── GhostOfTsushima/                       # Landscape layering, sunlight & exploration references
│   ├── CurrentGameScreenshots/                # In-engine screenshots captured from SparkVision
│   └── ApprovedVisualBaselines/               # Formally approved visual baselines (never overwritten)
│
├── Architecture/                              # Technical systems architecture
│   ├── README.md                              # Architecture index
│   ├── SystemArchitecture.md                  # High-level client-server & subsystem architecture
│   ├── UnrealArchitecture.md                  # C++ classes, Blueprints, GameMode & World Partition
│   └── JavaMissionControlArchitecture.md      # Java 21 server, HTTP handlers & SQLite schema
│
├── Campus/                                    # Campus geography, landmarks & modeling
│   ├── README.md                              # Campus documentation index
│   ├── CampusMasterplan.md                    # Master blockout, road network & scale definitions
│   ├── GeographicValidation.md                # WGS 84 / UTM Zone 46N coordinate audit & validation
│   ├── LandmarkRegister.md                    # Complete catalog of campus landmarks & coordinates
│   └── CurzonHall_Architecture.md             # Curzon Hall Indo-Saracenic modular construction
│
├── Gameplay/                                  # Design, mechanics, characters & progression
│   ├── README.md                              # Gameplay design index
│   ├── Level1_GameplayDesign.md               # Chapter 1: Curzon Hall & Campus historical narrative
│   ├── CharacterAndNPCs.md                    # Player character, student NPCs & opponent AI
│   ├── InteractionSystem.md                   # Archive terminals, dialogue prompts & triggers
│   ├── CombatSystem.md                        # Martial arts / historical combat mechanics
│   └── MissionProgression.md                  # Objective chains, level unlocking & save state
│
├── JavaIntegration/                           # Unreal-Java communication protocols
│   ├── README.md                              # Integration index
│   ├── API_Contract.md                        # RESTful endpoints, payloads & response schemas
│   ├── EventSpecification.md                  # Real-time event contracts & telemetry hooks
│   └── PersistenceDesign.md                   # SQLite tables, session isolation & migrations
│
├── VisualDesign/                              # Environment art, lighting & materials
│   ├── README.md                              # Visual design index
│   ├── ArtDirection.md                        # Style guide, cinematic palettes & camera composition
│   ├── EnvironmentQualityChecklist.md         # Environment validation & polish criteria
│   ├── MaterialAndLightingGuide.md            # PBR material parameters & Lumen lighting setups
│   └── AssetPipeline.md                       # Blender-to-Unreal export/import metric standards
│
├── Testing/                                   # Quality assurance & verification
│   ├── README.md                              # Testing index
│   ├── TestStrategy.md                        # Multi-tiered automated & manual testing plan
│   ├── GameplayTestCases.md                   # Player possession, collision & interaction test matrix
│   ├── VisualRegressionTests.md               # Viewport capture & camera comparison benchmarks
│   └── PerformanceBenchmark.md                # Target framerates, draw calls & memory budgets
│
├── Screenshots/                               # Structured screenshot repository
│   ├── README.md                              # Screenshot catalog & guidelines
│   ├── Baseline/                              # Initial milestone baselines
│   ├── Development/                           # Work-in-progress captures
│   ├── Gameplay/                              # Active PIE gameplay screenshots
│   └── Final/                                 # Polished release-grade visual renders
│
└── DevelopmentLogs/                           # Historical audit trails & version logs
    ├── README.md                              # Development log index
    └── GitDevelopmentLog.md                   # Detailed Git commit history & milestone reports
```

---

## 3. Current Project Status

| Area | Status | Key Deliverables Completed | Next Priorities |
| :--- | :---: | :--- | :--- |
| **Campus Geography** | `COMPLETED` | UTM Zone 46N reprojection, 7 core landmarks, road network | Micro-terrain blending |
| **Curzon Hall Hero** | `COMPLETED` | 8 modular FBX kits, PBR materials, authentic silhouette | Interior hall layout |
| **Java Mission Control** | `COMPLETED` | Session isolation, 5/5 archive tracking, Level 2 unlock | Dynamic event streaming |
| **Unreal MCP Workflow** | `COMPLETED` | 19 toolsets verified, headless PIE automation, viewport capture | PCG volume scripting |
| **Full Campus Detailing** | `IN PROGRESS` | Doyel Chattar, Shaheed Minar, TSC, Hero shade trees | Arts Faculty & Library mesh detail |
| **Gameplay Core** | `IN PROGRESS` | Third-person possession, archive terminals, NPC dialogue | Combat combo polish |

---

## 4. Documentation Maintenance Guidelines

1. **Format**: All technical and design documentation must be authored in GitHub Flavored Markdown (`.md`).
2. **Standard Template**: Every document follows the unified standard structure:
   - Clear Title & Metadata
   - Purpose & Scope
   - Architectural / Implementation Specifications
   - Current Status (`NOT STARTED`, `IN PROGRESS`, `COMPLETED`)
   - Verification Evidence & Visual References
   - Remaining Tasks & Action Items
3. **No Fabricated Information**: All coordinates, dimensions, class names, test results, and performance numbers must reflect real assets and code present in this repository.
4. **Git Discipline**: Any updates to documentation should be committed with structured conventional commit prefixes (`docs:`, `chore:`) and pushed to the remote repository.
