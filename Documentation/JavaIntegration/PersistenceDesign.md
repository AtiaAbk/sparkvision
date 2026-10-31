# SPARKVISION — PERSISTENCE & DATABASE ARCHITECTURE

## 1. Title & Executive Purpose

* **Document**: `PersistenceDesign.md`
* **Purpose**: Details the relational schema, connection pooling, ACID transaction guarantees, session isolation mechanisms, and migration policies for the embedded SQLite database (`sparkvision_missions.db`).

---

## 2. Relational Schema Architecture

```sql
PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;

-- 1. Sessions Table: Records gameplay instances
CREATE TABLE IF NOT EXISTS sessions (
    session_id TEXT PRIMARY KEY,
    start_time INTEGER NOT NULL,
    end_time INTEGER,
    current_chapter TEXT DEFAULT 'chapter-01',
    completed BOOLEAN DEFAULT 0
);

-- 2. Discovered Archives Table: Tracks terminal interactions
CREATE TABLE IF NOT EXISTS discovered_archives (
    session_id TEXT NOT NULL,
    archive_id TEXT NOT NULL,
    discovered_at INTEGER NOT NULL,
    PRIMARY KEY (session_id, archive_id),
    FOREIGN KEY (session_id) REFERENCES sessions(session_id) ON DELETE CASCADE
);

-- 3. Chapter Progress Table: Stores chapter-level gate flags
CREATE TABLE IF NOT EXISTS chapter_progress (
    session_id TEXT NOT NULL,
    chapter_id TEXT NOT NULL,
    unlocked BOOLEAN DEFAULT 0,
    completed BOOLEAN DEFAULT 0,
    PRIMARY KEY (session_id, chapter_id),
    FOREIGN KEY (session_id) REFERENCES sessions(session_id) ON DELETE CASCADE
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_archives_session ON discovered_archives (session_id);
CREATE INDEX IF NOT EXISTS idx_progress_session ON chapter_progress (session_id);
```

---

## 3. Session Isolation & Concurrency Model

* **Thread-Safe DAO**: `MissionDatabase.java` wraps all SQLite operations inside synchronized helper blocks or connection pools to avoid SQLITE_BUSY locking on multi-threaded HTTP handling.
* **Deterministic Session Partitioning**: All read and write queries enforce `session_id = ?`. This allows historical baseline validation sessions (e.g. `test_session_unreal_001` with 5/5 archives) to persist indefinitely while new user play-sessions execute concurrently.

---

## 4. Current Status

* **Status**: `COMPLETED`
* **Evidence**:
  - SQLite database initialized and tested with over 10 test sessions.
  - Verification test passed: `session_level1_fresh_001` (0/5) vs `test_session_unreal_001` (5/5).
* **Remaining Tasks**:
  - Implement automated periodic `.backup` snapshotting of `sparkvision_missions.db` to prevent corruption during unexpected shutdowns.
