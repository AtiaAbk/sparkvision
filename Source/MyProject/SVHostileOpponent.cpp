// Copyright SparkVision Dhaka University. All Rights Reserved.

#include "SVHostileOpponent.h"
#include "Components/CapsuleComponent.h"
#include "Components/SkeletalMeshComponent.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Kismet/GameplayStatics.h"
#include "UObject/ConstructorHelpers.h"
#include "SVCharacter.h"

ASVHostileOpponent::ASVHostileOpponent()
{
	PrimaryActorTick.bCanEverTick = true;

	GetCapsuleComponent()->InitCapsuleSize(42.0f, 96.0f);
	GetCapsuleComponent()->SetCollisionProfileName(TEXT("Pawn"));

	GetCharacterMovement()->bOrientRotationToMovement = true;
	GetCharacterMovement()->MaxWalkSpeed = 340.0f;

	// Assign Manny skeletal mesh & unarmed animation blueprint
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
}

void ASVHostileOpponent::BeginPlay()
{
	Super::BeginPlay();
}

void ASVHostileOpponent::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);

	if (bIsDefeated) return;

	TimeSinceLastAttack += DeltaTime;

	ACharacter* PlayerChar = UGameplayStatics::GetPlayerCharacter(this, 0);
	if (PlayerChar)
	{
		float Distance = FVector::Dist(GetActorLocation(), PlayerChar->GetActorLocation());
		if (Distance < 1200.0f && Distance > AttackRange)
		{
			// Move toward player
			FVector Direction = (PlayerChar->GetActorLocation() - GetActorLocation()).GetSafeNormal();
			AddMovementInput(Direction, 1.0f);
		}
		else if (Distance <= AttackRange && TimeSinceLastAttack >= AttackCooldown)
		{
			// Execute baton attack
			TimeSinceLastAttack = 0.0f;
			if (ASVCharacter* SVChar = Cast<ASVCharacter>(PlayerChar))
			{
				SVChar->TakeDamageAmount(AttackDamage, this);
				UE_LOG(LogTemp, Warning, TEXT("[SVHostileOpponent] Baton strike delivered to player!"));
			}
		}
	}
}

void ASVHostileOpponent::ReceiveStrike(float DamageAmount)
{
	if (bIsDefeated) return;

	Health -= DamageAmount;
	UE_LOG(LogTemp, Log, TEXT("[SVHostileOpponent] Received %f strike damage. Remaining health: %f"), DamageAmount, Health);

	if (Health <= 0.0f)
	{
		bIsDefeated = true;
		GetCharacterMovement()->DisableMovement();
		SetActorEnableCollision(false);
		OnOpponentDefeated.Broadcast(this);
		UE_LOG(LogTemp, Log, TEXT("[SVHostileOpponent] Opponent neutralized!"));
	}
}
