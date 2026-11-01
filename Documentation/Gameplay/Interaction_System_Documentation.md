# SparkVision — Interaction & NPC Dialogue Architecture

## 1. Universal C++ Interaction Interface (`USVInteractableInterface`)
The interaction architecture relies on a polymorphic Unreal Engine C++ Interface:
```cpp
UINTERFACE(MinimalAPI, Blueprintable)
class USVInteractableInterface : public UInterface { GENERATED_BODY() };

class MYPROJECT_API ISVInteractableInterface {
    GENERATED_BODY()
public:
    UFUNCTION(BlueprintNativeEvent, BlueprintCallable, Category = "SparkVision|Interaction")
    FText GetInteractionPrompt();

    UFUNCTION(BlueprintNativeEvent, BlueprintCallable, Category = "SparkVision|Interaction")
    void OnInteract(AActor* Interactor);
};
```

## 2. Detection & Sweep Mechanics
- Performed inside `ASVCharacter::ScanForInteractables()`.
- Uses a multi-sphere sweep (`UKismetSystemLibrary::SphereTraceMultiForObjects`) originating from the player location extending 320 cm forward with a 280 cm radius.
- Filters for actors implementing `USVInteractableInterface`.
- Validates facing angle and unobstructed line of sight.

## 3. Student NPC System (`ASVStudentNPC`)
- Implements `ISVInteractableInterface`.
- Endowed with skeletal mesh mannequin (`SKM_Manny_Simple` / `SKM_Quinn_Simple`) and unarmed animation blueprint.
- Hosts structured bilingual dialogue tables (Bengali dialogue text + English subtitle text).
- Maintains stateful dialogue progression across player interactions.
- Key Level 1 Characters:
  1. **Tanvir (Student Organizer)** — Stationed at Curzon Hall South Portico. Briefs player on the July 2024 academic protests.
  2. **Nusrat (Research Scholar)** — Stationed at DU Central Library / Hakim Chattar. Discusses historical documentation and the 1921 university origins.
  3. **Fahim (Cultural Activist)** — Stationed at TSC / Raju Memorial. Discusses campus solidarity and the July 14 assembly.
