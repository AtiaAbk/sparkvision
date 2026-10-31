// Copyright SparkVision Dhaka University. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/HUD.h"
#include "SVHUD.generated.h"

UCLASS()
class MYPROJECT_API ASVHUD : public AHUD
{
	GENERATED_BODY()

public:
	ASVHUD();

	virtual void DrawHUD() override;

	UFUNCTION(BlueprintCallable, Category = "SparkVision|UI")
	void SetLetterboxActive(bool bActive);

	UFUNCTION(BlueprintCallable, Category = "SparkVision|UI")
	void DisplayArchiveRecord(const FText& Title, const FText& Description);

	UFUNCTION(BlueprintCallable, Category = "SparkVision|UI")
	void DismissArchiveRecord();

protected:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SparkVision|UI")
	bool bShowCompass = true;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SparkVision|UI")
	bool bShowVitals = true;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SparkVision|UI")
	bool bLetterboxActive = false;

	float LetterboxProgress = 0.0f;

	bool bShowingArchiveCard = false;
	FText ActiveArchiveTitle;
	FText ActiveArchiveDescription;
	float CardDisplayDuration = 0.0f;

private:
	void DrawCompassRibbon(float ScreenWidth, float ScreenHeight, float CameraYaw);
	void DrawVitalsGauge(float ScreenWidth, float ScreenHeight);
	void DrawInteractionPrompt(float ScreenWidth, float ScreenHeight);
	void DrawLetterboxBars(float ScreenWidth, float ScreenHeight);
	void DrawArchiveModal(float ScreenWidth, float ScreenHeight);
};
