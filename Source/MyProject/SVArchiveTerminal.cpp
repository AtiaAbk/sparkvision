// Copyright SparkVision Dhaka University. All Rights Reserved.

#include "SVArchiveTerminal.h"
#include "Components/StaticMeshComponent.h"
#include "Components/SphereComponent.h"
#include "Kismet/GameplayStatics.h"
#include "SVMissionControlSubsystem.h"

ASVArchiveTerminal::ASVArchiveTerminal()
{
	PrimaryActorTick.bCanEverTick = false;

	BaseMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("BaseMesh"));
	RootComponent = BaseMesh;

	InteractionSphere = CreateDefaultSubobject<USphereComponent>(TEXT("InteractionSphere"));
	InteractionSphere->SetupAttachment(RootComponent);
	InteractionSphere->SetSphereRadius(250.0f);
	InteractionSphere->SetCollisionResponseToAllChannels(ECR_Ignore);
	InteractionSphere->SetCollisionResponseToChannel(ECC_Pawn, ECR_Overlap);
}

void ASVArchiveTerminal::BeginPlay()
{
	Super::BeginPlay();
}

FText ASVArchiveTerminal::GetInteractionPrompt_Implementation()
{
	if (bIsDiscovered)
	{
		return FText::Format(FText::FromString(TEXT("{0} (Already Recovered)")), ArchiveTitle);
	}
	return FText::Format(FText::FromString(TEXT("Press [E] to Inspect Archive: {0}")), ArchiveTitle);
}

void ASVArchiveTerminal::OnInteract_Implementation(AActor* Interactor)
{
	if (bIsDiscovered)
	{
		UE_LOG(LogTemp, Log, TEXT("[SVArchiveTerminal] Archive %s already discovered."), *ArchiveId);
		return;
	}

	bIsDiscovered = true;
	UE_LOG(LogTemp, Log, TEXT("[SVArchiveTerminal] Discovered archive: %s - %s"), *ArchiveId, *ArchiveTitle.ToString());

	OnArchiveDiscovered.Broadcast(ArchiveId);

	if (UGameInstance* GI = GetGameInstance())
	{
		if (USVMissionControlSubsystem* MCSubsystem = GI->GetSubsystem<USVMissionControlSubsystem>())
		{
			MCSubsystem->ReportArchiveDiscovered(ArchiveId);
		}
	}
}
