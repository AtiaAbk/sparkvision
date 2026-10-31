// Copyright SparkVision Dhaka University. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "Interfaces/IHttpRequest.h"
#include "Interfaces/IHttpResponse.h"
#include "SVMissionControlSubsystem.generated.h"

DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnConnectionStatusChanged, bool, bConnected, const FString&, Message);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_ThreeParams(FOnArchiveDiscoveredUpdated, const FString&, ArchiveId, int32, ArchivesFound, int32, TotalArchives);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnLevel2Unlocked, bool, bUnlocked);

UCLASS(BlueprintType)
class MYPROJECT_API USVMissionControlSubsystem : public UGameInstanceSubsystem
{
	GENERATED_BODY()

public:
	virtual void Initialize(FSubsystemCollectionBase& Collection) override;
	virtual void Deinitialize() override;

	/** Configuration */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SparkVision|MissionControl")
	FString BaseUrl = TEXT("http://127.0.0.1:8080");

	UPROPERTY(BlueprintReadOnly, Category = "SparkVision|MissionControl")
	FString CurrentSessionId;

	UPROPERTY(BlueprintReadOnly, Category = "SparkVision|MissionControl")
	bool bIsConnected = false;

	UPROPERTY(BlueprintReadOnly, Category = "SparkVision|MissionControl")
	int32 CurrentArchivesFound = 0;

	UPROPERTY(BlueprintReadOnly, Category = "SparkVision|MissionControl")
	int32 TotalArchivesRequired = 5;

	UPROPERTY(BlueprintReadOnly, Category = "SparkVision|MissionControl")
	bool bIsLevel2Unlocked = false;

	/** Delegates for UI & Blueprints */
	UPROPERTY(BlueprintAssignable, Category = "SparkVision|MissionControl")
	FOnConnectionStatusChanged OnConnectionStatusChanged;

	UPROPERTY(BlueprintAssignable, Category = "SparkVision|MissionControl")
	FOnArchiveDiscoveredUpdated OnArchiveDiscoveredUpdated;

	UPROPERTY(BlueprintAssignable, Category = "SparkVision|MissionControl")
	FOnLevel2Unlocked OnLevel2Unlocked;

	/** Async HTTP Operations */
	UFUNCTION(BlueprintCallable, Category = "SparkVision|MissionControl")
	void CheckHealth();

	UFUNCTION(BlueprintCallable, Category = "SparkVision|MissionControl")
	void StartSession(const FString& InSessionId, const FString& ChapterId = TEXT("chapter-01"));

	UFUNCTION(BlueprintCallable, Category = "SparkVision|MissionControl")
	void FetchChapterMissions();

	UFUNCTION(BlueprintCallable, Category = "SparkVision|MissionControl")
	void ReportArchiveDiscovered(const FString& ArchiveId);

	UFUNCTION(BlueprintCallable, Category = "SparkVision|MissionControl")
	void ReportLevel1Victory();

private:
	void OnHealthResponseReceived(FHttpRequestPtr Request, FHttpResponsePtr Response, bool bConnectedSuccessfully);
	void OnStartSessionResponseReceived(FHttpRequestPtr Request, FHttpResponsePtr Response, bool bConnectedSuccessfully);
	void OnFetchChapterResponseReceived(FHttpRequestPtr Request, FHttpResponsePtr Response, bool bConnectedSuccessfully);
	void OnEventReportResponseReceived(FHttpRequestPtr Request, FHttpResponsePtr Response, bool bConnectedSuccessfully);

	TSet<FString> SentEventIds;
};
