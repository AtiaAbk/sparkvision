// Copyright SparkVision Dhaka University. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "SVInteractableInterface.h"
#include "SVSaveGame.h"
#include "SVCharacter.generated.h"

class USpringArmComponent;
class UCameraComponent;
class UInputMappingContext;
class UInputAction;
struct FInputActionValue;

USTRUCT(BlueprintType)
struct FSVWaypoint
{
	GENERATED_BODY()

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SparkVision|Waypoint")
	FString Id;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SparkVision|Waypoint")
	FText NameBengali;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SparkVision|Waypoint")
	FText NameEnglish;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SparkVision|Waypoint")
	FVector Location = FVector::ZeroVector;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SparkVision|Waypoint")
	float Radius = 2500.0f;

	UPROPERTY(BlueprintReadOnly, Category = "SparkVision|Waypoint")
	bool bVisited = false;
};

DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnNearbyInteractableChanged, const FText&, PromptText);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnHealthChangedSignature, float, CurrentHealth, float, MaxHealth);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnQiChangedSignature, float, CurrentQi, float, MaxQi);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnCombatVictorySignature);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnParrySuccessSignature);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnMissionUpdatedSignature, const FString&, MissionId, const FText&, MissionDesc);

UCLASS()
class MYPROJECT_API ASVCharacter : public ACharacter
{
	GENERATED_BODY()

public:
	ASVCharacter();

protected:
	virtual void BeginPlay() override;
	virtual void Tick(float DeltaTime) override;
	virtual void SetupPlayerInputComponent(class UInputComponent* PlayerInputComponent) override;
	virtual void Landed(const FHitResult& Hit) override;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = Camera)
	USpringArmComponent* CameraBoom;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = Camera)
	UCameraComponent* FollowCamera;

	/** Enhanced Input assets */
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = Input)
	UInputMappingContext* DefaultMappingContext;

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = Input)
	UInputMappingContext* MouseLookMappingContext;

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = Input)
	UInputAction* MoveAction;

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = Input)
	UInputAction* LookAction;

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = Input)
	UInputAction* JumpAction;

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = Input)
	UInputAction* MouseLookAction;

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = Input)
	UInputAction* InteractAction;

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = Input)
	UInputAction* SprintAction;

	void Move(const FInputActionValue& Value);
	void Look(const FInputActionValue& Value);
	void MouseLook(const FInputActionValue& Value);

public:
	UFUNCTION(BlueprintCallable, Category = "SparkVision|Controls")
	void Interact();

	UFUNCTION(BlueprintCallable, Category = "SparkVision|Controls")
	void StartSprint();

	UFUNCTION(BlueprintCallable, Category = "SparkVision|Controls")
	void StopSprint();

	UFUNCTION(BlueprintCallable, Category = "SparkVision|Controls")
	void Dash();

	UFUNCTION(BlueprintCallable, Category = "SparkVision|Combat")
	void PerformLightStrike();

	UFUNCTION(BlueprintCallable, Category = "SparkVision|Combat")
	void StartParry();

	UFUNCTION(BlueprintCallable, Category = "SparkVision|Combat")
	void StopParry();

	/** Direct Keyboard/Mouse Fallback Handlers */
	void MoveForwardDirect(float Val);
	void MoveBackwardDirect(float Val);
	void MoveRightDirect(float Val);
	void MoveLeftDirect(float Val);
	void LookYawDirect(float Val);
	void LookPitchDirect(float Val);

	/** Number Key and Menu Handlers */
	void OnNumberKeyPressed(int32 Number);
	void OnKey1() { OnNumberKeyPressed(1); }
	void OnKey2() { OnNumberKeyPressed(2); }
	void OnKey3() { OnNumberKeyPressed(3); }
	void OnKey4() { OnNumberKeyPressed(4); }
	void OnKey5() { OnNumberKeyPressed(5); }
	void OnKey6() { OnNumberKeyPressed(6); }
	void OnKeyEsc();
	void OnKeySpace();
	void OnKeySpaceReleased();
	void OnKeyEnter();
	void OnMenuUp();
	void OnMenuDown();
	void OnKeyTab();

	/** Campus Landmark Fast Travel */
	UFUNCTION(BlueprintCallable, Category = "SparkVision|FastTravel")
	void TeleportToCurzon();

	UFUNCTION(BlueprintCallable, Category = "SparkVision|FastTravel")
	void TeleportToDoyel();

	UFUNCTION(BlueprintCallable, Category = "SparkVision|FastTravel")
	void TeleportToShaheedMinar();

	UFUNCTION(BlueprintCallable, Category = "SparkVision|FastTravel")
	void TeleportToTSC();

	UFUNCTION(BlueprintCallable, Category = "SparkVision|FastTravel")
	void TeleportToLibrary();

	UFUNCTION(BlueprintCallable, Category = "SparkVision|FastTravel")
	void TeleportToKalaBhaban();

	/** Character Selection & Customization */
	UPROPERTY(BlueprintReadOnly, Category = "SparkVision|Character")
	bool bIsFemaleProtagonist = false;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SparkVision|Character")
	int32 ProtagonistOutfitStyle = 0;

	UFUNCTION(BlueprintCallable, Category = "SparkVision|Character")
	void SelectProtagonist(bool bFemale);

	UFUNCTION(BlueprintCallable, Category = "SparkVision|Character")
	void SetProtagonistOutfit(int32 OutfitIndex);

	/** 5 Landmark Waypoints & Climax Mission */
	UPROPERTY(BlueprintReadOnly, Category = "SparkVision|Mission")
	TArray<FSVWaypoint> CampusWaypoints;

	UPROPERTY(BlueprintReadOnly, Category = "SparkVision|Mission")
	int32 ActiveWaypointIndex = 0;

	UPROPERTY(BlueprintReadOnly, Category = "SparkVision|Mission")
	bool bAllWaypointsVisited = false;

	UPROPERTY(BlueprintReadOnly, Category = "SparkVision|Mission")
	bool bClimaxEncounterActive = false;

	UPROPERTY(BlueprintReadOnly, Category = "SparkVision|Mission")
	int32 ClimaxRetryCount = 0;

	UPROPERTY(BlueprintReadOnly, Category = "SparkVision|Mission")
	bool bIsArrested = false;

	UFUNCTION(BlueprintPure, Category = "SparkVision|Mission")
	FSVWaypoint GetActiveWaypoint() const;

	void CheckLandmarkWaypoints();
	void TriggerPoliceArrest(const FString& InVictimName);
	void TriggerClimaxDefeat();
	void RetryClimaxCombat();
	void SpawnClimaxCadreSquad();

	/** Vitals (Health & Qi stamina) */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SparkVision|Vitals")
	float MaxHealth = 100.0f;

	UPROPERTY(BlueprintReadOnly, Category = "SparkVision|Vitals")
	float CurrentHealth = 100.0f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SparkVision|Vitals")
	float MaxQi = 100.0f;

	UPROPERTY(BlueprintReadOnly, Category = "SparkVision|Vitals")
	float CurrentQi = 100.0f;

	UPROPERTY(BlueprintReadOnly, Category = "SparkVision|Controls")
	bool bIsSprinting = false;

	UPROPERTY(BlueprintReadOnly, Category = "SparkVision|Controls")
	bool bIsAirGliding = false;

	UPROPERTY(BlueprintReadOnly, Category = "SparkVision|Controls")
	bool bIsParrying = false;

	UPROPERTY(BlueprintReadOnly, Category = "SparkVision|Controls")
	bool bIsBlocking = false;

	UPROPERTY(BlueprintAssignable, Category = "SparkVision|Vitals")
	FOnHealthChangedSignature OnHealthChanged;

	UPROPERTY(BlueprintAssignable, Category = "SparkVision|Vitals")
	FOnQiChangedSignature OnQiChanged;

	UPROPERTY(BlueprintAssignable, Category = "SparkVision|Combat")
	FOnParrySuccessSignature OnParrySuccess;

	UPROPERTY(BlueprintAssignable, Category = "SparkVision|Combat")
	FOnCombatVictorySignature OnCombatVictory;

	UPROPERTY(BlueprintAssignable, Category = "SparkVision|Interaction")
	FOnNearbyInteractableChanged OnNearbyInteractableChanged;

	UPROPERTY(BlueprintAssignable, Category = "SparkVision|Mission")
	FOnMissionUpdatedSignature OnMissionUpdated;

	UFUNCTION(BlueprintCallable, Category = "SparkVision|Combat")
	void TakeDamageAmount(float Damage, AActor* DamageCauser = nullptr);

	UFUNCTION(BlueprintPure, Category = "SparkVision|Vitals")
	float GetHealthPercent() const { return (MaxHealth > 0.f) ? (CurrentHealth / MaxHealth) : 0.f; }

	UFUNCTION(BlueprintPure, Category = "SparkVision|Vitals")
	float GetQiPercent() const { return (MaxQi > 0.f) ? (CurrentQi / MaxQi) : 0.f; }

	UFUNCTION(BlueprintPure, Category = "SparkVision|Interaction")
	FText GetCurrentPromptText() const { return CurrentPromptText; }

	FString GetCurrentLandmarkName() const;

	/** Mission Progression & Quest System */
	UPROPERTY(BlueprintReadOnly, Category = "SparkVision|Mission")
	FString ActiveMissionId = TEXT("L1_M01");

	UPROPERTY(BlueprintReadOnly, Category = "SparkVision|Mission")
	TArray<FString> DiscoveredArchiveIds;

	UPROPERTY(BlueprintReadOnly, Category = "SparkVision|Mission")
	TArray<FString> SpokenNPCIds;

	UPROPERTY(BlueprintReadOnly, Category = "SparkVision|Mission")
	TArray<FString> VisitedLandmarkNames;

	UPROPERTY(BlueprintReadOnly, Category = "SparkVision|Mission")
	bool bLevel1Completed = false;

	UPROPERTY(BlueprintReadOnly, Category = "SparkVision|Mission")
	bool bLevel2Unlocked = false;

	void OnNPCSpoken(const FString& InNPCId);
	void OnArchiveRecovered(const FString& InArchiveId);
	void CheckMissionProgression();
	void CompleteLevel1Chapter();

	UFUNCTION(BlueprintPure, Category = "SparkVision|Mission")
	FText GetActiveMissionDescription() const;

	UFUNCTION(BlueprintPure, Category = "SparkVision|Mission")
	int32 GetDiscoveredArchiveCount() const { return DiscoveredArchiveIds.Num(); }

	/** Persistence */
	UFUNCTION(BlueprintCallable, Category = "SparkVision|Persistence")
	void SaveGameProgress(const FString& SlotName = TEXT("SVSave_Slot0"));

	UFUNCTION(BlueprintCallable, Category = "SparkVision|Persistence")
	bool LoadGameProgress(const FString& SlotName = TEXT("SVSave_Slot0"));

private:
	void ScanForInteractables();
	void UpdateCameraFraming(float DeltaTime);
	void UpdateVitals(float DeltaTime);

	UPROPERTY()
	AActor* CurrentFocusedInteractable = nullptr;

	FText CurrentPromptText;

	// Initial movement detection for L1_M01
	FVector SpawnLocation;
	bool bHasMovedSignificantly = false;
	bool bHasJumped = false;

	// Camera Framing Targets
	float TargetArmDistance = 380.0f;
	float TargetFOV = 75.0f;
	FVector TargetSocketOffset = FVector(0.0f, 45.0f, 25.0f);

	// Where Winds Meet Wuxia Mechanics State
	int32 AirLeapCount = 0;
	float ParryWindowTimer = 0.0f;
	const float MaxParryWindow = 0.45f;
	bool bParryKeyDown = false;
	float CurrentBankRoll = 0.0f;
	float PreviousActorYaw = 0.0f;

	// CPU Optimization: Frequency Throttling for Traces & Queries
	float TimeSinceLastInteractScan = 0.0f;
	float TimeSinceLastMissionCheck = 0.0f;
	mutable FString CachedLandmarkName;
	mutable FVector CachedLandmarkQueryLocation = FVector::ZeroVector;
};
