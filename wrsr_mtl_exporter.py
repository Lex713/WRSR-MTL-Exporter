bl_info = {
    "name": "Workers & Resources MTL Exporter",
    "author": "Lex713",
    "version": (1, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Misc Tab",
    "description": "Select mesh objects you want and make an mtl material file for Workers & Resources: Soviet Republic",
    "category": "Import-Export",
}

import bpy
import os

# ---------- PROPERTIES ----------
class WRSettings(bpy.types.PropertyGroup):
    diffuse: bpy.props.FloatVectorProperty(
        name="Diffuse RGBA", subtype="COLOR",
        default=(1.0, 1.0, 1.0, 1.0), size=4, min=0.0, max=1.0
    )
    specular: bpy.props.FloatVectorProperty(
        name="Specular RGBA", subtype="COLOR",
        default=(1.0, 1.0, 1.0, 1.0), size=4, min=0.0, max=1.0
    )
    ambient: bpy.props.FloatVectorProperty(
        name="Ambient RGBA", subtype="COLOR",
        default=(1.0, 1.0, 1.0, 1.0), size=4, min=0.0, max=1.0
    )
    specular_power: bpy.props.FloatProperty(
        name="Specular Power", default=2.0, min=0.0
    )
    texture_prefix: bpy.props.StringProperty(
        name="Texture Path Prefix", default=""
    )
    export_path: bpy.props.StringProperty(
        name="Export Path", subtype="FILE_PATH"
    )

# ---------- PANEL ----------
class WRPanel(bpy.types.Panel):
    bl_label = "W&R MTL Export"
    bl_idname = "VIEW3D_PT_wr_mtl_export"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Misc'

    def draw(self, context):
        layout = self.layout
        settings = context.scene.wr_settings

        layout.prop(settings, "diffuse")
        layout.prop(settings, "specular")
        layout.prop(settings, "ambient")
        layout.prop(settings, "specular_power")
        layout.prop(settings, "texture_prefix")
        layout.prop(settings, "export_path")
        layout.operator("export_scene.wr_mtl")

# ---------- OPERATOR ----------
class EXPORT_OT_wr_mtl(bpy.types.Operator):
    bl_label = "Export W&R MTL"
    bl_idname = "export_scene.wr_mtl"

    def execute(self, context):
        settings = context.scene.wr_settings
        objs = [o for o in context.selected_objects if o.type == 'MESH']
        lines = []

        for obj in objs:
            for slot in obj.material_slots:
                mat = slot.material
                if not mat:
                    continue

                lines.append(f"$SUBMATERIAL {mat.name}")

                # Default textures
                tex_paths = ["blankspecular.dds", "blankspecular.dds", "blankbump.dds"]

                # Try to detect textures from nodes
                if mat.use_nodes:
                    for node in mat.node_tree.nodes:
                        if node.type == 'TEX_IMAGE' and node.image:
                            img_name = os.path.basename(node.image.filepath)
                            # Fill slots in order for now (0,1,2)
                            if tex_paths[0] == "blankspecular.dds":
                                tex_paths[0] = img_name
                            elif tex_paths[1] == "blankspecular.dds":
                                tex_paths[1] = img_name
                            else:
                                tex_paths[2] = img_name

                # Write textures
                for i, tex in enumerate(tex_paths):
                    if tex in ("blankspecular.dds", "blankbump.dds"):
                        lines.append(f"$TEXTURE {i} {tex}")
                    else:
                        lines.append(f"$TEXTURE_MTL {i} {settings.texture_prefix}{tex}")

                def fmt_col(col): return " ".join(f"{c:.6f}" for c in col)

                lines.append(f"$DIFFUSECOLOR {fmt_col(settings.diffuse)}")
                lines.append(f"$SPECULARCOLOR {fmt_col(settings.specular)}")
                lines.append(f"$AMBIENTCOLOR {fmt_col(settings.ambient)}")
                lines.append(f"$SPECULARPOWER {settings.specular_power:.6f}")
                lines.append("")

        # End of file
        lines.append("$END")

        # Save file
        with open(settings.export_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(lines))

        self.report({'INFO'}, f"Exported {len(objs)} objects' materials.")
        return {'FINISHED'}

# ---------- REGISTER ----------
def register():
    bpy.utils.register_class(WRSettings)
    bpy.types.Scene.wr_settings = bpy.props.PointerProperty(type=WRSettings)
    bpy.utils.register_class(WRPanel)
    bpy.utils.register_class(EXPORT_OT_wr_mtl)

def unregister():
    bpy.utils.unregister_class(WRSettings)
    del bpy.types.Scene.wr_settings
    bpy.utils.unregister_class(WRPanel)
    bpy.utils.unregister_class(EXPORT_OT_wr_mtl)

if __name__ == "__main__":
    register()