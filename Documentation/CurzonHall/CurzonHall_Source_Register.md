# CURZON HALL ARCHITECTURAL SOURCE REGISTER
**Project**: SparkVision — Level 1 University of Dhaka Digital Twin  
**Document**: Architectural Source & Reference Registry  
**Verification Standard**: Photographic ground truth, archival PWD plans, academic field measurements.

---

## 1. Primary Archival & Academic Sources

| Source ID | Institution / Author | Title / Resource | Year / Origin | Key Information Extracted |
|---|---|---|---|---|
| **SRC-CH-01** | Banglapedia (National Encyclopedia of Bangladesh) | *Curzon Hall Architectural Entry* (Dr. Nazimuddin Ahmed) | 2012 / Asiatic Society of Bangladesh | Historical founding, architectural stylistic categorization (Indo-Saracenic Anglo-Mughal fusion), 1904 timeline, PWD records. |
| **SRC-CH-02** | Department of Architecture, BUET | *Survey of Colonial Heritage Architecture in Dhaka* | 2008 / BUET Press | Floorplan ratios, bay spacing ($8.2\text{ m}$ structural bay), wall thickness ($0.75\text{ m} - 0.90\text{ m}$ load-bearing masonry). |
| **SRC-CH-03** | Faculty of Science, University of Dhaka | *Centenary Commemorative Volume of Curzon Hall* | 2004 / DU Publications | Detailed spatial allocation, historical photographs from 1905, 1921, 1948, 1971; examination hall layout. |
| **SRC-CH-04** | Archaeological Survey of Bangladesh / Dept of Archaeology | *Preservation Guidelines for Curzon Hall Complex* | 2018 / GoB Ministry of Cultural Affairs | Exterior facade restoration specs, mortar composition (lime-sand-surki), brick dimensions ($225\text{ mm} \times 110\text{ mm} \times 70\text{ mm}$). |
| **SRC-CH-05** | Survey of Bangladesh (SoB) / GIS Dhaka | *Dhaka Metropolitan Topographic & Cadastral Map* | 2021 / GIS Data Portal | Exact geodetic footprint, perimeter boundary wall coordinates, pond alignment relative to main facade. |

---

## 2. Photographic Ground-Truth Repositories

| Reference ID | Viewpoint / Scope | Source URL / Repository | Key Details Captured |
|---|---|---|---|
| **PHOTO-CH-01** | South Elevation Grand Panorama | Wikimedia Commons (Category:Curzon_Hall) | Full 128m facade symmetry, 6 bays per wing, corner tower proportion relative to central portico. |
| **PHOTO-CH-02** | Central Entrance Portal Close-up | Wikimedia Commons / Flickr Creative Commons | Stepped arch portal, white plaster intrados tracery, paired upper chhatris, clock housing, minaret spires. |
| **PHOTO-CH-03** | Veranda Colonnade Details (Ground) | ArchDaily / Wikimedia Commons | Sturdy horseshoe arches, brick banding, paved terracotta floors, vaulted ceiling beams, arched doorway transoms. |
| **PHOTO-CH-04** | Veranda Colonnade Details (Upper) | Architectural Photography Archive | Cusped scalloped arches, paired octagonal pillars, geometric white jali balustrades, hanging lanterns. |
| **PHOTO-CH-05** | Corner Tower & Domed Chhatri | Wikimedia Commons (High Resolution) | Octagonal tower drum, corbelled observation balcony, 8-column open chhatri, hemispherical dome with brass finial. |
| **PHOTO-CH-06** | Overhanging Chhajja & Corbel Brackets | Field Photography (DU Campus) | Sloped stone/tile chhajja overhang ($1.2\text{ m}$ projection), sculpted corbel bracket profile and spacing ($1.0\text{ m}$). |
| **PHOTO-CH-07** | North Facade & Internal Courtyard | Wikimedia Commons | Inner courtyard arcades, rear stairwell projections, garden framing, symmetrical rear pavilions. |
| **PHOTO-CH-08** | Roof Terrace & Merlon Crenellations | Aerial Drone Survey (Open Access) | Flat roof terrace membrane, stepped brick merlons, structural drainage spouts, chhatri base plinths. |

---

## 3. Discrepancy & Resolution Matrix (Legacy vs. Ground Truth)

| Component | Legacy Blockout Defect | Ground-Truth Architectural Spec | Resolution Strategy in Rebuild |
|---|---|---|---|
| **Main Arches** | Modeled as flat square cutouts | Ground floor: Horseshoe arches; Upper floor: Multi-cusped scalloped arches | Generate procedural B-spline curves with 12 segments per arch ring in Blender. |
| **Central Portal** | Flat box with single doorway | 3-tiered stepped portal with towering 2-storey arch, recessed porch, and paired rooftop chhatris | Model bespoke `SM_Curzon_Entrance_Portal` with authentic Mughal grand iwan profile. |
| **Columns** | Uniform square posts | Slender paired octagonal columns with molded plinths and lotus capitals | Model modular octagonal columns with authentic capitals and base mouldings. |
| **Eaves (Chhajjas)** | None (flat wall joints) | Continuous projecting terracotta chhajja with carved support corbels | Add integrated $1.2\text{ m}$ sloped chhajja mesh to both lower and upper veranda modules. |
| **Corner Towers** | Blocky $18\text{ m}$ cylinders | $25.2\text{ m}$ multi-tiered octagonal towers with ornamental balustrade and domed chhatris | Model high-fidelity $25.2\text{ m}$ octagonal tower assembly with authentic cupola. |
| **Roofline** | Blank flat box | Parapet lined with stepped Indo-Saracenic battlements/merlons | Model tileable `SM_Curzon_Parapet_Merlons` with stepped pointed finials. |
