# SPARKVISION — ENVIRONMENT ASSET INVENTORY
## Complete 3D Botanical Mesh, Foliage, Decal & PBR Material Register

---

### 1. Static Mesh Vegetation Assets (`/Game/SparkVision/Campus/Environment/`)

| Asset Name | Species / Type | Triangles | LODs | Dimensions ($L \times W \times H\text{ m}$) | Assigned PBR Materials | Content Browser Path |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| `SM_Tree_Raintree_Avenue` | *Albizia saman* | 3,840 | 3 | $22.0 \times 20.0 \times 17.5$ | `MI_Bark_Tree`, `MI_Foliage_Raintree_Leaf` | `/Game/SparkVision/Campus/Environment/` |
| `SM_Tree_Krishnachura_Bloom` | *Delonix regia* | 3,120 | 3 | $14.5 \times 13.0 \times 11.2$ | `MI_Bark_Tree`, `MI_Foliage_Krishnachura_Red` | `/Game/SparkVision/Campus/Environment/` |
| `SM_Tree_Radhachura_Yellow` | *Peltophorum pterocarpum* | 3,240 | 3 | $13.5 \times 12.0 \times 12.8$ | `MI_Bark_Tree`, `MI_Foliage_Radhachura_Yellow` | `/Game/SparkVision/Campus/Environment/` |
| `SM_Tree_Banyan_Mature` | *Ficus benghalensis* | 5,680 | 4 | $28.0 \times 26.0 \times 18.5$ | `MI_Bark_Tree`, `MI_Foliage_Banyan_Leaf` | `/Game/SparkVision/Campus/Environment/` |
| `SM_Tree_Jarul_Purple` | *Lagerstroemia speciosa* | 2,760 | 3 | $9.5 \times 8.8 \times 10.2$ | `MI_Bark_Tree`, `MI_Foliage_Jarul_Lilac` | `/Game/SparkVision/Campus/Environment/` |
| `SM_Tree_Neem_Delicate` | *Azadirachta indica* | 2,420 | 3 | $8.2 \times 7.5 \times 9.0$ | `MI_Bark_Tree`, `MI_Foliage_Neem_Green` | `/Game/SparkVision/Campus/Environment/` |
| `SM_Tree_Palm_Coconut` | *Cocos nucifera* / *Roystonea* | 2,160 | 3 | $6.5 \times 6.5 \times 14.5$ | `MI_Bark_Palm`, `MI_Foliage_PalmFrond` | `/Game/SparkVision/Campus/Environment/` |
| `SM_Tree_Palm_BetelNut` | *Areca catechu* | 1,480 | 2 | $3.5 \times 3.5 \times 12.0$ | `MI_Bark_Palm`, `MI_Foliage_PalmFrond` | `/Game/SparkVision/Campus/Environment/` |
| `SM_Cluster_Bamboo_Thicket` | *Bambusa tulda* | 4,120 | 3 | $4.2 \times 3.8 \times 8.2$ | `MI_Stem_BambooGold`, `MI_Foliage_BambooLeaf` | `/Game/SparkVision/Campus/Environment/` |
| `SM_Curzon_Hedge_Low` | *Duranta repens* (Hedge) | 860 | 2 | $4.0 \times 0.7 \times 0.85$ | `MI_Curzon_Hedge` | `/Game/SparkVision/Campus/CurzonModular/` |
| `SM_Plant_Reeds_Kashful` | *Saccharum spontaneum* | 1,240 | 2 | $2.2 \times 2.0 \times 1.6$ | `MI_Stem_ReedGreen`, `MI_Foliage_KashfulWhite` | `/Game/SparkVision/Campus/Environment/` |
| `SM_Pond_WaterLily_Cluster` | *Nymphaea nouchali* (Shapla) | 1,680 | 2 | $3.2 \times 3.0 \times 0.25$ | `MI_Foliage_LilyPad`, `MI_Flower_Shapla` | `/Game/SparkVision/Campus/Environment/` |
| `SM_Curzon_Pond_Ghat` | Colonial Brick Pukur Ghat | 940 | 2 | $18.0 \times 8.0 \times 2.4$ | `MI_Curzon_StonePaving`, `MI_Water_Pond` | `/Game/SparkVision/Campus/Environment/` |
| `SM_Decal_Petal_Scatter` | Fallen Blossom Decal | 2 (Decal Quad)| N/A | $3.0 \times 3.0 \times 0.2$ | `MI_Decal_KrishnachuraPetals` | `/Game/SparkVision/Campus/Environment/` |

---

### 2. Physically Based Material Register (`/Game/SparkVision/Materials/`)

| Material Instance Name | Parent Master Material | Shading Model | Primary Parameters | Base Color Tint (Hex) | Roughness |
| :--- | :--- | :--- | :--- | :---: | :---: |
| `MI_Bark_Tree` | `M_Bark_Master` | Default Lit | Macro bark tiling, normal intensity | Charcoal-Brown (`#36281D`) | 0.85 |
| `MI_Bark_Palm` | `M_Bark_Master` | Default Lit | Ringed annular displacement | Cement-Grey (`#6E685F`) | 0.80 |
| `MI_Foliage_Raintree_Leaf` | `M_Foliage_TwoSided` | Two-Sided Foliage | Subsurface scattering, wind WPO | Rich Emerald (`#285418`) | 0.45 |
| `MI_Foliage_Krishnachura_Red` | `M_Foliage_TwoSided` | Two-Sided Foliage | Scarlet petal emissive highlight | Fiery Scarlet (`#C42214`) | 0.40 |
| `MI_Foliage_Radhachura_Yellow` | `M_Foliage_TwoSided` | Two-Sided Foliage | Golden flower cluster transmission | Warm Gold (`#D4A018`) | 0.42 |
| `MI_Foliage_Banyan_Leaf` | `M_Foliage_TwoSided` | Two-Sided Foliage | Glossy leathery upper cuticle | Deep Forest (`#1C3D12`) | 0.35 |
| `MI_Foliage_Jarul_Lilac` | `M_Foliage_TwoSided` | Two-Sided Foliage | Lilac petal transmission | Soft Lilac (`#9A64A8`) | 0.40 |
| `MI_Foliage_Neem_Green` | `M_Foliage_TwoSided` | Two-Sided Foliage | Airy feathery translucency | Bright Spring (`#427D20`) | 0.48 |
| `MI_Foliage_PalmFrond` | `M_Foliage_TwoSided` | Two-Sided Foliage | Long frond bend, wind flutter | Glossy Palm (`#2D611B`) | 0.38 |
| `MI_Foliage_BambooLeaf` | `M_Foliage_TwoSided` | Two-Sided Foliage | Slender flutter, golden-green tint | Bamboo Yellow-Green (`#587524`)| 0.50 |
| `MI_Curzon_Hedge` | `M_Foliage_TwoSided` | Two-Sided Foliage | Boxwood dense leaf scatter | Manicured Boxwood (`#295E1E`)| 0.65 |
| `MI_Foliage_LilyPad` | `M_Foliage_TwoSided` | Two-Sided Foliage | Waxy water-beading clearcoat | Pond Green (`#244D1E`) | 0.25 |
| `MI_Flower_Shapla` | `M_Foliage_TwoSided` | Two-Sided Foliage | White-violet dual gradient | Pale Violet-White (`#EDE6F2`) | 0.30 |
| `MI_Water_Pond` | `M_Water_Master` | Single Layer Water | Depth absorption, dual normal ripples| Murky Deltaic Green (`#162919`)| 0.08 |
| `MI_Decal_KrishnachuraPetals` | `M_Decal_Master` | DBuffer Translucent | Opacity mask, normal scatter | Crimson Petal (`#B81E12`) | 0.55 |
