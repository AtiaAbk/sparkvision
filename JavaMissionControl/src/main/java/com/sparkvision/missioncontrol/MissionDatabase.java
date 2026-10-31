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

        try (Connection conn = connect(); Statement stmt = conn.createStatement()) {
            stmt.execute(createSessions);
            stmt.execute(createEvents);
            stmt.execute(createArchives);
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
        String checkSql = "SELECT 1 FROM discovered_archives WHERE archive_id = ?;";
        try (Connection conn = connect(); PreparedStatement checkStmt = conn.prepareStatement(checkSql)) {
            checkStmt.setString(1, archiveId);
            try (ResultSet rs = checkStmt.executeQuery()) {
                if (rs.next()) {
                    return false; // Already discovered
                }
            }
        } catch (SQLException e) {
            System.err.println("[MissionDatabase] Error checking archive: " + e.getMessage());
            return false;
        }

        String insertSql = "INSERT INTO discovered_archives(archive_id, session_id, discovered_at) VALUES (?, ?, ?);";
        try (Connection conn = connect(); PreparedStatement insertStmt = conn.prepareStatement(insertSql)) {
            insertStmt.setString(1, archiveId);
            insertStmt.setString(2, sessionId);
            insertStmt.setLong(3, System.currentTimeMillis());
            insertStmt.executeUpdate();
            return true;
        } catch (SQLException e) {
            System.err.println("[MissionDatabase] Error saving archive: " + e.getMessage());
            return false;
        }
    }

    public synchronized Set<String> getDiscoveredArchives() {
        Set<String> set = new HashSet<>();
        String sql = "SELECT archive_id FROM discovered_archives;";
        try (Connection conn = connect(); Statement stmt = conn.createStatement(); ResultSet rs = stmt.executeQuery(sql)) {
            while (rs.next()) {
                set.add(rs.getString("archive_id"));
            }
        } catch (SQLException e) {
            System.err.println("[MissionDatabase] Error getting archives: " + e.getMessage());
        }
        return set;
    }

    public synchronized void completeLevel(String sessionId, String chapterId) {
        String sql = "UPDATE sessions SET completed = 1 WHERE session_id = ? OR chapter_id = ?;";
        try (Connection conn = connect(); PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setString(1, sessionId);
            pstmt.setString(2, chapterId);
            pstmt.executeUpdate();
        } catch (SQLException e) {
            System.err.println("[MissionDatabase] Error completing level: " + e.getMessage());
        }
    }

    public synchronized boolean isChapterCompleted(String chapterId) {
        String sql = "SELECT 1 FROM sessions WHERE chapter_id = ? AND completed = 1;";
        try (Connection conn = connect(); PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setString(1, chapterId);
            try (ResultSet rs = pstmt.executeQuery()) {
                return rs.next();
            }
        } catch (SQLException e) {
            return false;
        }
    }
}
