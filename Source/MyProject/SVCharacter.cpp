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

	GetCharacterMovement()->bOrientRotationToMovement = true;
	GetCharacterMovement()->RotationRate = FRotator(0.0f, 500.0f, 0.0f);
	GetCharacterMovement()->JumpZVelocity = 600.f;
	GetCharacterMovement()->AirControl = 0.35f;
	GetCharacterMovement()->MaxWalkSpeed = 500.f;
	GetCharacterMovement()->MinAnalogWalkSpeed = 20.f;
	GetCharacterMovement()->BrakingDecelerationWalking = 2000.f;

	CameraBoom = CreateDefaultSubobject<USpringArmComponent>(TEXT("CameraBoom"));
	CameraBoom->SetupAttachment(RootComponent);
	CameraBoom->TargetArmLength = 400.0f;
	CameraBoom->bUsePawnControlRotation = true;

	FollowCamera = CreateDefaultSubobject<UCameraComponent>(TEXT("FollowCamera"));
	FollowCamera->SetupAttachment(CameraBoom, USpringArmComponent::SocketName);
	FollowCamera->bUsePawnControlRotation = false;

	CurrentHealth = MaxHealth;
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

void ASVCharacter::ScanForInteractables()
{
	FVector Start = GetActorLocation();
	FVector End = Start + (GetActorForwardVector() * 250.0f);

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
			FText Prompt = ISVInteractableInterface::Execute_GetInteractionPrompt(CurrentFocusedInteractable);
			OnNearbyInteractableChanged.Broadcast(Prompt);
		}
		else
		{
			OnNearbyInteractableChanged.Broadcast(FText::GetEmpty());
		}
	}
}

void ASVCharacter::Interact()
{
	if (CurrentFocusedInteractable)
	{
		ISVInteractableInterface::Execute_OnInteract(CurrentFocusedInteractable, this);
		FText Prompt = ISVInteractableInterface::Execute_GetInteractionPrompt(CurrentFocusedInteractable);
		OnNearbyInteractableChanged.Broadcast(Prompt);
	}
}

void ASVCharacter::Strike()
{
	bIsAttacking = true;
	UE_LOG(LogTemp, Log, TEXT("[SVCharacter] Strike executed against hostile forces!"));

	// Trace forward for hostile encounter actors
	FVector Start = GetActorLocation();
	FVector End = Start + (GetActorForwardVector() * 200.0f);

	FHitResult Hit;
	FCollisionQueryParams Params;
	Params.AddIgnoredActor(this);

	if (GetWorld()->LineTraceSingleByChannel(Hit, Start, End, ECC_Pawn, Params))
	{
		if (Hit.GetActor())
		{
			UE_LOG(LogTemp, Log, TEXT("[SVCharacter] Hit opponent: %s"), *Hit.GetActor()->GetName());
		}
	}
}

void ASVCharacter::TakeDamageAmount(float Damage)
{
	CurrentHealth = FMath::Clamp(CurrentHealth - Damage, 0.0f, MaxHealth);
	OnHealthChanged.Broadcast(CurrentHealth, MaxHealth);
	UE_LOG(LogTemp, Warning, TEXT("[SVCharacter] Took %f damage. Current Health: %f / %f"), Damage, CurrentHealth, MaxHealth);
}

void ASVCharacter::ResetHealth()
{
	CurrentHealth = MaxHealth;
	OnHealthChanged.Broadcast(CurrentHealth, MaxHealth);
}
