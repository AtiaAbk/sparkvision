# SparkVision — Java Mission Control Integration

## 1. Architectural Role
Java Mission Control is a mandatory academic component of SparkVision. It operates as an independent backend service managing mission persistence, session validation, objective verification, and chapter progression using SQLite.

## 2. Service Endpoints (`http://localhost:8080`)

| Endpoint | Method | Purpose | Payload / Response |
| :--- | :--- | :--- | :--- |
| `/api/v1/health` | `GET` | Health check & service readiness | `{"status":"HEALTHY","timestamp":...}` |
| `/api/v1/session/start` | `POST` | Initialize academic mission session | `{"sessionId":"...","chapterId":"chapter-01"}` |
| `/api/v1/missions/chapter-01` | `GET` | Retrieve chapter 1 objectives & discovered archives | Returns archive list, count, and completion state |
| `/api/v1/events` | `POST` | Record gameplay events (`ARCHIVE_DISCOVERED`, `LEVEL1_COMPLETED`) | Idempotent event registration and unlocked flags |

## 3. Unreal C++ Client Integration (`USVMissionControlSubsystem`)
- Subsystem derived from `UGameInstanceSubsystem`.
- Lifecycle: Automatically initialized when game instance starts.
- Threading: 100% Non-blocking asynchronous HTTP requests via `FHttpModule` and `IHttpRequest`.
- Resilience: If the Java service is temporarily offline, the game continues gracefully in local offline mode, queuing events and updating the HUD indicator.
