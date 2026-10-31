package com.sparkvision.missioncontrol;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;
import java.util.Set;
import java.util.concurrent.Executors;

public class MissionControlServer {
    private static final int DEFAULT_PORT = 8080;
    private final int port;
    private final MissionDatabase db;
    private final ObjectMapper mapper;
    private HttpServer server;

    public MissionControlServer(int port, String dbPath) {
        this.port = port;
        this.db = new MissionDatabase(dbPath);
        this.mapper = new ObjectMapper();
    }

    public static void main(String[] args) throws IOException {
        int port = DEFAULT_PORT;
        if (args.length > 0) {
            try {
                port = Integer.parseInt(args[0]);
            } catch (NumberFormatException ignored) {}
        }
        MissionControlServer server = new MissionControlServer(port, "sparkvision_missions.db");
        server.start();
        System.out.println("[MissionControlServer] Running on http://localhost:" + port);
    }

    public void start() throws IOException {
        server = HttpServer.create(new InetSocketAddress(port), 0);
        server.setExecutor(Executors.newFixedThreadPool(8));

        server.createContext("/api/v1/health", new HealthHandler());
        server.createContext("/api/v1/session/start", new SessionStartHandler());
        server.createContext("/api/v1/missions/chapter-01", new Chapter01Handler());
        server.createContext("/api/v1/events", new EventsHandler());

        server.start();
    }

    public void stop() {
        if (server != null) {
            server.stop(0);
        }
    }

    private class HealthHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            if ("GET".equalsIgnoreCase(exchange.getRequestMethod())) {
                MissionModels.HealthResponse response = new MissionModels.HealthResponse();
                sendJsonResponse(exchange, 200, response);
            } else {
                exchange.sendResponseHeaders(405, -1);
            }
        }
    }

    private class SessionStartHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            if ("POST".equalsIgnoreCase(exchange.getRequestMethod())) {
                MissionModels.StartSessionRequest req = mapper.readValue(exchange.getRequestBody(), MissionModels.StartSessionRequest.class);
                String sId = (req.sessionId != null && !req.sessionId.isBlank()) ? req.sessionId : "session_" + System.currentTimeMillis();
                db.startSession(sId, req.chapterId);

                MissionModels.StartSessionResponse resp = new MissionModels.StartSessionResponse();
                resp.success = true;
                resp.sessionId = sId;
                resp.currentChapter = req.chapterId;
                resp.message = "Session initialized for SparkVision Level 1";
                sendJsonResponse(exchange, 200, resp);
            } else {
                exchange.sendResponseHeaders(405, -1);
            }
        }
    }

    private class Chapter01Handler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            if ("GET".equalsIgnoreCase(exchange.getRequestMethod())) {
                Set<String> discovered = db.getDiscoveredArchives();

                MissionModels.ChapterMissionResponse resp = new MissionModels.ChapterMissionResponse();
                resp.chapterId = "chapter-01";
                resp.title = "Where It All Began";
                resp.period = "July 1–14, 2024";
                resp.setting = "Dhaka University — Curzon Hall Heritage Precinct";
                resp.totalArchivesRequired = 5;
                resp.archivesFound = discovered.size();
                resp.level2Unlocked = db.isChapterCompleted("chapter-01") || discovered.size() >= 5;

                List<MissionModels.ArchiveInfo> list = new ArrayList<>();
                list.add(new MissionModels.ArchiveInfo("archive_01", "Curzon Hall Arcade Founding Record", "Curzon Hall Central Arcade", discovered.contains("archive_01")));
                list.add(new MissionModels.ArchiveInfo("archive_02", "Aparajeyo Bangla 1952/1971 Chronicle", "Arts Faculty Plaza", discovered.contains("archive_02")));
                list.add(new MissionModels.ArchiveInfo("archive_03", "Raju Anti-Terrorism Memorial Declaration", "TSC Intersection", discovered.contains("archive_03")));
                list.add(new MissionModels.ArchiveInfo("archive_04", "Central Library & Hakim Chattar Reform Gazette", "Central Library", discovered.contains("archive_04")));
                list.add(new MissionModels.ArchiveInfo("archive_05", "Teacher-Student Centre (TSC) Unity Manifesto", "TSC Courtyard", discovered.contains("archive_05")));

                resp.archives = list;
                sendJsonResponse(exchange, 200, resp);
            } else {
                exchange.sendResponseHeaders(405, -1);
            }
        }
    }

    private class EventsHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            if ("POST".equalsIgnoreCase(exchange.getRequestMethod())) {
                InputStream is = exchange.getRequestBody();
                MissionModels.GameEventRequest req = mapper.readValue(is, MissionModels.GameEventRequest.class);

                MissionModels.GameEventResponse resp = new MissionModels.GameEventResponse();
                resp.eventId = req.eventId;

                // Idempotency check: if event already processed, return current state without double-counting
                if (req.eventId != null && db.hasProcessedEvent(req.eventId)) {
                    resp.success = true;
                    resp.message = "Event already recorded (Idempotent response)";
                    Set<String> discovered = db.getDiscoveredArchives();
                    resp.archivesFound = discovered.size();
                    resp.totalArchives = 5;
                    resp.allArchivesFound = (discovered.size() >= 5);
                    resp.level2Unlocked = db.isChapterCompleted("chapter-01") || resp.allArchivesFound;
                    sendJsonResponse(exchange, 200, resp);
                    return;
                }

                // Process new event
                if ("ARCHIVE_DISCOVERED".equalsIgnoreCase(req.eventType)) {
                    boolean newlyRecorded = db.recordArchiveDiscovered(req.targetId, req.sessionId);
                    db.recordEvent(req.eventId, req.sessionId, req.eventType, mapper.writeValueAsString(req));

                    Set<String> discovered = db.getDiscoveredArchives();
                    resp.success = true;
                    resp.message = newlyRecorded ? ("Archive " + req.targetId + " registered successfully") : "Archive already discovered";
                    resp.archivesFound = discovered.size();
                    resp.totalArchives = 5;
                    resp.allArchivesFound = (discovered.size() >= 5);
                    resp.level2Unlocked = db.isChapterCompleted("chapter-01") || resp.allArchivesFound;
                } else if ("LEVEL1_COMPLETED".equalsIgnoreCase(req.eventType) || "COMBAT_VICTORY".equalsIgnoreCase(req.eventType)) {
                    db.completeLevel(req.sessionId, "chapter-01");
                    db.recordEvent(req.eventId, req.sessionId, req.eventType, mapper.writeValueAsString(req));
                    Set<String> discovered = db.getDiscoveredArchives();
                    resp.success = true;
                    resp.message = "Level 1 victory registered! Chapter 2 unlocked.";
                    resp.archivesFound = discovered.size();
                    resp.totalArchives = 5;
                    resp.allArchivesFound = true;
                    resp.level2Unlocked = true;
                } else {
                    db.recordEvent(req.eventId, req.sessionId, req.eventType, mapper.writeValueAsString(req));
                    Set<String> discovered = db.getDiscoveredArchives();
                    resp.success = true;
                    resp.message = "Event recorded: " + req.eventType;
                    resp.archivesFound = discovered.size();
                    resp.totalArchives = 5;
                    resp.allArchivesFound = (discovered.size() >= 5);
                    resp.level2Unlocked = db.isChapterCompleted("chapter-01");
                }

                sendJsonResponse(exchange, 200, resp);
            } else {
                exchange.sendResponseHeaders(405, -1);
            }
        }
    }

    private void sendJsonResponse(HttpExchange exchange, int statusCode, Object data) throws IOException {
        byte[] bytes = mapper.writeValueAsBytes(data);
        exchange.getResponseHeaders().set("Content-Type", "application/json; charset=UTF-8");
        exchange.getResponseHeaders().set("Access-Control-Allow-Origin", "*");
        exchange.sendResponseHeaders(statusCode, bytes.length);
        try (OutputStream os = exchange.getResponseBody()) {
            os.write(bytes);
        }
    }
}
