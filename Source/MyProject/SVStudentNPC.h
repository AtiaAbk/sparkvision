// Copyright SparkVision Dhaka University. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "SVInteractableInterface.h"
#include "SVStudentNPC.generated.h"

USTRUCT(BlueprintType)
struct FSVDialogueEntry
{
	GENERATED_BODY()

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SparkVision|Dialogue")
	FText BengaliText;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SparkVision|Dialogue")
	FText EnglishSubtitle;
};

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
	FString NPCId = TEXT("NPC_Tanvir");

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SparkVision|NPC")
	bool bIsFemale = false;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SparkVision|NPC")
	int32 OutfitStyle = 0;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SparkVision|NPC")
	FText NPCName = FText::FromString(TEXT("Tanvir (Student Organizer)"));

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SparkVision|NPC")
	FText NPCRole = FText::FromString(TEXT("Curzon Science Faculty Representative"));

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SparkVision|NPC")
	TArray<FSVDialogueEntry> DialogueEntries;

	UPROPERTY(BlueprintReadOnly, Category = "SparkVision|NPC")
	int32 CurrentDialogueIndex = 0;

	virtual FText GetInteractionPrompt_Implementation() override;
	virtual void OnInteract_Implementation(AActor* Interactor) override;

	UFUNCTION(BlueprintCallable, Category = "SparkVision|NPC")
	bool GetCurrentDialogue(FText& OutBengali, FText& OutEnglish) const;
};
