// Copyright SparkVision Dhaka University. All Rights Reserved.

#include "SVCharacter.h"
#include "Camera/CameraComponent.h"
#include "GameFramework/SpringArmComponent.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "EnhancedInputComponent.h"
#include "EnhancedInputSubsystems.h"
#include "Kismet/KismetSystemLibrary.h"
#include "Engine/World.h"
#include "SVMissionControlSubsystem.h"

ASVCharacter::ASVCharacter()
{
	PrimaryActorTick.bCanEverTick = true;

	bUseControllerRotationPitch = false;
	bUseControllerRotationYaw = false;
	bUseControllerRotationRoll = false;

	// Where Winds Meet Locomotion Tuning
	GetCharacterMovement()->bOrientRotationToMovement = true;
	GetCharacterMovement()->RotationRate = FRotator(0.0f, 720.0f, 0.0f); // Fast, responsive turning
	GetCharacterMovement()->JumpZVelocity = 650.0f;
	GetCharacterMovement()->AirControl = 0.40f;
	GetCharacterMovement()->MaxWalkSpeed = 480.0f;
	GetCharacterMovement()->MinAnalogWalkSpeed = 20.0f;
	GetCharacterMovement()->BrakingDecelerationWalking = 2400.0f;
	GetCharacterMovement()->MaxAcceleration = 2200.0f;

	// Where Winds Meet Dynamic Camera Setup
	CameraBoom = CreateDefaultSubobject<USpringArmComponent>(TEXT("CameraBoom"));
	CameraBoom->SetupAttachment(RootComponent);
	CameraBoom->TargetArmLength = 380.0f;
	CameraBoom->SocketOffset = FVector(0.0f, 45.0f, 25.0f); // Cinematic over-the-shoulder offset
	CameraBoom->bUsePawnControlRotation = true;
	CameraBoom->bEnableCameraLag = true;
	CameraBoom->CameraLagSpeed = 7.5f;
	CameraBoom->bEnableCameraRotationLag = true;
	CameraBoom->CameraRotationLagSpeed = 9.0f;
	CameraBoom->CameraLagMaxDistance = 80.0f;

	FollowCamera = CreateDefaultSubobject<UCameraComponent>(TEXT("FollowCamera"));
	FollowCamera->SetupAttachment(CameraBoom, USpringArmComponent::SocketName);
	FollowCamera->bUsePawnControlRotation = false;
	FollowCamera->SetFieldOfView(75.0f);

	CurrentHealth = MaxHealth;
	CurrentQi = MaxQi;
}

void ASVCharacter::BeginPlay()
{
	Super::BeginPlay();

	if (APlayerController* PlayerController = Cast<APlayerController>(Controller))
	{
		if (UEnhancedInputLocalPlayerSubsystem* Subsystem = ULocalPlayer::GetSubsystem<UEnhancedInputLocalPlayerSubsystem>(PlayerController->GetLocalPlayer()))
		{
			if (DefaultMappingContext)
			{
				Subsystem->AddMappingContext(DefaultMappingContext, 0);
			}
		}
	}
}

void ASVCharacter::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);

	ScanForInteractables();
	UpdateCameraFraming(DeltaTime);
	UpdateVitals(DeltaTime);
}

void ASVCharacter::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{
	Super::SetupPlayerInputComponent(PlayerInputComponent);

	if (UEnhancedInputComponent* EnhancedInputComponent = Cast<UEnhancedInputComponent>(PlayerInputComponent))
	{
		if (JumpAction)
		{
			EnhancedInputComponent->BindAction(JumpAction, ETriggerEvent::Started, this, &ACharacter::Jump);
			EnhancedInputComponent->BindAction(JumpAction, ETriggerEvent::Completed, this, &ACharacter::StopJumping);
		}
		if (MoveAction)
		{
			EnhancedInputComponent->BindAction(MoveAction, ETriggerEvent::Triggered, this, &ASVCharacter::Move);
		}
		if (LookAction)
		{
			EnhancedInputComponent->BindAction(LookAction, ETriggerEvent::Triggered, this, &ASVCharacter::Look);
		}
		if (InteractAction)
		{
			EnhancedInputComponent->BindAction(InteractAction, ETriggerEvent::Started, this, &ASVCharacter::Interact);
		}
		if (StrikeAction)
		{
			EnhancedInputComponent->BindAction(StrikeAction, ETriggerEvent::Started, this, &ASVCharacter::Strike);
		}
		if (SprintAction)
		{
			EnhancedInputComponent->BindAction(SprintAction, ETriggerEvent::Started, this, &ASVCharacter::StartSprint);
			EnhancedInputComponent->BindAction(SprintAction, ETriggerEvent::Completed, this, &ASVCharacter::StopSprint);
		}
		if (ParryAction)
		{
			EnhancedInputComponent->BindAction(ParryAction, ETriggerEvent::Started, this, &ASVCharacter::StartParry);
			EnhancedInputComponent->BindAction(ParryAction, ETriggerEvent::Completed, this, &ASVCharacter::StopParry);
		}
		if (DashAction)
		{
			EnhancedInputComponent->BindAction(DashAction, ETriggerEvent::Started, this, &ASVCharacter::Dash);
		}
	}
}

void ASVCharacter::Move(const FInputActionValue& Value)
{
	FVector2D MovementVector = Value.Get<FVector2D>();

	if (Controller != nullptr)
	{
		const FRotator Rotation = Controller->GetControlRotation();
		const FRotator YawRotation(0, Rotation.Yaw, 0);

		const FVector ForwardDirection = FRotationMatrix(YawRotation).GetUnitAxis(EAxis::X);
		const FVector RightDirection = FRotationMatrix(YawRotation).GetUnitAxis(EAxis::Y);

		AddMovementInput(ForwardDirection, MovementVector.Y);
		AddMovementInput(RightDirection, MovementVector.X);
	}
}

void ASVCharacter::Look(const FInputActionValue& Value)
{
	FVector2D LookAxisVector = Value.Get<FVector2D>();

	if (Controller != nullptr)
	{
		AddControllerYawInput(LookAxisVector.X);
		AddControllerPitchInput(LookAxisVector.Y);
	}
}

void ASVCharacter::StartSprint()
{
	if (CurrentQi > 10.0f)
	{
		bIsSprinting = true;
		GetCharacterMovement()->MaxWalkSpeed = 880.0f;
	}
}

void ASVCharacter::StopSprint()
{
	bIsSprinting = false;
	GetCharacterMovement()->MaxWalkSpeed = 480.0f;
}

void ASVCharacter::StartParry()
{
	bIsBlocking = true;
	bIsParrying = true;
	ParryWindowTimer = ParryWindowDuration;
	UE_LOG(LogTemp, Log, TEXT("[SVCharacter] Parry stance engaged (Window: %.0fms)"), ParryWindowDuration * 1000.0f);
}

void ASVCharacter::StopParry()
{
	bIsBlocking = false;
	bIsParrying = false;
	ParryWindowTimer = 0.0f;
}

void ASVCharacter::Dash()
{
	if (CurrentQi >= 20.0f)
	{
		CurrentQi -= 20.0f;
		OnQiChanged.Broadcast(CurrentQi, MaxQi);

		FVector DashDirection = GetActorForwardVector();
		if (GetCharacterMovement()->Velocity.SizeSquared2D() > 100.0f)
		{
			DashDirection = GetCharacterMovement()->Velocity.GetSafeNormal2D();
		}
		LaunchCharacter(DashDirection * 1200.0f + FVector(0.0f, 0.0f, 150.0f), true, true);
		UE_LOG(LogTemp, Log, TEXT("[SVCharacter] Qinggong Evasive Dash executed!"));
	}
}

void ASVCharacter::UpdateCameraFraming(float DeltaTime)
{
	// Where Winds Meet Dynamic Camera Interpolation:
	// - Sprint: Pull back for speed sense (ArmLength: 460cm, FOV: 85)
	// - Combat/Parry: Close-in tactical framing (ArmLength: 260cm, FOV: 70)
	// - Exploration: Standard grand vista (ArmLength: 380cm, FOV: 75)
	if (bIsSprinting && GetCharacterMovement()->Velocity.Size() > 500.0f)
	{
		TargetArmDistance = 460.0f;
		TargetFOV = 85.0f;
		TargetSocketOffset = FVector(0.0f, 35.0f, 20.0f);
	}
	else if (bIsBlocking || bIsAttacking)
	{
		TargetArmDistance = 280.0f;
		TargetFOV = 70.0f;
		TargetSocketOffset = FVector(0.0f, 55.0f, 25.0f);
	}
	else
	{
		TargetArmDistance = 380.0f;
		TargetFOV = 75.0f;
		TargetSocketOffset = FVector(0.0f, 45.0f, 25.0f);
	}

	CameraBoom->TargetArmLength = FMath::FInterpTo(CameraBoom->TargetArmLength, TargetArmDistance, DeltaTime, 4.0f);
	CameraBoom->SocketOffset = FMath::VInterpTo(CameraBoom->SocketOffset, TargetSocketOffset, DeltaTime, 4.0f);
	FollowCamera->FieldOfView = FMath::FInterpTo(FollowCamera->FieldOfView, TargetFOV, DeltaTime, 4.0f);
}

void ASVCharacter::UpdateVitals(float DeltaTime)
{
	// Qi consumption and regeneration
	if (bIsSprinting && GetCharacterMovement()->Velocity.Size() > 500.0f)
	{
		CurrentQi = FMath::Clamp(CurrentQi - (18.0f * DeltaTime), 0.0f, MaxQi);
		if (CurrentQi <= 0.0f)
		{
			StopSprint();
		}
		OnQiChanged.Broadcast(CurrentQi, MaxQi);
	}
	else if (!bIsBlocking)
	{
		if (CurrentQi < MaxQi)
		{
			CurrentQi = FMath::Clamp(CurrentQi + (22.0f * DeltaTime), 0.0f, MaxQi);
			OnQiChanged.Broadcast(CurrentQi, MaxQi);
		}
	}

	// Parry window decay
	if (bIsParrying)
	{
		ParryWindowTimer -= DeltaTime;
		if (ParryWindowTimer <= 0.0f)
		{
			bIsParrying = false; // Transition from active parry window into normal block
		}
	}

	// Combo decay
	if (AttackResetTimer > 0.0f)
	{
		AttackResetTimer -= DeltaTime;
		if (AttackResetTimer <= 0.0f)
		{
			ComboStep = 0;
			bIsAttacking = false;
		}
	}
}

void ASVCharacter::ScanForInteractables()
{
	FVector Start = GetActorLocation();
	FVector End = Start + (GetActorForwardVector() * 260.0f);

	TArray<TEnumAsByte<EObjectTypeQuery>> ObjectTypes;
	ObjectTypes.Add(UEngineTypes::ConvertToObjectType(ECC_WorldDynamic));
	ObjectTypes.Add(UEngineTypes::ConvertToObjectType(ECC_Pawn));

	TArray<AActor*> ActorsToIgnore;
	ActorsToIgnore.Add(this);

	TArray<FHitResult> HitResults;
	bool bHit = UKismetSystemLibrary::SphereTraceMultiForObjects(
		GetWorld(), Start, End, 220.0f,
		ObjectTypes, false, ActorsToIgnore,
		EDrawDebugTrace::None, HitResults, true
	);

	AActor* BestInteractable = nullptr;
	if (bHit)
	{
		for (const FHitResult& Hit : HitResults)
		{
			if (Hit.GetActor() && Hit.GetActor()->GetClass()->ImplementsInterface(USVInteractableInterface::StaticClass()))
			{
				BestInteractable = Hit.GetActor();
				break;
			}
		}
	}

	if (BestInteractable != CurrentFocusedInteractable)
	{
		CurrentFocusedInteractable = BestInteractable;
		if (CurrentFocusedInteractable)
		{
			CurrentPromptText = ISVInteractableInterface::Execute_GetInteractionPrompt(CurrentFocusedInteractable);
			OnNearbyInteractableChanged.Broadcast(CurrentPromptText);
		}
		else
		{
			CurrentPromptText = FText::GetEmpty();
			OnNearbyInteractableChanged.Broadcast(CurrentPromptText);
		}
	}
}

void ASVCharacter::Interact()
{
	if (CurrentFocusedInteractable)
	{
		ISVInteractableInterface::Execute_OnInteract(CurrentFocusedInteractable, this);
		CurrentPromptText = ISVInteractableInterface::Execute_GetInteractionPrompt(CurrentFocusedInteractable);
		OnNearbyInteractableChanged.Broadcast(CurrentPromptText);
	}
}

void ASVCharacter::Strike()
{
	bIsAttacking = true;
	ComboStep = (ComboStep + 1) % 3;
	AttackResetTimer = 0.85f;

	UE_LOG(LogTemp, Log, TEXT("[SVCharacter] Martial Strike combo chain hit %d executed!"), ComboStep + 1);

	// Forward hit trace
	FVector Start = GetActorLocation();
	FVector End = Start + (GetActorForwardVector() * 220.0f);

	FHitResult Hit;
	FCollisionQueryParams Params;
	Params.AddIgnoredActor(this);

	if (GetWorld()->LineTraceSingleByChannel(Hit, Start, End, ECC_Pawn, Params))
	{
		if (Hit.GetActor())
		{
			UE_LOG(LogTemp, Log, TEXT("[SVCharacter] Connected strike against: %s"), *Hit.GetActor()->GetName());
		}
	}
}

bool ASVCharacter::TryDeflectAttack(float IncomingDamage, AActor* Attacker)
{
	if (bIsParrying)
	{
		// Perfect Wuxia Parry / Deflection! 0 damage, posture damage to attacker
		OnParrySuccess.Broadcast();
		UE_LOG(LogTemp, Warning, TEXT("[SVCharacter] PERFECT PARRY! Deflected incoming attack from %s!"), *GetNameSafe(Attacker));
		return true;
	}
	else if (bIsBlocking && CurrentQi >= 15.0f)
	{
		// Standard Block: 75% damage mitigation, drains stamina
		CurrentQi -= 15.0f;
		OnQiChanged.Broadcast(CurrentQi, MaxQi);
		TakeDamageAmount(IncomingDamage * 0.25f);
		UE_LOG(LogTemp, Log, TEXT("[SVCharacter] Blocked attack with partial damage mitigation."));
		return true;
	}

	// Unblocked hit
	TakeDamageAmount(IncomingDamage);
	return false;
}

void ASVCharacter::TakeDamageAmount(float Damage)
{
	CurrentHealth = FMath::Clamp(CurrentHealth - Damage, 0.0f, MaxHealth);
	OnHealthChanged.Broadcast(CurrentHealth, MaxHealth);
	UE_LOG(LogTemp, Warning, TEXT("[SVCharacter] Took %.1f damage. Current Health: %.1f / %.1f"), Damage, CurrentHealth, MaxHealth);
}

void ASVCharacter::ResetHealth()
{
	CurrentHealth = MaxHealth;
	CurrentQi = MaxQi;
	OnHealthChanged.Broadcast(CurrentHealth, MaxHealth);
	OnQiChanged.Broadcast(CurrentQi, MaxQi);
}
