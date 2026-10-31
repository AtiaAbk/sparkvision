# APPROVED VISUAL BASELINES (QUALITY GATE ARCHIVE)

## 1. Purpose & Governance

This directory is an **immutable archive of formally approved visual-quality baselines**.

A screenshot in this directory represents a locked milestone quality gate that has undergone rigorous review against:
1. Authentic architectural reference photographs of the University of Dhaka.
2. Verified UTM Zone 46N metric scales and proportions.
3. Cinematic lighting and atmospheric standards inspired by *Where Winds Meet* and *Ghost of Tsushima*.

> [!CAUTION]
> **PROTECTION RULE**:
> Files in this directory **MUST NEVER BE AUTOMATICALLY OVERWRITTEN** by automated capture scripts or unreviewed developer commits. Promotion of a screenshot into `ApprovedVisualBaselines/` requires explicit human review and quality verification.

---

## 2. Approved Baselines Register

| Baseline Filename | Landmark / Feature | Milestone Gate | Approval Criteria Met |
| :--- | :--- | :---: | :--- |
| `Approved_Curzon_Hero_FrontFacade.png` | Curzon Hall South Elevation | Phase 2 Complete | Proportions verified; absence of unhistorical central dome confirmed; brick PBR calibrated. |
| `Approved_Curzon_Hero_AngledCinematic.png` | Curzon Hall 45° Perspective | Phase 2 Complete | Multi-tier veranda depth, corner towers, chhatris, and warm lighting verified. |
| `Approved_Campus_Geographic_Master.png` | Campus Wide Plan (UTM 46N) | Phase 1.1 Complete | Accurate metric distances (Curzon to TSC = 1550m; Doyel Chattar = 412m). |
| `Approved_PIE_PlayerPossession.png` | Curzon Promenade Gameplay | Phase 2.1 Complete | Player character grounded at Z=107.65; zero collision clipping; working 3rd person camera. |

---

## 3. Promotion & Review Procedure

When a new environment feature or landmark reaches completion:
1. The developer captures standard evaluation views into `CurrentGameScreenshots/`.
2. A side-by-side comparison against `ApprovedVisualBaselines/` and reference photos is conducted.
3. If the new visual quality exceeds or establishes a new benchmark, a copy is promoted into this folder with the prefix `Approved_`.
4. A changelog entry is appended to this README detailing the approved visual enhancements.

---

## 4. Current Status

* **Status**: `COMPLETED`
* **Evidence**: Phase 1, Phase 1.1, and Phase 2 baselines established and logged.
* **Remaining Tasks**:
  - Promote Phase 3 landmark renders (Doyel Chattar, Shaheed Minar, Raju Sculpture) upon final peer review.
