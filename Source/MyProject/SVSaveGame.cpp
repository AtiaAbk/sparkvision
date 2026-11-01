// Copyright SparkVision Dhaka University. All Rights Reserved.

#include "SVSaveGame.h"

USVSaveGame::USVSaveGame()
{
	SaveSlotName = TEXT("SVSave_Slot0");
	UserIndex = 0;
	Timestamp = FDateTime::Now();

	PlayerLocation = FVector(-3500.0f, 0.0f, 105.65f); // Curzon Promenade
	PlayerRotation = FRotator(0.0f, 0.0f, 0.0f);

	CurrentChapter = TEXT("chapter-01");
	ActiveMissionId = TEXT("L1_M01");

	bLevel1Completed = false;
	bLevel2Unlocked = false;

	MasterVolume = 1.0f;
	ScalabilityQualityLevel = 2; // Medium/High default
}
