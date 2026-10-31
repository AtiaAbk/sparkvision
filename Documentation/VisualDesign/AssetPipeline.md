# SPARKVISION — ASSET CREATION & IMPORT PIPELINE

## 1. Title & Executive Purpose

* **Document**: `AssetPipeline.md`
* **Purpose**: Defines standard operating procedures for 3D modeling in Blender 5.2.3 LTS, metric unit export settings, automated FBX compilation, and programmatic asset ingestion via Unreal MCP into Unreal Engine 5.8.

---

## 2. Blender-to-Unreal Unit Scale Standard

Unreal Engine operates strictly in **centimeters** ($1\text{ uu} = 1\text{ cm}$).

### 2.1 Blender Scene Configuration
* **Unit System**: Metric
* **Unit Scale**: `1.0` (1 Blender Unit = 1 Meter)
* **Length**: Meters

### 2.2 FBX Export Settings
To achieve perfect 1:1 scale correspondence without unexpected $100\times$ or $0.01\times$ scaling:
```python
bpy.ops.export_scene.fbx(
    filepath="SourceAssets/Models/SM_Asset.fbx",
    use_selection=True,
    global_scale=1.0,
    apply_unit_scale=True,
    bake_space_transform=True,
    axis_forward='-Z',
    axis_up='Y',
    apply_scale_options='FBX_SCALE_ALL'
)
```

---

## 3. Automated Import Workflow via Unreal MCP

Asset ingestion is driven programmatically by Python scripts utilizing the Unreal MCP bridge:

```text
Blender Modeling -> Export FBX to SourceAssets/Models/
                     │
                     ▼
             Scripts/import_*.py
                     │
                     ▼
          Unreal MCP (AssetTools.import_asset)
                     │
                     ▼
       Target Folder (/Game/SparkVision/Campus/...)
                     │
                     ▼
      PBR Material Assignment (MaterialTools.set_material)
                     │
                     ▼
      Save to Disk (AssetTools.save_assets)
```

---

## 4. Current Status

* **Status**: `COMPLETED`
* **Evidence**:
  - 8 modular Curzon assets and 4 Phase 3 landmark FBX models exported and imported with zero scale mismatch.
  - Bounding box audit confirmed exact metric dimensions (e.g. `SM_Curzon_Entrance_Portal` = 17m × 5m × 20m).
* **Remaining Tasks**:
  - Implement automated collision mesh generation (`UCX_` hulls) in export scripts.
