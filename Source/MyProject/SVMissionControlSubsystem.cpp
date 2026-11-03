// Copyright SparkVision Dhaka University. All Rights Reserved.

#include "SVMissionControlSubsystem.h"
#include "HttpModule.h"
#include "JsonObjectConverter.h"
#include "Serialization/JsonSerializer.h"
#include "Misc/Guid.h"

void USVMissionControlSubsystem::Initialize(FSubsystemCollectionBase& Collection)
{
	Super::Initialize(Collection);
	UE_LOG(LogTemp, Log, TEXT("[SVMissionControlSubsystem] Initialized. Mission Control BaseUrl: %s"), *BaseUrl);
	CurrentSessionId = FString::Printf(TEXT("unreal_session_%lld"), FDateTime::UtcNow().ToUnixTimestamp());
	
	// Automatically perform initial health check
	CheckHealth();
}

void USVMissionControlSubsystem::Deinitialize()
{
	Super::Deinitialize();
	UE_LOG(LogTemp, Log, TEXT("[SVMissionControlSubsystem] Deinitialized."));
}

void USVMissionControlSubsystem::CheckHealth()
{
	FHttpModule* Http = &FHttpModule::Get();
	if (!Http) return;

	TSharedRef<IHttpRequest, ESPMode::ThreadSafe> Request = Http->CreateRequest();
	Request->OnProcessRequestComplete().BindUObject(this, &USVMissionControlSubsystem::OnHealthResponseReceived);
	Request->SetURL(FString::Printf(TEXT("%s/api/v1/health"), *BaseUrl));
	Request->SetVerb(TEXT("GET"));
	Request->SetHeader(TEXT("Content-Type"), TEXT("application/json"));
	Request->ProcessRequest();
}

void USVMissionControlSubsystem::OnHealthResponseReceived(FHttpRequestPtr Request, FHttpResponsePtr Response, bool bConnectedSuccessfully)
{
	if (bConnectedSuccessfully && Response.IsValid() && Response->GetResponseCode() == 200)
	{
		bIsConnected = true;
		FString RespStr = Response->GetContentAsString();
		UE_LOG(LogTemp, Log, TEXT("[SVMissionControlSubsystem] Health check succeeded: %s"), *RespStr);
		OnConnectionStatusChanged.Broadcast(true, TEXT("Connected to Java Mission Control"));

		// Follow up by starting session and fetching mission state
		StartSession(CurrentSessionId, TEXT("chapter-01"));
	}
	else
	{
		bIsConnected = false;
		FString ErrMsg = Response.IsValid() ? FString::Printf(TEXT("HTTP error %d"), Response->GetResponseCode()) : TEXT("Connection failed");
		UE_LOG(LogTemp, Warning, TEXT("[SVMissionControlSubsystem] Health check failed: %s"), *ErrMsg);
		OnConnectionStatusChanged.Broadcast(false, ErrMsg);
	}
}

void USVMissionControlSubsystem::StartSession(const FString& InSessionId, const FString& ChapterId)
{
	FHttpModule* Http = &FHttpModule::Get();
	if (!Http) return;

	TSharedRef<IHttpRequest, ESPMode::ThreadSafe> Request = Http->CreateRequest();
	Request->OnProcessRequestComplete().BindUObject(this, &USVMissionControlSubsystem::OnStartSessionResponseReceived);
	Request->SetURL(FString::Printf(TEXT("%s/api/v1/session/start"), *BaseUrl));
	Request->SetVerb(TEXT("POST"));
	Request->SetHeader(TEXT("Content-Type"), TEXT("application/json"));

	TSharedPtr<FJsonObject> JsonObj = MakeShareable(new FJsonObject());
	JsonObj->SetStringField(TEXT("sessionId"), InSessionId.IsEmpty() ? CurrentSessionId : InSessionId);
	JsonObj->SetStringField(TEXT("chapterId"), ChapterId);

	FString Body;
	TSharedRef<TJsonWriter<>> Writer = TJsonWriterFactory<>::Create(&Body);
	FJsonSerializer::Serialize(JsonObj.ToSharedRef(), Writer);

	Request->SetContentAsString(Body);
	Request->ProcessRequest();
}

void USVMissionControlSubsystem::OnStartSessionResponseReceived(FHttpRequestPtr Request, FHttpResponsePtr Response, bool bConnectedSuccessfully)
{
	if (bConnectedSuccessfully && Response.IsValid() && Response->GetResponseCode() == 200)
	{
		UE_LOG(LogTemp, Log, TEXT("[SVMissionControlSubsystem] Session registered: %s"), *Response->GetContentAsString());
		FetchChapterMissions();
	}
}

void USVMissionControlSubsystem::FetchChapterMissions()
{
	FHttpModule* Http = &FHttpModule::Get();
	if (!Http) return;

	TSharedRef<IHttpRequest, ESPMode::ThreadSafe> Request = Http->CreateRequest();
	Request->OnProcessRequestComplete().BindUObject(this, &USVMissionControlSubsystem::OnFetchChapterResponseReceived);
	Request->SetURL(FString::Printf(TEXT("%s/api/v1/missions/chapter-01"), *BaseUrl));
	Request->SetVerb(TEXT("GET"));
	Request->SetHeader(TEXT("Content-Type"), TEXT("application/json"));
	Request->ProcessRequest();
}

void USVMissionControlSubsystem::OnFetchChapterResponseReceived(FHttpRequestPtr Request, FHttpResponsePtr Response, bool bConnectedSuccessfully)
{
	if (bConnectedSuccessfully && Response.IsValid() && Response->GetResponseCode() == 200)
	{
		TSharedPtr<FJsonObject> JsonObj;
		TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(Response->GetContentAsString());
		if (FJsonSerializer::Deserialize(Reader, JsonObj) && JsonObj.IsValid())
		{
			CurrentArchivesFound = JsonObj->GetIntegerField(TEXT("archivesFound"));
			TotalArchivesRequired = JsonObj->GetIntegerField(TEXT("totalArchivesRequired"));
			bIsLevel2Unlocked = JsonObj->GetBoolField(TEXT("level2Unlocked"));

			UE_LOG(LogTemp, Log, TEXT("[SVMissionControlSubsystem] Missions updated: %d / %d archives, Level 2 Unlocked: %d"),
				CurrentArchivesFound, TotalArchivesRequired, bIsLevel2Unlocked);

			OnArchiveDiscoveredUpdated.Broadcast(TEXT("SYNC"), CurrentArchivesFound, TotalArchivesRequired);
			if (bIsLevel2Unlocked)
			{
				OnLevel2Unlocked.Broadcast(true);
			}
		}
	}
}

void USVMissionControlSubsystem::ReportArchiveDiscovered(const FString& ArchiveId)
{
	FString EventId = FString::Printf(TEXT("evt_archive_%s_%lld"), *ArchiveId, FDateTime::UtcNow().ToUnixTimestamp());
	if (SentEventIds.Contains(ArchiveId))
	{
		UE_LOG(LogTemp, Warning, TEXT("[SVMissionControlSubsystem] Archive %s already reported in this session"), *ArchiveId);
		return;
	}
	SentEventIds.Add(ArchiveId);

	FHttpModule* Http = &FHttpModule::Get();
	if (!Http) return;

	TSharedRef<IHttpRequest, ESPMode::ThreadSafe> Request = Http->CreateRequest();
	Request->OnProcessRequestComplete().BindUObject(this, &USVMissionControlSubsystem::OnEventReportResponseReceived);
	Request->SetURL(FString::Printf(TEXT("%s/api/v1/events"), *BaseUrl));
	Request->SetVerb(TEXT("POST"));
	Request->SetHeader(TEXT("Content-Type"), TEXT("application/json"));

	TSharedPtr<FJsonObject> JsonObj = MakeShareable(new FJsonObject());
	JsonObj->SetStringField(TEXT("eventId"), EventId);
	JsonObj->SetStringField(TEXT("sessionId"), CurrentSessionId);
	JsonObj->SetStringField(TEXT("eventType"), TEXT("ARCHIVE_DISCOVERED"));
	JsonObj->SetStringField(TEXT("targetId"), ArchiveId);
	JsonObj->SetStringField(TEXT("timestamp"), FDateTime::UtcNow().ToIso8601());

	FString Body;
	TSharedRef<TJsonWriter<>> Writer = TJsonWriterFactory<>::Create(&Body);
	FJsonSerializer::Serialize(JsonObj.ToSharedRef(), Writer);

	Request->SetContentAsString(Body);
	Request->ProcessRequest();
}

void USVMissionControlSubsystem::ReportLevel1Victory()
{
	FString EventId = FString::Printf(TEXT("evt_vic_%lld"), FDateTime::UtcNow().ToUnixTimestamp());

	FHttpModule* Http = &FHttpModule::Get();
	if (!Http) return;

	TSharedRef<IHttpRequest, ESPMode::ThreadSafe> Request = Http->CreateRequest();
	Request->OnProcessRequestComplete().BindUObject(this, &USVMissionControlSubsystem::OnEventReportResponseReceived);
	Request->SetURL(FString::Printf(TEXT("%s/api/v1/events"), *BaseUrl));
	Request->SetVerb(TEXT("POST"));
	Request->SetHeader(TEXT("Content-Type"), TEXT("application/json"));

	TSharedPtr<FJsonObject> JsonObj = MakeShareable(new FJsonObject());
	JsonObj->SetStringField(TEXT("eventId"), EventId);
	JsonObj->SetStringField(TEXT("sessionId"), CurrentSessionId);
	JsonObj->SetStringField(TEXT("eventType"), TEXT("LEVEL1_COMPLETED"));
	JsonObj->SetStringField(TEXT("targetId"), TEXT("chapter-01"));
	JsonObj->SetStringField(TEXT("timestamp"), FDateTime::UtcNow().ToIso8601());

	FString Body;
	TSharedRef<TJsonWriter<>> Writer = TJsonWriterFactory<>::Create(&Body);
	FJsonSerializer::Serialize(JsonObj.ToSharedRef(), Writer);

	Request->SetContentAsString(Body);
	Request->ProcessRequest();
}

void USVMissionControlSubsystem::OnEventReportResponseReceived(FHttpRequestPtr Request, FHttpResponsePtr Response, bool bConnectedSuccessfully)
{
	if (bConnectedSuccessfully && Response.IsValid() && Response->GetResponseCode() == 200)
	{
		TSharedPtr<FJsonObject> JsonObj;
		TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(Response->GetContentAsString());
		if (FJsonSerializer::Deserialize(Reader, JsonObj) && JsonObj.IsValid())
		{
			CurrentArchivesFound = JsonObj->GetIntegerField(TEXT("archivesFound"));
			TotalArchivesRequired = JsonObj->GetIntegerField(TEXT("totalArchives"));
			bIsLevel2Unlocked = JsonObj->GetBoolField(TEXT("level2Unlocked"));

			UE_LOG(LogTemp, Log, TEXT("[SVMissionControlSubsystem] Event Response: Found %d/%d archives, Level 2 Unlocked: %d"),
				CurrentArchivesFound, TotalArchivesRequired, bIsLevel2Unlocked);

			OnArchiveDiscoveredUpdated.Broadcast(TEXT("EVENT"), CurrentArchivesFound, TotalArchivesRequired);
			if (bIsLevel2Unlocked)
			{
				OnLevel2Unlocked.Broadcast(true);
			}
		}
	}
	else
	{
		UE_LOG(LogTemp, Error, TEXT("[SVMissionControlSubsystem] Failed to deliver event to Mission Control"));
	}
}

void USVMissionControlSubsystem::ReportCrime(const FString& VictimId)
{
	FHttpModule* Http = &FHttpModule::Get();
	if (!Http) return;

	TSharedRef<IHttpRequest, ESPMode::ThreadSafe> Request = Http->CreateRequest();
	Request->SetURL(FString::Printf(TEXT("%s/api/v1/events/crime"), *BaseUrl));
	Request->SetVerb(TEXT("POST"));
	Request->SetHeader(TEXT("Content-Type"), TEXT("application/json"));

	TSharedPtr<FJsonObject> JsonObj = MakeShareable(new FJsonObject());
	JsonObj->SetStringField(TEXT("sessionId"), CurrentSessionId);
	JsonObj->SetStringField(TEXT("victimId"), VictimId);
	JsonObj->SetStringField(TEXT("crimeType"), TEXT("ASSAULT_ON_STUDENT"));

	FString Body;
	TSharedRef<TJsonWriter<>> Writer = TJsonWriterFactory<>::Create(&Body);
	FJsonSerializer::Serialize(JsonObj.ToSharedRef(), Writer);

	Request->SetContentAsString(Body);
	Request->ProcessRequest();
	UE_LOG(LogTemp, Warning, TEXT("[SVMissionControlSubsystem] Reported Crime to Java Mission Control: %s"), *VictimId);
}

void USVMissionControlSubsystem::ReportCombatRetry()
{
	FHttpModule* Http = &FHttpModule::Get();
	if (!Http) return;

	TSharedRef<IHttpRequest, ESPMode::ThreadSafe> Request = Http->CreateRequest();
	Request->SetURL(FString::Printf(TEXT("%s/api/v1/events/combat/retry"), *BaseUrl));
	Request->SetVerb(TEXT("POST"));
	Request->SetHeader(TEXT("Content-Type"), TEXT("application/json"));

	TSharedPtr<FJsonObject> JsonObj = MakeShareable(new FJsonObject());
	JsonObj->SetStringField(TEXT("sessionId"), CurrentSessionId);
	JsonObj->SetStringField(TEXT("defeatReason"), TEXT("KNOCKED_DOWN_BY_LATHI_SQUAD"));

	FString Body;
	TSharedRef<TJsonWriter<>> Writer = TJsonWriterFactory<>::Create(&Body);
	FJsonSerializer::Serialize(JsonObj.ToSharedRef(), Writer);

	Request->SetContentAsString(Body);
	Request->ProcessRequest();
	UE_LOG(LogTemp, Log, TEXT("[SVMissionControlSubsystem] Reported Combat Retry to Java Mission Control"));
}

void USVMissionControlSubsystem::ReportWaypointVisited(const FString& WaypointId)
{
	FHttpModule* Http = &FHttpModule::Get();
	if (!Http) return;

	TSharedRef<IHttpRequest, ESPMode::ThreadSafe> Request = Http->CreateRequest();
	Request->SetURL(FString::Printf(TEXT("%s/api/v1/mission/waypoints"), *BaseUrl));
	Request->SetVerb(TEXT("POST"));
	Request->SetHeader(TEXT("Content-Type"), TEXT("application/json"));

	TSharedPtr<FJsonObject> JsonObj = MakeShareable(new FJsonObject());
	JsonObj->SetStringField(TEXT("sessionId"), CurrentSessionId);
	JsonObj->SetStringField(TEXT("waypointId"), WaypointId);

	FString Body;
	TSharedRef<TJsonWriter<>> Writer = TJsonWriterFactory<>::Create(&Body);
	FJsonSerializer::Serialize(JsonObj.ToSharedRef(), Writer);

	Request->SetContentAsString(Body);
	Request->ProcessRequest();
	UE_LOG(LogTemp, Log, TEXT("[SVMissionControlSubsystem] Reported Waypoint Visited: %s"), *WaypointId);
}
