# SparkVision — Archive Objective & Historical Recovery System

## 1. Archive Records Overview

Level 1 contains five core historical archive terminals (`archive_01` to `archive_05`) plus the foundational 1921 DU Boundary Stone / Shaheed Minar memorial (`archive_06`):

| Archive ID | Official Title | Authentic Campus Location | Historical Significance |
| :--- | :--- | :--- | :--- |
| **`archive_01`** | **Curzon Hall Arcade Founding Record** | Curzon Hall South Portico (`-2800, -250, 30`) | Founded in 1904; Indo-Saracenic architectural heritage, center of science education. |
| **`archive_02`** | **Aparajeyo Bangla Chronicle** | Arts Faculty Plaza (`73200, -95500, 30`) | Monument to the 1971 Liberation War; symbol of indomitable student resilience. |
| **`archive_03`** | **Raju Memorial Declaration** | TSC Mor Roundabout (`58800, -63500, 30`) | Dedicated to Moin Hossain Raju; monument against campus terrorism and violence. |
| **`archive_04`** | **Central Library Reform Gazette** | DU Central Library & Hakim Chattar (`73200, -71500, 30`) | Academic hub of reform, student debate, and literary heritage since 1921. |
| **`archive_05`** | **TSC Unity Manifesto** | Teacher-Student Centre Courtyard (`60400, -60200, 30`) | Hub of cultural solidarity, dialogue, and university communal life. |
| **`archive_06`** | **1921 Boundary Stone & Shaheed Minar** | Central Shaheed Minar (`-280, -53800, 30`) | Commemorates the 1952 Language Movement martyrs and 1921 founding perimeter. |

## 2. Terminal Mesh & Material Aesthetics
- Static Mesh: `SM_ArchiveTerminal`
- Material: `MI_Curzon_Brass` (polished heritage brass with golden specular reflections)
- Sphere collision trigger: 250 cm radius around pedestal.
- On interaction: displays parchment archive card on HUD and sends async REST payload to Java Mission Control.
