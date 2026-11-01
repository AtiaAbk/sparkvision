// Copyright SparkVision Dhaka University. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/SaveGame.h"
#include "SVSaveGame.generated.h"

/**
 * Native SaveGame object for persistent gameplay state across Level 1 & 2.
 */
UCLASS()
class MYPROJECT_API USVSaveGame : public USaveGame
{
	GENERATED_BODY()

public:
	USVSaveGame();

	UPROPERTY(VisibleAnywhere, Category = "SparkVision|SaveData")
	FString SaveSlotName;

	UPROPERTY(VisibleAnywhere, Category = "SparkVision|SaveData")
	uint32 UserIndex;

	UPROPERTY(VisibleAnywhere, Category = "SparkVision|SaveData")
	FDateTime Timestamp;

	UPROPERTY(VisibleAnywhere, Category = "SparkVision|SaveData")
	FVector PlayerLocation;

	UPROPERTY(VisibleAnywhere, Category = "SparkVision|SaveData")
	FRotator PlayerRotation;

	UPROPERTY(VisibleAnywhere, Category = "SparkVision|SaveData")
	FString CurrentChapter;

	UPROPERTY(VisibleAnywhere, Category = "SparkVision|SaveData")
	FString ActiveMissionId;

	UPROPERTY(VisibleAnywhere, Category = "SparkVision|SaveData")
	TArray<FString> DiscoveredArchives;

	UPROPERTY(VisibleAnywhere, Category = "SparkVision|SaveData")
	TArray<FString> SpokenNPCs;

	UPROPERTY(VisibleAnywhere, Category = "SparkVision|SaveData")
	TArray<FString> VisitedLandmarks;

	UPROPERTY(VisibleAnywhere, Category = "SparkVision|SaveData")
	bool bLevel1Completed;

	UPROPERTY(VisibleAnywhere, Category = "SparkVision|SaveData")
	bool bLevel2Unlocked;

	UPROPERTY(VisibleAnywhere, Category = "SparkVision|SaveData")
	float MasterVolume;

	UPROPERTY(VisibleAnywhere, Category = "SparkVision|SaveData")
	int32 ScalabilityQualityLevel;
};
