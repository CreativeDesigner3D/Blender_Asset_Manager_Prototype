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

# <pep8 compliant>
import bpy
from bpy.types import Header, Panel, Menu, UIList
from .. import pyclone_utils

class FILEBROWSER_PT_libraries(Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOLS'
    bl_label = "Display"
    bl_options = {'HIDE_HEADER'}

    @classmethod
    def poll(cls, context):
        if len(context.area.spaces) > 1:
            return True

        # can be None when save/reload with a file selector open
        return context.space_data.params is not None

    def draw(self, context):
        layout = self.layout
        wm_props = pyclone_utils.get_wm_props(context.window_manager)
        scene_props = pyclone_utils.get_scene_props(context.scene)
        col = layout.column(align=True)
        for library in wm_props.libraries:
            if library.name == scene_props.active_library_name:
                layout.operator('pc_library.set_active_library',text=library.name,icon=library.icon,emboss=True).library_name = library.name
            else:
                layout.operator('pc_library.set_active_library',text=library.name,icon=library.icon,emboss=False).library_name = library.name

#HACK: The rest of the classes are redefined so they can be hidden when displaying asset browser

class FILEBROWSER_PT_display(Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'HEADER'
    bl_label = "Display"

    @classmethod
    def poll(cls, context):
        if len(context.area.spaces) > 1:
            return False

        # can be None when save/reload with a file selector open
        return context.space_data.params is not None

    def draw(self, context):
        layout = self.layout
        
        space = context.space_data
        params = space.params

        layout.label(text="Display as")
        layout.column().prop(params, "display_type", expand=True)

        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        if params.display_type == 'THUMBNAIL':
            layout.prop(params, "display_size", text="Size")
        else:
            layout.prop(params, "show_details_size", text="Size")
            layout.prop(params, "show_details_datetime", text="Date")

        layout.prop(params, "recursion_level", text="Recursions")

        layout.use_property_split = False
        layout.separator()

        layout.label(text="Sort by")
        layout.column().prop(params, "sort_method", expand=True)
        layout.prop(params, "use_sort_invert")


class FILEBROWSER_PT_filter(Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'HEADER'
    bl_label = "Filter"

    @classmethod
    def poll(cls, context):
        if len(context.area.spaces) > 1:
            return False        
        # can be None when save/reload with a file selector open
        return context.space_data.params is not None

    def draw(self, context):
        layout = self.layout

        space = context.space_data
        params = space.params
        is_lib_browser = params.use_library_browsing

        row = layout.row(align=True)
        row.prop(params, "use_filter", text="", toggle=0)
        row.label(text="Filter")

        col = layout.column()
        col.active = params.use_filter

        row = col.row()
        row.label(icon='FILE_FOLDER')
        row.prop(params, "use_filter_folder", text="Folders", toggle=0)

        if params.filter_glob:
            col.label(text=params.filter_glob)
        else:
            row = col.row()
            row.label(icon='FILE_BLEND')
            row.prop(params, "use_filter_blender",
                     text=".blend Files", toggle=0)
            row = col.row()
            row.label(icon='FILE_BACKUP')
            row.prop(params, "use_filter_backup",
                     text="Backup .blend Files", toggle=0)
            row = col.row()
            row.label(icon='FILE_IMAGE')
            row.prop(params, "use_filter_image", text="Image Files", toggle=0)
            row = col.row()
            row.label(icon='FILE_MOVIE')
            row.prop(params, "use_filter_movie", text="Movie Files", toggle=0)
            row = col.row()
            row.label(icon='FILE_SCRIPT')
            row.prop(params, "use_filter_script",
                     text="Script Files", toggle=0)
            row = col.row()
            row.label(icon='FILE_FONT')
            row.prop(params, "use_filter_font", text="Font Files", toggle=0)
            row = col.row()
            row.label(icon='FILE_SOUND')
            row.prop(params, "use_filter_sound", text="Sound Files", toggle=0)
            row = col.row()
            row.label(icon='FILE_TEXT')
            row.prop(params, "use_filter_text", text="Text Files", toggle=0)

        col.separator()

        if is_lib_browser:
            row = col.row()
            row.label(icon='BLANK1')  # Indentation
            row.prop(params, "use_filter_blendid",
                     text="Blender IDs", toggle=0)
            if params.use_filter_blendid:
                row = col.row()
                row.label(icon='BLANK1')  # Indentation
                row.prop(params, "filter_id_category", text="")

                col.separator()

        layout.prop(params, "show_hidden")


def panel_poll_is_upper_region(region):
    # The upper region is left-aligned, the lower is split into it then.
    # Note that after "Flip Regions" it's right-aligned.
    return region.alignment in {'LEFT', 'RIGHT'}

class FILEBROWSER_PT_bookmarks_volumes(Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOLS'
    bl_category = "Bookmarks"
    bl_label = "Volumes"

    @classmethod
    def poll(cls, context):
        if len(context.area.spaces) > 1:
            return False        
        return panel_poll_is_upper_region(context.region)

    def draw(self, context):
        layout = self.layout
        space = context.space_data

        if space.system_folders:
            row = layout.row()
            row.template_list("FILEBROWSER_UL_dir", "system_folders", space, "system_folders",
                              space, "system_folders_active", item_dyntip_propname="path", rows=1, maxrows=10)


class FILEBROWSER_PT_bookmarks_system(Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOLS'
    bl_category = "Bookmarks"
    bl_label = "System"

    @classmethod
    def poll(cls, context):
        if len(context.area.spaces) > 1:
            return False        
        return not context.preferences.filepaths.hide_system_bookmarks and panel_poll_is_upper_region(context.region)

    def draw(self, context):
        layout = self.layout
        space = context.space_data

        if space.system_bookmarks:
            row = layout.row()
            row.template_list("FILEBROWSER_UL_dir", "system_bookmarks", space, "system_bookmarks",
                              space, "system_bookmarks_active", item_dyntip_propname="path", rows=1, maxrows=10)


class FILEBROWSER_PT_bookmarks_favorites(Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOLS'
    bl_category = "Bookmarks"
    bl_label = "Favorites"

    @classmethod
    def poll(cls, context):
        if len(context.area.spaces) > 1:
            return False        
        return panel_poll_is_upper_region(context.region)

    def draw(self, context):
        layout = self.layout
        space = context.space_data

        if space.bookmarks:
            row = layout.row()
            num_rows = len(space.bookmarks)
            row.template_list("FILEBROWSER_UL_dir", "bookmarks", space, "bookmarks",
                              space, "bookmarks_active", item_dyntip_propname="path",
                              rows=(2 if num_rows < 2 else 4), maxrows=10)

            col = row.column(align=True)
            col.operator("file.bookmark_add", icon='ADD', text="")
            col.operator("file.bookmark_delete", icon='REMOVE', text="")
            col.menu("FILEBROWSER_MT_bookmarks_context_menu",
                     icon='DOWNARROW_HLT', text="")

            if num_rows > 1:
                col.separator()
                col.operator("file.bookmark_move", icon='TRIA_UP',
                             text="").direction = 'UP'
                col.operator("file.bookmark_move", icon='TRIA_DOWN',
                             text="").direction = 'DOWN'
        else:
            layout.operator("file.bookmark_add", icon='ADD')


class FILEBROWSER_PT_bookmarks_recents(Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOLS'
    bl_category = "Bookmarks"
    bl_label = "Recents"

    @classmethod
    def poll(cls, context):
        if len(context.area.spaces) > 1:
            return False        
        return not context.preferences.filepaths.hide_recent_locations and panel_poll_is_upper_region(context.region)

    def draw(self, context):
        layout = self.layout
        space = context.space_data

        if space.recent_folders:
            row = layout.row()
            row.template_list("FILEBROWSER_UL_dir", "recent_folders", space, "recent_folders",
                              space, "recent_folders_active", item_dyntip_propname="path", rows=1, maxrows=10)

            col = row.column(align=True)
            col.operator("file.reset_recent", icon='X', text="")


class FILEBROWSER_PT_advanced_filter(Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOLS'
    bl_category = "Filter"
    bl_label = "Advanced Filter"

    @classmethod
    def poll(cls, context):
        if len(context.area.spaces) > 1:
            return False        
        # only useful in append/link (library) context currently...
        return context.space_data.params.use_library_browsing and panel_poll_is_upper_region(context.region)

    def draw(self, context):
        layout = self.layout
        space = context.space_data
        params = space.params

        if params and params.use_library_browsing:
            layout.prop(params, "use_filter_blendid")
            if params.use_filter_blendid:
                layout.separator()
                col = layout.column()
                col.prop(params, "filter_id")


class FILEBROWSER_PT_directory_path(Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'UI'
    bl_label = "Directory Path"
    bl_category = "Attributes"
    bl_options = {'HIDE_HEADER'}

    @classmethod
    def poll(cls, context):
        if len(context.area.spaces) > 1:
            return False   
        return True

    def is_header_visible(self, context):
        for region in context.area.regions:
            if region.type == 'HEADER' and region.height <= 1:
                return False

        return True

    def is_option_region_visible(self, context, space):
        if not space.active_operator:
            return False

        for region in context.area.regions:
            if region.type == 'TOOL_PROPS' and region.width <= 1:
                return False

        return True

    def draw(self, context):
        layout = self.layout
        space = context.space_data
        params = space.params

        layout.scale_x = 1.3
        layout.scale_y = 1.3

        row = layout.row()
        flow = row.grid_flow(row_major=True, columns=0, even_columns=False, even_rows=False, align=False)

        subrow = flow.row()

        subsubrow = subrow.row(align=True)
        subsubrow.operator("file.previous", text="", icon='BACK')
        subsubrow.operator("file.next", text="", icon='FORWARD')
        subsubrow.operator("file.parent", text="", icon='FILE_PARENT')
        subsubrow.operator("file.refresh", text="", icon='FILE_REFRESH')

        subsubrow = subrow.row()
        subsubrow.operator_context = 'EXEC_DEFAULT'
        subsubrow.operator("file.directory_new", icon='NEWFOLDER', text="")

        subrow.template_file_select_path(params)

        subrow = flow.row()

        subsubrow = subrow.row()
        subsubrow.scale_x = 0.6
        subsubrow.prop(params, "filter_search", text="", icon='VIEWZOOM')

        # Uses prop_with_popover() as popover() only adds the triangle icon in headers.
        subrow.prop_with_popover(
            params,
            "display_type",
            panel="FILEBROWSER_PT_display",
            text="",
            icon_only=True,
        )
        subrow.prop_with_popover(
            params,
            "display_type",
            panel="FILEBROWSER_PT_filter",
            text="",
            icon='FILTER',
            icon_only=True,
        )

        if space.active_operator:
            subrow.operator(
                "screen.region_toggle",
                text="",
                icon='PREFERENCES',
                depress=self.is_option_region_visible(context, space)
            ).region_type = 'TOOL_PROPS'


classes = (
    FILEBROWSER_PT_libraries,
    FILEBROWSER_PT_display,
    FILEBROWSER_PT_filter,
    FILEBROWSER_PT_bookmarks_volumes,
    FILEBROWSER_PT_bookmarks_system,
    FILEBROWSER_PT_bookmarks_favorites,
    FILEBROWSER_PT_bookmarks_recents,
    FILEBROWSER_PT_advanced_filter,
    FILEBROWSER_PT_directory_path,
)

register, unregister = bpy.utils.register_classes_factory(classes)

