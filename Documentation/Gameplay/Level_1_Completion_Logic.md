# SparkVision — Level 1 Completion & Level 2 Unlock Logic

## 1. Completion Prerequisites
Level 1 ("Where It All Began") cannot be completed by simply reaching a coordinate. All of the following criteria must be satisfied:
1. All 5 heritage archives secured (`archive_01` through `archive_05`).
2. Student leaders consulted (Tanvir, Nusrat, Fahim).
3. Player present at the Raju Memorial Assembly Plaza at TSC.
4. Player triggers the final July 14 pledge interaction: *"আমিও থাকব।"* ("I will be there too.").

## 2. Victory Sequence Flow
1. Cinematic letterbox bars expand to 15% screen height.
2. Character locomotion locks during cinematic resolution.
3. Ink-wash victory modal renders on screen:
   - Primary Header: **“আমিও থাকব।”** ("I will be there too.")
   - Subtitle: *“Dhaka University — July 14, 2024”*
   - Description: *“The five historical archives of Dhaka University have been preserved. You have committed to stand with fellow students as the movement transitions into a nationwide struggle for truth and justice.”*
   - Unlock Banner: *“CHAPTER 2 UNLOCKED: The Day the Streets Changed (July 15, 2024)”*
4. Event `LEVEL1_COMPLETED` is transmitted to Java Mission Control (`POST /api/v1/events`).
5. Progress is saved to `SVSave_Slot0.sav`.
6. Main Menu updates: **Continue Game** now loads the Chapter 2 transition.
