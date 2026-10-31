// Copyright SparkVision Dhaka University. All Rights Reserved.

#include "SVStudentNPC.h"

ASVStudentNPC::ASVStudentNPC()
{
	PrimaryActorTick.bCanEverTick = false;

	DialogueLines.Add(FText::FromString(TEXT("Welcome to Dhaka University campus. The year is July 2024. Our peaceful quota reform gatherings have begun across Curzon Hall and the Central Library.")));
	DialogueLines.Add(FText::FromString(TEXT("Inspect the five historical archives scattered around the campus landmarks to document the movement's peaceful origins.")));
	DialogueLines.Add(FText::FromString(TEXT("Be careful near the southern boundary—tensions are escalating and aggressive factions have been reported.")));
}

void ASVStudentNPC::BeginPlay()
{
	Super::BeginPlay();
}

FText ASVStudentNPC::GetInteractionPrompt_Implementation()
{
	return FText::Format(FText::FromString(TEXT("Press [E] to Speak with {0}")), NPCName);
}

void ASVStudentNPC::OnInteract_Implementation(AActor* Interactor)
{
	if (DialogueLines.Num() > 0)
	{
		FText CurrentText = DialogueLines[CurrentDialogueIndex];
		UE_LOG(LogTemp, Log, TEXT("[SVStudentNPC] %s: %s"), *NPCName.ToString(), *CurrentText.ToString());
		CurrentDialogueIndex = (CurrentDialogueIndex + 1) % DialogueLines.Num();
	}
}
