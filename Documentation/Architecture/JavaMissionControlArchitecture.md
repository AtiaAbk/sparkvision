# SPARKVISION — JAVA MISSION CONTROL ARCHITECTURE

## 1. Title & Executive Purpose

* **Document**: `JavaMissionControlArchitecture.md`
* **Purpose**: Defines the software architecture, package layout, HTTP server routing, database access patterns, and session isolation model of the companion **Java 21 Mission Control** subsystem.

---

## 2. Technology Stack & Project Structure

* **Runtime**: Java 21 LTS (OpenJDK 21 via Gradle toolchain)
* **Build System**: Gradle 8.x (`JavaMissionControl/build.gradle.kts`)
* **HTTP Microservice**: Lightweight embedded HTTP server (`com.sun.net.httpserver`)
* **Persistence Layer**: Embedded SQLite via JDBC (`org.xerial:sqlite-jdbc`)
* **JSON Serialization**: Google Gson (`com.google.code.gson`)
* **Source Location**: `/Users/atiaoishi/Downloads/sparkvision/JavaMissionControl/`

```text
JavaMissionControl/
├── build.gradle.kts
├── gradlew, gradlew.bat
└── src/
    ├── main/java/com/sparkvision/missioncontrol/
    │   ├── MissionControlServer.java    [Main entrypoint & HTTP route registry]
    │   ├── MissionDatabase.java          [JDBC DAO, connection pool & migrations]
    │   ├── models/                       [Session, Mission, Archive data records]
    │   └── handlers/                     [HealthHandler, Chapter01Handler, SessionHandler]
    └── test/java/com/sparkvision/missioncontrol/
        └── MissionControlServerTest.java [Automated unit & integration test suite]
```

---

## 3. Database Schema & Session Isolation Model

All persistent mission data is stored in `JavaMissionControl/sparkvision_missions.db`:

```sql
-- Active and historical player sessions
CREATE TABLE IF NOT EXISTS sessions (
    session_id TEXT PRIMARY KEY,
    start_time INTEGER NOT NULL,
    current_chapter TEXT DEFAULT 'chapter-01',
    completed BOOLEAN DEFAULT 0
);

-- Historical archive discoveries partitioned by session
CREATE TABLE IF NOT EXISTS discovered_archives (
    session_id TEXT NOT NULL,
    archive_id TEXT NOT NULL,
    discovered_at INTEGER NOT NULL,
    PRIMARY KEY (session_id, archive_id),
    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
);

-- Chapter milestone states
CREATE TABLE IF NOT EXISTS chapter_progress (
    session_id TEXT NOT NULL,
    chapter_id TEXT NOT NULL,
    unlocked BOOLEAN DEFAULT 0,
    completed BOOLEAN DEFAULT 0,
    PRIMARY KEY (session_id, chapter_id)
);
```

### Session Isolation Architecture:
* **Session Query Partitioning**: Every query in `MissionDatabase.java` filters on `session_id` (`WHERE session_id = ?`).
* **Preservation of Benchmark Records**: A historical baseline session (e.g. `test_session_unreal_001` with 5/5 archives) remains permanently intact in SQLite while fresh gameplay sessions start from 0/5 archives.

---

## 4. Current Status

* **Status**: `COMPLETED`
* **Evidence**:
  - Gradle test suite passes (`./gradlew test` -> `BUILD SUCCESSFUL`).
  - Session isolation verified between fresh session `session_level1_fresh_001` (0/5) and baseline `test_session_unreal_001` (5/5).
* **Remaining Tasks**:
  - Add SQLite WAL mode configuration for concurrent high-frequency write throughput.
