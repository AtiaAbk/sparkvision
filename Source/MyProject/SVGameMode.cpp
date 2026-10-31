// Copyright SparkVision Dhaka University. All Rights Reserved.

#include "SVGameMode.h"
#include "Kismet/GameplayStatics.h"
#include "SVMissionControlSubsystem.h"
#include "SVCharacter.h"

ASVGameMode::ASVGameMode()
{
	DefaultPawnClass = ASVCharacter::StaticClass();
}

void ASVGameMode::BeginPlay()
{
	Super::BeginPlay();
	UE_LOG(LogTemp, Log, TEXT("[SVGameMode] Level 1: Where It All Began initialized."));
}

void ASVGameMode::OnArchiveFound(const FString& ArchiveId)
{
	CurrentArchivesDiscovered++;
	UE_LOG(LogTemp, Log, TEXT("[SVGameMode] Archive registered: %s. Total: %d / %d"), *ArchiveId, CurrentArchivesDiscovered, RequiredArchives);

	if (CurrentArchivesDiscovered >= RequiredArchives && !bEncounterActive && !bLevel1Completed)
	{
		TriggerEncounter();
	}
}

void ASVGameMode::TriggerEncounter()
{
	bEncounterActive = true;
	UE_LOG(LogTemp, Warning, TEXT("[SVGameMode] All 5 archives found! Final confrontation initiated near Curzon perimeter."));
}

void ASVGameMode::OnEncounterCleared()
{
	bEncounterActive = false;
	bLevel1Completed = true;
	UE_LOG(LogTemp, Log, TEXT("[SVGameMode] Final confrontation cleared! Level 1 victory achieved!"));

	if (UGameInstance* GI = GetGameInstance())
	{
		if (USVMissionControlSubsystem* MCSubsystem = GI->GetSubsystem<USVMissionControlSubsystem>())
		{
			MCSubsystem->ReportLevel1Victory();
		}
	}
}

void ASVGameMode::RestartLevel1()
{
	UGameplayStatics::OpenLevel(this, FName(*UGameplayStatics::GetCurrentLevelName(this)));
}
