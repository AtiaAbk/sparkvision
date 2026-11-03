// Copyright SparkVision Dhaka University. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/HUD.h"
#include "SVHUD.generated.h"

UENUM(BlueprintType)
enum class ESVMenuState : uint8
{
	None,
	LoadingScreen,
	MainMenu,
	CharacterSelect,
	WorldSelect,
	PauseMenu,
	SettingsMenu,
	ControlsMenu,
	CreditsMenu,
	PoliceArrest,
	CombatDefeat
};

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

	UFUNCTION(BlueprintCallable, Category = "SparkVision|UI")
	void DisplayNPCDialogue(const FText& SpeakerName, const FText& InNPCRole, const FText& Bengali, const FText& English);

	UFUNCTION(BlueprintCallable, Category = "SparkVision|UI")
	void DismissNPCDialogue();

	UFUNCTION(BlueprintCallable, Category = "SparkVision|UI")
	void DisplayChapterVictory(const FText& DecisionTitle, const FText& SubtitleText, const FText& UnlockText);

	UFUNCTION(BlueprintCallable, Category = "SparkVision|UI")
	void DismissChapterVictory();

	void TogglePauseMenu();
	void ToggleMainMenu();
	void SetMenuState(ESVMenuState NewState) { CurrentMenuState = NewState; }
	ESVMenuState GetMenuState() const { return CurrentMenuState; }
	bool IsMenuOpen() const { return CurrentMenuState != ESVMenuState::None; }

	void HandleMenuAction(int32 OptionIndex);
	void DisplayPoliceArrest(const FString& InVictimName);
	void DisplayCombatDefeat(int32 Attempt, int32 MaxAttempts, bool bRetryAllowed);
	void StartGameFromMenu();

	UPROPERTY(BlueprintReadWrite, Category = "SparkVision|UI")
	int32 SelectedMenuIndex = 0;

	void MenuNavigateUp();
	void MenuNavigateDown();
	void MenuConfirmSelection();

protected:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SparkVision|UI")
	bool bShowCompass = true;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SparkVision|UI")
	bool bShowVitals = true;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SparkVision|UI")
	bool bLetterboxActive = false;

	float LetterboxProgress = 0.0f;

	// Loading Screen & Dynamic Menu
	float LoadingPipeProgress = 0.0f;
	float LoadingScreenTimer = 0.0f;
	bool bLoadingComplete = false;

	// Police Arrest Consequence
	bool bShowingPoliceArrest = false;
	FString PoliceVictimName;

	// Climax Combat Defeat
	bool bShowingCombatDefeat = false;
	int32 ClimaxAttemptNum = 1;
	int32 ClimaxMaxAttempts = 3;
	bool bClimaxRetryAllowed = true;

	// Archive Modal
	bool bShowingArchiveCard = false;
	FText ActiveArchiveTitle;
	FText ActiveArchiveDescription;
	float CardDisplayDuration = 0.0f;

	// NPC Dialogue
	bool bShowingDialogue = false;
	FText DialogueSpeakerName;
	FText DialogueSpeakerRole;
	FText DialogueBengaliText;
	FText DialogueEnglishSubtitle;
	float DialogueDuration = 0.0f;

	// Chapter 1 Complete Victory Modal
	bool bShowingVictoryModal = false;
	FText VictoryHeadline;
	FText VictorySubtitle;
	FText VictoryUnlockNotice;

	// Menu State
	ESVMenuState CurrentMenuState = ESVMenuState::LoadingScreen;

private:
	void DrawLoadingScreen(float ScreenWidth, float ScreenHeight);
	void DrawWaypointMarker(float ScreenWidth, float ScreenHeight);
	void DrawPoliceArrestModal(float ScreenWidth, float ScreenHeight);
	void DrawCombatDefeatModal(float ScreenWidth, float ScreenHeight);
	void DrawCompassRibbon(float ScreenWidth, float ScreenHeight, float CameraYaw);
	void DrawVitalsGauge(float ScreenWidth, float ScreenHeight);
	void DrawInteractionPrompt(float ScreenWidth, float ScreenHeight);
	void DrawLetterboxBars(float ScreenWidth, float ScreenHeight);
	void DrawArchiveModal(float ScreenWidth, float ScreenHeight);
	void DrawNPCDialogueModal(float ScreenWidth, float ScreenHeight);
	void DrawObjectiveTracker(float ScreenWidth, float ScreenHeight);
	void DrawVictoryModal(float ScreenWidth, float ScreenHeight);
	void DrawMainMenu(float ScreenWidth, float ScreenHeight);
	void DrawCharacterSelectMenu(float ScreenWidth, float ScreenHeight);
	void DrawWorldSelectMenu(float ScreenWidth, float ScreenHeight);
	void DrawPauseMenu(float ScreenWidth, float ScreenHeight);
	void DrawSettingsMenu(float ScreenWidth, float ScreenHeight);
	void DrawControlsMenu(float ScreenWidth, float ScreenHeight);
	void DrawCreditsMenu(float ScreenWidth, float ScreenHeight);
};
