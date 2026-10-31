# CAMPUS TREE INVENTORY & PLACEMENT MATRIX
**Project**: SparkVision — Level 1 University of Dhaka Digital Twin  
**Methodology**: Procedural generation in Blender $\rightarrow$ Modular static mesh library $\rightarrow$ Exact geolocated and ecologically logical level placement in `LV_Campus_Blockout.umap`.

---

## 1. 3D Vegetation Asset Library Specifications

| Asset Name | Triangle Count (LOD0) | Height / Spread (m) | Trunk & Bark Material | Leaf / Blossom Material | Animation / Shader Feature |
|---|---|---|---|---|---|
| **`SM_Tree_Banyan_Mature`** | 18,500 | $24.0\text{ m} / 36.0\text{ m}$ | `M_Bark_Banyan` (heavily fluted, buttressed with 6 aerial prop roots) | `M_Foliage_Banyan_Leaf` (dense dark green oval leaves) | Low-frequency trunk sway, multi-tier wind flutter. |
| **`SM_Tree_Raintree_Avenue`**| 14,200 | $28.0\text{ m} / 32.0\text{ m}$ | `M_Bark_Raintree` (fissured dark grey-brown with lichen patches) | `M_Foliage_Raintree_Leaf` (feathery bipinnate leaflets, pink blossom puffs) | Broad umbrella canopy, dappled light shadow casting. |
| **`SM_Tree_Krishnachura_Bloom`**| 12,800 | $15.0\text{ m} / 18.0\text{ m}$ | `M_Bark_Krishnachura` (smooth greyish bark) | `M_Foliage_Krishnachura_Red` (vibrant scarlet 5-petal flowers, fern foliage) | High-wind branch sway, falling petal particle attachment. |
| **`SM_Tree_Radhachura_Yellow`**| 11,500 | $16.0\text{ m} / 16.0\text{ m}$ | `M_Bark_Radhachura` (rough brown bark) | `M_Foliage_Radhachura_Yellow` (bright golden blossom clusters) | Fluttering flower spikes, contrasting yellow canopy. |
| **`SM_Tree_Jarul_Purple`** | 10,800 | $14.0\text{ m} / 12.0\text{ m}$ | `M_Bark_Jarul` (peeling mottled grey bark) | `M_Foliage_Jarul_Lilac` (dense crinkled lilac petals) | Water-margin canopy, purple blossom drops. |
| **`SM_Tree_Neem_Delicate`** | 9,400 | $12.0\text{ m} / 10.0\text{ m}$ | `M_Bark_Neem` (dark brown furrowed bark) | `M_Foliage_Neem_Green` (slender serrated leaflets) | Sensitive breeze flutter, light airy canopy shadow. |
| **`SM_Tree_Palm_Coconut`** | 5,200 | $20.0\text{ m} / 7.0\text{ m}$ | `M_Bark_PalmRinged` (curved ringed grey trunk) | `M_Foliage_PalmFrond` (arching pinnate fronds, coconut cluster) | Pronounced trunk curvature bending into wind vector. |
| **`SM_Tree_Palm_BetelNut`** | 3,800 | $16.0\text{ m} / 3.0\text{ m}$ | `M_Bark_BetelGreen` (pencil-straight green-ringed trunk) | `M_Foliage_BetelCrown` (compact upright fronds, orange betel nuts) | Rigid vertical accentuation, subtle tip flutter. |
| **`SM_Cluster_Bamboo_Thicket`**| 8,600 | $14.0\text{ m} / 8.0\text{ m}$ | `M_Stem_BambooGold` (striped golden/green culms) | `M_Foliage_BambooLeaf` (dense rustling lanceolate leaf clumps) | High-amplitude wind bending, organic creaking audio cue. |

---

## 2. Landmark-Specific Placement Matrix in `LV_Campus_Blockout.umap`

| Campus Zone / Sector | World Coordinate Extents | Key Tree Placements & Ecology Rules |
|---|---|---|
| **Curzon Hall Botanical Grounds** | $X \in [-4500, -1000]$, $Y \in [-6500, 6500]$ | 4 Mature Banyans framing corners; 8 Krishnachura trees along front lawns; 3 Bamboo thickets buffering south perimeter; 6 Coconut palms and 4 Jarul along pond banks. |
| **Fuller Road Grand Avenue** | $X \in [0, 8000]$, $Y \in [-12000, -6000]$ | 16 Massive Raintrees aligned at $25\text{ m}$ spacing along both sides of the roadway, creating the historic shaded canopy tunnel. |
| **The Mall & Central Field** | $X \in [6000, 14000]$, $Y \in [-5000, 5000]$ | 2 Ancient Landmark Banyans on field perimeter; 12 Coconut palms along eastern fence; open central turf grass for athletics. |
| **Arts Faculty (Kala Bhaban)** | $X \in [8000, 14000]$, $Y \in [-10000, -4000]$ | 6 Krishnachura trees around Aparajeyo Bangla sculpture; 8 Radhachura trees along car park; interior courtyard shade ferns. |
| **TSC & Raju Sculpture** | $X \in [3000, 7000]$, $Y \in [-3000, 3000]$ | 4 Spreading Rain trees providing pedestrian shade; 6 Neem trees along library perimeter; clipped bougainvillea hedges. |
| **Shaheed Minar Sanctuary** | $X \in [1000, 4500]$, $Y \in [4000, 8000]$ | Symmetrical rows of dark-green Ashoka trees and weeping weeping ficus framing the white marble monument; zero visual obstruction of central altar. |
| **Shahidullah Hall Quadrangle** | $X \in [-1000, 2000]$, $Y \in [5000, 10000]$ | 1 Historic Banyan in central courtyard; 8 Coconut palms around lake; 4 Kadam trees along water inlet. |
