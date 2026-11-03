// Copyright SparkVision Dhaka University. All Rights Reserved.

#include "SVHUD.h"
#include "Engine/Canvas.h"
#include "Engine/Engine.h"
#include "SVCharacter.h"
#include "Kismet/GameplayStatics.h"
#include "SVMissionControlSubsystem.h"

ASVHUD::ASVHUD()
{
	bShowCompass = true;
	bShowVitals = true;
	CurrentMenuState = ESVMenuState::None;
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

	if (CurrentMenuState == ESVMenuState::MainMenu)
	{
		switch (OptionIndex)
		{
		case 1: // Start New Game
			if (PlayerChar)
			{
				PlayerChar->TeleportToCurzon();
				PlayerChar->ActiveMissionId = TEXT("L1_M01");
			}
			CurrentMenuState = ESVMenuState::None;
			break;
		case 2: // Continue Saved Game
			if (PlayerChar)
			{
				PlayerChar->LoadGameProgress();
			}
			CurrentMenuState = ESVMenuState::None;
			break;
		case 3: // Controls
			CurrentMenuState = ESVMenuState::ControlsMenu;
			break;
		case 4: // Settings
			CurrentMenuState = ESVMenuState::SettingsMenu;
			break;
		case 5: // Credits
			CurrentMenuState = ESVMenuState::CreditsMenu;
			break;
		default:
			CurrentMenuState = ESVMenuState::None;
			break;
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
			if (PlayerChar)
			{
				PlayerChar->TeleportToCurzon();
				PlayerChar->ActiveMissionId = TEXT("L1_M01");
			}
			CurrentMenuState = ESVMenuState::None;
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
		// In submenus, any selection returns to previous menu
		CurrentMenuState = ESVMenuState::PauseMenu;
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

void ASVHUD::DrawMainMenu(float ScreenWidth, float ScreenHeight)
{
	DrawRect(FLinearColor(0.01f, 0.01f, 0.02f, 0.92f), 0.0f, 0.0f, ScreenWidth, ScreenHeight);

	const float MenuWidth = 600.0f;
	const float MenuX = (ScreenWidth - MenuWidth) * 0.5f;
	const float MenuY = ScreenHeight * 0.18f;

	UFont* BigFont = GEngine->GetLargeFont();
	UFont* MedFont = GEngine->GetMediumFont();
	UFont* SmallFont = GEngine->GetSmallFont();

	// Main Title
	DrawText(TEXT("SPARKVISION : BIRTH OF 36 JULY"), FLinearColor(0.98f, 0.88f, 0.50f, 1.0f), MenuX, MenuY, BigFont, 1.25f);
	DrawText(TEXT("Chapter 1: \"Where It All Began\" (July 1–14, 2024)"), FLinearColor(0.82f, 0.82f, 0.88f, 0.95f), MenuX, MenuY + 45.0f, MedFont, 1.0f);

	DrawRect(FLinearColor(0.85f, 0.72f, 0.40f, 0.85f), MenuX, MenuY + 80.0f, MenuWidth, 2.0f);

	// Menu Options
	struct FMenuOption { int32 Key; FString Label; };
	TArray<FMenuOption> Options = {
		{ 1, TEXT("[1]  Start New Game (Curzon Promenade)") },
		{ 2, TEXT("[2]  Continue Saved Game") },
		{ 3, TEXT("[3]  Controls & Traversal Guide") },
		{ 4, TEXT("[4]  Settings & Graphics Quality") },
		{ 5, TEXT("[5]  Project Heritage & Credits") }
	};

	float OptY = MenuY + 110.0f;
	for (const auto& Opt : Options)
	{
		DrawRect(FLinearColor(0.04f, 0.04f, 0.07f, 0.80f), MenuX, OptY - 4.0f, MenuWidth, 42.0f);
		DrawRect(FLinearColor(0.85f, 0.72f, 0.40f, 0.60f), MenuX, OptY - 4.0f, 3.0f, 42.0f);
		DrawText(Opt.Label, FLinearColor(0.95f, 0.95f, 0.98f, 1.0f), MenuX + 25.0f, OptY + 6.0f, MedFont, 1.0f);
		OptY += 56.0f;
	}

	DrawText(TEXT("Press 1, 2, 3, 4, or 5 to select   |   [Esc] Return to Campus"), FLinearColor(0.70f, 0.70f, 0.75f, 0.85f), MenuX, OptY + 20.0f, SmallFont, 0.9f);
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
