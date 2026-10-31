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
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnCombatVictorySignature);

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

	void Move(const FInputActionValue& Value);
	void Look(const FInputActionValue& Value);
	void Interact();
	void Strike();

public:
	/** Health and Combat state */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SparkVision|Combat")
	float MaxHealth = 100.0f;

	UPROPERTY(BlueprintReadOnly, Category = "SparkVision|Combat")
	float CurrentHealth = 100.0f;

	UPROPERTY(BlueprintReadOnly, Category = "SparkVision|Combat")
	bool bIsAttacking = false;

	UPROPERTY(BlueprintAssignable, Category = "SparkVision|Combat")
	FOnHealthChangedSignature OnHealthChanged;

	UPROPERTY(BlueprintAssignable, Category = "SparkVision|Combat")
	FOnCombatVictorySignature OnCombatVictory;

	UPROPERTY(BlueprintAssignable, Category = "SparkVision|Interaction")
	FOnNearbyInteractableChanged OnNearbyInteractableChanged;

	UFUNCTION(BlueprintCallable, Category = "SparkVision|Combat")
	void TakeDamageAmount(float Damage);

	UFUNCTION(BlueprintCallable, Category = "SparkVision|Combat")
	void ResetHealth();

private:
	void ScanForInteractables();
	UPROPERTY()
	AActor* CurrentFocusedInteractable = nullptr;
};
