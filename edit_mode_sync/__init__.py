from bpy.app.handlers import persistent
import bpy
bl_info = {
    "name": "Edit Mode Sync",
    "author": "Johnny Matthews",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "3d Viewport",
    "description": "Synchronize the selection and view of vertices, edges, and faces to overlay settings",
    "category": "Mesh",
}

# Use the Vertex Select Color for Edge Select
save = bpy.context.preferences.themes[0].view_3d.vertex_select[:3]
dark = (.3, .3, .3)

# @persistent


def do_select_settings(scene):
    if bpy.context.mode != 'EDIT_MESH':
        return
    space = None
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            space = area.spaces.active
            break
    if space is None:
        return

    theme = bpy.context.preferences.themes[0]

    vert = bpy.context.tool_settings.mesh_select_mode[0]
    edge = bpy.context.tool_settings.mesh_select_mode[1]
    face = bpy.context.tool_settings.mesh_select_mode[2]

    if vert and not edge and not face:
        space.overlay.show_edges = False
        theme.view_3d.edge_select = dark
        space.overlay.show_faces = False
        return

    if edge and not vert and not face:
        space.overlay.show_edges = True
        theme.view_3d.edge_select = save
        space.overlay.show_faces = False
        return

    if face and not vert and not edge:
        space.overlay.show_edges = False
        theme.view_3d.edge_select = dark
        space.overlay.show_faces = True
        return

    if vert and edge and not face:
        space.overlay.show_edges = True
        theme.view_3d.edge_select = save
        space.overlay.show_faces = False
        return

    if vert and not edge and face:
        space.overlay.show_edges = False
        theme.view_3d.edge_select = dark
        space.overlay.show_faces = True
        return

    if not vert and edge and face:
        space.overlay.show_edges = True
        theme.view_3d.edge_select = save
        space.overlay.show_faces = True
        return

    if vert and edge and face:
        space.overlay.show_edges = True
        theme.view_3d.edge_select = save
        space.overlay.show_faces = True
        return


def register():
    bpy.app.handlers.depsgraph_update_post.append(do_select_settings)


def unregister():
    try:
        bpy.app.handlers.depsgraph_update_post.remove(do_select_settings)
    except:
        pass

# if __name__ == "__main__":
#    register()
