// Copyright SparkVision Dhaka University. All Rights Reserved.

#include "SVCharacter.h"
#include "Camera/CameraComponent.h"
#include "GameFramework/SpringArmComponent.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Components/CapsuleComponent.h"
#include "Components/SkeletalMeshComponent.h"
#include "EnhancedInputComponent.h"
#include "EnhancedInputSubsystems.h"
#include "InputActionValue.h"
#include "InputMappingContext.h"
#include "InputAction.h"
#include "UObject/ConstructorHelpers.h"
#include "Kismet/KismetSystemLibrary.h"
#include "Engine/World.h"
#include "SVMissionControlSubsystem.h"
#include "SVHUD.h"

ASVCharacter::ASVCharacter()
{
	PrimaryActorTick.bCanEverTick = true;

	bUseControllerRotationPitch = false;
	bUseControllerRotationYaw = false;
	bUseControllerRotationRoll = false;

	// Responsive Movement Tuning
	GetCharacterMovement()->bOrientRotationToMovement = true;
	GetCharacterMovement()->RotationRate = FRotator(0.0f, 720.0f, 0.0f);
	GetCharacterMovement()->JumpZVelocity = 650.0f;
	GetCharacterMovement()->AirControl = 0.45f;
	GetCharacterMovement()->MaxWalkSpeed = 550.0f;
	GetCharacterMovement()->MinAnalogWalkSpeed = 20.0f;
	GetCharacterMovement()->BrakingDecelerationWalking = 2400.0f;
	GetCharacterMovement()->MaxAcceleration = 2200.0f;

	// Spring Arm & Camera
	CameraBoom = CreateDefaultSubobject<USpringArmComponent>(TEXT("CameraBoom"));
	CameraBoom->SetupAttachment(RootComponent);
	CameraBoom->TargetArmLength = 380.0f;
	CameraBoom->SocketOffset = FVector(0.0f, 45.0f, 25.0f);
	CameraBoom->bUsePawnControlRotation = true;
	CameraBoom->bEnableCameraLag = true;
	CameraBoom->CameraLagSpeed = 8.0f;
	CameraBoom->bEnableCameraRotationLag = true;
	CameraBoom->CameraRotationLagSpeed = 10.0f;

	FollowCamera = CreateDefaultSubobject<UCameraComponent>(TEXT("FollowCamera"));
	FollowCamera->SetupAttachment(CameraBoom, USpringArmComponent::SocketName);
	FollowCamera->bUsePawnControlRotation = false;
	FollowCamera->SetFieldOfView(75.0f);

	// Load Quinn Mannequin & Animation Assets
	static ConstructorHelpers::FObjectFinder<USkeletalMesh> SkeletalMeshFinder(TEXT("/Game/Characters/Mannequins/Meshes/SKM_Quinn_Simple.SKM_Quinn_Simple"));
	if (SkeletalMeshFinder.Succeeded())
	{
		GetMesh()->SetSkeletalMeshAsset(SkeletalMeshFinder.Object);
		GetMesh()->SetRelativeLocationAndRotation(FVector(0.0f, 0.0f, -90.0f), FRotator(0.0f, -90.0f, 0.0f));
	}

	static ConstructorHelpers::FClassFinder<UAnimInstance> AnimInstanceFinder(TEXT("/Game/Characters/Mannequins/Anims/Unarmed/ABP_Unarmed.ABP_Unarmed_C"));
	if (AnimInstanceFinder.Succeeded())
	{
		GetMesh()->SetAnimInstanceClass(AnimInstanceFinder.Class);
	}

	// Load Enhanced Input Assets
	static ConstructorHelpers::FObjectFinder<UInputMappingContext> DefaultIMCFinder(TEXT("/Game/Input/IMC_Default.IMC_Default"));
	if (DefaultIMCFinder.Succeeded())
	{
		DefaultMappingContext = DefaultIMCFinder.Object;
	}

	static ConstructorHelpers::FObjectFinder<UInputMappingContext> MouseLookIMCFinder(TEXT("/Game/Input/IMC_MouseLook.IMC_MouseLook"));
	if (MouseLookIMCFinder.Succeeded())
	{
		MouseLookMappingContext = MouseLookIMCFinder.Object;
	}

	static ConstructorHelpers::FObjectFinder<UInputAction> MoveActionFinder(TEXT("/Game/Input/Actions/IA_Move.IA_Move"));
	if (MoveActionFinder.Succeeded())
	{
		MoveAction = MoveActionFinder.Object;
	}

	static ConstructorHelpers::FObjectFinder<UInputAction> LookActionFinder(TEXT("/Game/Input/Actions/IA_Look.IA_Look"));
	if (LookActionFinder.Succeeded())
	{
		LookAction = LookActionFinder.Object;
	}

	static ConstructorHelpers::FObjectFinder<UInputAction> JumpActionFinder(TEXT("/Game/Input/Actions/IA_Jump.IA_Jump"));
	if (JumpActionFinder.Succeeded())
	{
		JumpAction = JumpActionFinder.Object;
	}

	static ConstructorHelpers::FObjectFinder<UInputAction> MouseLookActionFinder(TEXT("/Game/Input/Actions/IA_MouseLook.IA_MouseLook"));
	if (MouseLookActionFinder.Succeeded())
	{
		MouseLookAction = MouseLookActionFinder.Object;
	}

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
			if (MouseLookMappingContext)
			{
				Subsystem->AddMappingContext(MouseLookMappingContext, 1);
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

	// 1. Enhanced Input bindings
	if (UEnhancedInputComponent* EnhancedInputComponent = Cast<UEnhancedInputComponent>(PlayerInputComponent))
	{
		if (MoveAction)
		{
			EnhancedInputComponent->BindAction(MoveAction, ETriggerEvent::Triggered, this, &ASVCharacter::Move);
		}
		if (LookAction)
		{
			EnhancedInputComponent->BindAction(LookAction, ETriggerEvent::Triggered, this, &ASVCharacter::Look);
		}
		if (MouseLookAction)
		{
			EnhancedInputComponent->BindAction(MouseLookAction, ETriggerEvent::Triggered, this, &ASVCharacter::MouseLook);
		}
		if (JumpAction)
		{
			EnhancedInputComponent->BindAction(JumpAction, ETriggerEvent::Started, this, &ACharacter::Jump);
			EnhancedInputComponent->BindAction(JumpAction, ETriggerEvent::Completed, this, &ACharacter::StopJumping);
		}
	}

	// 2. Direct Fallback Key/Axis Bindings (guarantees immediate responsiveness on any desktop/editor setup)
	PlayerInputComponent->BindAxisKey(EKeys::W, this, &ASVCharacter::MoveForwardDirect);
	PlayerInputComponent->BindAxisKey(EKeys::S, this, &ASVCharacter::MoveBackwardDirect);
	PlayerInputComponent->BindAxisKey(EKeys::D, this, &ASVCharacter::MoveRightDirect);
	PlayerInputComponent->BindAxisKey(EKeys::A, this, &ASVCharacter::MoveLeftDirect);

	PlayerInputComponent->BindAxisKey(EKeys::MouseX, this, &ASVCharacter::LookYawDirect);
	PlayerInputComponent->BindAxisKey(EKeys::MouseY, this, &ASVCharacter::LookPitchDirect);

	PlayerInputComponent->BindKey(EKeys::SpaceBar, IE_Pressed, this, &ACharacter::Jump);
	PlayerInputComponent->BindKey(EKeys::SpaceBar, IE_Released, this, &ACharacter::StopJumping);

	PlayerInputComponent->BindKey(EKeys::LeftShift, IE_Pressed, this, &ASVCharacter::StartSprint);
	PlayerInputComponent->BindKey(EKeys::LeftShift, IE_Released, this, &ASVCharacter::StopSprint);

	PlayerInputComponent->BindKey(EKeys::E, IE_Pressed, this, &ASVCharacter::Interact);

	// 3. Landmark Fast Travel Keybinds (1 to 6)
	PlayerInputComponent->BindKey(EKeys::One, IE_Pressed, this, &ASVCharacter::TeleportToCurzon);
	PlayerInputComponent->BindKey(EKeys::Two, IE_Pressed, this, &ASVCharacter::TeleportToDoyel);
	PlayerInputComponent->BindKey(EKeys::Three, IE_Pressed, this, &ASVCharacter::TeleportToShaheedMinar);
	PlayerInputComponent->BindKey(EKeys::Four, IE_Pressed, this, &ASVCharacter::TeleportToTSC);
	PlayerInputComponent->BindKey(EKeys::Five, IE_Pressed, this, &ASVCharacter::TeleportToLibrary);
	PlayerInputComponent->BindKey(EKeys::Six, IE_Pressed, this, &ASVCharacter::TeleportToKalaBhaban);
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

void ASVCharacter::MouseLook(const FInputActionValue& Value)
{
	FVector2D LookAxisVector = Value.Get<FVector2D>();

	if (Controller != nullptr)
	{
		AddControllerYawInput(LookAxisVector.X);
		AddControllerPitchInput(LookAxisVector.Y);
	}
}

void ASVCharacter::MoveForwardDirect(float Val)
{
	if (Val != 0.0f && Controller != nullptr)
	{
		const FRotator YawRotation(0, Controller->GetControlRotation().Yaw, 0);
		const FVector Direction = FRotationMatrix(YawRotation).GetUnitAxis(EAxis::X);
		AddMovementInput(Direction, Val);
	}
}

void ASVCharacter::MoveBackwardDirect(float Val)
{
	if (Val != 0.0f && Controller != nullptr)
	{
		const FRotator YawRotation(0, Controller->GetControlRotation().Yaw, 0);
		const FVector Direction = FRotationMatrix(YawRotation).GetUnitAxis(EAxis::X);
		AddMovementInput(Direction, -Val);
	}
}

void ASVCharacter::MoveRightDirect(float Val)
{
	if (Val != 0.0f && Controller != nullptr)
	{
		const FRotator YawRotation(0, Controller->GetControlRotation().Yaw, 0);
		const FVector Direction = FRotationMatrix(YawRotation).GetUnitAxis(EAxis::Y);
		AddMovementInput(Direction, Val);
	}
}

void ASVCharacter::MoveLeftDirect(float Val)
{
	if (Val != 0.0f && Controller != nullptr)
	{
		const FRotator YawRotation(0, Controller->GetControlRotation().Yaw, 0);
		const FVector Direction = FRotationMatrix(YawRotation).GetUnitAxis(EAxis::Y);
		AddMovementInput(Direction, -Val);
	}
}

void ASVCharacter::LookYawDirect(float Val)
{
	if (Val != 0.0f)
	{
		AddControllerYawInput(Val);
	}
}

void ASVCharacter::LookPitchDirect(float Val)
{
	if (Val != 0.0f)
	{
		AddControllerPitchInput(-Val);
	}
}

void ASVCharacter::StartSprint()
{
	if (CurrentQi > 10.0f)
	{
		bIsSprinting = true;
		GetCharacterMovement()->MaxWalkSpeed = 950.0f; // Fast, athletic sprint across campus
	}
}

void ASVCharacter::StopSprint()
{
	bIsSprinting = false;
	GetCharacterMovement()->MaxWalkSpeed = 550.0f; // Standard running speed
}

void ASVCharacter::StartParry()
{
	if (!bIsAttacking && CurrentQi >= 10.0f)
	{
		bIsParrying = true;
		bIsBlocking = true;
		ParryWindowTimer = ParryWindowDuration;
		GetCharacterMovement()->MaxWalkSpeed = 220.0f;
	}
}

void ASVCharacter::StopParry()
{
	bIsParrying = false;
	bIsBlocking = false;
	GetCharacterMovement()->MaxWalkSpeed = bIsSprinting ? 950.0f : 550.0f;
}

void ASVCharacter::Dash()
{
	if (CurrentQi >= 25.0f && !bIsAttacking)
	{
		CurrentQi -= 25.0f;
		OnQiChanged.Broadcast(CurrentQi, MaxQi);

		FVector DashDirection = GetActorForwardVector();
		if (GetCharacterMovement()->Velocity.SizeSquared2D() > 100.0f)
		{
			DashDirection = GetCharacterMovement()->Velocity.GetSafeNormal2D();
		}
		LaunchCharacter(DashDirection * 1400.0f + FVector(0.0f, 0.0f, 250.0f), true, true);
	}
}

void ASVCharacter::TeleportToCurzon()
{
	SetActorLocationAndRotation(FVector(-3500.0f, 0.0f, 150.0f), FRotator(0.0f, 0.0f, 0.0f), false, nullptr, ETeleportType::ResetPhysics);
	if (Controller) Controller->SetControlRotation(FRotator(0.0f, 0.0f, 0.0f));
	UE_LOG(LogTemp, Log, TEXT("[SVCharacter] Teleported to Curzon Hall South Portico."));
}

void ASVCharacter::TeleportToDoyel()
{
	SetActorLocationAndRotation(FVector(7500.0f, -16500.0f, 150.0f), FRotator(0.0f, 90.0f, 0.0f), false, nullptr, ETeleportType::ResetPhysics);
	if (Controller) Controller->SetControlRotation(FRotator(0.0f, 90.0f, 0.0f));
	UE_LOG(LogTemp, Log, TEXT("[SVCharacter] Teleported to Doyel Chattar Roundabout."));
}

void ASVCharacter::TeleportToShaheedMinar()
{
	SetActorLocationAndRotation(FVector(-300.0f, -54000.0f, 150.0f), FRotator(0.0f, -90.0f, 0.0f), false, nullptr, ETeleportType::ResetPhysics);
	if (Controller) Controller->SetControlRotation(FRotator(0.0f, -90.0f, 0.0f));
	UE_LOG(LogTemp, Log, TEXT("[SVCharacter] Teleported to Central Shaheed Minar."));
}

void ASVCharacter::TeleportToTSC()
{
	SetActorLocationAndRotation(FVector(59000.0f, -63700.0f, 150.0f), FRotator(0.0f, 0.0f, 0.0f), false, nullptr, ETeleportType::ResetPhysics);
	if (Controller) Controller->SetControlRotation(FRotator(0.0f, 0.0f, 0.0f));
	UE_LOG(LogTemp, Log, TEXT("[SVCharacter] Teleported to TSC Mor & Raju Memorial."));
}

void ASVCharacter::TeleportToLibrary()
{
	SetActorLocationAndRotation(FVector(73500.0f, -71700.0f, 150.0f), FRotator(0.0f, -90.0f, 0.0f), false, nullptr, ETeleportType::ResetPhysics);
	if (Controller) Controller->SetControlRotation(FRotator(0.0f, -90.0f, 0.0f));
	UE_LOG(LogTemp, Log, TEXT("[SVCharacter] Teleported to DU Central Library & Hakim Chattar."));
}

void ASVCharacter::TeleportToKalaBhaban()
{
	SetActorLocationAndRotation(FVector(73500.0f, -95800.0f, 150.0f), FRotator(0.0f, 0.0f, 0.0f), false, nullptr, ETeleportType::ResetPhysics);
	if (Controller) Controller->SetControlRotation(FRotator(0.0f, 0.0f, 0.0f));
	UE_LOG(LogTemp, Log, TEXT("[SVCharacter] Teleported to Arts Faculty & Aparajeyo Bangla."));
}

FString ASVCharacter::GetCurrentLandmarkName() const
{
	const FVector MyLoc = GetActorLocation();

	struct FLandmarkZone { FString Name; FVector Loc; float Radius; };
	static const TArray<FLandmarkZone> Zones = {
		{ TEXT("Curzon Hall Heritage Precinct | কার্জন হল প্রাঙ্গণ"), FVector(-2850.0f, 0.0f, 50.0f), 12000.0f },
		{ TEXT("Doyel Chattar Roundabout | দোয়েল চত্বর"), FVector(7500.0f, -16500.0f, 50.0f), 6500.0f },
		{ TEXT("Central Shaheed Minar | কেন্দ্রীয় শহীদ মিনার"), FVector(-300.0f, -54000.0f, 50.0f), 7000.0f },
		{ TEXT("Teacher-Student Centre (TSC) | টিএসসি"), FVector(59000.0f, -63700.0f, 50.0f), 7000.0f },
		{ TEXT("DU Central Library & Hakim Chattar | কেন্দ্রীয় গ্রন্থাগার"), FVector(73500.0f, -71700.0f, 50.0f), 7500.0f },
		{ TEXT("Arts Faculty & Aparajeyo Bangla | কলাভবন ও অপরাজেয় বাংলা"), FVector(73500.0f, -95800.0f, 50.0f), 9000.0f }
	};

	for (const auto& Z : Zones)
	{
		if (FVector::Dist2D(MyLoc, Z.Loc) <= Z.Radius)
		{
			return Z.Name;
		}
	}
	return TEXT("University of Dhaka Campus | ঢাকা বিশ্ববিদ্যালয়");
}

void ASVCharacter::UpdateCameraFraming(float DeltaTime)
{
	if (bIsSprinting)
	{
		TargetArmDistance = 460.0f;
		TargetFOV = 84.0f;
		TargetSocketOffset = FVector(0.0f, 55.0f, 30.0f);
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
	if (bIsSprinting && GetCharacterMovement()->Velocity.Size() > 400.0f)
	{
		CurrentQi = FMath::Clamp(CurrentQi - (12.0f * DeltaTime), 0.0f, MaxQi);
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
			CurrentQi = FMath::Clamp(CurrentQi + (25.0f * DeltaTime), 0.0f, MaxQi);
			OnQiChanged.Broadcast(CurrentQi, MaxQi);
		}
	}

	if (bIsParrying)
	{
		ParryWindowTimer -= DeltaTime;
		if (ParryWindowTimer <= 0.0f)
		{
			bIsParrying = false;
		}
	}

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
	FVector End = Start + (GetActorForwardVector() * 320.0f);

	TArray<TEnumAsByte<EObjectTypeQuery>> ObjectTypes;
	ObjectTypes.Add(UEngineTypes::ConvertToObjectType(ECC_WorldDynamic));
	ObjectTypes.Add(UEngineTypes::ConvertToObjectType(ECC_WorldStatic));
	ObjectTypes.Add(UEngineTypes::ConvertToObjectType(ECC_Pawn));

	TArray<AActor*> ActorsToIgnore;
	ActorsToIgnore.Add(this);

	TArray<FHitResult> HitResults;
	bool bHit = UKismetSystemLibrary::SphereTraceMultiForObjects(
		GetWorld(), Start, End, 280.0f,
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

		// If interacting with an archive terminal, display modal on HUD
		if (APlayerController* PC = Cast<APlayerController>(Controller))
		{
			if (ASVHUD* HUD = Cast<ASVHUD>(PC->GetHUD()))
			{
				// Retrieve Title and Description from terminal
				FProperty* TitleProp = CurrentFocusedInteractable->GetClass()->FindPropertyByName(TEXT("ArchiveTitle"));
				FProperty* DescProp = CurrentFocusedInteractable->GetClass()->FindPropertyByName(TEXT("ArchiveDescription"));
				if (TitleProp && DescProp)
				{
					const FText* TitleVal = TitleProp->ContainerPtrToValuePtr<FText>(CurrentFocusedInteractable);
					const FText* DescVal = DescProp->ContainerPtrToValuePtr<FText>(CurrentFocusedInteractable);
					if (TitleVal && DescVal)
					{
						HUD->DisplayArchiveRecord(*TitleVal, *DescVal);
					}
				}
			}
		}
	}
}

void ASVCharacter::Strike()
{
	bIsAttacking = true;
	ComboStep = (ComboStep + 1) % 3;
	AttackResetTimer = 0.85f;
}

bool ASVCharacter::TryDeflectAttack(float IncomingDamage, AActor* Attacker)
{
	if (bIsParrying)
	{
		OnParrySuccess.Broadcast();
		return true;
	}
	else if (bIsBlocking && CurrentQi >= 15.0f)
	{
		CurrentQi -= 15.0f;
		OnQiChanged.Broadcast(CurrentQi, MaxQi);
		TakeDamageAmount(IncomingDamage * 0.25f);
		return true;
	}

	TakeDamageAmount(IncomingDamage);
	return false;
}

void ASVCharacter::TakeDamageAmount(float Damage)
{
	CurrentHealth = FMath::Clamp(CurrentHealth - Damage, 0.0f, MaxHealth);
	OnHealthChanged.Broadcast(CurrentHealth, MaxHealth);
}

void ASVCharacter::ResetHealth()
{
	CurrentHealth = MaxHealth;
	CurrentQi = MaxQi;
	OnHealthChanged.Broadcast(CurrentHealth, MaxHealth);
	OnQiChanged.Broadcast(CurrentQi, MaxQi);
}
