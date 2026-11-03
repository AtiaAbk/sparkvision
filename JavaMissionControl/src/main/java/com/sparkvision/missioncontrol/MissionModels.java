package com.sparkvision.missioncontrol;

import java.util.ArrayList;
import java.util.List;

public class MissionModels {

    public static class HealthResponse {
        public String status = "OK";
        public String service = "SparkVision Mission Control";
        public String version = "2.0.0";
        public long timestamp = System.currentTimeMillis();
    }

    public static class StartSessionRequest {
        public String sessionId;
        public String chapterId = "chapter-01";
        public String selectedCharacter = "MALE"; // "MALE" (Shovon) or "FEMALE" (Rina)
    }

    public static class StartSessionResponse {
        public boolean success;
        public String sessionId;
        public String message;
        public String currentChapter;
        public String selectedCharacter;
    }

    // AAA Main Menu & Character Selection Models
    public static class MenuConfigResponse {
        public String title = "SPARKVISION 2x12";
        public String subtitle = "University of Dhaka — Open World Chronicle (July 2024)";
        public List<CharacterOption> characterOptions = new ArrayList<>();
        public String selectedCharacter = "MALE";
        public List<WorldOption> worldOptions = new ArrayList<>();
        public String selectedWorld = "DU_CAMPUS";
        public String graphicsPreset = "ULTRA";
        public float masterVolume = 1.0f;
        public float sfxVolume = 0.9f;
        public float musicVolume = 0.8f;
    }

    public static class CharacterOption {
        public String id; // "MALE", "FEMALE"
        public String nameBengali;
        public String nameEnglish;
        public String role;
        public String department;
        public String meshPath;

        public CharacterOption() {}
        public CharacterOption(String id, String nameBengali, String nameEnglish, String role, String department, String meshPath) {
            this.id = id;
            this.nameBengali = nameBengali;
            this.nameEnglish = nameEnglish;
            this.role = role;
            this.department = department;
            this.meshPath = meshPath;
        }
    }

    public static class WorldOption {
        public String id;
        public String nameBengali;
        public String nameEnglish;
        public boolean available;

        public WorldOption() {}
        public WorldOption(String id, String nameBengali, String nameEnglish, boolean available) {
            this.id = id;
            this.nameBengali = nameBengali;
            this.nameEnglish = nameEnglish;
            this.available = available;
        }
    }

    public static class SelectCharacterRequest {
        public String sessionId;
        public String characterId; // "MALE" or "FEMALE"
    }

    // 5 Campus Landmark Navigation Waypoints (Where Winds Meet Style)
    public static class WaypointsResponse {
        public String activeTargetId;
        public String activeTargetNameBengali;
        public String activeTargetNameEnglish;
        public double targetX;
        public double targetY;
        public double targetZ;
        public int completedCount;
        public int totalWaypoints;
        public boolean allCompleted;
        public boolean climaxEncounterReady;
        public List<WaypointInfo> waypoints = new ArrayList<>();
    }

    public static class WaypointInfo {
        public String id;
        public String nameBengali;
        public String nameEnglish;
        public double x;
        public double y;
        public double z;
        public double radius;
        public boolean visited;

        public WaypointInfo() {}
        public WaypointInfo(String id, String nameBengali, String nameEnglish, double x, double y, double z, double radius, boolean visited) {
            this.id = id;
            this.nameBengali = nameBengali;
            this.nameEnglish = nameEnglish;
            this.x = x;
            this.y = y;
            this.z = z;
            this.radius = radius;
            this.visited = visited;
        }
    }

    public static class WaypointVisitRequest {
        public String sessionId;
        public String waypointId;
    }

    // Civilian Assault & Police Arrest (Consequence System)
    public static class CrimeAlertRequest {
        public String sessionId;
        public String victimId;
        public String crimeType = "ASSAULT_ON_STUDENT";
        public String description;
    }

    public static class CrimeAlertResponse {
        public boolean arrested = true;
        public String sirenSound = "Siren_Police_Emergency";
        public String messageBengali = "সাধারণ শিক্ষার্থীর ওপর আক্রমণের দায়ে আপনাকে পুলিশ আটক করেছে!";
        public String messageEnglish = "You have been arrested by police for assaulting an ordinary student!";
        public String status = "BUSTED";
        public boolean gameOver = true;
    }

    // Climax Combat: Helmeted Bike Cadres & 3-Defeat Retry Loop
    public static class ClimaxCombatResponse {
        public boolean active;
        public String leaderNameBengali = "ক্যাডার লিডার (নৌকা ক্যাপ ও হেলমেট পরিহিত)";
        public String leaderNameEnglish = "Cadre Squad Leader (Wearing Boat/Nouka Cap & Helmet)";
        public String enemySquadType = "Armed Bike Cadres with Bamboo Sticks (Lathis)";
        public int currentAttempt; // 1, 2, or 3
        public int maxAttempts = 3;
        public boolean retryAllowed;
        public boolean finalGameOver;
        public String statusMessageBengali;
        public String statusMessageEnglish;
    }

    public static class ClimaxDefeatRequest {
        public String sessionId;
        public String defeatReason = "KNOCKED_DOWN_BY_LATHI_SQUAD";
    }

    // Legacy Chapter 1 Compatibility
    public static class ChapterMissionResponse {
        public String chapterId;
        public String title;
        public String period;
        public String setting;
        public int totalArchivesRequired;
        public int archivesFound;
        public boolean level2Unlocked;
        public List<ArchiveInfo> archives;
    }

    public static class ArchiveInfo {
        public String id;
        public String name;
        public String location;
        public boolean discovered;

        public ArchiveInfo() {}
        public ArchiveInfo(String id, String name, String location, boolean discovered) {
            this.id = id;
            this.name = name;
            this.location = location;
            this.discovered = discovered;
        }
    }

    public static class GameEventRequest {
        public String eventId;
        public String sessionId;
        public String eventType;
        public String targetId;
        public String timestamp;
    }

    public static class GameEventResponse {
        public boolean success;
        public String eventId;
        public String message;
        public int archivesFound;
        public int totalArchives;
        public boolean allArchivesFound;
        public boolean level2Unlocked;
    }
}
