// Copyright SparkVision Dhaka University. All Rights Reserved.

#include "SVHUD.h"
#include "Engine/Canvas.h"
#include "Engine/Engine.h"
#include "SVCharacter.h"
#include "Kismet/GameplayStatics.h"
#include "Kismet/KismetSystemLibrary.h"
#include "GameFramework/PlayerController.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "SVMissionControlSubsystem.h"

ASVHUD::ASVHUD()
{
	bShowCompass = true;
	bShowVitals = true;
	CurrentMenuState = ESVMenuState::LoadingScreen;
	LoadingPipeProgress = 0.0f;
	LoadingScreenTimer = 0.0f;
	bLoadingComplete = false;
	bShowingPoliceArrest = false;
	bShowingCombatDefeat = false;
	ClimaxAttemptNum = 1;
	ClimaxMaxAttempts = 3;
	bClimaxRetryAllowed = true;
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

	// Dynamic Full-Screen Menu States
	if (CurrentMenuState == ESVMenuState::LoadingScreen)
	{
		DrawLoadingScreen(ScreenWidth, ScreenHeight);
		return;
	}
	else if (CurrentMenuState == ESVMenuState::MainMenu)
	{
		DrawMainMenu(ScreenWidth, ScreenHeight);
		return;
	}
	else if (CurrentMenuState == ESVMenuState::CharacterSelect)
	{
		DrawCharacterSelectMenu(ScreenWidth, ScreenHeight);
		return;
	}
	else if (CurrentMenuState == ESVMenuState::WorldSelect)
	{
		DrawWorldSelectMenu(ScreenWidth, ScreenHeight);
		return;
	}
	else if (CurrentMenuState == ESVMenuState::PoliceArrest)
	{
		DrawPoliceArrestModal(ScreenWidth, ScreenHeight);
		return;
	}
	else if (CurrentMenuState == ESVMenuState::CombatDefeat)
	{
		DrawCombatDefeatModal(ScreenWidth, ScreenHeight);
		return;
	}
	else if (CurrentMenuState == ESVMenuState::PauseMenu)
	{
		DrawPauseMenu(ScreenWidth, ScreenHeight);
		return;
	}
	else if (CurrentMenuState == ESVMenuState::SettingsMenu)
	{
		DrawSettingsMenu(ScreenWidth, ScreenHeight);
		return;
	}
	else if (CurrentMenuState == ESVMenuState::ControlsMenu)
	{
		DrawControlsMenu(ScreenWidth, ScreenHeight);
		return;
	}
	else if (CurrentMenuState == ESVMenuState::CreditsMenu)
	{
		DrawCreditsMenu(ScreenWidth, ScreenHeight);
		return;
	}

	// Normal In-Game HUD Elements
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

	DrawObjectiveTracker(ScreenWidth, ScreenHeight);
	DrawWaypointMarker(ScreenWidth, ScreenHeight);
	DrawInteractionPrompt(ScreenWidth, ScreenHeight);

	// Controls Helper Banner (Where Winds Meet aesthetic)
	UFont* SmallFont = GEngine->GetSmallFont();
	const FString ControlsText = TEXT("[W,A,S,D] Move   |   [Shift] Sprint   |   [Space] Jump   |   [E] Interact   |   [1-6] Fast Travel   |   [Esc] Pause Menu");
	const float LegendWidth = 720.0f;
	const float LegendX = (ScreenWidth - LegendWidth) * 0.5f;
	const float LegendY = ScreenHeight - 34.0f;

	DrawRect(FLinearColor(0.02f, 0.02f, 0.03f, 0.75f), LegendX - 10.0f, LegendY - 4.0f, LegendWidth + 20.0f, 24.0f);
	DrawRect(FLinearColor(0.82f, 0.68f, 0.38f, 0.75f), LegendX - 10.0f, LegendY - 4.0f, LegendWidth + 20.0f, 1.0f);
	DrawText(ControlsText, FLinearColor(0.92f, 0.88f, 0.78f, 0.95f), LegendX + 10.0f, LegendY, SmallFont, 0.85f);

	if (bShowingArchiveCard)
	{
		DrawArchiveModal(ScreenWidth, ScreenHeight);
	}
	else if (bShowingDialogue)
	{
		DrawNPCDialogueModal(ScreenWidth, ScreenHeight);
	}
	else if (bShowingVictoryModal)
	{
		DrawVictoryModal(ScreenWidth, ScreenHeight);
	}
}

void ASVHUD::SetLetterboxActive(bool bActive)
{
	bLetterboxActive = bActive;
}

void ASVHUD::TogglePauseMenu()
{
	if (CurrentMenuState == ESVMenuState::CharacterSelect || CurrentMenuState == ESVMenuState::WorldSelect ||
		CurrentMenuState == ESVMenuState::SettingsMenu || CurrentMenuState == ESVMenuState::ControlsMenu ||
		CurrentMenuState == ESVMenuState::CreditsMenu)
	{
		CurrentMenuState = ESVMenuState::MainMenu;
		return;
	}

	if (CurrentMenuState == ESVMenuState::PauseMenu)
	{
		CurrentMenuState = ESVMenuState::None;
	}
	else if (CurrentMenuState == ESVMenuState::None)
	{
		CurrentMenuState = ESVMenuState::PauseMenu;
	}
	else
	{
		CurrentMenuState = ESVMenuState::None;
	}
}

void ASVHUD::ToggleMainMenu()
{
	if (CurrentMenuState == ESVMenuState::MainMenu)
	{
		CurrentMenuState = ESVMenuState::None;
	}
	else
	{
		CurrentMenuState = ESVMenuState::MainMenu;
	}
}

void ASVHUD::HandleMenuAction(int32 OptionIndex)
{
	ASVCharacter* PlayerChar = Cast<ASVCharacter>(UGameplayStatics::GetPlayerCharacter(GetWorld(), 0));

	if (CurrentMenuState == ESVMenuState::LoadingScreen)
	{
		CurrentMenuState = ESVMenuState::MainMenu;
		return;
	}

	if (CurrentMenuState == ESVMenuState::MainMenu)
	{
		switch (OptionIndex)
		{
		case 1: // Start Game
			StartGameFromMenu();
			break;
		case 2: // Character Select
			CurrentMenuState = ESVMenuState::CharacterSelect;
			break;
		case 3: // World Select
			CurrentMenuState = ESVMenuState::WorldSelect;
			break;
		case 4: // Settings
			CurrentMenuState = ESVMenuState::SettingsMenu;
			break;
		case 5: // Exit Game
			if (APlayerController* PC = Cast<APlayerController>(UGameplayStatics::GetPlayerController(GetWorld(), 0)))
			{
				UKismetSystemLibrary::QuitGame(GetWorld(), PC, EQuitPreference::Quit, false);
			}
			break;
		default:
			break;
		}
	}
	else if (CurrentMenuState == ESVMenuState::CharacterSelect)
	{
		if (OptionIndex == 1) // Male (Shovon)
		{
			if (PlayerChar) PlayerChar->SelectProtagonist(false);
			CurrentMenuState = ESVMenuState::MainMenu;
		}
		else if (OptionIndex == 2) // Female (Rina)
		{
			if (PlayerChar) PlayerChar->SelectProtagonist(true);
			CurrentMenuState = ESVMenuState::MainMenu;
		}
		else
		{
			CurrentMenuState = ESVMenuState::MainMenu;
		}
	}
	else if (CurrentMenuState == ESVMenuState::WorldSelect)
	{
		// 1 is DU Campus (Active)
		CurrentMenuState = ESVMenuState::MainMenu;
	}
	else if (CurrentMenuState == ESVMenuState::PoliceArrest)
	{
		if (OptionIndex == 1)
		{
			StartGameFromMenu();
		}
		else
		{
			CurrentMenuState = ESVMenuState::MainMenu;
		}
	}
	else if (CurrentMenuState == ESVMenuState::CombatDefeat)
	{
		if (bClimaxRetryAllowed && OptionIndex == 1)
		{
			if (PlayerChar)
			{
				PlayerChar->RetryClimaxCombat();
			}
			CurrentMenuState = ESVMenuState::None;
		}
		else
		{
			CurrentMenuState = ESVMenuState::MainMenu;
		}
	}
	else if (CurrentMenuState == ESVMenuState::PauseMenu)
	{
		switch (OptionIndex)
		{
		case 1: // Resume
			CurrentMenuState = ESVMenuState::None;
			break;
		case 2: // Save Progress
			if (PlayerChar)
			{
				PlayerChar->SaveGameProgress();
			}
			CurrentMenuState = ESVMenuState::None;
			break;
		case 3: // Load Last Checkpoint
			if (PlayerChar)
			{
				PlayerChar->LoadGameProgress();
			}
			CurrentMenuState = ESVMenuState::None;
			break;
		case 4: // Restart Chapter 1
			StartGameFromMenu();
			break;
		case 5: // Return to Main Menu
			CurrentMenuState = ESVMenuState::MainMenu;
			break;
		default:
			CurrentMenuState = ESVMenuState::None;
			break;
		}
	}
	else
	{
		// In submenus (Settings, Controls, Credits), return to MainMenu
		CurrentMenuState = ESVMenuState::MainMenu;
	}
}

void ASVHUD::DisplayArchiveRecord(const FText& Title, const FText& Description)
{
	ActiveArchiveTitle = Title;
	ActiveArchiveDescription = Description;
	bShowingArchiveCard = true;
	SetLetterboxActive(true);
}

void ASVHUD::DismissArchiveRecord()
{
	bShowingArchiveCard = false;
	if (!bShowingDialogue && !bShowingVictoryModal)
	{
		SetLetterboxActive(false);
	}
}

void ASVHUD::DisplayNPCDialogue(const FText& SpeakerName, const FText& InNPCRole, const FText& Bengali, const FText& English)
{
	DialogueSpeakerName = SpeakerName;
	DialogueSpeakerRole = InNPCRole;
	DialogueBengaliText = Bengali;
	DialogueEnglishSubtitle = English;
	bShowingDialogue = true;
	SetLetterboxActive(true);
}

void ASVHUD::DismissNPCDialogue()
{
	bShowingDialogue = false;
	if (!bShowingArchiveCard && !bShowingVictoryModal)
	{
		SetLetterboxActive(false);
	}
}

void ASVHUD::DisplayChapterVictory(const FText& DecisionTitle, const FText& SubtitleText, const FText& UnlockText)
{
	VictoryHeadline = DecisionTitle;
	VictorySubtitle = SubtitleText;
	VictoryUnlockNotice = UnlockText;
	bShowingVictoryModal = true;
	SetLetterboxActive(true);
}

void ASVHUD::DismissChapterVictory()
{
	bShowingVictoryModal = false;
	SetLetterboxActive(false);
}

void ASVHUD::DrawCompassRibbon(float ScreenWidth, float ScreenHeight, float CameraYaw)
{
	const float RibbonWidth = FMath::Min(ScreenWidth * 0.5f, 650.0f);
	const float RibbonHeight = 24.0f;
	const float RibbonX = (ScreenWidth - RibbonWidth) * 0.5f;
	const float RibbonY = 28.0f;

	DrawRect(FLinearColor(0.02f, 0.02f, 0.03f, 0.75f), RibbonX, RibbonY, RibbonWidth, RibbonHeight);
	DrawRect(FLinearColor(0.85f, 0.72f, 0.45f, 0.85f), RibbonX, RibbonY, RibbonWidth, 1.5f);
	DrawRect(FLinearColor(0.95f, 0.82f, 0.50f, 1.0f), ScreenWidth * 0.5f - 2.0f, RibbonY - 4.0f, 4.0f, RibbonHeight + 8.0f);

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

	DrawRect(FLinearColor(0.03f, 0.03f, 0.04f, 0.75f), GaugeX - 10.0f, GaugeY - 26.0f, BarWidth + 24.0f, 68.0f);
	DrawRect(FLinearColor(0.85f, 0.72f, 0.45f, 0.85f), GaugeX - 10.0f, GaugeY - 26.0f, 3.0f, 68.0f);

	UFont* Font = GEngine->GetSmallFont();
	DrawText(TEXT("WANDERER-SCHOLAR | ঢাকা বিশ্ববিদ্যালয়"), FLinearColor(0.92f, 0.85f, 0.70f, 0.95f), GaugeX, GaugeY - 20.0f, Font, 0.85f);

	float HealthPct = PlayerChar->GetHealthPercent();
	DrawRect(FLinearColor(0.20f, 0.05f, 0.05f, 0.85f), GaugeX, GaugeY + 4.0f, BarWidth, 10.0f);
	DrawRect(FLinearColor(0.85f, 0.18f, 0.15f, 0.95f), GaugeX, GaugeY + 4.0f, BarWidth * HealthPct, 10.0f);

	float QiPct = PlayerChar->GetQiPercent();
	DrawRect(FLinearColor(0.05f, 0.15f, 0.10f, 0.85f), GaugeX, GaugeY + 20.0f, BarWidth * 0.85f, 6.0f);
	DrawRect(FLinearColor(0.22f, 0.78f, 0.55f, 0.95f), GaugeX, GaugeY + 20.0f, (BarWidth * 0.85f) * QiPct, 6.0f);

	if (PlayerChar->bIsSprinting)
	{
		DrawText(TEXT("QINGGONG SPRINT"), FLinearColor(0.3f, 0.9f, 0.7f, 0.9f), GaugeX + BarWidth + 20.0f, GaugeY + 16.0f, Font, 0.85f);
	}
	else if (PlayerChar->bIsAirGliding)
	{
		DrawText(TEXT("QINGGONG AIR GLIDE"), FLinearColor(0.2f, 0.85f, 0.95f, 0.95f), GaugeX + BarWidth + 20.0f, GaugeY + 16.0f, Font, 0.85f);
	}
	else if (PlayerChar->bIsParrying)
	{
		DrawText(TEXT("PARRY DEFLECT STANCE"), FLinearColor(1.0f, 0.85f, 0.2f, 1.0f), GaugeX + BarWidth + 20.0f, GaugeY + 16.0f, Font, 0.85f);
	}
	else if (PlayerChar->bIsBlocking)
	{
		DrawText(TEXT("GUARD BLOCK"), FLinearColor(0.35f, 0.65f, 1.0f, 0.95f), GaugeX + BarWidth + 20.0f, GaugeY + 16.0f, Font, 0.85f);
	}

	// Wuxia Controls Guide banner at bottom center
	const float ControlsBarWidth = 680.0f;
	const float ControlsBarHeight = 22.0f;
	const float ControlsBarX = (ScreenWidth - ControlsBarWidth) * 0.5f;
	const float ControlsBarY = ScreenHeight - 32.0f;
	DrawRect(FLinearColor(0.02f, 0.02f, 0.03f, 0.75f), ControlsBarX, ControlsBarY, ControlsBarWidth, ControlsBarHeight);
	DrawRect(FLinearColor(0.85f, 0.72f, 0.40f, 0.45f), ControlsBarX, ControlsBarY, ControlsBarWidth, 1.0f);
	DrawText(TEXT("[LMB / F] Martial Strike  •  [RMB / R] Deflect / Parry  •  [Space] Qinggong Leap / Glide  •  [Q / Alt] Dash  •  [Shift] Sprint"),
		FLinearColor(0.90f, 0.88f, 0.78f, 0.90f), ControlsBarX + 12.0f, ControlsBarY + 4.0f, Font, 0.78f);
}

void ASVHUD::DrawObjectiveTracker(float ScreenWidth, float ScreenHeight)
{
	ASVCharacter* PlayerChar = Cast<ASVCharacter>(UGameplayStatics::GetPlayerCharacter(GetWorld(), 0));
	if (!PlayerChar) return;

	const float PanelWidth = 340.0f;
	const float PanelHeight = 90.0f;
	const float PanelX = ScreenWidth - PanelWidth - 35.0f;
	const float PanelY = 28.0f;

	DrawRect(FLinearColor(0.03f, 0.03f, 0.05f, 0.85f), PanelX, PanelY, PanelWidth, PanelHeight);
	DrawRect(FLinearColor(0.85f, 0.72f, 0.40f, 0.85f), PanelX, PanelY, PanelWidth, 2.0f);
	DrawRect(FLinearColor(0.85f, 0.72f, 0.40f, 0.85f), PanelX, PanelY, 2.0f, PanelHeight);

	UFont* SmallFont = GEngine->GetSmallFont();

	// Title
	DrawText(TEXT("CHAPTER 1: WHERE IT ALL BEGAN"), FLinearColor(0.95f, 0.82f, 0.45f, 1.0f), PanelX + 12.0f, PanelY + 8.0f, SmallFont, 0.88f);

	// Mission Label
	FText MissionDesc = PlayerChar->GetActiveMissionDescription();
	DrawText(FString::Printf(TEXT("• [%s]"), *PlayerChar->ActiveMissionId), FLinearColor(0.92f, 0.92f, 0.95f, 1.0f), PanelX + 12.0f, PanelY + 26.0f, SmallFont, 0.82f);
	DrawText(MissionDesc.ToString(), FLinearColor(0.78f, 0.78f, 0.82f, 0.95f), PanelX + 12.0f, PanelY + 42.0f, SmallFont, 0.78f);

	// Archive count
	int32 ArchiveCount = PlayerChar->GetDiscoveredArchiveCount();
	DrawText(FString::Printf(TEXT("Archives Secured: %d / 5"), ArchiveCount), FLinearColor(0.4f, 0.9f, 0.5f, 1.0f), PanelX + 12.0f, PanelY + 68.0f, SmallFont, 0.82f);

	// Java Mission Control status indicator
	DrawRect(FLinearColor(0.2f, 0.85f, 0.3f, 1.0f), PanelX + PanelWidth - 18.0f, PanelY + 12.0f, 8.0f, 8.0f);
}

void ASVHUD::DrawInteractionPrompt(float ScreenWidth, float ScreenHeight)
{
	ASVCharacter* PlayerChar = Cast<ASVCharacter>(UGameplayStatics::GetPlayerCharacter(GetWorld(), 0));
	if (!PlayerChar) return;

	FText Prompt = PlayerChar->GetCurrentPromptText();
	if (Prompt.IsEmpty()) return;

	const FString PromptStr = Prompt.ToString();
	UFont* Font = GEngine->GetMediumFont();

	float TextWidth = PromptStr.Len() * 9.0f;
	float BoxWidth = TextWidth + 50.0f;
	float BoxHeight = 40.0f;
	float BoxX = (ScreenWidth - BoxWidth) * 0.5f;
	float BoxY = ScreenHeight * 0.65f;

	DrawRect(FLinearColor(0.03f, 0.03f, 0.05f, 0.90f), BoxX, BoxY, BoxWidth, BoxHeight);
	DrawRect(FLinearColor(0.85f, 0.72f, 0.38f, 0.95f), BoxX, BoxY, BoxWidth, 2.0f);
	DrawRect(FLinearColor(0.85f, 0.72f, 0.38f, 0.95f), BoxX, BoxY + BoxHeight - 2.0f, BoxWidth, 2.0f);

	DrawText(PromptStr, FLinearColor(1.0f, 0.95f, 0.85f, 1.0f), BoxX + 25.0f, BoxY + 10.0f, Font, 0.95f);
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

	DrawRect(FLinearColor(0.04f, 0.04f, 0.06f, 0.95f), ModalX, ModalY, ModalWidth, ModalHeight);
	DrawRect(FLinearColor(0.85f, 0.72f, 0.40f, 0.95f), ModalX, ModalY, ModalWidth, 3.0f);
	DrawRect(FLinearColor(0.85f, 0.72f, 0.40f, 0.95f), ModalX, ModalY + ModalHeight - 3.0f, ModalWidth, 3.0f);
	DrawRect(FLinearColor(0.85f, 0.72f, 0.40f, 0.95f), ModalX, ModalY, 3.0f, ModalHeight);
	DrawRect(FLinearColor(0.85f, 0.72f, 0.40f, 0.95f), ModalX + ModalWidth - 3.0f, ModalY, 3.0f, ModalHeight);

	UFont* BigFont = GEngine->GetLargeFont();
	UFont* MedFont = GEngine->GetMediumFont();
	UFont* SmallFont = GEngine->GetSmallFont();

	DrawText(ActiveArchiveTitle.ToString(), FLinearColor(0.98f, 0.90f, 0.65f, 1.0f), ModalX + 35.0f, ModalY + 22.0f, BigFont, 1.0f);
	DrawRect(FLinearColor(0.65f, 0.55f, 0.35f, 0.75f), ModalX + 35.0f, ModalY + 62.0f, ModalWidth - 70.0f, 1.5f);
	DrawText(ActiveArchiveDescription.ToString(), FLinearColor(0.88f, 0.88f, 0.92f, 0.95f), ModalX + 35.0f, ModalY + 76.0f, MedFont, 0.95f);
	DrawText(TEXT("[SPACE / E] Acknowledge & Continue Campus Exploration"), FLinearColor(0.78f, 0.78f, 0.82f, 0.90f), ModalX + 35.0f, ModalY + ModalHeight - 35.0f, SmallFont, 0.9f);
}

void ASVHUD::DrawNPCDialogueModal(float ScreenWidth, float ScreenHeight)
{
	const float ModalWidth = FMath::Min(ScreenWidth * 0.80f, 900.0f);
	const float ModalHeight = 175.0f;
	const float ModalX = (ScreenWidth - ModalWidth) * 0.5f;
	const float ModalY = ScreenHeight - ModalHeight - 55.0f;

	DrawRect(FLinearColor(0.03f, 0.03f, 0.05f, 0.95f), ModalX, ModalY, ModalWidth, ModalHeight);
	DrawRect(FLinearColor(0.85f, 0.72f, 0.40f, 0.95f), ModalX, ModalY, ModalWidth, 2.0f);
	DrawRect(FLinearColor(0.85f, 0.72f, 0.40f, 0.95f), ModalX, ModalY, 2.0f, ModalHeight);
	DrawRect(FLinearColor(0.85f, 0.72f, 0.40f, 0.95f), ModalX + ModalWidth - 2.0f, ModalY, 2.0f, ModalHeight);

	UFont* MedFont = GEngine->GetMediumFont();
	UFont* SmallFont = GEngine->GetSmallFont();

	// Speaker Name & Role
	FString SpeakerHeader = FString::Printf(TEXT("%s  —  %s"), *DialogueSpeakerName.ToString(), *DialogueSpeakerRole.ToString());
	DrawText(SpeakerHeader, FLinearColor(0.95f, 0.85f, 0.45f, 1.0f), ModalX + 30.0f, ModalY + 16.0f, MedFont, 0.95f);

	// Bengali Line
	DrawText(DialogueBengaliText.ToString(), FLinearColor(1.0f, 1.0f, 1.0f, 1.0f), ModalX + 30.0f, ModalY + 48.0f, MedFont, 0.95f);

	// English Subtitle
	DrawText(DialogueEnglishSubtitle.ToString(), FLinearColor(0.85f, 0.85f, 0.90f, 0.95f), ModalX + 30.0f, ModalY + 80.0f, SmallFont, 0.95f);

	// Interaction prompt
	DrawText(TEXT("[E] Continue Conversation   |   [Space] Close"), FLinearColor(0.70f, 0.70f, 0.75f, 0.85f), ModalX + 30.0f, ModalY + 135.0f, SmallFont, 0.85f);
}

void ASVHUD::DrawVictoryModal(float ScreenWidth, float ScreenHeight)
{
	const float ModalWidth = FMath::Min(ScreenWidth * 0.80f, 920.0f);
	const float ModalHeight = 320.0f;
	const float ModalX = (ScreenWidth - ModalWidth) * 0.5f;
	const float ModalY = (ScreenHeight - ModalHeight) * 0.5f;

	DrawRect(FLinearColor(0.02f, 0.02f, 0.04f, 0.96f), ModalX, ModalY, ModalWidth, ModalHeight);
	DrawRect(FLinearColor(0.85f, 0.72f, 0.40f, 0.95f), ModalX, ModalY, ModalWidth, 3.0f);
	DrawRect(FLinearColor(0.85f, 0.72f, 0.40f, 0.95f), ModalX, ModalY + ModalHeight - 3.0f, ModalWidth, 3.0f);
	DrawRect(FLinearColor(0.85f, 0.72f, 0.40f, 0.95f), ModalX, ModalY, 3.0f, ModalHeight);
	DrawRect(FLinearColor(0.85f, 0.72f, 0.40f, 0.95f), ModalX + ModalWidth - 3.0f, ModalY, 3.0f, ModalHeight);

	UFont* BigFont = GEngine->GetLargeFont();
	UFont* MedFont = GEngine->GetMediumFont();
	UFont* SmallFont = GEngine->GetSmallFont();

	// Historic Title
	DrawText(VictoryHeadline.ToString(), FLinearColor(0.98f, 0.88f, 0.50f, 1.0f), ModalX + 45.0f, ModalY + 30.0f, BigFont, 1.3f);
	DrawText(VictorySubtitle.ToString(), FLinearColor(0.80f, 0.80f, 0.85f, 0.90f), ModalX + 45.0f, ModalY + 80.0f, MedFont, 0.95f);

	DrawRect(FLinearColor(0.65f, 0.55f, 0.35f, 0.75f), ModalX + 45.0f, ModalY + 115.0f, ModalWidth - 90.0f, 1.5f);

	DrawText(TEXT("All 5 Historical Archives Secured. The peaceful academic assemblies of July 1–14 have concluded."), FLinearColor(0.92f, 0.92f, 0.95f, 1.0f), ModalX + 45.0f, ModalY + 135.0f, MedFont, 0.95f);
	DrawText(TEXT("You have committed to stand with fellow students as the movement transitions into a nationwide struggle for justice."), FLinearColor(0.85f, 0.85f, 0.90f, 0.90f), ModalX + 45.0f, ModalY + 170.0f, MedFont, 0.90f);

	// Unlock notice
	DrawRect(FLinearColor(0.10f, 0.30f, 0.15f, 0.85f), ModalX + 45.0f, ModalY + 215.0f, ModalWidth - 90.0f, 40.0f);
	DrawText(VictoryUnlockNotice.ToString(), FLinearColor(0.4f, 0.95f, 0.5f, 1.0f), ModalX + 65.0f, ModalY + 225.0f, MedFont, 1.0f);

	DrawText(TEXT("[SPACE] Continue Free-Roam Exploration   |   [Esc] Pause / Main Menu"), FLinearColor(0.75f, 0.75f, 0.80f, 0.85f), ModalX + 45.0f, ModalY + ModalHeight - 35.0f, SmallFont, 0.9f);
}

void ASVHUD::DrawLoadingScreen(float ScreenWidth, float ScreenHeight)
{
	float DeltaTime = GetWorld()->GetDeltaSeconds();
	LoadingScreenTimer += DeltaTime;

	// Fill the pipe smoothly over ~2.4 seconds
	LoadingPipeProgress = FMath::Clamp(LoadingScreenTimer / 2.4f, 0.0f, 1.0f);

	// Full-screen deep slate background (#050811)
	DrawRect(FLinearColor(0.02f, 0.03f, 0.05f, 1.0f), 0.0f, 0.0f, ScreenWidth, ScreenHeight);

	// Top & Bottom Gold Accent Frames
	DrawRect(FLinearColor(0.85f, 0.72f, 0.40f, 0.85f), 0.0f, 25.0f, ScreenWidth, 2.0f);
	DrawRect(FLinearColor(0.85f, 0.72f, 0.40f, 0.85f), 0.0f, ScreenHeight - 27.0f, ScreenWidth, 2.0f);

	UFont* BigFont = GEngine->GetLargeFont();
	UFont* MedFont = GEngine->GetMediumFont();
	UFont* SmallFont = GEngine->GetSmallFont();

	// Centered Header & Branding
	const float CenterX = ScreenWidth * 0.5f;
	const float CenterY = ScreenHeight * 0.36f;

	// SparkVision 2x12
	const FString MainTitle = TEXT("SPARKVISION 2x12");
	float TitleW = 0.0f, TitleH = 0.0f;
	GetTextSize(MainTitle, TitleW, TitleH, BigFont, 1.6f);
	DrawText(MainTitle, FLinearColor(0.98f, 0.88f, 0.45f, 1.0f), CenterX - (TitleW * 0.5f), CenterY - 70.0f, BigFont, 1.6f);

	// Bengali & English subtitle
	const FString SubTitle = TEXT("BIRTH OF 36 JULY  •  ঐতিহাসিক গণ-আন্দোলন ও ঢাকা বিশ্ববিদ্যালয়");
	float SubW = 0.0f, SubH = 0.0f;
	GetTextSize(SubTitle, SubW, SubH, MedFont, 1.05f);
	DrawText(SubTitle, FLinearColor(0.82f, 0.82f, 0.88f, 0.95f), CenterX - (SubW * 0.5f), CenterY, MedFont, 1.05f);

	// Subtle decorative divider
	const float DividerW = 500.0f;
	DrawRect(FLinearColor(0.85f, 0.72f, 0.40f, 0.60f), CenterX - (DividerW * 0.5f), CenterY + 38.0f, DividerW, 1.5f);

	// Loading Pipe / Cylindrical Tube Progress Bar
	const float PipeWidth = FMath::Min(ScreenWidth * 0.65f, 750.0f);
	const float PipeHeight = 28.0f;
	const float PipeX = CenterX - (PipeWidth * 0.5f);
	const float PipeY = CenterY + 70.0f;

	// Pipe outer shadow/casing
	DrawRect(FLinearColor(0.04f, 0.05f, 0.08f, 0.95f), PipeX - 3.0f, PipeY - 3.0f, PipeWidth + 6.0f, PipeHeight + 6.0f);
	// Pipe gold border
	DrawRect(FLinearColor(0.85f, 0.72f, 0.40f, 0.85f), PipeX - 1.0f, PipeY - 1.0f, PipeWidth + 2.0f, 1.0f);
	DrawRect(FLinearColor(0.85f, 0.72f, 0.40f, 0.85f), PipeX - 1.0f, PipeY + PipeHeight, PipeWidth + 2.0f, 1.0f);
	DrawRect(FLinearColor(0.85f, 0.72f, 0.40f, 0.85f), PipeX - 1.0f, PipeY - 1.0f, 1.0f, PipeHeight + 2.0f);
	DrawRect(FLinearColor(0.85f, 0.72f, 0.40f, 0.85f), PipeX + PipeWidth, PipeY - 1.0f, 1.0f, PipeHeight + 2.0f);

	// Inner fill (Emerald / Cyan glow #1CE8B5)
	const float FillWidth = PipeWidth * LoadingPipeProgress;
	if (FillWidth > 2.0f)
	{
		DrawRect(FLinearColor(0.11f, 0.91f, 0.71f, 0.95f), PipeX, PipeY, FillWidth, PipeHeight);
		// Top highlight strip inside the pipe for metallic cylindrical sheen
		DrawRect(FLinearColor(0.70f, 1.0f, 0.95f, 0.75f), PipeX, PipeY + 2.0f, FillWidth, 4.0f);
	}

	// Percentage Text
	int32 Pct = FMath::Clamp(FMath::RoundToInt(LoadingPipeProgress * 100.0f), 0, 100);
	const FString PctText = FString::Printf(TEXT("%d%%"), Pct);
	float PctW = 0.0f, PctH = 0.0f;
	GetTextSize(PctText, PctW, PctH, MedFont, 0.95f);
	DrawText(PctText, FLinearColor(0.98f, 0.98f, 1.0f, 1.0f), CenterX - (PctW * 0.5f), PipeY + 4.0f, MedFont, 0.95f);

	// Status label below pipe
	FString StatusStr = (LoadingPipeProgress < 1.0f)
		? TEXT("LOADING CAMPUS ASSETS & 1:1 METRIC ARCHITECTURAL TEXTURES...")
		: TEXT("INITIALIZATION COMPLETE • ENTERING MAIN MENU");
	float StatW = 0.0f, StatH = 0.0f;
	GetTextSize(StatusStr, StatW, StatH, SmallFont, 0.85f);
	DrawText(StatusStr, FLinearColor(0.75f, 0.75f, 0.80f, 0.85f), CenterX - (StatW * 0.5f), PipeY + PipeHeight + 14.0f, SmallFont, 0.85f);

	// Rotating Campus Lore / Gameplay Tips
	static const TArray<FString> Tips = {
		TEXT("টিপস: কার্জন হল ১৯০৪ সালে প্রতিষ্ঠিত ইন্দো-সারাসেনিক লাল ইটের ঐতিহ্যবাহী নিদর্শন।"),
		TEXT("টিপস: কেন্দ্রীয় শহীদ মিনার ১৯৫২ সালের ভাষা আন্দোলনের অমর শহীদদের স্মৃতিবিজড়িত স্মারক।"),
		TEXT("টিপস: [Shift] চেপে দৌড়ান এবং [Space] চেপে বাতাসে চিংগং (Qinggong) উইন্ড গ্লাইড করুন।"),
		TEXT("সতর্কতা: সাধারণ নিরীহ শিক্ষার্থীদের আঘাত করা সম্পূর্ণ নিষিদ্ধ। আঘাত করলে পুলিশ তাৎক্ষণিক গ্রেপ্তার করবে।")
	};
	int32 TipIdx = FMath::Clamp(FMath::FloorToInt(LoadingScreenTimer / 1.8f) % Tips.Num(), 0, Tips.Num() - 1);
	float TipW = 0.0f, TipH = 0.0f;
	GetTextSize(Tips[TipIdx], TipW, TipH, SmallFont, 0.95f);
	DrawText(Tips[TipIdx], FLinearColor(0.95f, 0.88f, 0.50f, 0.95f), CenterX - (TipW * 0.5f), ScreenHeight - 75.0f, SmallFont, 0.95f);

	// Check for completion transition
	if (LoadingPipeProgress >= 1.0f && !bLoadingComplete)
	{
		bLoadingComplete = true;
		CurrentMenuState = ESVMenuState::MainMenu;
		UE_LOG(LogTemp, Log, TEXT("[ASVHUD] Loading pipe complete! Transitioned to AAA Main Menu."));
	}
}

void ASVHUD::DrawMainMenu(float ScreenWidth, float ScreenHeight)
{
	DrawRect(FLinearColor(0.01f, 0.01f, 0.02f, 0.94f), 0.0f, 0.0f, ScreenWidth, ScreenHeight);

	const float MenuWidth = FMath::Min(ScreenWidth * 0.75f, 760.0f);
	const float MenuX = (ScreenWidth - MenuWidth) * 0.5f;
	const float MenuY = ScreenHeight * 0.12f;

	UFont* BigFont = GEngine->GetLargeFont();
	UFont* MedFont = GEngine->GetMediumFont();
	UFont* SmallFont = GEngine->GetSmallFont();

	// Main Title
	DrawText(TEXT("SPARKVISION 2x12"), FLinearColor(0.98f, 0.88f, 0.50f, 1.0f), MenuX, MenuY, BigFont, 1.4f);
	DrawText(TEXT("BIRTH OF 36 JULY: THE STUDENTS' RESISTANCE"), FLinearColor(0.85f, 0.85f, 0.90f, 0.95f), MenuX, MenuY + 45.0f, MedFont, 1.05f);

	DrawRect(FLinearColor(0.85f, 0.72f, 0.40f, 0.85f), MenuX, MenuY + 80.0f, MenuWidth, 2.0f);

	// Current Configuration Status Card
	ASVCharacter* PlayerChar = Cast<ASVCharacter>(UGameplayStatics::GetPlayerCharacter(GetWorld(), 0));
	bool bFemale = PlayerChar ? PlayerChar->bIsFemaleProtagonist : false;
	FString CharName = bFemale ? TEXT("Rina / রিনা (Female - Biochemistry & Molecular Biology)") : TEXT("Shovon / শোভন (Male - Department of Physics)");

	DrawRect(FLinearColor(0.05f, 0.07f, 0.10f, 0.85f), MenuX, MenuY + 95.0f, MenuWidth, 54.0f);
	DrawRect(FLinearColor(0.11f, 0.91f, 0.71f, 0.75f), MenuX, MenuY + 95.0f, 4.0f, 54.0f);
	DrawText(FString::Printf(TEXT("PROTAGONIST: %s"), *CharName), FLinearColor(0.95f, 0.95f, 0.98f, 1.0f), MenuX + 20.0f, MenuY + 102.0f, MedFont, 0.95f);
	DrawText(TEXT("ACTIVE WORLD: Dhaka University Campus (1:1 Metric Model | Curzon Hall Precinct)"), FLinearColor(0.75f, 0.85f, 0.90f, 0.90f), MenuX + 20.0f, MenuY + 128.0f, SmallFont, 0.85f);

	// Menu Options
	struct FMenuRow { int32 Key; FString Title; FString Sub; };
	TArray<FMenuRow> Rows = {
		{ 1, TEXT("[1]  START EXPLORATION"), TEXT("Spawn at Curzon Hall South Portico & begin 5-landmark journey") },
		{ 2, TEXT("[2]  SELECT PROTAGONIST"), TEXT("Choose between Shovon (Male) & Rina (Female)") },
		{ 3, TEXT("[3]  SELECT WORLD"), TEXT("DU Campus (Active) | Old Dhaka & Suhrawardy (Locked)") },
		{ 4, TEXT("[4]  SETTINGS & GRAPHICS"), TEXT("Configure Apple Silicon Metal resolution, post-processing & controls") },
		{ 5, TEXT("[5]  EXIT GAME"), TEXT("Quit to desktop") }
	};

	float RowY = MenuY + 170.0f;
	for (const auto& R : Rows)
	{
		DrawRect(FLinearColor(0.04f, 0.04f, 0.07f, 0.82f), MenuX, RowY - 4.0f, MenuWidth, 48.0f);
		DrawRect(FLinearColor(0.85f, 0.72f, 0.40f, 0.65f), MenuX, RowY - 4.0f, 3.0f, 48.0f);
		DrawText(R.Title, FLinearColor(0.98f, 0.95f, 0.88f, 1.0f), MenuX + 25.0f, RowY + 4.0f, MedFont, 1.0f);
		DrawText(R.Sub, FLinearColor(0.70f, 0.70f, 0.75f, 0.85f), MenuX + 25.0f, RowY + 27.0f, SmallFont, 0.85f);
		RowY += 60.0f;
	}

	DrawText(TEXT("Press 1, 2, 3, 4, or 5 to select   |   [Space] Quick Start"), FLinearColor(0.75f, 0.75f, 0.80f, 0.85f), MenuX, RowY + 15.0f, SmallFont, 0.9f);
}

void ASVHUD::DrawCharacterSelectMenu(float ScreenWidth, float ScreenHeight)
{
	DrawRect(FLinearColor(0.01f, 0.01f, 0.02f, 0.94f), 0.0f, 0.0f, ScreenWidth, ScreenHeight);

	const float MenuWidth = FMath::Min(ScreenWidth * 0.80f, 820.0f);
	const float MenuX = (ScreenWidth - MenuWidth) * 0.5f;
	const float MenuY = ScreenHeight * 0.15f;

	UFont* BigFont = GEngine->GetLargeFont();
	UFont* MedFont = GEngine->GetMediumFont();
	UFont* SmallFont = GEngine->GetSmallFont();

	DrawText(TEXT("SELECT PROTAGONIST | চরিত্র নির্বাচন"), FLinearColor(0.98f, 0.88f, 0.50f, 1.0f), MenuX, MenuY, BigFont, 1.3f);
	DrawText(TEXT("Choose your student perspective for the July 2024 campus movement"), FLinearColor(0.85f, 0.85f, 0.90f, 0.95f), MenuX, MenuY + 42.0f, MedFont, 1.0f);
	DrawRect(FLinearColor(0.85f, 0.72f, 0.40f, 0.85f), MenuX, MenuY + 75.0f, MenuWidth, 2.0f);

	ASVCharacter* PlayerChar = Cast<ASVCharacter>(UGameplayStatics::GetPlayerCharacter(GetWorld(), 0));
	bool bCurrentFemale = PlayerChar ? PlayerChar->bIsFemaleProtagonist : false;

	// Card 1: Male (Shovon)
	float Card1Y = MenuY + 100.0f;
	FLinearColor Border1 = (!bCurrentFemale) ? FLinearColor(0.11f, 0.91f, 0.71f, 1.0f) : FLinearColor(0.85f, 0.72f, 0.40f, 0.5f);
	DrawRect(FLinearColor(0.04f, 0.05f, 0.08f, 0.90f), MenuX, Card1Y, MenuWidth, 100.0f);
	DrawRect(Border1, MenuX, Card1Y, 4.0f, 100.0f);
	DrawText(TEXT("[1]  SHOVON (শোভন) - Male Protagonist  ") + FString(!bCurrentFemale ? TEXT("[CURRENTLY SELECTED]") : TEXT("")), FLinearColor(0.98f, 0.95f, 0.88f, 1.0f), MenuX + 25.0f, Card1Y + 12.0f, MedFont, 1.05f);
	DrawText(TEXT("• Department: Physics, Faculty of Science, University of Dhaka"), FLinearColor(0.85f, 0.85f, 0.90f, 0.95f), MenuX + 25.0f, Card1Y + 40.0f, SmallFont, 0.9f);
	DrawText(TEXT("• Specialty: Athletic stamina traversal, determined organizer, solid front-line resistance"), FLinearColor(0.75f, 0.75f, 0.80f, 0.90f), MenuX + 25.0f, Card1Y + 65.0f, SmallFont, 0.85f);

	// Card 2: Female (Rina)
	float Card2Y = MenuY + 220.0f;
	FLinearColor Border2 = (bCurrentFemale) ? FLinearColor(0.11f, 0.91f, 0.71f, 1.0f) : FLinearColor(0.85f, 0.72f, 0.40f, 0.5f);
	DrawRect(FLinearColor(0.04f, 0.05f, 0.08f, 0.90f), MenuX, Card2Y, MenuWidth, 100.0f);
	DrawRect(Border2, MenuX, Card2Y, 4.0f, 100.0f);
	DrawText(TEXT("[2]  RINA (রিনা) - Female Protagonist  ") + FString(bCurrentFemale ? TEXT("[CURRENTLY SELECTED]") : TEXT("")), FLinearColor(0.98f, 0.95f, 0.88f, 1.0f), MenuX + 25.0f, Card2Y + 12.0f, MedFont, 1.05f);
	DrawText(TEXT("• Department: Biochemistry & Molecular Biology, University of Dhaka"), FLinearColor(0.85f, 0.85f, 0.90f, 0.95f), MenuX + 25.0f, Card2Y + 40.0f, SmallFont, 0.9f);
	DrawText(TEXT("• Specialty: Agile Qinggong leap & glide, martial arts precision, fearless frontline voice"), FLinearColor(0.75f, 0.75f, 0.80f, 0.90f), MenuX + 25.0f, Card2Y + 65.0f, SmallFont, 0.85f);

	DrawText(TEXT("Press [1] for Shovon   |   Press [2] for Rina   |   [Esc] Back to Main Menu"), FLinearColor(0.75f, 0.75f, 0.80f, 0.85f), MenuX, Card2Y + 125.0f, SmallFont, 0.9f);
}

void ASVHUD::DrawWorldSelectMenu(float ScreenWidth, float ScreenHeight)
{
	DrawRect(FLinearColor(0.01f, 0.01f, 0.02f, 0.94f), 0.0f, 0.0f, ScreenWidth, ScreenHeight);

	const float MenuWidth = FMath::Min(ScreenWidth * 0.80f, 820.0f);
	const float MenuX = (ScreenWidth - MenuWidth) * 0.5f;
	const float MenuY = ScreenHeight * 0.15f;

	UFont* BigFont = GEngine->GetLargeFont();
	UFont* MedFont = GEngine->GetMediumFont();
	UFont* SmallFont = GEngine->GetSmallFont();

	DrawText(TEXT("SELECT WORLD REGION | বিশ্ব নির্বাচন"), FLinearColor(0.98f, 0.88f, 0.50f, 1.0f), MenuX, MenuY, BigFont, 1.3f);
	DrawText(TEXT("Dhaka historical exploration maps"), FLinearColor(0.85f, 0.85f, 0.90f, 0.95f), MenuX, MenuY + 42.0f, MedFont, 1.0f);
	DrawRect(FLinearColor(0.85f, 0.72f, 0.40f, 0.85f), MenuX, MenuY + 75.0f, MenuWidth, 2.0f);

	// World 1: DU Campus
	float W1Y = MenuY + 100.0f;
	DrawRect(FLinearColor(0.04f, 0.06f, 0.09f, 0.90f), MenuX, W1Y, MenuWidth, 80.0f);
	DrawRect(FLinearColor(0.11f, 0.91f, 0.71f, 1.0f), MenuX, W1Y, 4.0f, 80.0f);
	DrawText(TEXT("[1]  DHAKA UNIVERSITY CAMPUS (ঢাকা বিশ্ববিদ্যালয়)  [ACTIVE / PLAYABLE]"), FLinearColor(0.98f, 0.95f, 0.88f, 1.0f), MenuX + 25.0f, W1Y + 12.0f, MedFont, 1.0f);
	DrawText(TEXT("Curzon Hall, Doyel Chattar, Shaheed Minar, TSC & Raju Memorial, Arts Faculty"), FLinearColor(0.75f, 0.85f, 0.90f, 0.95f), MenuX + 25.0f, W1Y + 44.0f, SmallFont, 0.9f);

	// World 2: Old Dhaka
	float W2Y = MenuY + 200.0f;
	DrawRect(FLinearColor(0.03f, 0.03f, 0.04f, 0.80f), MenuX, W2Y, MenuWidth, 80.0f);
	DrawRect(FLinearColor(0.50f, 0.50f, 0.55f, 0.6f), MenuX, W2Y, 4.0f, 80.0f);
	DrawText(TEXT("[2]  OLD DHAKA & SADARGHAT (পুরান ঢাকা ও সদরঘাট)  [LOCKED / COMING SOON]"), FLinearColor(0.65f, 0.65f, 0.70f, 0.9f), MenuX + 25.0f, W2Y + 12.0f, MedFont, 1.0f);
	DrawText(TEXT("Ahsan Manzil, Shakharibazar heritage streets, Buriganga riverfront [Chapter 3]"), FLinearColor(0.55f, 0.55f, 0.60f, 0.85f), MenuX + 25.0f, W2Y + 44.0f, SmallFont, 0.9f);

	// World 3: Suhrawardy
	float W3Y = MenuY + 300.0f;
	DrawRect(FLinearColor(0.03f, 0.03f, 0.04f, 0.80f), MenuX, W3Y, MenuWidth, 80.0f);
	DrawRect(FLinearColor(0.50f, 0.50f, 0.55f, 0.6f), MenuX, W3Y, 4.0f, 80.0f);
	DrawText(TEXT("[3]  SUHRAWARDY UDYAN (সোহরাওয়ার্দী উদ্যান)  [LOCKED / COMING SOON]"), FLinearColor(0.65f, 0.65f, 0.70f, 0.9f), MenuX + 25.0f, W3Y + 12.0f, MedFont, 1.0f);
	DrawText(TEXT("Historic March 7th grounds, Shikha Chirantan eternal flame [Chapter 2]"), FLinearColor(0.55f, 0.55f, 0.60f, 0.85f), MenuX + 25.0f, W3Y + 44.0f, SmallFont, 0.9f);

	DrawText(TEXT("Press [1] to select DU Campus   |   [Esc] Back to Main Menu"), FLinearColor(0.75f, 0.75f, 0.80f, 0.85f), MenuX, W3Y + 105.0f, SmallFont, 0.9f);
}

void ASVHUD::DrawWaypointMarker(float ScreenWidth, float ScreenHeight)
{
	ASVCharacter* PlayerChar = Cast<ASVCharacter>(UGameplayStatics::GetPlayerCharacter(GetWorld(), 0));
	if (!PlayerChar) return;

	APlayerController* PC = Cast<APlayerController>(PlayerChar->GetController());
	if (!PC) return;

	FSVWaypoint ActiveWP = PlayerChar->GetActiveWaypoint();
	FVector TargetWorldPos = ActiveWP.Location + FVector(0.0f, 0.0f, 250.0f);

	float DistCm = FVector::Dist2D(PlayerChar->GetActorLocation(), ActiveWP.Location);
	float DistM = DistCm / 100.0f;

	FVector2D ScreenPos;
	bool bProjected = PC->ProjectWorldLocationToScreen(TargetWorldPos, ScreenPos);

	UFont* MedFont = GEngine->GetMediumFont();
	UFont* SmallFont = GEngine->GetSmallFont();

	// Pulsating glow factor
	float Pulse = 0.8f + 0.2f * FMath::Sin(GetWorld()->GetTimeSeconds() * 5.0f);
	FLinearColor MarkerColor = FLinearColor(0.11f, 0.91f, 0.71f, Pulse); // Cyan / Emerald
	if (PlayerChar->bAllWaypointsVisited)
	{
		MarkerColor = FLinearColor(0.98f, 0.25f, 0.25f, Pulse); // Crimson for Climax Battle
	}

	if (bProjected && ScreenPos.X >= 40.0f && ScreenPos.X <= ScreenWidth - 40.0f && ScreenPos.Y >= 40.0f && ScreenPos.Y <= ScreenHeight - 40.0f)
	{
		// 3D In-World Beacon Pin
		// Glowing diamond marker (layered rectangles)
		DrawRect(FLinearColor(0.02f, 0.02f, 0.03f, 0.85f), ScreenPos.X - 14.0f, ScreenPos.Y - 14.0f, 28.0f, 28.0f);
		DrawRect(MarkerColor, ScreenPos.X - 12.0f, ScreenPos.Y - 12.0f, 24.0f, 24.0f);
		DrawRect(FLinearColor(1.0f, 1.0f, 1.0f, 1.0f), ScreenPos.X - 4.0f, ScreenPos.Y - 4.0f, 8.0f, 8.0f);

		// Vertical light beam down
		DrawRect(FLinearColor(MarkerColor.R, MarkerColor.G, MarkerColor.B, 0.45f), ScreenPos.X - 1.0f, ScreenPos.Y + 14.0f, 2.0f, 35.0f);

		// Target Name & Distance tag
		FString DistText = (DistM >= 1000.0f)
			? FString::Printf(TEXT("%.1f km"), DistM / 1000.0f)
			: FString::Printf(TEXT("%d m"), FMath::RoundToInt(DistM));

		FString LabelStr = FString::Printf(TEXT("◆ %s [%s]"), *ActiveWP.NameEnglish.ToString(), *DistText);
		float TextW = 0.0f, TextH = 0.0f;
		GetTextSize(LabelStr, TextW, TextH, SmallFont, 0.95f);

		float LabelX = ScreenPos.X - (TextW * 0.5f);
		float LabelY = ScreenPos.Y - 32.0f;
		DrawRect(FLinearColor(0.02f, 0.02f, 0.04f, 0.88f), LabelX - 6.0f, LabelY - 2.0f, TextW + 12.0f, 20.0f);
		DrawRect(MarkerColor, LabelX - 6.0f, LabelY - 2.0f, TextW + 12.0f, 1.0f);
		DrawText(LabelStr, FLinearColor(0.98f, 0.95f, 0.88f, 1.0f), LabelX, LabelY, SmallFont, 0.95f);
	}
	else
	{
		// Off-screen indicator clamped to screen border (Where Winds Meet style arrow)
		FVector CamLoc;
		FRotator CamRot;
		PC->GetPlayerViewPoint(CamLoc, CamRot);
		FVector DirToTarget = (ActiveWP.Location - CamLoc).GetSafeNormal2D();
		FVector CamRight = FRotationMatrix(CamRot).GetScaledAxis(EAxis::Y).GetSafeNormal2D();

		float RightDot = FVector::DotProduct(CamRight, DirToTarget);

		float EdgeX = (RightDot > 0.0f) ? (ScreenWidth - 120.0f) : 120.0f;
		float EdgeY = ScreenHeight * 0.45f;

		FString ArrowStr = (RightDot > 0.0f) ? TEXT("▶ ") : TEXT("◀ ");
		FString DistText = (DistM >= 1000.0f) ? FString::Printf(TEXT("%.1f km"), DistM / 1000.0f) : FString::Printf(TEXT("%d m"), FMath::RoundToInt(DistM));
		FString OffscreenStr = ArrowStr + ActiveWP.NameEnglish.ToString() + TEXT(" (") + DistText + TEXT(")");

		DrawRect(FLinearColor(0.02f, 0.02f, 0.04f, 0.85f), EdgeX - 80.0f, EdgeY - 4.0f, 180.0f, 24.0f);
		DrawRect(MarkerColor, EdgeX - 80.0f, EdgeY - 4.0f, 180.0f, 1.5f);
		DrawText(OffscreenStr, FLinearColor(0.98f, 0.95f, 0.88f, 1.0f), EdgeX - 70.0f, EdgeY, SmallFont, 0.85f);
	}
}

void ASVHUD::DrawPoliceArrestModal(float ScreenWidth, float ScreenHeight)
{
	// Flashing red & blue police siren bar at top & bottom
	float Sine = FMath::Sin(GetWorld()->GetTimeSeconds() * 10.0f);
	FLinearColor SirenColor = (Sine > 0.0f) ? FLinearColor(0.9f, 0.1f, 0.1f, 0.9f) : FLinearColor(0.1f, 0.3f, 0.9f, 0.9f);
	DrawRect(SirenColor, 0.0f, 0.0f, ScreenWidth, 12.0f);
	DrawRect(SirenColor, 0.0f, ScreenHeight - 12.0f, ScreenWidth, 12.0f);

	// Dark semi-transparent background with red vignette
	DrawRect(FLinearColor(0.04f, 0.01f, 0.01f, 0.92f), 0.0f, 0.0f, ScreenWidth, ScreenHeight);

	const float ModalWidth = FMath::Min(ScreenWidth * 0.80f, 840.0f);
	const float ModalHeight = 360.0f;
	const float ModalX = (ScreenWidth - ModalWidth) * 0.5f;
	const float ModalY = (ScreenHeight - ModalHeight) * 0.5f;

	// Panel Box
	DrawRect(FLinearColor(0.08f, 0.02f, 0.02f, 0.96f), ModalX, ModalY, ModalWidth, ModalHeight);
	DrawRect(FLinearColor(0.95f, 0.20f, 0.20f, 1.0f), ModalX, ModalY, ModalWidth, 3.0f);
	DrawRect(FLinearColor(0.95f, 0.20f, 0.20f, 1.0f), ModalX, ModalY + ModalHeight - 3.0f, ModalWidth, 3.0f);
	DrawRect(FLinearColor(0.95f, 0.20f, 0.20f, 1.0f), ModalX, ModalY, 3.0f, ModalHeight);
	DrawRect(FLinearColor(0.95f, 0.20f, 0.20f, 1.0f), ModalX + ModalWidth - 3.0f, ModalY, 3.0f, ModalHeight);

	UFont* BigFont = GEngine->GetLargeFont();
	UFont* MedFont = GEngine->GetMediumFont();
	UFont* SmallFont = GEngine->GetSmallFont();

	// Headline
	DrawText(TEXT("BUSTED / পুলিশি গ্রেপ্তার"), FLinearColor(0.98f, 0.25f, 0.25f, 1.0f), ModalX + 40.0f, ModalY + 30.0f, BigFont, 1.4f);
	DrawText(TEXT("CIVILIAN ASSAULT DETECTED • CAMPUS POLICE INTERVENTION"), FLinearColor(0.85f, 0.85f, 0.90f, 0.90f), ModalX + 40.0f, ModalY + 80.0f, MedFont, 1.0f);

	DrawRect(FLinearColor(0.95f, 0.25f, 0.25f, 0.70f), ModalX + 40.0f, ModalY + 115.0f, ModalWidth - 80.0f, 1.5f);

	// Narrative Explanation
	DrawText(TEXT("আপনি সাধারণ নিরীহ শিক্ষার্থী / পথচারীর উপর আক্রমণ করেছেন!"), FLinearColor(0.98f, 0.95f, 0.90f, 1.0f), ModalX + 40.0f, ModalY + 135.0f, MedFont, 1.05f);
	FString VictimStr = FString::Printf(TEXT("Assault against civilian (%s) reported to Proctorial Body & DMP."), *PoliceVictimName);
	DrawText(VictimStr, FLinearColor(0.85f, 0.85f, 0.90f, 0.90f), ModalX + 40.0f, ModalY + 170.0f, SmallFont, 0.95f);
	DrawText(TEXT("সহিংসতা ও নিরপরাধের উপর আক্রমণ ঢাকা বিশ্ববিদ্যালয়ের গণতান্ত্রিক মূল্যবোধ পরিপন্থী।"), FLinearColor(0.80f, 0.80f, 0.85f, 0.90f), ModalX + 40.0f, ModalY + 200.0f, SmallFont, 0.95f);
	DrawText(TEXT("ঢাকা মেট্রোপলিটন পুলিশ আপনাকে তাৎক্ষণিকভাবে আটক করায় অভিযান সমাপ্ত ঘোষণা করা হলো।"), FLinearColor(0.80f, 0.80f, 0.85f, 0.90f), ModalX + 40.0f, ModalY + 225.0f, SmallFont, 0.95f);

	// Action buttons
	DrawRect(FLinearColor(0.04f, 0.04f, 0.07f, 0.85f), ModalX + 40.0f, ModalY + 265.0f, ModalWidth - 80.0f, 44.0f);
	DrawRect(FLinearColor(0.85f, 0.72f, 0.40f, 0.80f), ModalX + 40.0f, ModalY + 265.0f, 3.0f, 44.0f);
	DrawText(TEXT("[1] / [Space]  RESTART AT CURZON HALL       [2]  RETURN TO MAIN MENU"), FLinearColor(0.98f, 0.95f, 0.88f, 1.0f), ModalX + 60.0f, ModalY + 278.0f, MedFont, 0.95f);
}

void ASVHUD::DrawCombatDefeatModal(float ScreenWidth, float ScreenHeight)
{
	DrawRect(FLinearColor(0.03f, 0.01f, 0.01f, 0.93f), 0.0f, 0.0f, ScreenWidth, ScreenHeight);

	const float ModalWidth = FMath::Min(ScreenWidth * 0.82f, 860.0f);
	const float ModalHeight = 390.0f;
	const float ModalX = (ScreenWidth - ModalWidth) * 0.5f;
	const float ModalY = (ScreenHeight - ModalHeight) * 0.5f;

	// Panel Box
	DrawRect(FLinearColor(0.06f, 0.02f, 0.02f, 0.96f), ModalX, ModalY, ModalWidth, ModalHeight);
	DrawRect(FLinearColor(0.90f, 0.30f, 0.20f, 1.0f), ModalX, ModalY, ModalWidth, 3.0f);
	DrawRect(FLinearColor(0.90f, 0.30f, 0.20f, 1.0f), ModalX, ModalY + ModalHeight - 3.0f, ModalWidth, 3.0f);
	DrawRect(FLinearColor(0.90f, 0.30f, 0.20f, 1.0f), ModalX, ModalY, 3.0f, ModalHeight);
	DrawRect(FLinearColor(0.90f, 0.30f, 0.20f, 1.0f), ModalX + ModalWidth - 3.0f, ModalY, 3.0f, ModalHeight);

	UFont* BigFont = GEngine->GetLargeFont();
	UFont* MedFont = GEngine->GetMediumFont();
	UFont* SmallFont = GEngine->GetSmallFont();

	// Title
	DrawText(TEXT("DEFEATED / আঘাতপ্রাপ্ত"), FLinearColor(0.98f, 0.30f, 0.25f, 1.0f), ModalX + 40.0f, ModalY + 28.0f, BigFont, 1.4f);
	DrawText(TEXT("JULY 2024: CLIMACTIC CONFRONTATION WITH MOTORCYCLE CADRE SQUAD"), FLinearColor(0.85f, 0.85f, 0.90f, 0.90f), ModalX + 40.0f, ModalY + 76.0f, MedFont, 1.0f);

	DrawRect(FLinearColor(0.90f, 0.30f, 0.20f, 0.70f), ModalX + 40.0f, ModalY + 110.0f, ModalWidth - 80.0f, 1.5f);

	// Opposition Squad Info
	DrawText(TEXT("ক্যাডার প্রধান: নৌকা অঙ্কিত ক্যাপ পরিহিত স্কোয়াড লিডার (Nouka Cap Leader)"), FLinearColor(0.98f, 0.85f, 0.40f, 1.0f), ModalX + 40.0f, ModalY + 128.0f, MedFont, 0.95f);
	DrawText(TEXT("আক্রমণকারী দল: হেলমেট পরিহিত মোটরসাইকেল ক্যাডার ও লাঠিয়াল বাহিনী (Helmeted Cadres with Lathis)"), FLinearColor(0.85f, 0.85f, 0.90f, 0.90f), ModalX + 40.0f, ModalY + 158.0f, SmallFont, 0.95f);

	// Attempt Counter Pill
	FString AttemptStr = FString::Printf(TEXT("RESISTANCE ATTEMPT: [ %d / %d ]"), ClimaxAttemptNum, ClimaxMaxAttempts);
	DrawRect(FLinearColor(0.12f, 0.04f, 0.04f, 0.90f), ModalX + 40.0f, ModalY + 192.0f, 280.0f, 32.0f);
	DrawRect(FLinearColor(0.90f, 0.30f, 0.20f, 0.85f), ModalX + 40.0f, ModalY + 192.0f, 3.0f, 32.0f);
	DrawText(AttemptStr, FLinearColor(0.98f, 0.40f, 0.35f, 1.0f), ModalX + 55.0f, ModalY + 199.0f, MedFont, 0.95f);

	if (bClimaxRetryAllowed)
	{
		DrawText(TEXT("অস্ত্রধারীদের হামলার মুখে আপনি আঘাতপ্রাপ্ত হয়েছেন। কিন্তু ছাত্রদের মনোবল ভাঙেনি!"), FLinearColor(0.92f, 0.92f, 0.95f, 1.0f), ModalX + 40.0f, ModalY + 242.0f, MedFont, 0.95f);
		DrawText(TEXT("মার্শাল আর্ট প্রতিহত কৌশলে আবার লড়াই করুন।"), FLinearColor(0.80f, 0.80f, 0.85f, 0.90f), ModalX + 40.0f, ModalY + 272.0f, SmallFont, 0.90f);

		DrawRect(FLinearColor(0.04f, 0.04f, 0.07f, 0.85f), ModalX + 40.0f, ModalY + 310.0f, ModalWidth - 80.0f, 44.0f);
		DrawRect(FLinearColor(0.11f, 0.91f, 0.71f, 0.85f), ModalX + 40.0f, ModalY + 310.0f, 3.0f, 44.0f);
		DrawText(TEXT("[1] / [Space]  RETRY COMBAT (পুনরায় লড়াই)       [2]  RETURN TO MAIN MENU"), FLinearColor(0.98f, 0.95f, 0.88f, 1.0f), ModalX + 60.0f, ModalY + 323.0f, MedFont, 0.95f);
	}
	else
	{
		// 3 Retries Exhausted -> Dramatic Climax Transition
		DrawText(TEXT("অস্ত্রধারীদের নির্মম হামলার মুখে শিক্ষার্থীদের প্রত্যক্ষ প্রতিরোধ সাময়িকভাবে স্তব্ধ..."), FLinearColor(0.98f, 0.88f, 0.45f, 1.0f), ModalX + 40.0f, ModalY + 238.0f, MedFont, 1.0f);
		DrawText(TEXT("কিন্তু যে চেতনার স্ফুলিঙ্গ আজ জ্বলে উঠেছে, তা গোটা দেশকে জাগিয়ে জন্ম দেবে ৩৬ জুলাইয়ের!"), FLinearColor(0.95f, 0.95f, 0.98f, 1.0f), ModalX + 40.0f, ModalY + 268.0f, MedFont, 0.95f);
		DrawText(TEXT("Your courageous stand marks the inevitable dawn of the nationwide student movement."), FLinearColor(0.75f, 0.80f, 0.85f, 0.90f), ModalX + 40.0f, ModalY + 296.0f, SmallFont, 0.85f);

		DrawRect(FLinearColor(0.04f, 0.04f, 0.07f, 0.85f), ModalX + 40.0f, ModalY + 322.0f, ModalWidth - 80.0f, 44.0f);
		DrawRect(FLinearColor(0.85f, 0.72f, 0.40f, 0.85f), ModalX + 40.0f, ModalY + 322.0f, 3.0f, 44.0f);
		DrawText(TEXT("[1] / [Space]  RETURN TO AAA MAIN MENU (প্রধান মেনুতে ফিরে যান)"), FLinearColor(0.98f, 0.95f, 0.88f, 1.0f), ModalX + 60.0f, ModalY + 335.0f, MedFont, 0.95f);
	}
}

void ASVHUD::StartGameFromMenu()
{
	ASVCharacter* PlayerChar = Cast<ASVCharacter>(UGameplayStatics::GetPlayerCharacter(GetWorld(), 0));
	if (PlayerChar)
	{
		PlayerChar->TeleportToCurzon();
		PlayerChar->ActiveMissionId = TEXT("L1_M01");
		PlayerChar->bIsArrested = false;
		PlayerChar->CurrentHealth = PlayerChar->MaxHealth;
		PlayerChar->CurrentQi = PlayerChar->MaxQi;
		PlayerChar->GetCharacterMovement()->SetMovementMode(MOVE_Walking);

		if (APlayerController* PC = Cast<APlayerController>(PlayerChar->GetController()))
		{
			PlayerChar->EnableInput(PC);
		}
	}
	CurrentMenuState = ESVMenuState::None;
	UE_LOG(LogTemp, Log, TEXT("[ASVHUD] Started game from menu! Teleported to Curzon Hall."));
}

void ASVHUD::DisplayPoliceArrest(const FString& InVictimName)
{
	PoliceVictimName = InVictimName;
	bShowingPoliceArrest = true;
	CurrentMenuState = ESVMenuState::PoliceArrest;
	UE_LOG(LogTemp, Warning, TEXT("[ASVHUD] Police arrest modal displayed for victim: %s"), *InVictimName);
}

void ASVHUD::DisplayCombatDefeat(int32 Attempt, int32 MaxAttempts, bool bRetryAllowed)
{
	ClimaxAttemptNum = Attempt;
	ClimaxMaxAttempts = MaxAttempts;
	bClimaxRetryAllowed = bRetryAllowed;
	bShowingCombatDefeat = true;
	CurrentMenuState = ESVMenuState::CombatDefeat;
	UE_LOG(LogTemp, Warning, TEXT("[ASVHUD] Combat defeat modal displayed: Attempt %d/%d (RetryAllowed: %d)"),
		Attempt, MaxAttempts, bRetryAllowed ? 1 : 0);
}

void ASVHUD::DrawPauseMenu(float ScreenWidth, float ScreenHeight)
{
	DrawRect(FLinearColor(0.01f, 0.01f, 0.02f, 0.85f), 0.0f, 0.0f, ScreenWidth, ScreenHeight);

	const float MenuWidth = 550.0f;
	const float MenuX = (ScreenWidth - MenuWidth) * 0.5f;
	const float MenuY = ScreenHeight * 0.22f;

	UFont* BigFont = GEngine->GetLargeFont();
	UFont* MedFont = GEngine->GetMediumFont();
	UFont* SmallFont = GEngine->GetSmallFont();

	DrawText(TEXT("CAMPUS EXPLORATION PAUSED"), FLinearColor(0.95f, 0.85f, 0.50f, 1.0f), MenuX, MenuY, BigFont, 1.15f);
	DrawRect(FLinearColor(0.85f, 0.72f, 0.40f, 0.85f), MenuX, MenuY + 45.0f, MenuWidth, 2.0f);

	TArray<FString> PauseOptions = {
		TEXT("[1]  Resume Campus Exploration"),
		TEXT("[2]  Save Progress to Disk"),
		TEXT("[3]  Load Last Saved Checkpoint"),
		TEXT("[4]  Restart Chapter 1 (Curzon Hall)"),
		TEXT("[5]  Return to Main Menu")
	};

	float OptY = MenuY + 70.0f;
	for (const auto& OptStr : PauseOptions)
	{
		DrawRect(FLinearColor(0.04f, 0.04f, 0.07f, 0.80f), MenuX, OptY - 4.0f, MenuWidth, 38.0f);
		DrawRect(FLinearColor(0.85f, 0.72f, 0.40f, 0.60f), MenuX, OptY - 4.0f, 3.0f, 38.0f);
		DrawText(OptStr, FLinearColor(0.95f, 0.95f, 0.98f, 1.0f), MenuX + 20.0f, OptY + 5.0f, MedFont, 0.95f);
		OptY += 50.0f;
	}

	DrawText(TEXT("Press 1–5 to select   |   [Esc / P] Resume Exploration"), FLinearColor(0.70f, 0.70f, 0.75f, 0.85f), MenuX, OptY + 15.0f, SmallFont, 0.9f);
}

void ASVHUD::DrawSettingsMenu(float ScreenWidth, float ScreenHeight)
{
	DrawRect(FLinearColor(0.01f, 0.01f, 0.02f, 0.88f), 0.0f, 0.0f, ScreenWidth, ScreenHeight);

	const float MenuWidth = 650.0f;
	const float MenuX = (ScreenWidth - MenuWidth) * 0.5f;
	const float MenuY = ScreenHeight * 0.22f;

	UFont* BigFont = GEngine->GetLargeFont();
	UFont* MedFont = GEngine->GetMediumFont();
	UFont* SmallFont = GEngine->GetSmallFont();

	DrawText(TEXT("SETTINGS & GRAPHICS SCALABILITY"), FLinearColor(0.95f, 0.85f, 0.50f, 1.0f), MenuX, MenuY, BigFont, 1.15f);
	DrawRect(FLinearColor(0.85f, 0.72f, 0.40f, 0.85f), MenuX, MenuY + 45.0f, MenuWidth, 2.0f);

	DrawText(TEXT("• Target Hardware: Apple Silicon MacBook Air M4 (16 GB Unified Memory)"), FLinearColor(0.90f, 0.90f, 0.95f, 1.0f), MenuX, MenuY + 70.0f, MedFont, 0.9f);
	DrawText(TEXT("• Recommended Resolution: 1280x720 (Scalable) or 1920x1080"), FLinearColor(0.85f, 0.85f, 0.90f, 0.95f), MenuX, MenuY + 105.0f, MedFont, 0.9f);
	DrawText(TEXT("• Anti-Aliasing: TSR / Metal Scalable Post-Processing"), FLinearColor(0.85f, 0.85f, 0.90f, 0.95f), MenuX, MenuY + 140.0f, MedFont, 0.9f);
	DrawText(TEXT("• Foliage Instancing: Native Nanite & Foliage LOD Culling Active"), FLinearColor(0.85f, 0.85f, 0.90f, 0.95f), MenuX, MenuY + 175.0f, MedFont, 0.9f);

	DrawText(TEXT("Press any number (1–5) or [Esc] to return"), FLinearColor(0.70f, 0.70f, 0.75f, 0.85f), MenuX, MenuY + 230.0f, SmallFont, 0.9f);
}

void ASVHUD::DrawControlsMenu(float ScreenWidth, float ScreenHeight)
{
	DrawRect(FLinearColor(0.01f, 0.01f, 0.02f, 0.88f), 0.0f, 0.0f, ScreenWidth, ScreenHeight);

	const float MenuWidth = 700.0f;
	const float MenuX = (ScreenWidth - MenuWidth) * 0.5f;
	const float MenuY = ScreenHeight * 0.18f;

	UFont* BigFont = GEngine->GetLargeFont();
	UFont* MedFont = GEngine->GetMediumFont();
	UFont* SmallFont = GEngine->GetSmallFont();

	DrawText(TEXT("CONTROLS & CAMPUS TRAVERSAL GUIDE"), FLinearColor(0.95f, 0.85f, 0.50f, 1.0f), MenuX, MenuY, BigFont, 1.15f);
	DrawRect(FLinearColor(0.85f, 0.72f, 0.40f, 0.85f), MenuX, MenuY + 45.0f, MenuWidth, 2.0f);

	struct FControlRow { FString Key; FString Desc; };
	TArray<FControlRow> Rows = {
		{ TEXT("W / A / S / D"), TEXT("Walk / Jog across campus (550 cm/s)") },
		{ TEXT("Left Shift (Hold)"), TEXT("Athletic sprint traversal (950 cm/s)") },
		{ TEXT("Space"), TEXT("Jump / Clamber over obstacles") },
		{ TEXT("Mouse Look"), TEXT("360° dynamic camera orbit around player") },
		{ TEXT("E"), TEXT("Inspect Heritage Terminals & Speak with Student NPCs") },
		{ TEXT("1 – 6"), TEXT("Instant Fast Travel between 6 DU Landmarks") },
		{ TEXT("Esc / P"), TEXT("Open Pause Menu / Save / Load") }
	};

	float RowY = MenuY + 70.0f;
	for (const auto& R : Rows)
	{
		DrawText(R.Key, FLinearColor(0.95f, 0.85f, 0.45f, 1.0f), MenuX + 15.0f, RowY, MedFont, 0.95f);
		DrawText(R.Desc, FLinearColor(0.90f, 0.90f, 0.95f, 1.0f), MenuX + 220.0f, RowY, MedFont, 0.95f);
		RowY += 34.0f;
	}

	DrawText(TEXT("Press any key or [Esc] to return"), FLinearColor(0.70f, 0.70f, 0.75f, 0.85f), MenuX, RowY + 20.0f, SmallFont, 0.9f);
}

void ASVHUD::DrawCreditsMenu(float ScreenWidth, float ScreenHeight)
{
	DrawRect(FLinearColor(0.01f, 0.01f, 0.02f, 0.88f), 0.0f, 0.0f, ScreenWidth, ScreenHeight);

	const float MenuWidth = 680.0f;
	const float MenuX = (ScreenWidth - MenuWidth) * 0.5f;
	const float MenuY = ScreenHeight * 0.20f;

	UFont* BigFont = GEngine->GetLargeFont();
	UFont* MedFont = GEngine->GetMediumFont();
	UFont* SmallFont = GEngine->GetSmallFont();

	DrawText(TEXT("SPARKVISION : HERITAGE & PROJECT CREDITS"), FLinearColor(0.95f, 0.85f, 0.50f, 1.0f), MenuX, MenuY, BigFont, 1.15f);
	DrawRect(FLinearColor(0.85f, 0.72f, 0.40f, 0.85f), MenuX, MenuY + 45.0f, MenuWidth, 2.0f);

	DrawText(TEXT("SPARKVISION: BIRTH OF 36 JULY is a 3D historical exploration game"), FLinearColor(0.92f, 0.92f, 0.95f, 1.0f), MenuX, MenuY + 70.0f, MedFont, 0.9f);
	DrawText(TEXT("honoring the university students and citizens of the July 2024 movement in Bangladesh."), FLinearColor(0.85f, 0.85f, 0.90f, 0.95f), MenuX, MenuY + 98.0f, MedFont, 0.9f);

	DrawText(TEXT("Architectural Reconstruction:"), FLinearColor(0.95f, 0.85f, 0.45f, 1.0f), MenuX, MenuY + 140.0f, MedFont, 0.95f);
	DrawText(TEXT("1:1 Metric Model of University of Dhaka (Curzon Hall, Doyel Chattar,"), FLinearColor(0.90f, 0.90f, 0.95f, 1.0f), MenuX, MenuY + 165.0f, SmallFont, 0.95f);
	DrawText(TEXT("Shaheed Minar, TSC, Central Library, Kala Bhaban)."), FLinearColor(0.90f, 0.90f, 0.95f, 1.0f), MenuX, MenuY + 185.0f, SmallFont, 0.95f);

	DrawText(TEXT("Press any key or [Esc] to return"), FLinearColor(0.70f, 0.70f, 0.75f, 0.85f), MenuX, MenuY + 235.0f, SmallFont, 0.9f);
}
