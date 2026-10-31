// Copyright SparkVision Dhaka University. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "SVHostileOpponent.generated.h"

DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnOpponentDefeatedSignature, ASVHostileOpponent*, Opponent);

UCLASS()
class MYPROJECT_API ASVHostileOpponent : public ACharacter
{
	GENERATED_BODY()

public:
	ASVHostileOpponent();

protected:
	virtual void BeginPlay() override;
	virtual void Tick(float DeltaTime) override;

public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SparkVision|Combat")
	float Health = 60.0f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SparkVision|Combat")
	float AttackDamage = 15.0f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SparkVision|Combat")
	float AttackRange = 180.0f;

	UPROPERTY(BlueprintReadOnly, Category = "SparkVision|Combat")
	bool bIsDefeated = false;

	UPROPERTY(BlueprintAssignable, Category = "SparkVision|Combat")
	FOnOpponentDefeatedSignature OnOpponentDefeated;

	UFUNCTION(BlueprintCallable, Category = "SparkVision|Combat")
	void ReceiveStrike(float DamageAmount);

private:
	float AttackCooldown = 2.0f;
	float TimeSinceLastAttack = 0.0f;
};
