# UNIVERSITY OF DHAKA — BIRD & WILDLIFE ECOLOGICAL RESEARCH
## Avian Diversity, Campus Fauna, Behavioral Ecology & Audio Systems

---

### 1. Empirical Avian Survey Baseline

Research on the avifauna of the University of Dhaka campus (*Dhaka University Journal of Biological Sciences*, Vol. 28, Issue 2) documents **42 resident and seasonal bird species** belonging to 24 families inhabiting the campus's urban forest canopy, gardens, and wetlands.

The presence of ancient mature trees (Banyan, Rain Tree, Mahogany), historic building eaves (Curzon Hall, SM Hall), and water bodies (Curzon Pond, Shahidullah Hall Lake) creates vital micro-sanctuaries within high-density Dhaka.

---

### 2. Priority Documented Avian Species

| Scientific Name | English Name | Local Bengali Name | Family | Conservation Status | Preferred Campus Habitat | Characteristic Call / Audio Cue |
| :--- | :--- | :--- | :--- | :---: | :--- | :--- |
| *Copsychus saularis* | Oriental Magpie-Robin | দোয়েল (Doyel) | Muscicapidae | Resident (National Bird) | Open lawns, low hedges, Doyel Chattar, Curzon parterres | Melodious, fluting territorial whistling songs; sharp "churr" alarm |
| *Eudynamys scolopaceus* | Asian Koel | কোকিল (Kokil) | Cuculidae | Resident (Monsoon Vocalist) | Dense canopy of Banyan, Mango, and Rain trees | Resonant, ascending "Koo-Ooo! Koo-Ooo!" echoing across campus |
| *Dicrurus macrocercus* | Black Drongo | ফিঙে (Finge) | Dicruridae | Resident | High exposed twigs, lamp posts, overhead wires | Harsh, metallic chattering; mimics raptor calls |
| *Halcyon smyrnensis* | White-throated Kingfisher | ধলাগলা মাছরাঙা (Machhranga) | Alcedinidae | Resident | Curzon Botanical Pond, Shahidullah Lake margins | Piercing, ringing rattle call; flashes of brilliant electric blue |
| *Acridotheres tristis* | Common Myna | ভাত শালিক (Bhat Shalik) | Sturnidae | Resident | Open lawns, pedestrian footpaths, promenade verges | Raucous, varied gurgling, squeaks, and chirps |
| *Pycnonotus cafer* | Red-vented Bulbul | লালপাছা বুলবুলি (Bulbuli) | Pycnonotidae | Resident | Shrubbery, flowering Krishnachura, Banyan figs | Cheerful, chattering three-note phrase: "be-care-ful" |
| *Spilopelia chinensis* | Spotted Dove | তিলা ঘুঘু (Tila Ghughu) | Columbidae | Resident | Shaded garden soil, quiet courtyard walkways | Soft, rhythmic "kroo-kruk-kruk... kroo" cooing |
| *Passer domesticus* | House Sparrow | পাতি চড়ুই (Choroi) | Passeridae | Resident | Veranda cornices, roof eaves, colonial ventilators | Continuous lively chirping and hopping |
| *Psittacula krameri* | Rose-ringed Parakeet | টিয়া (Tiya) | Psittaculidae | Resident | Upper canopy of tall palms, old tree cavities | High-pitched shrieking "kee-ak, kee-ak" in flight |

---

### 3. Mammalian & Herpetological Wildlife

* **Northern Palm Squirrel (*Funambulus pennantii*) / কাঠবিড়ালি**:
  * Abundant across Curzon Hall, The Mall, and Fuller Road.
  * Forages on tree trunks, plinths, and lawns; darts between branches when approached by player character.
* **Asian Common Toad (*Duttaphrynus melanostictus*) / কুনো ব্যাঙ**:
  * Nocturnal and twilight presence around moist soil, lawn edges, and Curzon Pond ghat steps.
* **Garden Lizard (*Calotes versicolor*) / রক্তচোষা গিরগিটি**:
  * Sunning on tree trunks and brick walls during morning cloud breaks.

---

### 4. Implementation in SparkVision (Audio & Visual Life)

To maintain 60 FPS performance on Apple Silicon M4 without wasting compute on complex pathfinding:
1. **Perched Ambient Birds**: Low-poly animated bird meshes with idle grooming and head-bobbing animations placed on select branch sockets and telephone wires.
2. **Dynamic Flocking Triggers**: Lightweight particle splines simulating small flocks (3–6 birds) taking flight from lawn trees when player sprints within 8 meters.
3. **Soundscape Spatialization**:
   * Distance-attenuated audio emitters in Curzon canopy for the Asian Koel ("Koo-Ooo").
   * Surface-level directional audio around lawns for the Doyel and Myna.
   * Water-edge ambient Kingfisher calls near Curzon Botanical Pond.
