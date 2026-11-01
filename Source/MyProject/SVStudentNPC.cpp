// Copyright SparkVision Dhaka University. All Rights Reserved.

#include "SVStudentNPC.h"
#include "Components/CapsuleComponent.h"
#include "Components/SkeletalMeshComponent.h"
#include "UObject/ConstructorHelpers.h"
#include "Kismet/GameplayStatics.h"
#include "SVHUD.h"
#include "SVCharacter.h"

ASVStudentNPC::ASVStudentNPC()
{
	PrimaryActorTick.bCanEverTick = false;

	GetCapsuleComponent()->InitCapsuleSize(42.0f, 96.0f);
	GetCapsuleComponent()->SetCollisionProfileName(TEXT("Pawn"));

	// Load Manny skeletal mesh and unarmed animation blueprint
	static ConstructorHelpers::FObjectFinder<USkeletalMesh> MeshAsset(TEXT("/Game/Characters/Mannequins/Meshes/SKM_Manny_Simple.SKM_Manny_Simple"));
	if (MeshAsset.Succeeded())
	{
		GetMesh()->SetSkeletalMesh(MeshAsset.Object);
		GetMesh()->SetRelativeLocation(FVector(0.0f, 0.0f, -90.0f));
		GetMesh()->SetRelativeRotation(FRotator(0.0f, -90.0f, 0.0f));
	}

	static ConstructorHelpers::FClassFinder<UAnimInstance> AnimBpClass(TEXT("/Game/Characters/Mannequins/Anims/Unarmed/ABP_Unarmed.ABP_Unarmed_C"));
	if (AnimBpClass.Succeeded())
	{
		GetMesh()->SetAnimInstanceClass(AnimBpClass.Class);
	}

	// Default sample dialogue (can be customized per actor in level)
	FSVDialogueEntry Entry1;
	Entry1.BengaliText = FText::FromString(TEXT("কার্জন হলের প্রাঙ্গণে স্বাগতম। ২০২৪ সালের জুলাইয়ের এই দিনগুলোতে আমাদের শান্তিপূর্ণ আন্দোলন শুরু হয়েছে।"));
	Entry1.EnglishSubtitle = FText::FromString(TEXT("Welcome to the Curzon Hall quadrangle. In these early days of July 2024, our peaceful assembly has begun across the campus."));
	DialogueEntries.Add(Entry1);

	FSVDialogueEntry Entry2;
	Entry2.BengaliText = FText::FromString(TEXT("ইতিহাসের দলিলগুলো সংরক্ষণ করো—আমাদের পাঁচটি ঐতিহাসিক টার্মিনাল ঘুরে দেখো।"));
	Entry2.EnglishSubtitle = FText::FromString(TEXT("Document the history of our university—examine the five historical archive records across campus landmarks."));
	DialogueEntries.Add(Entry2);

	FSVDialogueEntry Entry3;
	Entry3.BengaliText = FText::FromString(TEXT("টিএসসি আর শহীদ মিনারে আমাদের সহযোদ্ধারা আছে। সাবধানে ক্যাম্পাসে চলাচল করো।"));
	Entry3.EnglishSubtitle = FText::FromString(TEXT("Our comrades are gathering at TSC and Shaheed Minar. Move carefully across the university avenues."));
	DialogueEntries.Add(Entry3);
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
	if (DialogueEntries.Num() == 0) return;

	FSVDialogueEntry CurrentEntry = DialogueEntries[CurrentDialogueIndex];
	UE_LOG(LogTemp, Log, TEXT("[SVStudentNPC] %s: %s"), *NPCName.ToString(), *CurrentEntry.EnglishSubtitle.ToString());

	// If player is interactor, notify player and HUD
	if (ASVCharacter* PlayerChar = Cast<ASVCharacter>(Interactor))
	{
		PlayerChar->OnNPCSpoken(NPCId);

		if (APlayerController* PC = Cast<APlayerController>(PlayerChar->GetController()))
		{
			if (ASVHUD* HUD = Cast<ASVHUD>(PC->GetHUD()))
			{
				HUD->DisplayNPCDialogue(NPCName, NPCRole, CurrentEntry.BengaliText, CurrentEntry.EnglishSubtitle);
			}
		}
	}

	// Advance dialogue index for subsequent conversations
	CurrentDialogueIndex = (CurrentDialogueIndex + 1) % DialogueEntries.Num();
}

bool ASVStudentNPC::GetCurrentDialogue(FText& OutBengali, FText& OutEnglish) const
{
	if (DialogueEntries.IsValidIndex(CurrentDialogueIndex))
	{
		OutBengali = DialogueEntries[CurrentDialogueIndex].BengaliText;
		OutEnglish = DialogueEntries[CurrentDialogueIndex].EnglishSubtitle;
		return true;
	}
	return false;
}
