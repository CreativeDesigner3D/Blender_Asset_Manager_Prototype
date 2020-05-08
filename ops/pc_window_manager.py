# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import bpy
import os
from bpy.types import Operator

from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       BoolVectorProperty,
                       PointerProperty,
                       CollectionProperty,
                       EnumProperty)

from .. import pyclone_utils

class WM_OT_drag_and_drop(bpy.types.Operator):
    bl_idname = "wm.drag_and_drop"
    bl_label = "Drag and Drop"
    bl_description = "This is a special operator that will be called when an image is dropped from the file browser"

    filepath: bpy.props.StringProperty(name="Message",default="Error")

    def execute(self, context):
        wm_props = pyclone_utils.get_wm_props(context.window_manager)
        scene_props = pyclone_utils.get_scene_props(context.scene)
        
        if scene_props.active_library_name in wm_props.libraries:
            lib = wm_props.libraries[scene_props.active_library_name]
            eval('bpy.ops.' + lib.drop_id + '("INVOKE_DEFAULT",filepath=self.filepath)')

        return {'FINISHED'}

classes = (
    WM_OT_drag_and_drop,
)

register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()
