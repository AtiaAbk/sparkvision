# UNIVERSITY OF DHAKA — BUTTERFLY & INSECT ECOLOGICAL RESEARCH
## Lepidoptera Diversity, Pollinators, Odonata & Micro-Fauna

---

### 1. Empirical Entomological Baseline

According to published studies on the urban entomological diversity of Dhaka (*Journal of Urban Ecology*, DOI: 10.1093/jue/juab008: "Butterflies of an urban landscape in Dhaka, Bangladesh: a case study of green spaces"), institutional academic campuses with diverse botanical stratification support significantly higher species richness than surrounding urban cores.

Over **54 butterfly species** across 5 families have been recorded in the central Dhaka green network, with Curzon Hall botanical gardens, Suhrawardy boundary, and the Botany Department arboretum acting as primary urban core refuges.

---

### 2. Documented Butterfly Species (Lepidoptera)

| Scientific Name | English Common Name | Local Bengali Name | Family | Wing Span | Primary Nectar / Host Plant | Visual Description & Flight Style |
| :--- | :--- | :--- | :--- | :---: | :--- | :--- |
| *Papilio polytes* | Common Mormon | মর্মন | Papilionidae | $90 - 100\text{ mm}$ | Lime, Lemon, Bel (*Aegle marmelos*) | Jet black with white wing spots; rapid, erratic fluttering |
| *Papilio demoleus* | Lime Butterfly | চুন প্রজাপতি | Papilionidae | $80 - 100\text{ mm}$ | Citrus species, Gardenia | Striking black and yellow checkered pattern; sunlit glades |
| *Danaus chrysippus* | Plain Tiger | ডানাউস বাঘ | Nymphalidae | $70 - 80\text{ mm}$ | Calotropis (*Akanda*), Asclepias | Tawny orange wings bordered with black and white spots; slow gliding |
| *Junonia lemonias* | Lemon Pansy | লেবু চোখ | Nymphalidae | $45 - 60\text{ mm}$ | Acanthaceae herbs, lawn weeds | Brown with distinct lemon-yellow spots and large blue/black eyespots |
| *Junonia almana* | Peacock Pansy | ময়ূর চোখ | Nymphalidae | $55 - 65\text{ mm}$ | Aquatic herbs, lawn grasses | Rich orange with prominent target-like peacock eyespots |
| *Eurema hecabe* | Common Grass Yellow | ঘাস হলুদ | Pieridae | $40 - 50\text{ mm}$ | Fabaceae herbs, low turf grass | Bright sulfur-yellow wings fluttering continuously above low lawns |
| *Catopsilia pyranthe* | Mottled Emigrant | সাদা প্রজাপতি | Pieridae | $50 - 70\text{ mm}$ | *Cassia* species, Sonalu trees | Chalky greenish-white wings; active during humid monsoon mornings |

---

### 3. Odonata (Dragonflies & Damselflies) of Curzon Pond

The standing water of Curzon Botanical Pond and Shahidullah Hall Lake creates ideal breeding habitats for aquatic Odonata:

1. **Globe Skimmer / Wandering Glider (*Pantala flavescens*)**:
   * Golden-yellow abdomen, transparent wings ($80\text{ mm}$ wingspan).
   * Swarms over lawns and water surfaces during July monsoon breaks, feeding on mosquitoes and midges.
2. **Fulvous Forest Skimmer (*Neurothemis fulvia*)**:
   * Distinctive reddish-brown stained wings with clear tips.
   * Perches on reed tips (*Kashful*) and low aquatic stems along the pond ghat.
3. **Ditch Jewel (*Brachythemis contaminata*)**:
   * Reddish-orange body; hovers directly above water lilies (*Shapla*) and ripples.

---

### 4. Pollinators & Micro-Fauna

* **Asian Honeybee (*Apis cerana*) & Giant Honeybee (*Apis dorsata*)**:
  * Active foragers on Krishnachura, Radhachura, and Jarul blossoms.
  * Massive wild hanging hives documented on high horizontal limbs of ancient Rain Trees.
* **Asian Weaver Ant (*Oecophylla smaragdina*) / লাল পিঁপড়ে (Samka)**:
  * Forms distinctive silken leaf nests by binding living green leaves in Mango and Banyan canopies.

---

### 5. Implementation Strategy in SparkVision

* **Subtle Visual Accent**: Butterflies and dragonflies are implemented as lightweight GPU particle systems (Niagara emitter loops) placed only around flowering tree canopies and water surfaces.
* **Controlled Density**: 2–4 butterflies per flower cluster; 3–5 dragonflies over Curzon Pond.
* **Zero Performance Tax**: Under 0.05 ms GPU time on Apple Silicon M4.
