import unreal

def build_level1_du_campus():
    # Load level
    level_path = "/Game/ThirdPerson/Lvl_ThirdPerson"
    world = unreal.EditorLoadingAndSavingUtils.load_map(level_path)
    if not world:
        print(f"[ERROR] Could not load level {level_path}")
        return

    # Load Static Meshes
    mesh_curzon = unreal.EditorAssetLibrary.load_asset("/Game/SparkVision/Campus/SM_CurzonHall")
    mesh_raju = unreal.EditorAssetLibrary.load_asset("/Game/SparkVision/Campus/SM_RajuSculpture")
    mesh_aparajeyo = unreal.EditorAssetLibrary.load_asset("/Game/SparkVision/Campus/SM_AparajeyoBangla")
    mesh_tsc = unreal.EditorAssetLibrary.load_asset("/Game/SparkVision/Campus/SM_TSC_Building")
    mesh_lib = unreal.EditorAssetLibrary.load_asset("/Game/SparkVision/Campus/SM_CentralLibrary")
    mesh_archive = unreal.EditorAssetLibrary.load_asset("/Game/SparkVision/Campus/SM_ArchiveTerminal")

    editor_actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

    # Spawn Curzon Hall (Hero Landmark at origin)
    curzon_actor = editor_actor_subsystem.spawn_actor_from_class(unreal.StaticMeshActor, unreal.Vector(0, 0, 0), unreal.Rotator(0, 0, 0))
    if curzon_actor and mesh_curzon:
        curzon_actor.set_actor_label("Curzon_Hall_Complex")
        curzon_actor.static_mesh_component.set_static_mesh(mesh_curzon)

    # Spawn Raju Sculpture (TSC Intersection, South-West)
    raju_actor = editor_actor_subsystem.spawn_actor_from_class(unreal.StaticMeshActor, unreal.Vector(-4500, -3500, 0), unreal.Rotator(0, 45, 0))
    if raju_actor and mesh_raju:
        raju_actor.set_actor_label("Raju_AntiTerrorism_Sculpture")
        raju_actor.static_mesh_component.set_static_mesh(mesh_raju)

    # Spawn Aparajeyo Bangla (Arts Plaza, North-West)
    aparajeyo_actor = editor_actor_subsystem.spawn_actor_from_class(unreal.StaticMeshActor, unreal.Vector(-3500, 3500, 0), unreal.Rotator(0, -30, 0))
    if aparajeyo_actor and mesh_aparajeyo:
        aparajeyo_actor.set_actor_label("Aparajeyo_Bangla_ArtsPlaza")
        aparajeyo_actor.static_mesh_component.set_static_mesh(mesh_aparajeyo)

    # Spawn TSC Building (Adjacent to Raju)
    tsc_actor = editor_actor_subsystem.spawn_actor_from_class(unreal.StaticMeshActor, unreal.Vector(-5500, -2500, 0), unreal.Rotator(0, 90, 0))
    if tsc_actor and mesh_tsc:
        tsc_actor.set_actor_label("TSC_Building_Complex")
        tsc_actor.static_mesh_component.set_static_mesh(mesh_tsc)

    # Spawn Central Library (North-Central)
    lib_actor = editor_actor_subsystem.spawn_actor_from_class(unreal.StaticMeshActor, unreal.Vector(-1500, 4500, 0), unreal.Rotator(0, 0, 0))
    if lib_actor and mesh_lib:
        lib_actor.set_actor_label("DU_Central_Library")
        lib_actor.static_mesh_component.set_static_mesh(mesh_lib)

    # Spawn 5 Historical Archives (ASVArchiveTerminal)
    archive_class = unreal.load_class(None, "/Script/MyProject.SVArchiveTerminal")
    if archive_class:
        archive_configs = [
            ("archive_01", "Curzon Hall Central Arcade Founding Record", unreal.Vector(0, -1200, 150), unreal.Rotator(0, 0, 0)),
            ("archive_02", "Aparajeyo Bangla 1952/1971 Chronicle", unreal.Vector(-3500, 3100, 150), unreal.Rotator(0, 45, 0)),
            ("archive_03", "Raju Anti-Terrorism Memorial Declaration", unreal.Vector(-4500, -3100, 150), unreal.Rotator(0, 90, 0)),
            ("archive_04", "Central Library & Hakim Chattar Reform Gazette", unreal.Vector(-1500, 4000, 150), unreal.Rotator(0, 0, 0)),
            ("archive_05", "Teacher-Student Centre (TSC) Unity Manifesto", unreal.Vector(-5500, -2100, 150), unreal.Rotator(0, 180, 0))
        ]

        for a_id, a_title, loc, rot in archive_configs:
            arch_act = editor_actor_subsystem.spawn_actor_from_class(archive_class, loc, rot)
            if arch_act:
                arch_act.set_actor_label(f"ArchiveTerminal_{a_id}")
                arch_act.set_editor_property("ArchiveId", a_id)
                arch_act.set_editor_property("ArchiveTitle", unreal.Text(a_title))
                if mesh_archive:
                    mesh_comp = arch_act.get_component_by_class(unreal.StaticMeshComponent)
                    if mesh_comp:
                        mesh_comp.set_static_mesh(mesh_archive)

    # Spawn Student NPCs
    npc_class = unreal.load_class(None, "/Script/MyProject.SVStudentNPC")
    if npc_class:
        npc1 = editor_actor_subsystem.spawn_actor_from_class(npc_class, unreal.Vector(400, -800, 100), unreal.Rotator(0, 180, 0))
        if npc1:
            npc1.set_actor_label("NPC_Student_Curzon")

        npc2 = editor_actor_subsystem.spawn_actor_from_class(npc_class, unreal.Vector(-4300, -3300, 100), unreal.Rotator(0, 135, 0))
        if npc2:
            npc2.set_actor_label("NPC_Student_Raju")

    # Spawn Hostile Opponents for the July 15 confrontation
    hostile_class = unreal.load_class(None, "/Script/MyProject.SVHostileOpponent")
    if hostile_class:
        h1 = editor_actor_subsystem.spawn_actor_from_class(hostile_class, unreal.Vector(1200, -1500, 100), unreal.Rotator(0, 90, 0))
        if h1:
            h1.set_actor_label("Opponent_Helmeted_01")
        h2 = editor_actor_subsystem.spawn_actor_from_class(hostile_class, unreal.Vector(1400, -1600, 100), unreal.Rotator(0, 90, 0))
        if h2:
            h2.set_actor_label("Opponent_Helmeted_02")

    # Save level
    unreal.EditorLoadingAndSavingUtils.save_map(world, level_path)
    print(f"[SUCCESS] Dhaka University Campus Level 1 successfully populated and saved to {level_path}")

if __name__ == "__main__":
    build_level1_du_campus()
