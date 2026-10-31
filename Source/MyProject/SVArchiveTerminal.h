// Copyright SparkVision Dhaka University. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "SVInteractableInterface.h"
#include "SVArchiveTerminal.generated.h"

class USphereComponent;
class UStaticMeshComponent;

DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnArchiveDiscoveredSignature, const FString&, ArchiveId);

UCLASS()
class MYPROJECT_API ASVArchiveTerminal : public AActor, public ISVInteractableInterface
{
	GENERATED_BODY()
	
public:	
	ASVArchiveTerminal();

protected:
	virtual void BeginPlay() override;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* BaseMesh;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	USphereComponent* InteractionSphere;

public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SparkVision|Archive")
	FString ArchiveId = TEXT("archive_01");

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SparkVision|Archive")
	FText ArchiveTitle = FText::FromString(TEXT("Curzon Hall Archive Record"));

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SparkVision|Archive")
	FText ArchiveDescription = FText::FromString(TEXT("Historical document recovered from Curzon Hall heritage precinct."));

	UPROPERTY(BlueprintReadOnly, Category = "SparkVision|Archive")
	bool bIsDiscovered = false;

	UPROPERTY(BlueprintAssignable, Category = "SparkVision|Archive")
	FOnArchiveDiscoveredSignature OnArchiveDiscovered;

	/** ISVInteractableInterface implementation */
	virtual FText GetInteractionPrompt_Implementation() override;
	virtual void OnInteract_Implementation(AActor* Interactor) override;
};
