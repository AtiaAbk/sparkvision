package com.sparkvision.missioncontrol;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.io.File;
import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

import static org.junit.jupiter.api.Assertions.*;

public class MissionControlServerTest {

    private static final int TEST_PORT = 18080;
    private static final String TEST_DB = "test_missions.db";
    private MissionControlServer server;
    private HttpClient client;

    @BeforeEach
    public void setUp() throws IOException {
        new File(TEST_DB).delete();
        server = new MissionControlServer(TEST_PORT, TEST_DB);
        server.start();
        client = HttpClient.newHttpClient();
    }

    @AfterEach
    public void tearDown() {
        if (server != null) {
            server.stop();
        }
        new File(TEST_DB).delete();
    }

    @Test
    public void testHealthEndpoint() throws Exception {
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("http://localhost:" + TEST_PORT + "/api/v1/health"))
                .GET()
                .build();

        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        assertEquals(200, response.statusCode());
        assertTrue(response.body().contains("\"status\":\"OK\""));
    }

    @Test
    public void testStartSession() throws Exception {
        String payload = "{\"sessionId\":\"sess_123\",\"chapterId\":\"chapter-01\"}";
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("http://localhost:" + TEST_PORT + "/api/v1/session/start"))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(payload))
                .build();

        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        assertEquals(200, response.statusCode());
        assertTrue(response.body().contains("\"success\":true"));
        assertTrue(response.body().contains("\"sessionId\":\"sess_123\""));
    }

    @Test
    public void testArchiveDiscoveryAndIdempotency() throws Exception {
        // First discovery
        String event1 = "{\"eventId\":\"evt_001\",\"sessionId\":\"sess_123\",\"eventType\":\"ARCHIVE_DISCOVERED\",\"targetId\":\"archive_01\"}";
        HttpRequest request1 = HttpRequest.newBuilder()
                .uri(URI.create("http://localhost:" + TEST_PORT + "/api/v1/events"))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(event1))
                .build();

        HttpResponse<String> response1 = client.send(request1, HttpResponse.BodyHandlers.ofString());
        assertEquals(200, response1.statusCode());
        assertTrue(response1.body().contains("\"archivesFound\":1"));

        // Duplicate event with same eventId should not increase count
        HttpResponse<String> responseDup = client.send(request1, HttpResponse.BodyHandlers.ofString());
        assertEquals(200, responseDup.statusCode());
        assertTrue(responseDup.body().contains("\"archivesFound\":1"));
        assertTrue(responseDup.body().contains("Idempotent"));

        // Discover second archive
        String event2 = "{\"eventId\":\"evt_002\",\"sessionId\":\"sess_123\",\"eventType\":\"ARCHIVE_DISCOVERED\",\"targetId\":\"archive_02\"}";
        HttpRequest request2 = HttpRequest.newBuilder()
                .uri(URI.create("http://localhost:" + TEST_PORT + "/api/v1/events"))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(event2))
                .build();

        HttpResponse<String> response2 = client.send(request2, HttpResponse.BodyHandlers.ofString());
        assertEquals(200, response2.statusCode());
        assertTrue(response2.body().contains("\"archivesFound\":2"));
    }

    @Test
    public void testChapterMissionStatus() throws Exception {
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("http://localhost:" + TEST_PORT + "/api/v1/missions/chapter-01"))
                .GET()
                .build();

        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        assertEquals(200, response.statusCode());
        assertTrue(response.body().contains("Curzon Hall Central Arcade"));
    }
}
