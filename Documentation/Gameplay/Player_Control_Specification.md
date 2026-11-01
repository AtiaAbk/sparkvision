# SparkVision — Player Control Specification
**Target Platform:** macOS / Apple Silicon (MacBook Air M4)  
**Input Architecture:** Enhanced Input + Direct Key/Axis Fallback  
**Character Class:** `ASVCharacter : public ACharacter`  

---

## 1. Input Layout & Keybindings

### 1.1 Desktop Keyboard & Mouse (Default)

| Action | Primary Input | Secondary / Fallback | Functionality |
| :--- | :--- | :--- | :--- |
| **Move Forward** | `W` | Up Arrow | Accelerate forward relative to camera yaw (550 cm/s walk/jog) |
| **Move Backward** | `S` | Down Arrow | Move backward relative to camera yaw |
| **Move Left** | `A` | Left Arrow | Strafe left relative to camera yaw |
| **Move Right** | `D` | Right Arrow | Strafe right relative to camera yaw |
| **Look Orbit** | `Mouse X / Y` | Trackpad drag | 360° pitch and yaw orbit around player pawn |
| **Sprint** | `Left Shift` (Hold) | Right Shift | High-speed athletic sprint (950 cm/s), consumes Qi/stamina |
| **Jump** | `Space` | - | Vertical leap with 650 cm/s jump impulse, authentic landing |
| **Interact / Talk** | `E` | Enter | Inspect archive terminals, talk to NPCs, dismiss modals |
| **Pause / Menu** | `Esc` | `P` | Open interactive Pause Menu with Save, Load, Settings |
| **Fast Travel** | `1` – `6` | NumPad 1–6 | Instantly travel between the 6 Dhaka University landmarks |

---

## 2. Locomotion Kinematics & Tuning

- **Ground Speed (Walk/Jog):** 550.0 cm/s
- **Ground Speed (Sprint):** 950.0 cm/s
- **Braking Deceleration:** 2048.0 cm/s² (responsive stops without ice-skate sliding)
- **Ground Friction:** 8.0
- **Jump Z Velocity:** 650.0 cm/s
- **Gravity Scale:** 1.5 (natural, weighty athletic descent)
- **Air Control:** 0.35 (tight lateral adjustments during jumps)
- **Orient Rotation to Movement:** Enabled (`bOrientRotationToMovement = true`, rotation rate: `FRotator(0.0f, 540.0f, 0.0f)`)
- **Controller Rotation Pitch/Roll/Yaw:** Disabled on pawn; camera boom uses pawn control rotation (`bUsePawnControlRotation = true`).

---

## 3. Camera Framing & Dynamic Spring Arm

- **Target Arm Length (Walk):** 380.0 cm
- **Target Arm Length (Sprint):** 460.0 cm (expands view during rapid traversal)
- **Target Socket Offset:** Walk: `(0, 45, 25)` cm, Sprint: `(0, 55, 30)` cm (over-the-shoulder perspective)
- **Field of View (FOV):** Walk: 75°, Sprint: 84°
- **Camera Collision:** Probe channel `ECC_Camera`, probe size 12.0 cm, smooth spherical lag interpolation (speed 4.0).
- **Pitch Limits:** Clamped to `[-60°, +45°]` to prevent clipping through terrain or inverting overhead.
