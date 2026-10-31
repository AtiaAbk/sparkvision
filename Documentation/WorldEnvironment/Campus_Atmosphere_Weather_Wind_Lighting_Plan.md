# CAMPUS ATMOSPHERE, WEATHER, WIND & LIGHTING PLAN
**Project**: SparkVision — Level 1 University of Dhaka Digital Twin  
**Aesthetic Benchmark**: *Ghost of Tsushima* Golden Hour & *Where Winds Meet* Dynamic Weather  
**Lighting Architecture**: Unreal Engine 5.8 Software Lumen (Mesh Distance Fields) + Directional Light + Volumetric Fog + PostProcess Color Grading.

---

## 1. Atmosphere & Lighting Configurations

### A. "Golden Afternoon" (Default Cinematic Baseline)
* **Sun Elevation / Azimuth**: Altitude $28^\circ$, Azimuth $235^\circ$ (South-West afternoon sun).
* **Directional Light Intensity**: $45,000\text{ Lux}$, Light Color `#FFF2DC` (warm golden amber).
* **Volumetric Fog**: Density `0.012`, Albedo `#F7E5C8`, Extinction Scale `1.0`, View Distance `65,000 UU`.
* **Skylight**: Cubemap capture with subtle azure fill (`#95BBE5`, intensity `1.2`).
* **Visual Mood**: Warm, nostalgic, cinematic golden light filtering through dense Raintree branches and casting long dramatic shadows across the red-brick facade of Curzon Hall.

### B. "Pre-Monsoon Nor'wester / Kalbaishakhi" (Dramatic Weather State)
* **Sun Elevation**: Obscured by dense storm front; directional light drops to $8,000\text{ Lux}$.
* **Atmospheric Color**: Dark bruised cobalt-slate (`#2B3542`) with sickly green-yellow horizon highlights.
* **Wind Vector**: Sudden surge from $2.0\text{ m/s}$ to $14.5\text{ m/s}$ directed from North-West ($315^\circ$).
* **Foliage Motion**: Heavy swaying of Banyan limbs, violent flutter of Krishnachura leaves, bamboo thickets groaning and bending at $35^\circ$.
* **Particles**: High-speed swirling gusts of scarlet petals, dried mango leaves, and dust clouds across open asphalt plazas.

### C. "Monsoon Rain & Wet Specular" (Atmospheric Rain State)
* **Precipitation**: Niagara rain mesh particles with dynamic splash decals on ground planes.
* **Surface Materials**: Runtime wetness roughness clamp ($0.05 - 0.20$), boosting specular reflections of street lamps and building facades.
* **Atmosphere**: Heavy localized fog near Curzon pond, dripping water trickles from chhajja eaves.

---

## 2. Post-Process Volume & Color Grading
* **Tone Mapper**: ACES filmic tonemapper.
* **Contrast & Saturation**:
  - Global Contrast: `1.12` (crisp shadow separation).
  - Global Saturation: `1.15` (vibrant natural Bengal greens and warm brick reds).
  - Shadow Tint: Subtle warm umber (`#150E0A`) preventing cold digital blacks.
* **Bloom**: Convolution bloom with subtle lens flare on direct sun occlusion.
