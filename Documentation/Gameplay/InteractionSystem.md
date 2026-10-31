# SPARKVISION — INTERACTION SYSTEM SPECIFICATION

## 1. Title & Executive Purpose

* **Document**: `InteractionSystem.md`
* **Purpose**: Details the contextual interaction framework, player detection volumes, visual interaction prompts, and backend event dispatchers for in-world assets.

---

## 2. Interaction Interface Architecture

All interactive actors implement the `ISVInteractableInterface` C++ interface:

```cpp
UINTERFACE(MinimalAPI, Blueprintable)
class USVInteractableInterface : public UInterface
{
    GENERATED_BODY()
};

class MYPROJECT_API ISVInteractableInterface
{
    GENERATED_BODY()
public:
    UFUNCTION(BlueprintNativeEvent, BlueprintCallable, Category = "Interaction")
    bool CanInteract(APawn* InteractingPawn) const;

    UFUNCTION(BlueprintNativeEvent, BlueprintCallable, Category = "Interaction")
    void OnInteract(APawn* InteractingPawn);

    UFUNCTION(BlueprintNativeEvent, BlueprintCallable, Category = "Interaction")
    FText GetInteractionPrompt() const;
};
```

---

## 3. Historical Archive Terminal (`ASVArchiveTerminal`)

* **Actor Setup**:
  - `RootComponent`: `USceneComponent`
  - `MeshComponent`: `UStaticMeshComponent` (vintage telegraph/radio terminal terminal mesh)
  - `TriggerVolume`: `USphereComponent` (Radius = $180\text{ cm}$)
  - `PointLightComponent`: Pulsing cyan/amber status indicator
* **Interaction Workflow**:
  1. Player steps within $180\text{ cm}$ sphere -> `OnComponentBeginOverlap` fires.
  2. UI displays contextual prompt: `[E] Examine Archive`.
  3. Player presses **'E'**:
     - Plays vintage mechanical audio click.
     - Terminal lights shift to solid green.
     - Displays full-screen historical archive document HUD.
     - Calls `USVMissionControlSubsystem::RecordArchiveDiscovered(ArchiveId)`.

---

## 4. Current Status

* **Status**: `COMPLETED`
* **Evidence**:
  - 5 archive terminals (`ArchiveTerminal_archive_01` through `05`) instantiated in `LV_Campus_Blockout`.
  - Trigger overlaps successfully hooked to `USVMissionControlSubsystem`.
* **Remaining Tasks**:
  - Design custom UMG Slate inspection widget with archival parchment styling.
