// Copyright SparkVision Dhaka University. All Rights Reserved.

#include "SVCharacter.h"
#include "Camera/CameraComponent.h"
#include "Components/CapsuleComponent.h"
#include "Components/InputComponent.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "GameFramework/Controller.h"
#include "GameFramework/SpringArmComponent.h"
#include "EnhancedInputComponent.h"
#include "EnhancedInputSubsystems.h"
#include "InputMappingContext.h"
#include "InputAction.h"
#include "InputActionValue.h"
#include "UObject/ConstructorHelpers.h"
#include "Engine/LocalPlayer.h"
#include "Kismet/GameplayStatics.h"
#include "Kismet/KismetSystemLibrary.h"
#include "SVHUD.h"
#include "SVMissionControlSubsystem.h"
#include "SVSaveGame.h"

ASVCharacter::ASVCharacter()
{
	PrimaryActorTick.bCanEverTick = true;

	GetCapsuleComponent()->InitCapsuleSize(42.f, 96.0f);
	GetCapsuleComponent()->SetCollisionProfileName(TEXT("Pawn"));

	bUseControllerRotationPitch = false;
	bUseControllerRotationYaw = false;
	bUseControllerRotationRoll = false;

	GetCharacterMovement()->bOrientRotationToMovement = true;
	GetCharacterMovement()->RotationRate = FRotator(0.0f, 540.0f, 0.0f);
	GetCharacterMovement()->JumpZVelocity = 650.f;
	GetCharacterMovement()->AirControl = 0.35f;
	GetCharacterMovement()->MaxWalkSpeed = 550.f; // Standard walking/jogging speed
	GetCharacterMovement()->MinAnalogWalkSpeed = 20.f;
	GetCharacterMovement()->BrakingDecelerationWalking = 2048.f;
	GetCharacterMovement()->BrakingDecelerationFalling = 1500.0f;
	GetCharacterMovement()->GravityScale = 1.5f;

	CameraBoom = CreateDefaultSubobject<USpringArmComponent>(TEXT("CameraBoom"));
	CameraBoom->SetupAttachment(RootComponent);
	CameraBoom->TargetArmLength = 380.0f;
	CameraBoom->bUsePawnControlRotation = true;
	CameraBoom->bEnableCameraLag = true;
	CameraBoom->CameraLagSpeed = 4.0f;
	CameraBoom->SocketOffset = FVector(0.0f, 45.0f, 25.0f);
	CameraBoom->ProbeSize = 12.0f;
	CameraBoom->ProbeChannel = ECC_Camera;

	FollowCamera = CreateDefaultSubobject<UCameraComponent>(TEXT("FollowCamera"));
	FollowCamera->SetupAttachment(CameraBoom, USpringArmComponent::SocketName);
	FollowCamera->bUsePawnControlRotation = false;
	FollowCamera->FieldOfView = 75.0f;

	// Load Quinn mannequin mesh
	static ConstructorHelpers::FObjectFinder<USkeletalMesh> MeshAsset(TEXT("/Game/Characters/Mannequins/Meshes/SKM_Quinn_Simple.SKM_Quinn_Simple"));
	if (MeshAsset.Succeeded())
	{
		GetMesh()->SetSkeletalMesh(MeshAsset.Object);
		GetMesh()->SetRelativeLocation(FVector(0.0f, 0.0f, -90.0f));
		GetMesh()->SetRelativeRotation(FRotator(0.0f, -90.0f, 0.0f));
	}

	// Load Unarmed animation blueprint
	static ConstructorHelpers::FClassFinder<UAnimInstance> AnimBpClass(TEXT("/Game/Characters/Mannequins/Anims/Unarmed/ABP_Unarmed.ABP_Unarmed_C"));
	if (AnimBpClass.Succeeded())
	{
		GetMesh()->SetAnimInstanceClass(AnimBpClass.Class);
	}

	// Enhanced Input Assets
	static ConstructorHelpers::FObjectFinder<UInputMappingContext> IMC_DefaultFinder(TEXT("/Game/ThirdPerson/Input/IMC_Default.IMC_Default"));
	if (IMC_DefaultFinder.Succeeded()) DefaultMappingContext = IMC_DefaultFinder.Object;

	static ConstructorHelpers::FObjectFinder<UInputMappingContext> IMC_MouseLookFinder(TEXT("/Game/ThirdPerson/Input/IMC_MouseLook.IMC_MouseLook"));
	if (IMC_MouseLookFinder.Succeeded()) MouseLookMappingContext = IMC_MouseLookFinder.Object;

	static ConstructorHelpers::FObjectFinder<UInputAction> IA_MoveFinder(TEXT("/Game/ThirdPerson/Input/Actions/IA_Move.IA_Move"));
	if (IA_MoveFinder.Succeeded()) MoveAction = IA_MoveFinder.Object;

	static ConstructorHelpers::FObjectFinder<UInputAction> IA_LookFinder(TEXT("/Game/ThirdPerson/Input/Actions/IA_Look.IA_Look"));
	if (IA_LookFinder.Succeeded()) LookAction = IA_LookFinder.Object;

	static ConstructorHelpers::FObjectFinder<UInputAction> IA_MouseLookFinder(TEXT("/Game/ThirdPerson/Input/Actions/IA_MouseLook.IA_MouseLook"));
	if (IA_MouseLookFinder.Succeeded()) MouseLookAction = IA_MouseLookFinder.Object;

	static ConstructorHelpers::FObjectFinder<UInputAction> IA_JumpFinder(TEXT("/Game/ThirdPerson/Input/Actions/IA_Jump.IA_Jump"));
	if (IA_JumpFinder.Succeeded()) JumpAction = IA_JumpFinder.Object;

	static ConstructorHelpers::FObjectFinder<UInputAction> IA_InteractFinder(TEXT("/Game/ThirdPerson/Input/Actions/IA_Interact.IA_Interact"));
	if (IA_InteractFinder.Succeeded()) InteractAction = IA_InteractFinder.Object;

	static ConstructorHelpers::FObjectFinder<UInputAction> IA_SprintFinder(TEXT("/Game/ThirdPerson/Input/Actions/IA_Sprint.IA_Sprint"));
	if (IA_SprintFinder.Succeeded()) SprintAction = IA_SprintFinder.Object;

	CurrentHealth = MaxHealth;
	CurrentQi = MaxQi;
	ActiveMissionId = TEXT("L1_M01");
}

void ASVCharacter::BeginPlay()
{
	Super::BeginPlay();

	SpawnLocation = GetActorLocation();

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

		PlayerController->PlayerCameraManager->ViewPitchMin = -60.0f;
		PlayerController->PlayerCameraManager->ViewPitchMax = 45.0f;
	}

	// Initialize Java Mission Control session
	if (UGameInstance* GI = GetGameInstance())
	{
		if (USVMissionControlSubsystem* MCSubsystem = GI->GetSubsystem<USVMissionControlSubsystem>())
		{
			FString SessionId = FString::Printf(TEXT("DU_Session_%lld"), FDateTime::Now().ToUnixTimestamp());
			MCSubsystem->StartSession(SessionId, TEXT("chapter-01"));
			MCSubsystem->CheckHealth();
		}
	}

	UE_LOG(LogTemp, Log, TEXT("[ASVCharacter] Spawned at %s. Active Mission: %s"), *SpawnLocation.ToString(), *ActiveMissionId);
}

void ASVCharacter::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);

	UpdateCameraFraming(DeltaTime);
	UpdateVitals(DeltaTime);

	// CPU Optimization: Throttle interactable trace to 10 Hz (every 0.10s)
	TimeSinceLastInteractScan += DeltaTime;
	if (TimeSinceLastInteractScan >= 0.10f)
	{
		ScanForInteractables();
		TimeSinceLastInteractScan = 0.0f;
	}

	// CPU Optimization: Throttle mission progression check to 4 Hz (every 0.25s)
	TimeSinceLastMissionCheck += DeltaTime;
	if (TimeSinceLastMissionCheck >= 0.25f)
	{
		CheckMissionProgression();
		TimeSinceLastMissionCheck = 0.0f;
	}
}

void ASVCharacter::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{
	Super::SetupPlayerInputComponent(PlayerInputComponent);

	if (UEnhancedInputComponent* EnhancedInputComponent = Cast<UEnhancedInputComponent>(PlayerInputComponent))
	{
		if (JumpAction)
		{
			EnhancedInputComponent->BindAction(JumpAction, ETriggerEvent::Started, this, &ASVCharacter::OnKeySpace);
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
		if (MouseLookAction)
		{
			EnhancedInputComponent->BindAction(MouseLookAction, ETriggerEvent::Triggered, this, &ASVCharacter::MouseLook);
		}
		if (InteractAction)
		{
			EnhancedInputComponent->BindAction(InteractAction, ETriggerEvent::Started, this, &ASVCharacter::Interact);
		}
		if (SprintAction)
		{
			EnhancedInputComponent->BindAction(SprintAction, ETriggerEvent::Started, this, &ASVCharacter::StartSprint);
			EnhancedInputComponent->BindAction(SprintAction, ETriggerEvent::Completed, this, &ASVCharacter::StopSprint);
		}
	}

	// Direct Key & Axis Bindings (Dual-Layer Fallback for bulletproof controls)
	PlayerInputComponent->BindAxisKey(EKeys::W, this, &ASVCharacter::MoveForwardDirect);
	PlayerInputComponent->BindAxisKey(EKeys::S, this, &ASVCharacter::MoveBackwardDirect);
	PlayerInputComponent->BindAxisKey(EKeys::D, this, &ASVCharacter::MoveRightDirect);
	PlayerInputComponent->BindAxisKey(EKeys::A, this, &ASVCharacter::MoveLeftDirect);

	PlayerInputComponent->BindAxisKey(EKeys::Up, this, &ASVCharacter::MoveForwardDirect);
	PlayerInputComponent->BindAxisKey(EKeys::Down, this, &ASVCharacter::MoveBackwardDirect);
	PlayerInputComponent->BindAxisKey(EKeys::Right, this, &ASVCharacter::MoveRightDirect);
	PlayerInputComponent->BindAxisKey(EKeys::Left, this, &ASVCharacter::MoveLeftDirect);

	PlayerInputComponent->BindAxisKey(EKeys::MouseX, this, &ASVCharacter::LookYawDirect);
	PlayerInputComponent->BindAxisKey(EKeys::MouseY, this, &ASVCharacter::LookPitchDirect);

	PlayerInputComponent->BindKey(EKeys::SpaceBar, IE_Pressed, this, &ASVCharacter::OnKeySpace);
	PlayerInputComponent->BindKey(EKeys::SpaceBar, IE_Released, this, &ACharacter::StopJumping);

	PlayerInputComponent->BindKey(EKeys::LeftShift, IE_Pressed, this, &ASVCharacter::StartSprint);
	PlayerInputComponent->BindKey(EKeys::LeftShift, IE_Released, this, &ASVCharacter::StopSprint);

	PlayerInputComponent->BindKey(EKeys::E, IE_Pressed, this, &ASVCharacter::Interact);
	PlayerInputComponent->BindKey(EKeys::Escape, IE_Pressed, this, &ASVCharacter::OnKeyEsc);
	PlayerInputComponent->BindKey(EKeys::P, IE_Pressed, this, &ASVCharacter::OnKeyEsc);

	// Number keys (1 - 6) for Menus or Landmark Fast Travel
	PlayerInputComponent->BindKey(EKeys::One, IE_Pressed, this, &ASVCharacter::OnKey1);
	PlayerInputComponent->BindKey(EKeys::Two, IE_Pressed, this, &ASVCharacter::OnKey2);
	PlayerInputComponent->BindKey(EKeys::Three, IE_Pressed, this, &ASVCharacter::OnKey3);
	PlayerInputComponent->BindKey(EKeys::Four, IE_Pressed, this, &ASVCharacter::OnKey4);
	PlayerInputComponent->BindKey(EKeys::Five, IE_Pressed, this, &ASVCharacter::OnKey5);
	PlayerInputComponent->BindKey(EKeys::Six, IE_Pressed, this, &ASVCharacter::OnKey6);
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

void ASVCharacter::OnKeySpace()
{
	// Check if HUD is showing archive modal or dialogue or victory
	if (APlayerController* PC = Cast<APlayerController>(Controller))
	{
		if (ASVHUD* HUD = Cast<ASVHUD>(PC->GetHUD()))
		{
			HUD->DismissArchiveRecord();
			HUD->DismissNPCDialogue();
			HUD->DismissChapterVictory();
		}
	}

	bHasJumped = true;
	Jump();
}

void ASVCharacter::OnKeyEsc()
{
	if (APlayerController* PC = Cast<APlayerController>(Controller))
	{
		if (ASVHUD* HUD = Cast<ASVHUD>(PC->GetHUD()))
		{
			HUD->TogglePauseMenu();
		}
	}
}

void ASVCharacter::OnNumberKeyPressed(int32 Number)
{
	if (APlayerController* PC = Cast<APlayerController>(Controller))
	{
		if (ASVHUD* HUD = Cast<ASVHUD>(PC->GetHUD()))
		{
			if (HUD->IsMenuOpen())
			{
				HUD->HandleMenuAction(Number);
				return;
			}
		}
	}

	// If no menu is open, handle Fast Travel
	switch (Number)
	{
	case 1: TeleportToCurzon(); break;
	case 2: TeleportToDoyel(); break;
	case 3: TeleportToShaheedMinar(); break;
	case 4: TeleportToTSC(); break;
	case 5: TeleportToLibrary(); break;
	case 6: TeleportToKalaBhaban(); break;
	default: break;
	}
}

void ASVCharacter::StartSprint()
{
	if (CurrentQi > 10.0f)
	{
		bIsSprinting = true;
		GetCharacterMovement()->MaxWalkSpeed = 950.0f;
	}
}

void ASVCharacter::StopSprint()
{
	bIsSprinting = false;
	GetCharacterMovement()->MaxWalkSpeed = 550.0f;
}

void ASVCharacter::Dash()
{
	if (CurrentQi >= 25.0f)
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

	// CPU Optimization: If player hasn't moved more than 200 units since last query, return cached landmark
	if (!CachedLandmarkName.IsEmpty() && FVector::DistSquared2D(MyLoc, CachedLandmarkQueryLocation) < 40000.0f)
	{
		return CachedLandmarkName;
	}

	CachedLandmarkQueryLocation = MyLoc;

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
			CachedLandmarkName = Z.Name;
			return CachedLandmarkName;
		}
	}
	CachedLandmarkName = TEXT("University of Dhaka Campus | ঢাকা বিশ্ববিদ্যালয়");
	return CachedLandmarkName;
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
	else
	{
		if (CurrentQi < MaxQi)
		{
			CurrentQi = FMath::Clamp(CurrentQi + (25.0f * DeltaTime), 0.0f, MaxQi);
			OnQiChanged.Broadcast(CurrentQi, MaxQi);
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
				FProperty* TitleProp = CurrentFocusedInteractable->GetClass()->FindPropertyByName(TEXT("ArchiveTitle"));
				FProperty* DescProp = CurrentFocusedInteractable->GetClass()->FindPropertyByName(TEXT("ArchiveDescription"));
				FProperty* IdProp = CurrentFocusedInteractable->GetClass()->FindPropertyByName(TEXT("ArchiveId"));
				if (TitleProp && DescProp)
				{
					const FText* TitleVal = TitleProp->ContainerPtrToValuePtr<FText>(CurrentFocusedInteractable);
					const FText* DescVal = DescProp->ContainerPtrToValuePtr<FText>(CurrentFocusedInteractable);
					if (TitleVal && DescVal)
					{
						HUD->DisplayArchiveRecord(*TitleVal, *DescVal);
					}
				}
				if (IdProp)
				{
					const FString* IdVal = IdProp->ContainerPtrToValuePtr<FString>(CurrentFocusedInteractable);
					if (IdVal)
					{
						OnArchiveRecovered(*IdVal);
					}
				}
			}
		}
	}
}

void ASVCharacter::OnNPCSpoken(const FString& InNPCId)
{
	if (!SpokenNPCIds.Contains(InNPCId))
	{
		SpokenNPCIds.Add(InNPCId);
		UE_LOG(LogTemp, Log, TEXT("[ASVCharacter] Spoken with NPC: %s. Total spoken: %d"), *InNPCId, SpokenNPCIds.Num());
		CheckMissionProgression();
	}
}

void ASVCharacter::OnArchiveRecovered(const FString& InArchiveId)
{
	if (!DiscoveredArchiveIds.Contains(InArchiveId))
	{
		DiscoveredArchiveIds.Add(InArchiveId);
		UE_LOG(LogTemp, Log, TEXT("[ASVCharacter] Secured archive: %s. Total archives: %d/5"), *InArchiveId, DiscoveredArchiveIds.Num());
		CheckMissionProgression();
	}
}

void ASVCharacter::CheckMissionProgression()
{
	FString OldMission = ActiveMissionId;

	// Track landmark visits
	FString CurrentLandmark = GetCurrentLandmarkName();
	if (!CurrentLandmark.Contains(TEXT("Campus")) && !VisitedLandmarkNames.Contains(CurrentLandmark))
	{
		VisitedLandmarkNames.Add(CurrentLandmark);
	}

	// L1_M01: Move and jump
	if (ActiveMissionId == TEXT("L1_M01"))
	{
		if (FVector::Dist2D(GetActorLocation(), SpawnLocation) > 400.0f || bHasJumped)
		{
			ActiveMissionId = TEXT("L1_M02");
			OnMissionUpdated.Broadcast(ActiveMissionId, GetActiveMissionDescription());
		}
	}
	// L1_M02: Visit at least 2 distinct landmarks
	else if (ActiveMissionId == TEXT("L1_M02"))
	{
		if (VisitedLandmarkNames.Num() >= 2)
		{
			ActiveMissionId = TEXT("L1_M03");
			OnMissionUpdated.Broadcast(ActiveMissionId, GetActiveMissionDescription());
		}
	}
	// L1_M03: Speak with student organizers
	else if (ActiveMissionId == TEXT("L1_M03"))
	{
		if (SpokenNPCIds.Num() >= 1)
		{
			ActiveMissionId = TEXT("L1_M04");
			OnMissionUpdated.Broadcast(ActiveMissionId, GetActiveMissionDescription());
		}
	}
	// L1_M04: Recover all 5 historical archives
	else if (ActiveMissionId == TEXT("L1_M04"))
	{
		if (DiscoveredArchiveIds.Num() >= 5)
		{
			ActiveMissionId = TEXT("L1_M05");
			OnMissionUpdated.Broadcast(ActiveMissionId, GetActiveMissionDescription());
		}
	}
	// L1_M05: Reach TSC / Raju Memorial Assembly
	else if (ActiveMissionId == TEXT("L1_M05"))
	{
		FVector TSCLocation(59000.0f, -63700.0f, 50.0f);
		if (FVector::Dist2D(GetActorLocation(), TSCLocation) <= 4000.0f)
		{
			ActiveMissionId = TEXT("L1_M06");
			OnMissionUpdated.Broadcast(ActiveMissionId, GetActiveMissionDescription());
			CompleteLevel1Chapter();
		}
	}

	if (OldMission != ActiveMissionId)
	{
		UE_LOG(LogTemp, Log, TEXT("[ASVCharacter] Mission Advanced: %s -> %s"), *OldMission, *ActiveMissionId);
		SaveGameProgress();
	}
}

void ASVCharacter::CompleteLevel1Chapter()
{
	if (bLevel1Completed) return;

	bLevel1Completed = true;
	bLevel2Unlocked = true;

	UE_LOG(LogTemp, Log, TEXT("[ASVCharacter] *** LEVEL 1 COMPLETED! Chapter 2 Unlocked! ***"));

	// Notify Java Mission Control
	if (UGameInstance* GI = GetGameInstance())
	{
		if (USVMissionControlSubsystem* MCSubsystem = GI->GetSubsystem<USVMissionControlSubsystem>())
		{
			MCSubsystem->ReportLevel1Victory();
		}
	}

	// Display Victory Modal on HUD
	if (APlayerController* PC = Cast<APlayerController>(Controller))
	{
		if (ASVHUD* HUD = Cast<ASVHUD>(PC->GetHUD()))
		{
			HUD->DisplayChapterVictory(
				FText::FromString(TEXT("“আমিও থাকব।”")),
				FText::FromString(TEXT("July 14, 2024 — University of Dhaka")),
				FText::FromString(TEXT("CHAPTER 2 UNLOCKED: The Day the Streets Changed (July 15, 2024)"))
			);
		}
	}

	SaveGameProgress();
}

FText ASVCharacter::GetActiveMissionDescription() const
{
	if (ActiveMissionId == TEXT("L1_M01"))
		return FText::FromString(TEXT("Campus Arrival: Explore basic locomotion, camera orbit, sprint [Shift], and jump [Space]."));
	if (ActiveMissionId == TEXT("L1_M02"))
		return FText::FromString(TEXT("Landmark Survey: Traverse Dhaka University landmarks [1-6 Fast Travel available]."));
	if (ActiveMissionId == TEXT("L1_M03"))
		return FText::FromString(TEXT("Voices of the Campus: Speak with student organizers [E] near Curzon, Library, or TSC."));
	if (ActiveMissionId == TEXT("L1_M04"))
		return FText::FromString(TEXT("Securing the Archives: Recover all 5 Historical Heritage Terminals across campus."));
	if (ActiveMissionId == TEXT("L1_M05"))
		return FText::FromString(TEXT("Solidarity Assembly: Gather at Raju Anti-Terrorism Memorial Plaza at TSC Mor."));
	if (ActiveMissionId == TEXT("L1_M06"))
		return FText::FromString(TEXT("The July 14 Pledge: Confirm solidarity — 'আমিও থাকব।' (I will be there too)."));

	return FText::FromString(TEXT("Dhaka University Campus Exploration"));
}

void ASVCharacter::SaveGameProgress(const FString& SlotName)
{
	USVSaveGame* SaveInstance = Cast<USVSaveGame>(UGameplayStatics::CreateSaveGameObject(USVSaveGame::StaticClass()));
	if (!SaveInstance) return;

	SaveInstance->SaveSlotName = SlotName;
	SaveInstance->Timestamp = FDateTime::Now();
	SaveInstance->PlayerLocation = GetActorLocation();
	SaveInstance->PlayerRotation = GetActorRotation();
	SaveInstance->CurrentChapter = TEXT("chapter-01");
	SaveInstance->ActiveMissionId = ActiveMissionId;
	SaveInstance->DiscoveredArchives = DiscoveredArchiveIds;
	SaveInstance->SpokenNPCs = SpokenNPCIds;
	SaveInstance->VisitedLandmarks = VisitedLandmarkNames;
	SaveInstance->bLevel1Completed = bLevel1Completed;
	SaveInstance->bLevel2Unlocked = bLevel2Unlocked;

	UGameplayStatics::SaveGameToSlot(SaveInstance, SlotName, 0);
	UE_LOG(LogTemp, Log, TEXT("[ASVCharacter] Game progress successfully saved to slot: %s"), *SlotName);
}

bool ASVCharacter::LoadGameProgress(const FString& SlotName)
{
	if (!UGameplayStatics::DoesSaveGameExist(SlotName, 0))
	{
		UE_LOG(LogTemp, Warning, TEXT("[ASVCharacter] No savegame found at slot: %s"), *SlotName);
		return false;
	}

	USVSaveGame* LoadedGame = Cast<USVSaveGame>(UGameplayStatics::LoadGameFromSlot(SlotName, 0));
	if (!LoadedGame) return false;

	SetActorLocationAndRotation(LoadedGame->PlayerLocation, LoadedGame->PlayerRotation, false, nullptr, ETeleportType::ResetPhysics);
	ActiveMissionId = LoadedGame->ActiveMissionId;
	DiscoveredArchiveIds = LoadedGame->DiscoveredArchives;
	SpokenNPCIds = LoadedGame->SpokenNPCs;
	VisitedLandmarkNames = LoadedGame->VisitedLandmarks;
	bLevel1Completed = LoadedGame->bLevel1Completed;
	bLevel2Unlocked = LoadedGame->bLevel2Unlocked;

	UE_LOG(LogTemp, Log, TEXT("[ASVCharacter] Successfully loaded savegame from slot: %s. Mission: %s, Archives: %d"),
		*SlotName, *ActiveMissionId, DiscoveredArchiveIds.Num());

	return true;
}
