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

import bpy,os

from bpy.types import (Header, 
                       Menu, 
                       Panel, 
                       Operator,
                       PropertyGroup)

from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       PointerProperty,
                       EnumProperty,
                       CollectionProperty)

from .. import pyclone_utils

class pc_library_OT_set_active_library(Operator):
    bl_idname = "pc_library.set_active_library"
    bl_label = "Set Active Library"
    bl_options = {'UNDO'}
    
    library_name: StringProperty(name='Library Name')

    def execute(self, context):
        pyclone_scene = pyclone_utils.get_scene_props(context.scene)
        pyclone_scene.active_library_name = self.library_name

        pyclone_wm = pyclone_utils.get_wm_props(context.window_manager)
        for library in pyclone_wm.libraries:
            if library.name == self.library_name:
                if library.activate_id != "":
                    eval('bpy.ops.' + library.activate_id + '("INVOKE_DEFAULT",library_name=self.library_name)')
                    
        context.area.tag_redraw()
        return {'FINISHED'}

classes = (
    pc_library_OT_set_active_library,
)

register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()
