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

	// Configure authentic human attire & role appearance
	FString NameStr = NPCName.ToString();
	FString RoleStr = NPCRole.ToString();

	bool bFemaleChar = bIsFemale || NameStr.Contains(TEXT("Nusrat")) || NameStr.Contains(TEXT("Sadia")) ||
		NameStr.Contains(TEXT("Nabila")) || NameStr.Contains(TEXT("Ananya")) || NameStr.Contains(TEXT("Laboni")) ||
		NameStr.Contains(TEXT("Farhana")) || NameStr.Contains(TEXT("Rina")) || NameStr.Contains(TEXT("Sumi")) ||
		NameStr.Contains(TEXT("Mitu")) || NameStr.Contains(TEXT("Moushumi")) || NameStr.Contains(TEXT("Tania")) ||
		NameStr.Contains(TEXT("Rehana")) || NameStr.Contains(TEXT("Bristi")) || NameStr.Contains(TEXT("Proma")) ||
		NameStr.Contains(TEXT("Rupa")) || RoleStr.Contains(TEXT("Female Faculty"));

	if (bFemaleChar)
	{
		bIsFemale = true;
		if (USkeletalMesh* QuinnMesh = Cast<USkeletalMesh>(StaticLoadObject(USkeletalMesh::StaticClass(), nullptr, TEXT("/Game/Characters/Mannequins/Meshes/SKM_Quinn_Simple.SKM_Quinn_Simple"))))
		{
			GetMesh()->SetSkeletalMesh(QuinnMesh);
			GetMesh()->SetRelativeLocation(FVector(0.0f, 0.0f, -90.0f));
			GetMesh()->SetRelativeRotation(FRotator(0.0f, -90.0f, 0.0f));
		}

		UMaterialInterface* FemaleOutfitMat = nullptr;
		if (RoleStr.Contains(TEXT("Professor")) || RoleStr.Contains(TEXT("Faculty")) || RoleStr.Contains(TEXT("Teacher")))
		{
			// Formal Handloom Saree for Female Faculty
			FemaleOutfitMat = Cast<UMaterialInterface>(StaticLoadObject(UMaterialInterface::StaticClass(), nullptr, TEXT("/Game/SparkVision/Materials/MI_Teacher_SareeFormal.MI_Teacher_SareeFormal")));
		}
		else if (OutfitStyle == 1 || NameStr.Contains(TEXT("Sadia")) || NameStr.Contains(TEXT("Tania")) || NameStr.Contains(TEXT("Proma")))
		{
			// Mustard Yellow Contemporary Kurti
			FemaleOutfitMat = Cast<UMaterialInterface>(StaticLoadObject(UMaterialInterface::StaticClass(), nullptr, TEXT("/Game/SparkVision/Materials/MI_Student_Kurti_Mustard.MI_Student_Kurti_Mustard")));
		}
		else if (OutfitStyle == 2 || NameStr.Contains(TEXT("Farhana")) || NameStr.Contains(TEXT("Rehana")) || NameStr.Contains(TEXT("Rupa")))
		{
			// Rose-Tan Modest Hijab Ensemble
			FemaleOutfitMat = Cast<UMaterialInterface>(StaticLoadObject(UMaterialInterface::StaticClass(), nullptr, TEXT("/Game/SparkVision/Materials/MI_Student_Hijab_Rose.MI_Student_Hijab_Rose")));
		}
		else
		{
			// Pastel Floral Salwar Kameez
			FemaleOutfitMat = Cast<UMaterialInterface>(StaticLoadObject(UMaterialInterface::StaticClass(), nullptr, TEXT("/Game/SparkVision/Materials/MI_Student_SalwarKameez_Pastel.MI_Student_SalwarKameez_Pastel")));
		}

		if (FemaleOutfitMat)
		{
			GetMesh()->SetMaterial(0, FemaleOutfitMat);
			GetMesh()->SetMaterial(1, FemaleOutfitMat);
		}
	}
	else
	{
		if (USkeletalMesh* MannyMesh = Cast<USkeletalMesh>(StaticLoadObject(USkeletalMesh::StaticClass(), nullptr, TEXT("/Game/Characters/Mannequins/Meshes/SKM_Manny_Simple.SKM_Manny_Simple"))))
		{
			GetMesh()->SetSkeletalMesh(MannyMesh);
			GetMesh()->SetRelativeLocation(FVector(0.0f, 0.0f, -90.0f));
			GetMesh()->SetRelativeRotation(FRotator(0.0f, -90.0f, 0.0f));
		}

		UMaterialInterface* TorsoMat = nullptr;
		UMaterialInterface* LegsMat = Cast<UMaterialInterface>(StaticLoadObject(UMaterialInterface::StaticClass(), nullptr, TEXT("/Game/SparkVision/Materials/MI_Student_DenimLegs.MI_Student_DenimLegs")));

		if (RoleStr.Contains(TEXT("Professor")) || RoleStr.Contains(TEXT("Teacher")) || NameStr.Contains(TEXT("Prof")))
		{
			// Senior Faculty / Professor Safari Khaki Shirt & Tailored Charcoal Trousers
			TorsoMat = Cast<UMaterialInterface>(StaticLoadObject(UMaterialInterface::StaticClass(), nullptr, TEXT("/Game/SparkVision/Materials/MI_Teacher_FormalSafari.MI_Teacher_FormalSafari")));
			LegsMat = Cast<UMaterialInterface>(StaticLoadObject(UMaterialInterface::StaticClass(), nullptr, TEXT("/Game/SparkVision/Materials/MI_Teacher_DarkTrousers.MI_Teacher_DarkTrousers")));
		}
		else if (RoleStr.Contains(TEXT("Security")) || RoleStr.Contains(TEXT("Proctorial")) || NameStr.Contains(TEXT("Security")))
		{
			// University Proctorial Guard Khaki Safari Uniform & Khaki Trousers
			TorsoMat = Cast<UMaterialInterface>(StaticLoadObject(UMaterialInterface::StaticClass(), nullptr, TEXT("/Game/SparkVision/Materials/MI_Security_ProctorialKhaki.MI_Security_ProctorialKhaki")));
			LegsMat = Cast<UMaterialInterface>(StaticLoadObject(UMaterialInterface::StaticClass(), nullptr, TEXT("/Game/Characters/Mannequins/Materials/Manny/MI_Student_KhakiLegs.MI_Student_KhakiLegs")));
		}
		else if (RoleStr.Contains(TEXT("Staff")) || RoleStr.Contains(TEXT("Technician")) || RoleStr.Contains(TEXT("Demonstrator")))
		{
			// Campus Staff / Lab Demonstrator Slate-Blue Work Shirt & Khaki Pants
			TorsoMat = Cast<UMaterialInterface>(StaticLoadObject(UMaterialInterface::StaticClass(), nullptr, TEXT("/Game/SparkVision/Materials/MI_Staff_LabBlue.MI_Staff_LabBlue")));
			LegsMat = Cast<UMaterialInterface>(StaticLoadObject(UMaterialInterface::StaticClass(), nullptr, TEXT("/Game/Characters/Mannequins/Materials/Manny/MI_Student_KhakiLegs.MI_Student_KhakiLegs")));
		}
		else if (RoleStr.Contains(TEXT("Maintenance")) || RoleStr.Contains(TEXT("Grounds")))
		{
			// Campus Grounds & Maintenance Olive Twill Workwear
			TorsoMat = Cast<UMaterialInterface>(StaticLoadObject(UMaterialInterface::StaticClass(), nullptr, TEXT("/Game/SparkVision/Materials/MI_Staff_GroundsOlive.MI_Staff_GroundsOlive")));
			LegsMat = Cast<UMaterialInterface>(StaticLoadObject(UMaterialInterface::StaticClass(), nullptr, TEXT("/Game/SparkVision/Materials/MI_Staff_GroundsOlive.MI_Staff_GroundsOlive")));
		}
		else if (OutfitStyle == 0 || NameStr.Contains(TEXT("Tanvir")) || NameStr.Contains(TEXT("Farhan")) || NameStr.Contains(TEXT("Alok")) || NameStr.Contains(TEXT("Arif")))
		{
			// Traditional Handspun White Cotton Panjabi + Pajama/Denim
			TorsoMat = Cast<UMaterialInterface>(StaticLoadObject(UMaterialInterface::StaticClass(), nullptr, TEXT("/Game/SparkVision/Materials/MI_Student_Panjabi_White.MI_Student_Panjabi_White")));
		}
		else if (OutfitStyle == 2 || NameStr.Contains(TEXT("Sabbir")) || NameStr.Contains(TEXT("Ashik")) || NameStr.Contains(TEXT("Kabir")) || NameStr.Contains(TEXT("Sajid")))
		{
			// Collegiate Navy Oxford Shirt & Khaki Chinos
			TorsoMat = Cast<UMaterialInterface>(StaticLoadObject(UMaterialInterface::StaticClass(), nullptr, TEXT("/Game/Characters/Mannequins/Materials/Manny/MI_Student_NavyTorso.MI_Student_NavyTorso")));
			LegsMat = Cast<UMaterialInterface>(StaticLoadObject(UMaterialInterface::StaticClass(), nullptr, TEXT("/Game/Characters/Mannequins/Materials/Manny/MI_Student_KhakiLegs.MI_Student_KhakiLegs")));
		}
		else if (OutfitStyle == 3 || NameStr.Contains(TEXT("Anik")) || NameStr.Contains(TEXT("Zahid")) || NameStr.Contains(TEXT("Palash")))
		{
			// Casual Charcoal Tee & Indigo Denim
			TorsoMat = Cast<UMaterialInterface>(StaticLoadObject(UMaterialInterface::StaticClass(), nullptr, TEXT("/Game/SparkVision/Materials/MI_Student_CharcoalTorso.MI_Student_CharcoalTorso")));
		}
		else
		{
			// Dhaka University Maroon Shirt & Indigo Denim
			TorsoMat = Cast<UMaterialInterface>(StaticLoadObject(UMaterialInterface::StaticClass(), nullptr, TEXT("/Game/SparkVision/Materials/MI_Student_MaroonTorso.MI_Student_MaroonTorso")));
		}

		if (LegsMat) GetMesh()->SetMaterial(0, LegsMat);
		if (TorsoMat) GetMesh()->SetMaterial(1, TorsoMat);
	}
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
