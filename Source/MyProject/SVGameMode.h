// Copyright SparkVision Dhaka University. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/GameModeBase.h"
#include "SVGameMode.generated.h"

class ASVHostileOpponent;

UCLASS()
class MYPROJECT_API ASVGameMode : public AGameModeBase
{
	GENERATED_BODY()

public:
	ASVGameMode();

	virtual void BeginPlay() override;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SparkVision|Level1")
	int32 RequiredArchives = 5;

	UPROPERTY(BlueprintReadOnly, Category = "SparkVision|Level1")
	int32 CurrentArchivesDiscovered = 0;

	UPROPERTY(BlueprintReadOnly, Category = "SparkVision|Level1")
	bool bEncounterActive = false;

	UPROPERTY(BlueprintReadOnly, Category = "SparkVision|Level1")
	bool bLevel1Completed = false;

	UFUNCTION(BlueprintCallable, Category = "SparkVision|Level1")
	void OnArchiveFound(const FString& ArchiveId);

	UFUNCTION(BlueprintCallable, Category = "SparkVision|Level1")
	void OnEncounterCleared();

	UFUNCTION(BlueprintCallable, Category = "SparkVision|Level1")
	void TriggerEncounter();

	UFUNCTION(BlueprintCallable, Category = "SparkVision|Level1")
	void RestartLevel1();
};
