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

bl_info = {
    "name": "Blender Asset Manager Prototype",
    "author": "Andrew Peel",
    "version": (0, 0, 1),
    "blender": (2, 83, 0),
    "location": "File Browser",
    "description": "Blender Asset Manager Prototype",
    "warning": "",
    "wiki_url": "",
    "category": "Asset Management",
}

from .ui import pc_filebrowser_ui
from .ops import pc_library
from .ops import pc_general
from .ops import pc_window_manager
from . import pyclone_props

def register():
    pc_filebrowser_ui.register()
    pc_library.register()
    pc_general.register()
    pc_window_manager.register()
    pyclone_props.register()

def unregister():
    pc_filebrowser_ui.unregister()
    pc_library.unregister()
    pc_general.unregister()
    pc_window_manager.unregister()
    pyclone_props.unregister()