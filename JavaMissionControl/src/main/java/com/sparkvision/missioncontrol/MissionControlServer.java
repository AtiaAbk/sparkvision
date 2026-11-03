package com.sparkvision.missioncontrol;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.InetSocketAddress;
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
        server.createContext("/api/v1/menu/config", new MenuConfigHandler());
        server.createContext("/api/v1/mission/waypoints", new WaypointsHandler());
        server.createContext("/api/v1/events/crime", new CrimeHandler());
        server.createContext("/api/v1/events/combat/retry", new CombatRetryHandler());
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
                if (req.selectedCharacter != null) {
                    db.setCharacter(sId, req.selectedCharacter);
                }

                MissionModels.StartSessionResponse resp = new MissionModels.StartSessionResponse();
                resp.success = true;
                resp.sessionId = sId;
                resp.currentChapter = req.chapterId;
                resp.selectedCharacter = db.getCharacter(sId);
                resp.message = "Session initialized for SparkVision 2x12: University of Dhaka";
                sendJsonResponse(exchange, 200, resp);
            } else {
                exchange.sendResponseHeaders(405, -1);
            }
        }
    }

    // AAA Main Menu & Character Selection Handler
    private class MenuConfigHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            String method = exchange.getRequestMethod();
            if ("GET".equalsIgnoreCase(method)) {
                String sessionId = exchange.getRequestHeaders().getFirst("X-Session-ID");
                MissionModels.MenuConfigResponse resp = new MissionModels.MenuConfigResponse();

                resp.characterOptions.add(new MissionModels.CharacterOption(
                    "MALE",
                    "শোভন (Shovon)",
                    "Shovon (Male Student)",
                    "Undergraduate Researcher",
                    "Department of Physics, Curzon Hall",
                    "/Game/Characters/Mannequins/Meshes/SKM_Manny_Simple.SKM_Manny_Simple"
                ));

                resp.characterOptions.add(new MissionModels.CharacterOption(
                    "FEMALE",
                    "রিনা (Rina)",
                    "Rina (Female Student)",
                    "Biochemistry Scholar & Debate Finalist",
                    "Department of Biochemistry & Molecular Biology, Curzon Hall",
                    "/Game/Characters/Mannequins/Meshes/SKM_Quinn_Simple.SKM_Quinn_Simple"
                ));

                resp.selectedCharacter = (sessionId != null) ? db.getCharacter(sessionId) : "MALE";

                resp.worldOptions.add(new MissionModels.WorldOption("DU_CAMPUS", "ঢাকা বিশ্ববিদ্যালয় প্রাঙ্গণ (DU Campus)", "Dhaka University Campus (Curzon to Arts)", true));
                resp.worldOptions.add(new MissionModels.WorldOption("OLD_DHAKA", "পুরান ঢাকা ঐতিহ্য অঞ্চল (Old Dhaka)", "Old Dhaka Heritage District", false));
                resp.worldOptions.add(new MissionModels.WorldOption("SUHRAWARDY", "সোহরাওয়ার্দী উদ্যান অভয়ারণ্য (Suhrawardy)", "Suhrawardy Udyan Sanctuary", false));

                sendJsonResponse(exchange, 200, resp);
            } else if ("POST".equalsIgnoreCase(method)) {
                MissionModels.SelectCharacterRequest req = mapper.readValue(exchange.getRequestBody(), MissionModels.SelectCharacterRequest.class);
                String sId = (req.sessionId != null && !req.sessionId.isBlank()) ? req.sessionId : "default_session";
                db.setCharacter(sId, req.characterId);

                MissionModels.StartSessionResponse resp = new MissionModels.StartSessionResponse();
                resp.success = true;
                resp.sessionId = sId;
                resp.selectedCharacter = req.characterId;
                resp.message = "Character selection updated to " + req.characterId;
                sendJsonResponse(exchange, 200, resp);
            } else {
                exchange.sendResponseHeaders(405, -1);
            }
        }
    }

    // 5 Campus Landmarks Navigation Waypoints Handler (Where Winds Meet Style)
    private class WaypointsHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            String method = exchange.getRequestMethod();
            if ("GET".equalsIgnoreCase(method)) {
                String sessionId = exchange.getRequestHeaders().getFirst("X-Session-ID");
                Set<String> visited = db.getVisitedWaypoints(sessionId);

                MissionModels.WaypointsResponse resp = new MissionModels.WaypointsResponse();
                resp.totalWaypoints = 5;

                // 5 Sequential Campus Landmark Waypoints
                List<MissionModels.WaypointInfo> list = new ArrayList<>();
                list.add(new MissionModels.WaypointInfo("curzon_portico", "১. কার্জন হল সম্মুখ তোরণ", "1. Curzon Hall Heritage Portico", -3350.0, 0.0, 80.0, 2500.0, visited.contains("curzon_portico")));
                list.add(new MissionModels.WaypointInfo("shaheed_minar", "২. কেন্দ্রীয় শহীদ মিনার বেদি", "2. Central Shaheed Minar Monument Plaza", -2200.0, -54000.0, 100.0, 2500.0, visited.contains("shaheed_minar")));
                list.add(new MissionModels.WaypointInfo("tsc_raju", "৩. টিএসসি ও রাজু ভাস্কর্য প্রাঙ্গণ", "3. Teacher-Student Centre (TSC) & Raju Memorial", 57000.0, -62500.0, 150.0, 2500.0, visited.contains("tsc_raju")));
                list.add(new MissionModels.WaypointInfo("kala_bhaban", "৪. কলা ভবন ও অপরাজেয় বাংলা", "4. Faculty of Arts (Kala Bhaban) & Aparajeyo Bangla", 70500.0, -95000.0, 150.0, 2500.0, visited.contains("kala_bhaban")));
                list.add(new MissionModels.WaypointInfo("doyel_chattar", "৫. দোয়েল চত্বর জাতীয় পাখি ফোয়ারা", "5. Doyel Chattar National Bird Monument", 30500.0, -22000.0, 100.0, 2500.0, visited.contains("doyel_chattar")));

                resp.waypoints = list;
                resp.completedCount = visited.size();
                resp.allCompleted = (visited.size() >= 5);
                resp.climaxEncounterReady = resp.allCompleted;

                // Find first unvisited target as active waypoint
                MissionModels.WaypointInfo active = null;
                for (MissionModels.WaypointInfo wp : list) {
                    if (!wp.visited) {
                        active = wp;
                        break;
                    }
                }
                if (active != null) {
                    resp.activeTargetId = active.id;
                    resp.activeTargetNameBengali = active.nameBengali;
                    resp.activeTargetNameEnglish = active.nameEnglish;
                    resp.targetX = active.x;
                    resp.targetY = active.y;
                    resp.targetZ = active.z;
                } else {
                    resp.activeTargetId = "climax_courtyard";
                    resp.activeTargetNameBengali = "চূড়ান্ত মুখোমুখি: কার্জন উত্তর চত্বর";
                    resp.activeTargetNameEnglish = "Climactic Confrontation: Curzon North Courtyard";
                    resp.targetX = -1850.0;
                    resp.targetY = 1600.0;
                    resp.targetZ = 80.0;
                }

                sendJsonResponse(exchange, 200, resp);
            } else if ("POST".equalsIgnoreCase(method)) {
                MissionModels.WaypointVisitRequest req = mapper.readValue(exchange.getRequestBody(), MissionModels.WaypointVisitRequest.class);
                boolean newlyVisited = db.recordWaypointVisited(req.waypointId, req.sessionId);

                MissionModels.GameEventResponse resp = new MissionModels.GameEventResponse();
                resp.success = true;
                resp.message = newlyVisited ? ("Waypoint " + req.waypointId + " registered successfully") : "Already visited";
                Set<String> visited = db.getVisitedWaypoints(req.sessionId);
                resp.archivesFound = visited.size();
                resp.totalArchives = 5;
                resp.allArchivesFound = (visited.size() >= 5);
                resp.level2Unlocked = resp.allArchivesFound;
                sendJsonResponse(exchange, 200, resp);
            } else {
                exchange.sendResponseHeaders(405, -1);
            }
        }
    }

    // Civilian Assault & Police Arrest (Consequence System)
    private class CrimeHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            if ("POST".equalsIgnoreCase(exchange.getRequestMethod())) {
                MissionModels.CrimeAlertRequest req = mapper.readValue(exchange.getRequestBody(), MissionModels.CrimeAlertRequest.class);
                db.recordCrime(req.sessionId, req.victimId, req.crimeType);

                MissionModels.CrimeAlertResponse resp = new MissionModels.CrimeAlertResponse();
                sendJsonResponse(exchange, 200, resp);
            } else {
                exchange.sendResponseHeaders(405, -1);
            }
        }
    }

    // Climax Combat: Helmeted Bike Cadres & 3-Defeat Retry Loop
    private class CombatRetryHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            if ("POST".equalsIgnoreCase(exchange.getRequestMethod())) {
                MissionModels.ClimaxDefeatRequest req = mapper.readValue(exchange.getRequestBody(), MissionModels.ClimaxDefeatRequest.class);
                int attempts = db.recordClimaxDefeat(req.sessionId);

                MissionModels.ClimaxCombatResponse resp = new MissionModels.ClimaxCombatResponse();
                resp.active = true;
                resp.currentAttempt = attempts;
                resp.maxAttempts = 3;
                resp.retryAllowed = (attempts < 3);
                resp.finalGameOver = (attempts >= 3);

                if (resp.retryAllowed) {
                    resp.statusMessageBengali = "আঘাতপ্রাপ্ত! আপনি পুনরায় লড়াইয়ের সুযোগ পাচ্ছেন (চেষ্টা: " + attempts + "/3)";
                    resp.statusMessageEnglish = "Knocked Down! Retry available (Attempt: " + attempts + "/3)";
                } else {
                    resp.statusMessageBengali = "অস্ত্রধারীদের হামলার মুখে প্রতিরোধ সাময়িকভাবে স্তব্ধ... কিন্তু চেতনা অমর! মূল মেন্যুতে ফিরে যাচ্ছে।";
                    resp.statusMessageEnglish = "Overpowered by armed cadres... Resistance pauses, but spirit remains eternal! Returning to Main Menu.";
                }

                sendJsonResponse(exchange, 200, resp);
            } else {
                exchange.sendResponseHeaders(405, -1);
            }
        }
    }

    // Legacy Chapter 1
    private class Chapter01Handler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            if ("GET".equalsIgnoreCase(exchange.getRequestMethod())) {
                String sessionId = exchange.getRequestHeaders().getFirst("X-Session-ID");
                Set<String> discovered = (sessionId != null && !sessionId.isBlank())
                        ? db.getDiscoveredArchives(sessionId)
                        : db.getDiscoveredArchives();

                MissionModels.ChapterMissionResponse resp = new MissionModels.ChapterMissionResponse();
                resp.chapterId = "chapter-01";
                resp.title = "Where It All Began";
                resp.period = "July 1–14, 2024";
                resp.setting = "Dhaka University — Curzon Hall Heritage Precinct";
                resp.totalArchivesRequired = 5;
                resp.archivesFound = discovered.size();
                resp.level2Unlocked = (sessionId != null && !sessionId.isBlank())
                        ? (db.isChapterCompleted("chapter-01", sessionId) || discovered.size() >= 5)
                        : (db.isChapterCompleted("chapter-01") || discovered.size() >= 5);

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
