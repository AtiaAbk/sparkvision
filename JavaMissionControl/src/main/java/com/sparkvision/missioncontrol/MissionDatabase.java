package com.sparkvision.missioncontrol;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.HashSet;
import java.util.Set;

public class MissionDatabase {
    private final String dbUrl;

    public MissionDatabase(String dbFilePath) {
        this.dbUrl = "jdbc:sqlite:" + dbFilePath;
        initializeSchema();
    }

    private Connection connect() throws SQLException {
        return DriverManager.getConnection(dbUrl);
    }

    private void initializeSchema() {
        String createSessions = """
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                started_at INTEGER,
                chapter_id TEXT,
                completed INTEGER DEFAULT 0
            );
        """;

        String createEvents = """
            CREATE TABLE IF NOT EXISTS processed_events (
                event_id TEXT PRIMARY KEY,
                session_id TEXT,
                event_type TEXT,
                payload_json TEXT,
                received_at INTEGER
            );
        """;

        String createArchives = """
            CREATE TABLE IF NOT EXISTS discovered_archives (
                archive_id TEXT PRIMARY KEY,
                session_id TEXT,
                discovered_at INTEGER
            );
        """;

        String createSessionSettings = """
            CREATE TABLE IF NOT EXISTS session_settings (
                session_id TEXT PRIMARY KEY,
                selected_character TEXT DEFAULT 'MALE',
                selected_world TEXT DEFAULT 'DU_CAMPUS',
                graphics_preset TEXT DEFAULT 'ULTRA'
            );
        """;

        String createWaypoints = """
            CREATE TABLE IF NOT EXISTS visited_waypoints (
                waypoint_id TEXT,
                session_id TEXT,
                visited_at INTEGER,
                PRIMARY KEY(waypoint_id, session_id)
            );
        """;

        String createClimax = """
            CREATE TABLE IF NOT EXISTS climax_state (
                session_id TEXT PRIMARY KEY,
                attempt_count INTEGER DEFAULT 0,
                defeated INTEGER DEFAULT 0,
                last_updated INTEGER
            );
        """;

        String createCrime = """
            CREATE TABLE IF NOT EXISTS crime_log (
                crime_id TEXT PRIMARY KEY,
                session_id TEXT,
                victim_id TEXT,
                crime_type TEXT,
                recorded_at INTEGER
            );
        """;

        try (Connection conn = connect(); Statement stmt = conn.createStatement()) {
            stmt.execute(createSessions);
            stmt.execute(createEvents);
            stmt.execute(createArchives);
            stmt.execute(createSessionSettings);
            stmt.execute(createWaypoints);
            stmt.execute(createClimax);
            stmt.execute(createCrime);
        } catch (SQLException e) {
            System.err.println("[MissionDatabase] Schema initialization error: " + e.getMessage());
        }
    }

    public synchronized void startSession(String sessionId, String chapterId) {
        String sql = "INSERT OR REPLACE INTO sessions(session_id, started_at, chapter_id, completed) VALUES (?, ?, ?, 0);";
        try (Connection conn = connect(); PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setString(1, sessionId);
            pstmt.setLong(2, System.currentTimeMillis());
            pstmt.setString(3, chapterId);
            pstmt.executeUpdate();
        } catch (SQLException e) {
            System.err.println("[MissionDatabase] Error recording session: " + e.getMessage());
        }
    }

    public synchronized void setCharacter(String sessionId, String characterId) {
        String sql = "INSERT INTO session_settings(session_id, selected_character) VALUES (?, ?) ON CONFLICT(session_id) DO UPDATE SET selected_character = excluded.selected_character;";
        try (Connection conn = connect(); PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setString(1, sessionId);
            pstmt.setString(2, characterId);
            pstmt.executeUpdate();
        } catch (SQLException e) {
            System.err.println("[MissionDatabase] Error setting character: " + e.getMessage());
        }
    }

    public synchronized String getCharacter(String sessionId) {
        String sql = "SELECT selected_character FROM session_settings WHERE session_id = ?;";
        try (Connection conn = connect(); PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setString(1, sessionId);
            try (ResultSet rs = pstmt.executeQuery()) {
                if (rs.next()) {
                    return rs.getString("selected_character");
                }
            }
        } catch (SQLException e) {
            System.err.println("[MissionDatabase] Error getting character: " + e.getMessage());
        }
        return "MALE";
    }

    public synchronized boolean recordWaypointVisited(String waypointId, String sessionId) {
        String sId = (sessionId != null && !sessionId.isBlank()) ? sessionId : "default_session";
        String sql = "INSERT OR IGNORE INTO visited_waypoints(waypoint_id, session_id, visited_at) VALUES (?, ?, ?);";
        try (Connection conn = connect(); PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setString(1, waypointId);
            pstmt.setString(2, sId);
            pstmt.setLong(3, System.currentTimeMillis());
            return pstmt.executeUpdate() > 0;
        } catch (SQLException e) {
            System.err.println("[MissionDatabase] Error recording waypoint: " + e.getMessage());
            return false;
        }
    }

    public synchronized Set<String> getVisitedWaypoints(String sessionId) {
        Set<String> set = new HashSet<>();
        String sId = (sessionId != null && !sessionId.isBlank()) ? sessionId : "default_session";
        String sql = "SELECT waypoint_id FROM visited_waypoints WHERE session_id = ?;";
        try (Connection conn = connect(); PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setString(1, sId);
            try (ResultSet rs = pstmt.executeQuery()) {
                while (rs.next()) {
                    set.add(rs.getString("waypoint_id"));
                }
            }
        } catch (SQLException e) {
            System.err.println("[MissionDatabase] Error reading waypoints: " + e.getMessage());
        }
        return set;
    }

    public synchronized int recordClimaxDefeat(String sessionId) {
        String sId = (sessionId != null && !sessionId.isBlank()) ? sessionId : "default_session";
        int currentAttempt = getClimaxAttempt(sId);
        int nextAttempt = Math.min(currentAttempt + 1, 3);
        String sql = "INSERT INTO climax_state(session_id, attempt_count, defeated, last_updated) VALUES (?, ?, 1, ?) ON CONFLICT(session_id) DO UPDATE SET attempt_count = excluded.attempt_count, last_updated = excluded.last_updated;";
        try (Connection conn = connect(); PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setString(1, sId);
            pstmt.setInt(2, nextAttempt);
            pstmt.setLong(3, System.currentTimeMillis());
            pstmt.executeUpdate();
        } catch (SQLException e) {
            System.err.println("[MissionDatabase] Error recording climax defeat: " + e.getMessage());
        }
        return nextAttempt;
    }

    public synchronized int getClimaxAttempt(String sessionId) {
        String sId = (sessionId != null && !sessionId.isBlank()) ? sessionId : "default_session";
        String sql = "SELECT attempt_count FROM climax_state WHERE session_id = ?;";
        try (Connection conn = connect(); PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setString(1, sId);
            try (ResultSet rs = pstmt.executeQuery()) {
                if (rs.next()) {
                    return rs.getInt("attempt_count");
                }
            }
        } catch (SQLException e) {
            System.err.println("[MissionDatabase] Error reading climax attempt: " + e.getMessage());
        }
        return 0;
    }

    public synchronized void recordCrime(String sessionId, String victimId, String crimeType) {
        String crimeId = "crime_" + System.currentTimeMillis();
        String sql = "INSERT INTO crime_log(crime_id, session_id, victim_id, crime_type, recorded_at) VALUES (?, ?, ?, ?, ?);";
        try (Connection conn = connect(); PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setString(1, crimeId);
            pstmt.setString(2, sessionId);
            pstmt.setString(3, victimId);
            pstmt.setString(4, crimeType);
            pstmt.setLong(5, System.currentTimeMillis());
            pstmt.executeUpdate();
        } catch (SQLException e) {
            System.err.println("[MissionDatabase] Error recording crime: " + e.getMessage());
        }
    }

    public synchronized boolean hasProcessedEvent(String eventId) {
        String sql = "SELECT 1 FROM processed_events WHERE event_id = ?;";
        try (Connection conn = connect(); PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setString(1, eventId);
            try (ResultSet rs = pstmt.executeQuery()) {
                return rs.next();
            }
        } catch (SQLException e) {
            System.err.println("[MissionDatabase] Error checking event: " + e.getMessage());
            return false;
        }
    }

    public synchronized void recordEvent(String eventId, String sessionId, String eventType, String payloadJson) {
        String sql = "INSERT INTO processed_events(event_id, session_id, event_type, payload_json, received_at) VALUES (?, ?, ?, ?, ?);";
        try (Connection conn = connect(); PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setString(1, eventId);
            pstmt.setString(2, sessionId);
            pstmt.setString(3, eventType);
            pstmt.setString(4, payloadJson);
            pstmt.setLong(5, System.currentTimeMillis());
            pstmt.executeUpdate();
        } catch (SQLException e) {
            System.err.println("[MissionDatabase] Error recording event: " + e.getMessage());
        }
    }

    public synchronized boolean recordArchiveDiscovered(String archiveId, String sessionId) {
        String sql = "INSERT OR IGNORE INTO discovered_archives(archive_id, session_id, discovered_at) VALUES (?, ?, ?);";
        try (Connection conn = connect(); PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setString(1, archiveId);
            pstmt.setString(2, sessionId);
            pstmt.setLong(3, System.currentTimeMillis());
            return pstmt.executeUpdate() > 0;
        } catch (SQLException e) {
            System.err.println("[MissionDatabase] Error recording archive: " + e.getMessage());
            return false;
        }
    }

    public synchronized Set<String> getDiscoveredArchives() {
        return getDiscoveredArchives(null);
    }

    public synchronized Set<String> getDiscoveredArchives(String sessionId) {
        Set<String> set = new HashSet<>();
        String sql = (sessionId != null && !sessionId.isBlank())
                ? "SELECT archive_id FROM discovered_archives WHERE session_id = ?;"
                : "SELECT archive_id FROM discovered_archives;";
        try (Connection conn = connect(); PreparedStatement pstmt = conn.prepareStatement(sql)) {
            if (sessionId != null && !sessionId.isBlank()) {
                pstmt.setString(1, sessionId);
            }
            try (ResultSet rs = pstmt.executeQuery()) {
                while (rs.next()) {
                    set.add(rs.getString("archive_id"));
                }
            }
        } catch (SQLException e) {
            System.err.println("[MissionDatabase] Error reading archives: " + e.getMessage());
        }
        return set;
    }

    public synchronized void completeLevel(String sessionId, String chapterId) {
        String sql = "UPDATE sessions SET completed = 1 WHERE session_id = ? AND chapter_id = ?;";
        try (Connection conn = connect(); PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setString(1, sessionId);
            pstmt.setString(2, chapterId);
            pstmt.executeUpdate();
        } catch (SQLException e) {
            System.err.println("[MissionDatabase] Error completing level: " + e.getMessage());
        }
    }

    public synchronized boolean isChapterCompleted(String chapterId) {
        return isChapterCompleted(chapterId, null);
    }

    public synchronized boolean isChapterCompleted(String chapterId, String sessionId) {
        String sql = (sessionId != null && !sessionId.isBlank())
                ? "SELECT 1 FROM sessions WHERE chapter_id = ? AND completed = 1 AND session_id = ?;"
                : "SELECT 1 FROM sessions WHERE chapter_id = ? AND completed = 1;";
        try (Connection conn = connect(); PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setString(1, chapterId);
            if (sessionId != null && !sessionId.isBlank()) {
                pstmt.setString(2, sessionId);
            }
            try (ResultSet rs = pstmt.executeQuery()) {
                return rs.next();
            }
        } catch (SQLException e) {
            System.err.println("[MissionDatabase] Error checking completion: " + e.getMessage());
            return false;
        }
    }
}
