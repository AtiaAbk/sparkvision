import unreal

def import_fbx_assets():
    models_dir = "/Users/atiaoishi/Downloads/sparkvision/SourceAssets/Models"
    destination_path = "/Game/SparkVision/Campus"

    import_tasks = []
    models = [
        "SM_CurzonHall.fbx",
        "SM_RajuSculpture.fbx",
        "SM_AparajeyoBangla.fbx",
        "SM_TSC_Building.fbx",
        "SM_CentralLibrary.fbx",
        "SM_ArchiveTerminal.fbx"
    ]

    for model in models:
        task = unreal.AssetImportTask()
        task.filename = f"{models_dir}/{model}"
        task.destination_path = destination_path
        task.destination_name = model.replace(".fbx", "")
        task.replace_existing = True
        task.automated = True
        task.save = True

        options = unreal.FbxImportUI()
        options.import_mesh = True
        options.import_textures = False
        options.import_materials = False
        options.import_as_skeletal = False
        options.static_mesh_import_data.combine_meshes = True
        options.static_mesh_import_data.auto_generate_collision = True
        task.options = options
        import_tasks.append(task)

    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(import_tasks)
    print(f"[SUCCESS] Imported {len(models)} DU Landmark meshes into {destination_path}")

if __name__ == "__main__":
    import_fbx_assets()
