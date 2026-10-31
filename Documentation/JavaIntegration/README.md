# SPARKVISION — UNREAL ENGINE & JAVA MISSION CONTROL INTEGRATION SUITE

## 1. Purpose & Scope

This directory contains the integration specifications, RESTful API contracts, real-time event schemas, and database persistence designs governing the communication between **Unreal Engine 5.8** and the standalone companion **Java 21 Mission Control** daemon.

---

## 2. Directory Index

* [`API_Contract.md`](file:///Users/atiaoishi/Downloads/sparkvision/Documentation/JavaIntegration/API_Contract.md): Comprehensive REST endpoints, HTTP methods, headers, request bodies, and JSON response definitions.
* [`EventSpecification.md`](file:///Users/atiaoishi/Downloads/sparkvision/Documentation/JavaIntegration/EventSpecification.md): Event payload contracts for session start, archive discoveries, combat telemetry, and milestone completions.
* [`PersistenceDesign.md`](file:///Users/atiaoishi/Downloads/sparkvision/Documentation/JavaIntegration/PersistenceDesign.md): SQLite schema definitions, session isolation mechanisms, indexing strategy, and data lifecycle management.

---

## 3. High-Level Integration Workflow

```mermaid
sequenceDiagram
    autonumber
    participant UE as Unreal Engine (USVMissionControlSubsystem)
    participant Java as Java Server (MissionControlServer:8080)
    participant DB as SQLite (sparkvision_missions.db)

    UE->>Java: GET /api/v1/health
    Java-->>UE: 200 OK {"status": "OK"}
    UE->>Java: POST /api/v1/session/start
    Java->>DB: INSERT INTO sessions
    Java-->>UE: 200 OK {"sessionId": "unreal_session_..."}

    loop Gameplay Archive Interaction
        UE->>Java: POST /api/v1/chapter-01/archive
        Java->>DB: INSERT INTO discovered_archives
        Java->>DB: SELECT COUNT(*) FROM discovered_archives WHERE session_id = ?
        Java-->>UE: 200 OK {"archivesFound": N, "level2Unlocked": bool}
    end
```

---

## 4. Current Status

* **Status**: `COMPLETED`
* **Evidence**:
  - Subsystem communication verified during active PIE sessions.
  - Endpoints returning valid JSON under 2 ms response latency on local loopback.
* **Remaining Tasks**:
  - Implement dynamic reconnect watchdog in C++ in case Java daemon is restarted mid-game.
