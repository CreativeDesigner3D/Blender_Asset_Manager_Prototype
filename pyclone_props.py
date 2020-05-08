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
from bpy.types import (
        Operator,
        Panel,
        PropertyGroup,
        UIList,
        )
from bpy.props import (
        BoolProperty,
        FloatProperty,
        IntProperty,
        PointerProperty,
        StringProperty,
        CollectionProperty,
        EnumProperty,
        )

class Library(bpy.types.PropertyGroup):
    activate_id: bpy.props.StringProperty(name="Activate ID",
                                          description="This is the operator id that gets called when you activate the library")

    drop_id: bpy.props.StringProperty(name="Drop ID",
                                      description="This is the operator id that gets called when you drop a file onto the 3D Viewport")

    icon: bpy.props.StringProperty(name="Icon",
                                   description="This is the icon to display in the panel")


class PC_Window_Manager_Props(bpy.types.PropertyGroup):
    libraries: CollectionProperty(name="Libraries",
                                  type=Library)

    def add_library(self,name,activate_id,drop_id,icon):
        lib = self.libraries.add()
        lib.name = name
        lib.activate_id = activate_id
        lib.drop_id = drop_id
        lib.icon = icon
        return lib

    def remove_library(self,name):
        for i, lib in enumerate(self.libraries):
            if lib.name == name:
                self.libraries.remove(i)

    @classmethod
    def register(cls):
        bpy.types.WindowManager.pyclone = bpy.props.PointerProperty(
            name="PyClone",
            description="PyClone Properties",
            type=cls,
        )
        
    @classmethod
    def unregister(cls):
        del bpy.types.WindowManager.pyclone    


class PC_Scene_Props(PropertyGroup):
    active_library_name: StringProperty(name="Active Library Name",default="")

    @classmethod
    def register(cls):
        bpy.types.Scene.pyclone = PointerProperty(
            name="PyClone",
            description="PyClone Properties",
            type=cls,
        )
        
    @classmethod
    def unregister(cls):
        del bpy.types.Scene.pyclone


classes = (
    Library,
    PC_Window_Manager_Props,
    PC_Scene_Props,
)

register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()