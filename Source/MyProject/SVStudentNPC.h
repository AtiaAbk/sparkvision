// Copyright SparkVision Dhaka University. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "SVInteractableInterface.h"
#include "SVStudentNPC.generated.h"

UCLASS()
class MYPROJECT_API ASVStudentNPC : public ACharacter, public ISVInteractableInterface
{
	GENERATED_BODY()

public:
	ASVStudentNPC();

protected:
	virtual void BeginPlay() override;

public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SparkVision|NPC")
	FText NPCName = FText::FromString(TEXT("Tanvir (Student Organizer)"));

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SparkVision|NPC")
	TArray<FText> DialogueLines;

	UPROPERTY(BlueprintReadOnly, Category = "SparkVision|NPC")
	int32 CurrentDialogueIndex = 0;

	virtual FText GetInteractionPrompt_Implementation() override;
	virtual void OnInteract_Implementation(AActor* Interactor) override;
};
