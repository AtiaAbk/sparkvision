# SPARKVISION — REST API CONTRACT (UNREAL <-> JAVA MISSION CONTROL)

## 1. Title & Executive Purpose

* **Document**: `API_Contract.md`
* **Purpose**: Formal specification of all HTTP REST endpoints exposed by Java Mission Control (`http://127.0.0.1:8080`) consumed by Unreal Engine's `USVMissionControlSubsystem`.

---

## 2. API Endpoints Specification

### 2.1 Health Check
* **Endpoint**: `GET /api/v1/health`
* **Purpose**: Engine pre-flight verification during subsystem initialization.
* **Headers**: `Accept: application/json`
* **Response (200 OK)**:
```json
{
  "status": "OK",
  "service": "SparkVision Mission Control",
  "version": "1.0.0",
  "timestamp": 1793434572684
}
```

---

### 2.2 Session Initialization
* **Endpoint**: `POST /api/v1/session/start`
* **Purpose**: Registers a new gameplay or evaluation session.
* **Headers**: `Content-Type: application/json`, `Accept: application/json`
* **Request Body**:
```json
{
  "clientVersion": "UnrealEngine-5.8",
  "mapName": "LV_Campus_Blockout",
  "timestamp": 1793434577000
}
```
* **Response (200 OK)**:
```json
{
  "success": true,
  "sessionId": "unreal_session_1793434577",
  "message": "Session initialized for SparkVision Level 1",
  "currentChapter": "chapter-01"
}
```

---

### 2.3 Chapter 1 Status & Telemetry
* **Endpoint**: `GET /api/v1/chapter-01/status?sessionId={sessionId}`
* **Purpose**: Queries current archive collection state and level unlock status for a specific player session.
* **Headers**: `Accept: application/json`, `X-Session-ID: {sessionId}`
* **Response (200 OK)**:
```json
{
  "chapterId": "chapter-01",
  "title": "Voices of Curzon Hall",
  "sessionId": "unreal_session_1793434577",
  "archivesFound": 5,
  "totalArchivesRequired": 5,
  "level2Unlocked": true,
  "archives": [
    {"archiveId": "archive_01", "name": "Founding Stones", "discovered": true},
    {"archiveId": "archive_02", "name": "Folk Renaissance", "discovered": true},
    {"archiveId": "archive_03", "name": "Language Martyrs", "discovered": true},
    {"archiveId": "archive_04", "name": "Student Resistance", "discovered": true},
    {"archiveId": "archive_05", "name": "Charter of Liberation", "discovered": true}
  ]
}
```

---

### 2.4 Archive Discovery Submission
* **Endpoint**: `POST /api/v1/chapter-01/archive`
* **Purpose**: Submits discovery of a newly encountered in-world historical terminal.
* **Headers**: `Content-Type: application/json`, `Accept: application/json`
* **Request Body**:
```json
{
  "sessionId": "unreal_session_1793434577",
  "archiveId": "archive_03",
  "location": "Shaheed Minar",
  "timestamp": 1793434580000
}
```
* **Response (200 OK)**:
```json
{
  "success": true,
  "chapterId": "chapter-01",
  "archivesFound": 3,
  "totalArchivesRequired": 5,
  "level2Unlocked": false,
  "message": "Archive registered: archive_03"
}
```

---

## 3. Current Status

* **Status**: `COMPLETED`
* **Evidence**:
  - Live curl and Unreal HTTP requests tested against all 4 endpoints with 100% schema compliance.
* **Remaining Tasks**:
  - Add API endpoints for Chapter 2 (Inner Sanctum) quest lines.
