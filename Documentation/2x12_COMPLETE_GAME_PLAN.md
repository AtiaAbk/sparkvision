# 2x12 — Complete Game Plan and LLM Handoff Document

**Project:** 2x12 — Bangladesh Historical 3D Game  
**Genre:** Historical, narrative-driven 3D action-adventure / exploration  
**Engine/framework:** Java + libGDX (desktop/LWJGL3)  
**Primary development environment:** Apple Silicon MacBook Air M4, 16 GB RAM  
**Known project folder:** `/Users/atiaoishi/Downloads/2x12`  
**Known branch:** `3d` (verify current branch before work)

> **How to use this file:** Give the whole Markdown document to any LLM or coding agent before asking it to continue the game. The existing repository is the source of truth for implementation. This document captures the remembered story decisions and the overall intended direction. Where an exact old decision could not be recovered, the document labels the continuation as a **proposed plan**, rather than pretending it was previously finalized.

---

## 1. The vision

Build a complete, immersive 3D historical game focused on Bangladesh's history and student-led events. The game should combine an explorable, recognizable real-world environment with story missions, conversations, meaningful choices, cinematic moments, crowd behaviour, and—where appropriate to the historical period—high-quality action and conflict sequences.

The experience should feel like a polished third-person action-adventure, with the atmosphere and production ambition of modern 3D games such as *Where Winds Meet* used only as a broad quality reference. Do not copy its characters, assets, maps, interface, or protected content. The game's own identity, locations, history, characters, and presentation must remain original and Bangladesh-focused.

The project must not remain only a 3D environment demo. The long-term goal is a complete playable game with:

- A connected sequence of levels and a clear beginning, middle, and ending.
- Historically grounded locations and events.
- A controllable player character, smooth third-person camera, collisions, interaction, and traversal.
- NPCs, dialogue, Bengali speech/dialogue, and English subtitles.
- Mission/objective tracking, exploration, discoveries, and progression between levels.
- Crowds and event-driven world behaviour where the story requires them.
- Appropriate action/conflict mechanics where they fit the historical story; do not add combat to peaceful scenes just for spectacle.
- Cinematic scenes, environmental sound, music, lighting, animation, and polished UI.
- Educational/historical context presented without interrupting the game constantly.
- Reliable performance and a build that can be demonstrated at a university project/TechFest presentation.

## 2. Important story decisions already present in the recovered plan

These are the most specific remembered story details and should be preserved:

- **Level 1 title:** “Where It All Began.”
- **Level 1 period:** Mid-June 2024 through 14 July 2024.
- **Level 1 setting:** University of Dhaka campus, with a historically grounded, geographically convincing campus environment.
- **Level 1 tone/gameplay:** Peaceful exploration, dialogue, social participation, gathering/posters, crowd awareness and trust. **No combat, weapons, enemies, or player death in Level 1.**
- **Level 1 mission identifiers:** `L1_M01` through `L1_M06`.
- **Level 1 scene identifiers:** `SC01`–`SC10` and `SC19`–`SC20`.
- **Level 1 ending:** The protagonist decides, “আমিও থাকব।” (“I will be there too.”), followed by a transition to **15 July** and Level 2.
- **Level 1 implementation order:** scene → environment → player → camera → NPCs → dialogue/subtitles → date/objective UI → missions → gathering/posters/crowd → trust/awareness → cinematic → 14 July ending.
- **Broader story structure:** a main story arc with multiple levels. Each level should define location/map, time period, objective, missions, characters/dialogue, cutscenes/events, gameplay mechanics, challenges/enemies where historically appropriate, and ending.
- **Known Level 2 transition:** It begins on **15 July 2024**, continuing the story from Level 1.

The earlier retrieved conversation context did **not** contain the exact final names, mission lists, characters, or endings for all later levels. Later-level outlines below are therefore an organized continuation proposal designed to extend the known story without falsely claiming those details were previously finalized.

---

## 3. Main narrative structure

### Core narrative idea

The player follows a student protagonist through a rapidly changing historical period. The story begins with ordinary campus life, conversations, observation, and gradual awareness. As events intensify, the protagonist must navigate uncertainty, solidarity, fear, difficult decisions, public gatherings, danger, and the consequences of historical events.

The player should not be presented as single-handedly causing real history. The protagonist is a fictional participant moving through carefully researched public events alongside many people. Real historical figures, dates, events, locations, casualty details, and claims must be researched and treated respectfully. Clearly distinguish fictional dialogue and composite characters from documented historical facts.

### Story design rules

1. Every level advances the central narrative; avoid levels that exist only to show off scenery.
2. Every major event needs a date/time, location, objective, cast, mission flow, gameplay mechanics, and ending/transition.
3. Use the player's exploration and conversations to communicate context, not long unskippable lectures.
4. Keep a record of factual references for each historical scene.
5. Never invent a quote and attribute it to a real person.
6. Sensitive scenes should be handled with dignity. Do not gamify real suffering or reward violence.
7. Let the gameplay change with the period: peaceful exploration early, crowded navigation and evasion under pressure, then survival/rescue/documentation and reflection as appropriate.
8. Provide English subtitles for Bengali dialogue and design the dialogue system so the language can be expanded later.

---

## 4. Full level roadmap

This roadmap gives the project a complete beginning-to-ending structure. **Level 1 and the 15 July Level 2 transition are remembered decisions. The detailed content for Levels 2 onward is a proposed continuation and must be validated against historical research and the user's preferred original story before it is treated as final.** The level count can be adjusted after the full narrative is locked.

### Level 1 — “Where It All Began”

**Period:** Mid-June 2024 – 14 July 2024  
**Primary setting:** University of Dhaka campus  
**Tone:** Observational, peaceful, gradually intensifying  
**Combat:** None. No weapons, enemies, or death mechanics.

**Purpose:** Introduce the protagonist, campus, key locations, social relationships, the developing student movement, and the emotional decision to participate.

**World/environment requirements:**
- A recognizable Dhaka University campus with Curzon Hall as a key landmark.
- Connected roads, walkways, courtyards, open areas, campus gates/walls, lawns, trees, and campus props.
- Additional DU locations according to the selected playable map: Applied Physics, Geology, Fisheries, Applied Chemistry, Zoology, pond, Botany, Chemistry, Biochemistry/Molecular Biology, TSC, Shahid Minar, and other relevant locations if the map scope supports them.
- Research-driven geography and architectural proportions. If the playable map compresses the real campus, preserve the meaningful relative layout and document the compression.
- Students, staff, security personnel, small groups, posters, conversations, and gathering activity that evolve as the level progresses.

**Mission chain:** `L1_M01`–`L1_M06`. The exact historic mission labels should be recovered from prior design notes if available; until then, use this functional sequence as a safe working interpretation:
1. Arrive and learn the basic movement/camera controls.
2. Explore the campus and identify important landmarks.
3. Speak with key student NPCs and learn what is happening.
4. Observe notices/posters and gather context through optional conversations.
5. Participate in a peaceful gathering and build awareness/trust through dialogue and choices.
6. Reach the 14 July story endpoint and decide to participate: **“আমিও থাকব।”**

**Scene sequence:** Preserve `SC01`–`SC10` and `SC19`–`SC20` identifiers if they exist in the source/story files. Do not reassign identifiers without checking existing usage.

**UI/gameplay:** date and objective UI, interaction prompt, dialogue panel, Bengali dialogue with English subtitles, basic mission tracker, optional awareness/trust state, gathering/poster interactions, and an appropriate ending cinematic.

**Exit condition:** Complete the final 14 July sequence; show the transition to **15 JULY** and load Level 2.

### Level 2 — “The Day the Streets Changed” *(proposed continuation; starts 15 July 2024)*

**Period:** Starts 15 July 2024. The exact end date should be set only after the historical chapter is researched and the story's pacing is approved.  
**Setting:** Dhaka University and connected nearby public spaces/roads, based on researched events.  
**Tone:** Tension, uncertainty, solidarity, crowded movement, consequential choices.

**Purpose:** Continue immediately from Level 1's ending. Show how the protagonist's decision to participate changes everyday campus life. Introduce larger gatherings, changing crowd density, conflicting information, and the risks of moving through a volatile public situation.

**Mission design:**
- Rejoin friends and establish the day's objective.
- Navigate to a verified gathering point using the map and directions.
- Speak with NPCs with differing information; distinguish confirmed facts from rumours.
- Help the group coordinate peacefully and safely.
- Navigate a changing crowd while avoiding blocked routes and dangerous areas.
- Reach the chapter's key event and transition through a cinematic based on researched historical chronology.

**Gameplay systems introduced:** larger crowds, crowd flow and avoidance, dynamic route access, mission updates triggered by world events, more advanced NPC schedules, contextual dialogue, and a stronger minimap/objective system.

**Historical safeguards:** Do not invent a specific confrontation, slogan, order, injury, or action and present it as fact. Verify the timeline and setting before staging the sequence. If a scene is fictionalized, mark it internally as a dramatization and avoid attributing invented statements to real people.

**Ending:** A major event changes the protagonist's understanding of the situation and sets up Level 3. The exact event, date, and ending dialogue must be chosen from verified history.

### Level 3 — “A City on Edge” *(proposed continuation)*

**Period:** The next verified chapter of the July 2024 events, with exact dates to be established through research.  
**Setting:** Selected Dhaka streets, campus routes, and public spaces relevant to the documented events.  
**Tone:** Urgency, confusion, risk, responsibility.

**Purpose:** Expand the game beyond the initial campus area and make the player navigate a city under pressure. Emphasize the human experience and consequences rather than turning real events into a score-based combat spectacle.

**Mission possibilities:**
- Reach a destination while routes change and crowds move.
- Find a separated friend or help an NPC reach safety.
- Deliver verified information between groups or identify conflicting reports.
- Choose between a safer route and a shorter, riskier route.
- Assist with first aid or evacuation if supported by the story and historically appropriate.
- Record/document events through an in-game journal or evidence system without fabricating real-world evidence.

**Gameplay systems:** expanded traversal, route choices, crowd-state changes, safe-zone navigation, contextual interactions, more complex mission dependencies, and stronger audio/visual cues for nearby events.

**Combat rule:** Any physical confrontation must be justified by the researched story and designed with care. Avoid arcade-style kill counts, loot rewards for violence, or fictional heroics that distort the documented events.

**Ending:** A consequential sequence that leads into the next historically verified chapter. Exact events and dialogue remain subject to research.

### Level 4 — “Voices Across the City” *(proposed continuation)*

**Period:** A subsequent chapter chosen from the verified historical timeline.  
**Setting:** Multiple connected urban/campus locations, with any new area based on a researched map.  
**Tone:** Community, communication, fear, solidarity, and difficult choices.

**Purpose:** Show that the story is larger than one protagonist. The player helps people communicate, finds safe routes, supports community needs, and understands how information and collective decisions affect the story.

**Mission possibilities:**
- Visit several NPCs to understand different perspectives.
- Complete a time-sensitive communication or supply task.
- Help a vulnerable character reach a safe location.
- Gather journal entries or verified context that unlocks an optional historical archive.
- Make a choice that changes trust, access to information, or who can assist in a later mission—not the real historical outcome itself.

**Systems:** branching conversations, companion/friend state, optional side objectives, a journal/archive, and a mission state machine that supports multiple objectives without hard-coded logic in the world class.

**Ending:** A story beat that raises the stakes and transitions to the next researched event.

### Level 5 — “The Cost of Courage” *(proposed continuation)*

**Period and setting:** Determined by the verified historical sequence; avoid assigning exact dates before research.  
**Tone:** Serious, emotionally grounded, focused on consequences and human safety.

**Purpose:** Represent the human cost of the events respectfully. The player may need to make fast decisions, protect a companion, assist injured people, find shelter, or navigate a dangerous area. The design should centre survival, care, and consequences—not violence as entertainment.

**Mission possibilities:**
- Respond to an urgent request for help.
- Locate and assist a missing/separated character.
- Navigate to a safe place while avoiding hazardous routes.
- Help NPCs with evacuation or first aid if appropriate and researched.
- Decide what information to share when the facts are uncertain.

**Systems:** companion follow/assist behaviour, simple rescue interactions, safe-zone logic, mission urgency without unfair timers, and cinematic/audio restraint for sensitive scenes.

**Historical safeguards:** Any depicted injury, death, named person, casualty figure, or alleged act must be verified and treated sensitively. Avoid graphic spectacle. Do not fabricate real victim identities or attribute fictional suffering to actual people.

**Ending:** A reflective but forward-moving transition to the next chapter.

### Level 6 — “A Turning Point” *(proposed continuation)*

**Period:** A major turning point selected after research establishes the game's complete historical scope.  
**Setting:** The locations required by the documented event; do not invent geography for dramatic convenience.  
**Tone:** High stakes, uncertainty, collective action, reflection.

**Purpose:** Deliver the narrative's major climax through a sequence of connected missions and cinematics. The protagonist remains one participant among many; the game should not falsely imply that a single fictional character determines national events.

**Mission structure:**
- Complete several linked objectives in an open, navigable area.
- Use earlier relationships and trust to access help or information.
- Make choices about safety, communication, assistance, and priorities.
- Experience the key event through a carefully researched cinematic and playable aftermath.
- Preserve the player's agency without offering choices that rewrite documented history in misleading ways.

**Systems:** multi-stage mission orchestration, reliable save/checkpoint support, contextual crowd reactions, more sophisticated cinematic transitions, and performance testing under high NPC density.

**Ending:** Resolve the central immediate conflict of the chosen historical chapter and prepare for the aftermath.

### Level 7 — “After the Storm” *(proposed continuation)*

**Period:** The aftermath of the game's selected historical arc, based on verified dates and events.  
**Setting:** Returning to key locations, community spaces, and memorial/reflective areas relevant to the story.  
**Tone:** Reflection, memory, accountability, recovery, learning.

**Purpose:** Show consequences, relationships, what has changed, and how the protagonist understands the experience. Return to locations from earlier levels so the player can see the difference in atmosphere and meaning.

**Mission possibilities:**
- Reconnect with key characters and learn their outcomes.
- Return to important locations and view journal entries or historical context.
- Help with a community recovery task if historically appropriate.
- Review the player's collected historical archive and optional discoveries.
- Complete a final personal objective tied to the protagonist's growth.

**Systems:** world-state changes across chapters, a story journal, optional historical notes, completed-mission review, and a closing cinematic.

**Ending:** A grounded conclusion that honours the people and events represented. Provide a credits/reference section listing reliable sources and explaining which characters or dialogue were fictionalized.

### Optional epilogue / educational archive

After the main ending, offer an optional archive containing sourced timelines, location notes, selected public-domain or properly licensed photographs/documents, a glossary, and a clear distinction between verified history and fictional storytelling. The archive should be informative but should not be required to finish the main story.

---

## 5. Level design template — required for every level

Before coding a new level, complete this design sheet:

1. **Level number and title**
2. **Dates/time period** (verified)
3. **Real-world location(s)** and map references
4. **Narrative purpose** and what changes by the end
5. **Opening scene** and how the player enters the level
6. **Main objective** and 3–6 mission beats
7. **Mission IDs** using a consistent naming scheme (`L2_M01`, etc.)
8. **Scene/cutscene IDs** without colliding with existing identifiers
9. **Characters/NPCs** and whether each is real, fictional, or a composite
10. **Dialogue** in Bengali with English subtitle text and source/fictionalization notes
11. **World layout** with playable boundaries, routes, landmarks and safe/blocked areas
12. **Gameplay systems** introduced or reused
13. **Challenges** appropriate to the period; do not add enemies or combat by default
14. **Optional discoveries/side objectives**
15. **UI/audio/animation needs**
16. **Ending and transition** to the next level
17. **Historical source register** supporting dates, events, places and factual dialogue
18. **Acceptance tests** for gameplay, build, navigation, performance and story continuity

---

## 6. Shared gameplay systems

### Player and camera
- Third-person player movement with consistent acceleration/speed and responsive input.
- Smooth follow camera, sensible framing, collision/obstruction handling, and stable behaviour near walls and crowds.
- Collision against buildings, walls, fences, props and terrain boundaries.
- Context-aware interaction key (for example `E`) for NPCs, posters, doors, objects and mission triggers.
- Animations for idle, walk, run, turn, interaction, and any later actions actually supported by the character model.

### Dialogue and NPCs
- Dialogue data should be separate from the world-rendering code.
- Bengali dialogue with English subtitles; support timing, speaker names, optional choices and localization.
- NPC states should support idle, conversation, walking, gathering, reacting to world events, and following/helping where appropriate.
- Avoid spawning unlimited NPCs. Use bounded crowd sizes, distance-based updates, animation/mesh reuse and other practical optimizations.
- Keep fictional/composite character notes separate from real historical people.

### Missions and progression
- Use a `Mission`/`MissionManager` or equivalent architecture if compatible with the current repository.
- Support prerequisites, objective completion, triggers, optional tasks, checkpoints and level transitions.
- Keep mission logic out of giant `LevelXWorld` methods where practical.
- Save completed objectives and story state if save functionality is included.
- Make objective markers reflect actual world coordinates and state.

### Map and HUD
- Date/period indicator appropriate to the chapter.
- Active objective and progress display.
- Direction indicator and mini-map/full-map based on real level data.
- Landmarks, discovered locations and useful destination labels.
- Dialogue/subtitle UI with readable text and safe screen margins.
- Awareness/trust only if it has meaningful, explainable effects; do not add a meaningless score bar.
- Keep menus, HUD, subtitles and mission notifications visually consistent.

### Sound and cinematics
- Ambient campus/city audio appropriate to each place and period.
- Footsteps and interaction sounds; positional audio where practical.
- Music used selectively to support the scene, not constantly overpower dialogue.
- Cinematic camera transitions and fades that do not leave the game stuck or break input.
- Provide skip/continue behaviour for non-essential cinematics where appropriate.

### Historical journal / education layer
- Optional entries tied to landmarks, events, or collected objects.
- Each factual entry must have reliable source information.
- Label dramatized scenes and composite characters appropriately.
- Do not present AI-generated text or unverified online claims as authoritative history.

---

## 7. Level 1 environment: specific architecture and geography plan

Level 1 is the immediate implementation priority and should be built as a coherent place, not as isolated cubes.

### Curzon Hall
- Treat Curzon Hall as the hero landmark.
- Research the building's overall silhouette, façade rhythm, red-brick appearance, arches, columns, windows, entrances, roofline and distinctive architectural features.
- Use verified dimensions where available; otherwise estimate from multiple views and label estimates internally.
- Build the main massing first, then distinctive architecture, then materials and fine detail.
- Compare front, side and oblique screenshots with references.
- Check scale by placing the player beside entrances, stairs and windows.

### Surrounding DU-inspired map
The previously discussed Level 1 reference list included Applied Physics, Geology, Fisheries, Applied Chemistry, Zoology, the pond, Botany, Chemistry, Biochemistry/Molecular Biology, TSC, Shahid Minar, connecting roads, campus gates/walls, paths and crowd zones. Include only those that fit the researched playable map and ensure their relative placement is plausible.

### Environment implementation order
1. Reference collection and source register.
2. Master map and scale convention.
3. Ground/terrain and playable boundaries.
4. Roads and paths.
5. Main buildings and landmarks.
6. Courtyards/open areas and lawns.
7. Trees and vegetation.
8. Walls, gates, railings and campus props.
9. NPCs and crowd zones.
10. Lighting, sky, weather/atmosphere.
11. Ambient/positional sound.
12. Animation and interactions.
13. LOD/visibility/performance optimization.
14. Multi-angle visual review and final Level 1 test.

---

## 8. Technical architecture and project safety

### Known stack and architecture
- Java + libGDX + Gradle; desktop/LWJGL3 target.
- Previously discussed architecture: `Main` → `GameManager`/`GameState` → `World`/`WorldManager` → `Level1World` and player/input/camera.
- Previously discussed next gameplay classes include `Mission.java` and `MissionManager.java`, subject to what actually exists in the current repository.
- `Level1World.java` has been a major, large file in prior implementation work. Avoid growing it without limit; modularize carefully when a clear need arises.

### Inspect before modifying
1. Check `git status`, current branch and recent commits.
2. Inspect the real source tree and build files.
3. Find the launcher, game-state handling, world interface, player, camera, input, collision, asset and UI code.
4. Read the current implementation before replacing a file.
5. Run the baseline build and record the result.
6. Identify the smallest change that advances the current milestone.

Do not switch to Unity, Unreal, Godot, or another framework unless the user explicitly authorizes a change after a technical discussion. Do not replace working architecture with generic code. Never assume a class, constant, method, asset path or field exists without checking.

### Build and verification
Use the repository's wrapper, normally:

```bash
./gradlew :core:build
```

A successful build is necessary but not sufficient. Launch the game where feasible, test the changed behaviour, and inspect a screenshot or in-game viewpoint for visual work. Report exactly what was verified and what was not.

### Git workflow
- One coherent implementation change per step.
- Prefer one Git commit per meaningful step, as requested by the user.
- Never claim a commit exists unless it was actually made.
- Before changes, check for uncommitted work and protect it.
- After changes, report files changed, build/test result, known issues, and a suggested commit message.

### Code delivery preference
- Give complete, copy-paste-ready terminal commands when practical.
- When replacing a file, give the full replacement file, not a fragment that leaves the user guessing.
- Keep edits scoped; do not rewrite unrelated systems.
- Explain destructive commands and avoid deleting assets, backups or user work.
- Keep Java/libGDX compatibility and dispose resources correctly.
- Avoid per-frame allocations, unbounded NPC creation and unnecessary dependencies.
- Target reliable performance on the M4 MacBook Air with 16 GB RAM.

---

## 9. Overall implementation roadmap

### Phase A — Audit and baseline
- Confirm the project builds and launches.
- Map current classes and identify implemented vs planned features.
- Check Git state and preserve existing work.

### Phase B — Story bible and historical research
- Lock the overall historical scope and level count with the user.
- Build a timeline with dates, places, source links and confidence levels.
- Finalize each level's mission flow and scene IDs.
- Mark real characters, fictional characters and composite characters clearly.
- Decide which moments are playable, cinematic or optional journal content.

### Phase C — Finish Level 1
- Complete DU-inspired environment layout and Curzon Hall.
- Finish player movement, camera, collision and interactions.
- Implement `L1_M01`–`L1_M06`, `SC01`–`SC10`, `SC19`–`SC20` without identifier collisions.
- Add NPCs, dialogue/subtitles, date/objective UI, gathering/posters and awareness/trust only where meaningful.
- Finish the 14 July cinematic and “আমিও থাকব।” ending.
- Verify the 15 July transition into Level 2.

### Phase D — Build reusable systems
- Mission manager and level transition flow.
- Dialogue/subtitle data system.
- NPC and crowd state system.
- Objective marker/map system.
- Checkpoints/save state if required.
- Shared UI, audio and cinematic helpers.

### Phase E — Implement later levels sequentially
For each level, do not begin full coding until the story sheet and historical sources are ready. Implement one vertical slice at a time:
1. Level design and reference research.
2. Greybox map and route testing.
3. Mission logic and transition.
4. NPCs/dialogue and events.
5. Required mechanics.
6. Art, lighting, sound and cinematics.
7. Build, playtest, bug fix, performance check.
8. Commit and document completion.

### Phase F — Full-game integration
- Ensure level transitions preserve story/player state.
- Test the entire game from start to finish, not only individual levels.
- Check input/camera/UI consistency across levels.
- Check that optional objectives and dialogue cannot soft-lock progression.
- Add credits, sources, controls and accessibility settings as feasible.

### Phase G — Polish and presentation
- Optimize rendering, geometry, assets and NPC updates.
- Remove obvious clipping, floating objects, repeated-pattern artefacts and abrupt world boundaries.
- Test all levels at normal gameplay camera angles and on the target Mac.
- Capture clean screenshots and a short demo video.
- Prepare an honest progress report that separates implemented features from planned features.

---

## 10. Acceptance criteria for the complete game

The game should not be described as complete until all applicable items are verified:

- [ ] A player can start a new game and reach the first playable level.
- [ ] Level 1's peaceful tone and no-combat rule are preserved.
- [ ] The protagonist's 14 July decision and 15 July transition work.
- [ ] All planned levels are accessible in sequence and have distinct narrative purposes.
- [ ] Each level has a start, objectives, playable mission flow, ending and transition.
- [ ] Player movement, camera and collisions remain reliable throughout the game.
- [ ] NPC interaction and dialogue/subtitles work in actual play.
- [ ] Map/objective UI points to real destinations and updates correctly.
- [ ] Historical places and key events are researched and source-tracked.
- [ ] Fictional dialogue and composite characters are not misrepresented as factual records.
- [ ] Sensitive historical content is presented respectfully.
- [ ] No known build-breaking errors remain.
- [ ] The game can be completed from beginning to ending without a blocker.
- [ ] Performance is acceptable on the target machine.
- [ ] Credits and historical references are included.
- [ ] Screenshots/video and a clear feature-status report are ready for presentation.

---

## 11. Instructions to any LLM or coding agent

You are continuing an existing Java/libGDX project, not starting a new game. Read this document first, then inspect the actual repository before proposing or editing code.

**Your first response should provide:**
1. A concise summary of the existing architecture and entry points.
2. A status table separating implemented, partially implemented, broken, and planned features.
3. The current branch and uncommitted changes.
4. The result of `./gradlew :core:build`.
5. The exact current status of Level 1, including Curzon Hall, player/camera/collision, missions, NPCs, dialogue, UI and transitions.
6. Any source/story documents in the repository that may contain the original full Level 2+ plan.
7. One safe, high-value next step.

Then work incrementally. Do not invent codebase details, do not silently replace the architecture, and do not claim historical accuracy without sources. If a later-level detail was not finalized, label it as a proposal and ask only the focused question necessary to lock the story. Preserve the user's one-step-at-a-time, complete-file, copy-paste-ready workflow.

**Immediate priority:** Audit and continue the existing Level 1 work first, while recovering/locking the full story bible for Levels 2 onward. Keep Level 1's remembered details and the 15 July 2024 Level 2 transition intact.
