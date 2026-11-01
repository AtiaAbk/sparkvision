// Copyright SparkVision Dhaka University. All Rights Reserved.

#include "SVHUD.h"
#include "Engine/Canvas.h"
#include "Engine/Engine.h"
#include "SVCharacter.h"
#include "Kismet/GameplayStatics.h"

ASVHUD::ASVHUD()
{
	bShowCompass = true;
	bShowVitals = true;
}

void ASVHUD::DrawHUD()
{
	Super::DrawHUD();

	if (!Canvas) return;

	const float ScreenWidth = Canvas->ClipX;
	const float ScreenHeight = Canvas->ClipY;

	// Smooth letterbox interpolation
	float TargetLetterbox = bLetterboxActive ? 1.0f : 0.0f;
	LetterboxProgress = FMath::FInterpTo(LetterboxProgress, TargetLetterbox, GetWorld()->GetDeltaSeconds(), 5.0f);

	if (LetterboxProgress > 0.01f)
	{
		DrawLetterboxBars(ScreenWidth, ScreenHeight);
	}

	// Dynamic Camera Yaw for Compass
	float CameraYaw = 0.0f;
	if (APlayerCameraManager* CamManager = UGameplayStatics::GetPlayerCameraManager(GetWorld(), 0))
	{
		CameraYaw = CamManager->GetCameraRotation().Yaw;
	}

	if (bShowCompass)
	{
		DrawCompassRibbon(ScreenWidth, ScreenHeight, CameraYaw);
	}

	if (bShowVitals)
	{
		DrawVitalsGauge(ScreenWidth, ScreenHeight);
	}

	DrawInteractionPrompt(ScreenWidth, ScreenHeight);

	// Controls Helper Banner (Where Winds Meet aesthetic)
	UFont* SmallFont = GEngine->GetSmallFont();
	const FString ControlsText = TEXT("[W,A,S,D] Move   |   [Shift] Sprint   |   [Space] Jump   |   [E] Inspect   |   [1-6] Fast Travel");
	const float LegendWidth = 620.0f;
	const float LegendX = (ScreenWidth - LegendWidth) * 0.5f;
	const float LegendY = ScreenHeight - 34.0f;

	DrawRect(FLinearColor(0.02f, 0.02f, 0.03f, 0.70f), LegendX - 10.0f, LegendY - 4.0f, LegendWidth + 20.0f, 24.0f);
	DrawRect(FLinearColor(0.82f, 0.68f, 0.38f, 0.75f), LegendX - 10.0f, LegendY - 4.0f, LegendWidth + 20.0f, 1.0f);
	DrawText(ControlsText, FLinearColor(0.92f, 0.88f, 0.78f, 0.95f), LegendX + 15.0f, LegendY, SmallFont, 0.88f);

	if (bShowingArchiveCard)
	{
		DrawArchiveModal(ScreenWidth, ScreenHeight);
	}
}

void ASVHUD::SetLetterboxActive(bool bActive)
{
	bLetterboxActive = bActive;
}

void ASVHUD::DisplayArchiveRecord(const FText& Title, const FText& Description)
{
	ActiveArchiveTitle = Title;
	ActiveArchiveDescription = Description;
	bShowingArchiveCard = true;
	CardDisplayDuration = 8.0f;
	SetLetterboxActive(true);
}

void ASVHUD::DismissArchiveRecord()
{
	bShowingArchiveCard = false;
	SetLetterboxActive(false);
}

void ASVHUD::DrawCompassRibbon(float ScreenWidth, float ScreenHeight, float CameraYaw)
{
	const float RibbonWidth = FMath::Min(ScreenWidth * 0.5f, 650.0f);
	const float RibbonHeight = 24.0f;
	const float RibbonX = (ScreenWidth - RibbonWidth) * 0.5f;
	const float RibbonY = 28.0f;

	// Dark semi-translucent ink backing
	DrawRect(FLinearColor(0.02f, 0.02f, 0.03f, 0.75f), RibbonX, RibbonY, RibbonWidth, RibbonHeight);
	
	// Golden top accent border
	DrawRect(FLinearColor(0.85f, 0.72f, 0.45f, 0.85f), RibbonX, RibbonY, RibbonWidth, 1.5f);
	// Center diamond tick
	DrawRect(FLinearColor(0.95f, 0.82f, 0.50f, 1.0f), ScreenWidth * 0.5f - 2.0f, RibbonY - 4.0f, 4.0f, RibbonHeight + 8.0f);

	// Cardinal Points: N (0), E (90), S (180), W (-90/270)
	struct FCompassPoint { float Angle; FString Label; bool bMajor; };
	TArray<FCompassPoint> Points = {
		{ 0.0f, TEXT("N"), true },
		{ 45.0f, TEXT("NE"), false },
		{ 90.0f, TEXT("E"), true },
		{ 135.0f, TEXT("SE"), false },
		{ 180.0f, TEXT("S"), true },
		{ -180.0f, TEXT("S"), true },
		{ -135.0f, TEXT("SW"), false },
		{ -90.0f, TEXT("W"), true },
		{ -45.0f, TEXT("NW"), false }
	};

	UFont* Font = GEngine->GetSmallFont();
	for (const auto& Pt : Points)
	{
		float Diff = FMath::FindDeltaAngleDegrees(CameraYaw, Pt.Angle);
		if (FMath::Abs(Diff) < 65.0f)
		{
			float PixelOffset = (Diff / 65.0f) * (RibbonWidth * 0.45f);
			float DrawX = (ScreenWidth * 0.5f) + PixelOffset - 6.0f;
			FLinearColor TextColor = Pt.bMajor ? FLinearColor(0.95f, 0.85f, 0.60f, 0.95f) : FLinearColor(0.65f, 0.65f, 0.68f, 0.65f);
			DrawText(Pt.Label, TextColor, DrawX, RibbonY + 4.0f, Font, 0.95f);
		}
	}

	// Active Landmark Objective Marker on Compass
	ASVCharacter* PlayerChar = Cast<ASVCharacter>(UGameplayStatics::GetPlayerCharacter(GetWorld(), 0));
	FString LandmarkName = PlayerChar ? PlayerChar->GetCurrentLandmarkName() : TEXT("University of Dhaka Campus | ঢাকা বিশ্ববিদ্যালয়");

	DrawText(FString::Printf(TEXT("◆ %s"), *LandmarkName), FLinearColor(0.95f, 0.82f, 0.40f, 0.95f), RibbonX + 12.0f, RibbonY + RibbonHeight + 6.0f, Font, 0.95f);
}

void ASVHUD::DrawVitalsGauge(float ScreenWidth, float ScreenHeight)
{
	ASVCharacter* PlayerChar = Cast<ASVCharacter>(UGameplayStatics::GetPlayerCharacter(GetWorld(), 0));
	if (!PlayerChar) return;

	const float GaugeX = 50.0f;
	const float GaugeY = ScreenHeight - 95.0f;
	const float BarWidth = 260.0f;

	// Dark slate ink plate
	DrawRect(FLinearColor(0.03f, 0.03f, 0.04f, 0.75f), GaugeX - 10.0f, GaugeY - 26.0f, BarWidth + 24.0f, 68.0f);
	// Outer decorative trim
	DrawRect(FLinearColor(0.85f, 0.72f, 0.45f, 0.85f), GaugeX - 10.0f, GaugeY - 26.0f, 3.0f, 68.0f);

	UFont* Font = GEngine->GetSmallFont();
	DrawText(TEXT("WANDERER-SCHOLAR | ঢাকা বিশ্ববিদ্যালয়"), FLinearColor(0.92f, 0.85f, 0.70f, 0.95f), GaugeX, GaugeY - 20.0f, Font, 0.85f);

	// Health Bar (Crimson/Vermilion - Wuxia style)
	float HealthPct = PlayerChar->GetHealthPercent();
	DrawRect(FLinearColor(0.20f, 0.05f, 0.05f, 0.85f), GaugeX, GaugeY + 4.0f, BarWidth, 10.0f);
	DrawRect(FLinearColor(0.85f, 0.18f, 0.15f, 0.95f), GaugeX, GaugeY + 4.0f, BarWidth * HealthPct, 10.0f);

	// Internal Energy / Qi / Stamina Bar (Jade Celadon Green - Where Winds Meet style)
	float QiPct = PlayerChar->GetQiPercent();
	DrawRect(FLinearColor(0.05f, 0.15f, 0.10f, 0.85f), GaugeX, GaugeY + 20.0f, BarWidth * 0.85f, 6.0f);
	DrawRect(FLinearColor(0.22f, 0.78f, 0.55f, 0.95f), GaugeX, GaugeY + 20.0f, (BarWidth * 0.85f) * QiPct, 6.0f);

	// State Indicators (Parry / Sprint)
	if (PlayerChar->bIsParrying)
	{
		DrawText(TEXT("[PARRY STANCE ACTIVE]"), FLinearColor(1.0f, 0.85f, 0.2f, 1.0f), GaugeX + BarWidth + 20.0f, GaugeY + 2.0f, Font, 0.95f);
	}
	else if (PlayerChar->bIsSprinting)
	{
		DrawText(TEXT("QINGGONG SPRINT"), FLinearColor(0.3f, 0.9f, 0.7f, 0.9f), GaugeX + BarWidth + 20.0f, GaugeY + 16.0f, Font, 0.85f);
	}
}

void ASVHUD::DrawInteractionPrompt(float ScreenWidth, float ScreenHeight)
{
	ASVCharacter* PlayerChar = Cast<ASVCharacter>(UGameplayStatics::GetPlayerCharacter(GetWorld(), 0));
	if (!PlayerChar) return;

	FText Prompt = PlayerChar->GetCurrentPromptText();
	if (Prompt.IsEmpty()) return;

	const FString PromptStr = Prompt.ToString();
	UFont* Font = GEngine->GetMediumFont();

	float TextWidth = PromptStr.Len() * 10.0f;
	float BoxWidth = TextWidth + 60.0f;
	float BoxHeight = 44.0f;
	float BoxX = (ScreenWidth - BoxWidth) * 0.5f;
	float BoxY = ScreenHeight * 0.65f;

	// Ink-wash dark badge with gold border
	DrawRect(FLinearColor(0.03f, 0.03f, 0.05f, 0.90f), BoxX, BoxY, BoxWidth, BoxHeight);
	DrawRect(FLinearColor(0.85f, 0.72f, 0.38f, 0.95f), BoxX, BoxY, BoxWidth, 2.0f);
	DrawRect(FLinearColor(0.85f, 0.72f, 0.38f, 0.95f), BoxX, BoxY + BoxHeight - 2.0f, BoxWidth, 2.0f);

	// Centered Prompt Text
	DrawText(PromptStr, FLinearColor(1.0f, 0.95f, 0.85f, 1.0f), BoxX + 30.0f, BoxY + 11.0f, Font, 1.0f);
}

void ASVHUD::DrawLetterboxBars(float ScreenWidth, float ScreenHeight)
{
	float BarHeight = ScreenHeight * 0.12f * LetterboxProgress;
	DrawRect(FLinearColor::Black, 0.0f, 0.0f, ScreenWidth, BarHeight);
	DrawRect(FLinearColor::Black, 0.0f, ScreenHeight - BarHeight, ScreenWidth, BarHeight);
}

void ASVHUD::DrawArchiveModal(float ScreenWidth, float ScreenHeight)
{
	const float ModalWidth = FMath::Min(ScreenWidth * 0.75f, 850.0f);
	const float ModalHeight = 240.0f;
	const float ModalX = (ScreenWidth - ModalWidth) * 0.5f;
	const float ModalY = (ScreenHeight - ModalHeight) * 0.5f;

	// Parchment Slate Card
	DrawRect(FLinearColor(0.04f, 0.04f, 0.06f, 0.95f), ModalX, ModalY, ModalWidth, ModalHeight);
	// Outer Double Gold Border (Where Winds Meet style)
	DrawRect(FLinearColor(0.85f, 0.72f, 0.40f, 0.95f), ModalX, ModalY, ModalWidth, 3.0f);
	DrawRect(FLinearColor(0.85f, 0.72f, 0.40f, 0.95f), ModalX, ModalY + ModalHeight - 3.0f, ModalWidth, 3.0f);
	DrawRect(FLinearColor(0.85f, 0.72f, 0.40f, 0.95f), ModalX, ModalY, 3.0f, ModalHeight);
	DrawRect(FLinearColor(0.85f, 0.72f, 0.40f, 0.95f), ModalX + ModalWidth - 3.0f, ModalY, 3.0f, ModalHeight);

	UFont* BigFont = GEngine->GetLargeFont();
	UFont* MedFont = GEngine->GetMediumFont();
	UFont* SmallFont = GEngine->GetSmallFont();

	// Title
	DrawText(ActiveArchiveTitle.ToString(), FLinearColor(0.98f, 0.90f, 0.65f, 1.0f), ModalX + 35.0f, ModalY + 22.0f, BigFont, 1.0f);
	DrawRect(FLinearColor(0.65f, 0.55f, 0.35f, 0.75f), ModalX + 35.0f, ModalY + 62.0f, ModalWidth - 70.0f, 1.5f);

	// Description Body
	DrawText(ActiveArchiveDescription.ToString(), FLinearColor(0.88f, 0.88f, 0.92f, 0.95f), ModalX + 35.0f, ModalY + 76.0f, MedFont, 0.95f);

	// Action button
	DrawText(TEXT("[SPACE / E] Acknowledge & Continue Campus Exploration"), FLinearColor(0.78f, 0.78f, 0.82f, 0.90f), ModalX + 35.0f, ModalY + ModalHeight - 35.0f, SmallFont, 0.9f);
}
