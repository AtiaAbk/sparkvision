// Copyright SparkVision Dhaka University. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "SVInteractableInterface.h"
#include "SVCharacter.generated.h"

class USpringArmComponent;
class UCameraComponent;
class UInputMappingContext;
class UInputAction;
struct FInputActionValue;

DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnNearbyInteractableChanged, const FText&, PromptText);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnHealthChangedSignature, float, CurrentHealth, float, MaxHealth);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnQiChangedSignature, float, CurrentQi, float, MaxQi);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnCombatVictorySignature);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnParrySuccessSignature);

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

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = Camera)
	USpringArmComponent* CameraBoom;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = Camera)
	UCameraComponent* FollowCamera;

	/** Input actions */
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = Input)
	UInputMappingContext* DefaultMappingContext;

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = Input)
	UInputAction* MoveAction;

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = Input)
	UInputAction* LookAction;

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = Input)
	UInputAction* JumpAction;

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = Input)
	UInputAction* InteractAction;

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = Input)
	UInputAction* StrikeAction;

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = Input)
	UInputAction* SprintAction;

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = Input)
	UInputAction* ParryAction;

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = Input)
	UInputAction* DashAction;

	void Move(const FInputActionValue& Value);
	void Look(const FInputActionValue& Value);
	void Interact();
	void Strike();
	void StartSprint();
	void StopSprint();
	void StartParry();
	void StopParry();
	void Dash();

public:
	/** Health & Vitals (Where Winds Meet standard) */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SparkVision|Combat")
	float MaxHealth = 100.0f;

	UPROPERTY(BlueprintReadOnly, Category = "SparkVision|Combat")
	float CurrentHealth = 100.0f;

	/** Internal Energy / Qi / Stamina (Where Winds Meet standard) */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SparkVision|Combat")
	float MaxQi = 100.0f;

	UPROPERTY(BlueprintReadOnly, Category = "SparkVision|Combat")
	float CurrentQi = 100.0f;

	UPROPERTY(BlueprintReadOnly, Category = "SparkVision|Combat")
	bool bIsAttacking = false;

	UPROPERTY(BlueprintReadOnly, Category = "SparkVision|Combat")
	bool bIsSprinting = false;

	UPROPERTY(BlueprintReadOnly, Category = "SparkVision|Combat")
	bool bIsParrying = false;

	UPROPERTY(BlueprintReadOnly, Category = "SparkVision|Combat")
	bool bIsBlocking = false;

	UPROPERTY(BlueprintReadOnly, Category = "SparkVision|Combat")
	int32 ComboStep = 0;

	UPROPERTY(BlueprintAssignable, Category = "SparkVision|Combat")
	FOnHealthChangedSignature OnHealthChanged;

	UPROPERTY(BlueprintAssignable, Category = "SparkVision|Combat")
	FOnQiChangedSignature OnQiChanged;

	UPROPERTY(BlueprintAssignable, Category = "SparkVision|Combat")
	FOnCombatVictorySignature OnCombatVictory;

	UPROPERTY(BlueprintAssignable, Category = "SparkVision|Combat")
	FOnParrySuccessSignature OnParrySuccess;

	UPROPERTY(BlueprintAssignable, Category = "SparkVision|Interaction")
	FOnNearbyInteractableChanged OnNearbyInteractableChanged;

	UFUNCTION(BlueprintCallable, Category = "SparkVision|Combat")
	void TakeDamageAmount(float Damage);

	UFUNCTION(BlueprintCallable, Category = "SparkVision|Combat")
	void ResetHealth();

	UFUNCTION(BlueprintCallable, Category = "SparkVision|Combat")
	bool TryDeflectAttack(float IncomingDamage, AActor* Attacker);

	UFUNCTION(BlueprintPure, Category = "SparkVision|Vitals")
	float GetHealthPercent() const { return (MaxHealth > 0.f) ? (CurrentHealth / MaxHealth) : 0.f; }

	UFUNCTION(BlueprintPure, Category = "SparkVision|Vitals")
	float GetQiPercent() const { return (MaxQi > 0.f) ? (CurrentQi / MaxQi) : 0.f; }

	UFUNCTION(BlueprintPure, Category = "SparkVision|Interaction")
	FText GetCurrentPromptText() const { return CurrentPromptText; }

private:
	void ScanForInteractables();
	void UpdateCameraFraming(float DeltaTime);
	void UpdateVitals(float DeltaTime);

	UPROPERTY()
	AActor* CurrentFocusedInteractable = nullptr;

	FText CurrentPromptText;

	float ParryWindowTimer = 0.0f;
	const float ParryWindowDuration = 0.20f; // 200ms deflection window (Where Winds Meet style)

	float AttackResetTimer = 0.0f;

	// Camera Framing Targets
	float TargetArmDistance = 380.0f;
	float TargetFOV = 75.0f;
	FVector TargetSocketOffset = FVector(0.0f, 45.0f, 25.0f);
};
