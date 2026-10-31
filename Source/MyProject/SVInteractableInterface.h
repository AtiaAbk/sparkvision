// Copyright SparkVision Dhaka University. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "UObject/Interface.h"
#include "SVInteractableInterface.generated.h"

UINTERFACE(MinimalAPI, Blueprintable)
class USVInteractableInterface : public UInterface
{
	GENERATED_BODY()
};

class MYPROJECT_API ISVInteractableInterface
{
	GENERATED_BODY()

public:
	UFUNCTION(BlueprintNativeEvent, BlueprintCallable, Category = "SparkVision|Interaction")
	FText GetInteractionPrompt();

	UFUNCTION(BlueprintNativeEvent, BlueprintCallable, Category = "SparkVision|Interaction")
	void OnInteract(AActor* Interactor);
};
