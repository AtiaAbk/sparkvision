package com.sparkvision.missioncontrol;

import java.util.List;

public class MissionModels {

    public static class HealthResponse {
        public String status = "OK";
        public String service = "SparkVision Mission Control";
        public String version = "1.0.0";
        public long timestamp = System.currentTimeMillis();
    }

    public static class StartSessionRequest {
        public String sessionId;
        public String chapterId = "chapter-01";
    }

    public static class StartSessionResponse {
        public boolean success;
        public String sessionId;
        public String message;
        public String currentChapter;
    }

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
