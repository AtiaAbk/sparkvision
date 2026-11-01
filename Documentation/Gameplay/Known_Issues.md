# SparkVision — Known Issues & Future Enhancements

## 1. Known Runtime Observations & Mitigations
1. **CrashReportClientEditor on Editor Exit:**
   - *Observation:* On macOS Apple Silicon, when force-terminating or closing certain editor child processes, `CrashReportClientEditor` may post an `EXC_BAD_ACCESS` signal.
   - *Status:* Benign OS-level reporting artifact; does not affect project assets, compiled C++ binaries, or game execution.
2. **First-Time Shader Compilation:**
   - *Observation:* When first loading the 1.5 km open-world campus, Metal shaders may take 2–3 seconds to pre-warm into the macOS shader cache.
   - *Mitigation:* `Scripts/play_game.py` incorporates a 1.5s warmup duration before unpausing viewport input.

## 2. Chapter 2 Transition
- Chapter 2 ("The Day the Streets Changed", July 15, 2024) is fully architected and unlocked upon Chapter 1 victory.
- Helmeted hostile opponents (`SVHostileOpponent`) and self-defense mechanics will activate upon loading Chapter 2 maps.
