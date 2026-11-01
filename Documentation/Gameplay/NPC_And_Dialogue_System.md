# SparkVision — NPC & Dialogue System Specification

## 1. Character Roster (Level 1)

### 1.1 Tanvir (Student Organizer)
- **Location:** Curzon Hall South Portico entrance steps (`X = -2900, Y = -350, Z = 30`).
- **Role:** Guides incoming students, explains the quota reform movement's peaceful roots, points towards the 5 heritage archives.
- **Dialogue Lines:**
  - *Bengali:* "কার্জন হলের প্রাঙ্গণে স্বাগতম। ২০২৪ সালের জুলাইয়ের এই দিনগুলোতে আমাদের শান্তিপূর্ণ আন্দোলন শুরু হয়েছে।"
  - *English:* "Welcome to the Curzon Hall quadrangle. In these early days of July 2024, our peaceful assembly for fairness has begun."
  - *Bengali:* "ইতিহাসের দলিলগুলো সংরক্ষণ করো—আমাদের পাঁচটি ঐতিহাসিক টার্মিনাল ঘুরে দেখো।"
  - *English:* "Document the history of our campus—examine the five historical archive records across Dhaka University."

### 1.2 Nusrat (Research Scholar)
- **Location:** DU Central Library Ramp & Hakim Chattar (`X = 73100, Y = -71800, Z = 30`).
- **Role:** University researcher, provides historical background on 1952 Language Movement and 1921 founding.
- **Dialogue Lines:**
  - *Bengali:* "হাকিম চত্বর আর সেন্ট্রাল লাইব্রেরি সবসময়ই মুক্তচিন্তার কেন্দ্র। ১৯৫২ থেকে ১৯৭১—এই মাটি অন্যায়ের বিরুদ্ধে কথা বলেছে।"
  - *English:* "Hakim Chattar and the Central Library have always been the cradle of free inquiry. From 1952 to 1971, this soil stood against injustice."

### 1.3 Fahim (Cultural Activist)
- **Location:** TSC Raju Anti-Terrorism Memorial Plaza (`X = 58900, Y = -63600, Z = 30`).
- **Role:** Cultural organizer at TSC, leads the July 14 solidarity pledge.
- **Dialogue Lines:**
  - *Bengali:* "টিএসসির রাজু ভাস্কর্য সন্ত্রাসবিরোধী ঐক্যের প্রতীক। ১৪ জুলাই রাত নেমে আসছে—আমরা কালকের জন্য প্রস্তুত।"
  - *English:* "The Raju Memorial at TSC stands for resistance against oppression. As the night of July 14 falls, we stand ready for tomorrow."
  - *Bengali:* "তুমি কি কালকের সমাবেশে আমাদের সাথে থাকবে?"
  - *English:* "Will you stand with us tomorrow?"

## 2. Audio & Visual Presentation
- Dialogue UI renders in a dark ink-wash slate modal at bottom center of screen.
- Displays speaker name, role, Bengali primary text, and English translation subtitle.
- Interactive response prompt: `[E] Continue Dialogue` / `[Space] Close`.
