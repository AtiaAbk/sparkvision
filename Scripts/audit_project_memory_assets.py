import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mcp_client

def audit():
    print("Finding all assets under /Game...")
    res = mcp_client.invoke_tool('find_assets', 'editor_toolset.toolsets.asset.AssetTools', {
        'folder_path': '/Game',
        'name': '',
        'recursive': True
    })
    assets = res.get('returnValue', [])
    print(f"Total assets found: {len(assets)}")
    
    classes = {}
    textures = []
    meshes = []
    
    for a in assets:
        try:
            cls_info = mcp_client.invoke_tool('get_asset_class', 'editor_toolset.toolsets.asset.AssetTools', {'asset_path': a})
            cls_name = cls_info.get('returnValue', 'Unknown')
            classes[cls_name] = classes.get(cls_name, 0) + 1
            if 'Texture2D' in cls_name:
                textures.append(a)
            elif 'StaticMesh' in cls_name:
                meshes.append(a)
        except Exception as e:
            pass
            
    print("\nAsset classes breakdown:")
    for k, v in sorted(classes.items(), key=lambda x: x[1], reverse=True):
        print(f"  {k}: {v}")
        
    print(f"\nAuditing {len(textures)} textures...")
    tex_details = []
    for t in textures:
        ref = {'refPath': f"{t}.{t.split('/')[-1]}"}
        try:
            sz = mcp_client.invoke_tool('get_size', 'editor_toolset.toolsets.texture.TextureTools', {'texture': ref}).get('returnValue', {})
            props_str = mcp_client.invoke_tool('get_properties', 'editor_toolset.toolsets.object.ObjectTools', {
                'instance': ref,
                'properties': ['neverStream', 'lODGroup', 'mipGenSettings', 'compressionSettings', 'maxTextureSize', 'sRGB', 'virtualTextureStreaming']
            }).get('returnValue', '{}')
            props = json.loads(props_str)
            width = sz.get('x', 0)
            height = sz.get('y', 0)
            tex_details.append({
                'path': t,
                'width': width,
                'height': height,
                'pixels': width * height,
                'neverStream': props.get('neverStream', False),
                'group': props.get('lODGroup', ''),
                'mips': props.get('mipGenSettings', ''),
                'format': props.get('compressionSettings', ''),
                'maxSize': props.get('maxTextureSize', 0),
                'vt': props.get('virtualTextureStreaming', False)
            })
        except Exception as e:
            # print(f"Error reading texture {t}: {e}")
            pass

    tex_details.sort(key=lambda x: x['pixels'], reverse=True)
    
    print("\nTop 25 Largest Textures by Resolution:")
    for td in tex_details[:25]:
        print(f"  {td['path']} | {td['width']}x{td['height']} | NeverStream={td['neverStream']} | MaxSize={td['maxSize']} | Group={td['group']}")

    never_stream_count = sum(1 for td in tex_details if td['neverStream'])
    print(f"\nTextures with NeverStream=True: {never_stream_count}")
    for td in tex_details:
        if td['neverStream']:
            print(f"  [NEVER STREAM] {td['path']} ({td['width']}x{td['height']})")

    # Save to json report
    out_file = "Documentation/Performance/texture_audit.json"
    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    with open(out_file, "w") as f:
        json.dump(tex_details, f, indent=2)
    print(f"\nWrote full texture audit to {out_file}")

if __name__ == '__main__':
    audit()
