import bpy
from bpy.types import Operator, Panel
from bpy.utils import register_class, unregister_class
from .properties import CustomProperties
from . import utils
from . import construct
from . import calc

# Information about the addon
bl_info = {
    'name': 'Synthetic Data Generator',
    'author': 'Orsós Emil István',
    'version': (0, 4),
    'blender': (2, 80, 0),
    'location': '3D View > Toolbar > Synthetic Data Generator',
    'description': 'Generates synthetic images for machine learning.',
    "warning": "Requires installation of dependencies"
}


class CalculateObjectData(Operator):
    bl_idname = 'object.calc_obj_data'
    bl_label = 'Calculate Object Data'
    bl_description = "Calculates and saves object data to a .json file.\n" \
                     "USE METERS AS LENGTH UNIT WHEN USING THIS FEATURE"

    def execute(self, context):
        if bpy.context.scene.custom_properties.ids_filepath == '':
            utils.show_message_box('A file containing object IDs must be selected!',
                                   'IDs not found!', 'ERROR')
        elif bpy.context.scene.custom_properties.obj_data_filepath == '':
            utils.show_message_box('Select a folder for exportation!',
                                   'IDs not found!', 'ERROR')
        else:
            construct.construct_id_dictionary()
            calc.calc_diameter_of_objects()

        return {'FINISHED'}


class Rendering(Operator):
    bl_idname = 'render.render_images'
    bl_label = 'Render'
    bl_description = "Starts the rendering process.\n" \
                     "Note that this will rebuild your compositor node tree"

    def execute(self, context):

        cam = utils.get_objects(context)

        if cam is None:
            utils.show_message_box('Select a camera using the eyedropper!',
                                   'Camera not found!', 'ERROR')
        elif bpy.context.scene.custom_properties.ids_filepath == '':
            utils.show_message_box('A file containing object IDs must be selected!',
                                   'IDs not found!', 'ERROR')
        else:
            utils.rotate_and_render(context)

        return {'FINISHED'}


class Reposition(Operator):
    bl_idname = 'render.reposition'
    bl_label = 'Reposition'
    bl_description = "Repositions objects in the scene with random lighting."

    def execute(self, context):

        cam = utils.get_objects(context)

        if cam is None:
            utils.show_message_box('Select a camera using the eyedropper!',
                                   'Camera not found!', 'ERROR')
        else:
            utils.reposition(context)

        return {'FINISHED'}


class GetCurrentSettings(Operator):
    bl_idname = 'render.get_current_settings'
    bl_label = 'Get Current Settings'
    bl_description = "Get the current settings of all eyedropped objects."

    def execute(self, context):
        cam = utils.get_objects(context)

        if cam is None:
            utils.show_message_box('Select a camera using the eyedropper!',
                                   'Camera not found!', 'ERROR')
        else:
            utils.get_current_settings(context)

        return {'FINISHED'}


class ZeroEverything(Operator):
    bl_idname = 'render.zero_everything'
    bl_label = 'Zero Everything'
    bl_description = "Set everything to zero."

    def execute(self, context):
        utils.zero_everything(context)
        return {'FINISHED'}


class ResetDefault(Operator):
    bl_idname = 'render.reset_default'
    bl_label = 'Reset Default'
    bl_description = "Return to default values."

    def execute(self, context):
        utils.reset_default(context)
        return {'FINISHED'}


# The main panel of the addon
class SDG(Panel):
    bl_idname = 'SDG_PT_Panel'
    bl_label = 'Synthetic Data Generator'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Synthetic Data Generator'

    def draw(self, context):
        cust_prop = context.scene.custom_properties
        layout = self.layout

        layout.prop(cust_prop, 'render_count')
        layout.prop(cust_prop, 'return_to_original', text='Return To Original')
        layout.operator('render.reposition', text='Reposition')
        layout.operator('render.render_images', text='Render')
        layout.label(text='')
        layout.label(text='Object IDs\' path:')
        layout.prop(cust_prop, 'ids_filepath')
        layout.row().label(text='')
        layout.operator('render.get_current_settings', text='Get Current Settings')
        layout.operator('render.reset_default', text='Reset Default Values')
        layout.operator('render.zero_everything', text='Zero Everything')
        layout.row().label(text='')
        layout.row().label(text='Depth map:')
        row = layout.row(align=True)
        row.prop(cust_prop, 'depth_max_distance')


# The main panel of the addon
class Extras(Panel):
    bl_idname = 'SDG_PT_Extras'
    bl_label = 'Extras'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Synthetic Data Generator'
    bl_parent_id = 'SDG_PT_Panel'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

        layout.label(text='Calculate data of objects:')
        layout.label(text='Export folder:')
        layout.prop(context.scene.custom_properties, 'obj_data_filepath')
        layout.operator('object.calc_obj_data', text='Calculate')


# The camera's sub-panel on the main panel
class CameraPanel(Panel):
    bl_idname = 'SDG_PT_Camera'
    bl_label = 'Camera'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Synthetic Data Generator'
    bl_parent_id = 'SDG_PT_Panel'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        cust_prop = context.scene.custom_properties
        layout = self.layout

        layout.prop(cust_prop, 'camera')

        layout.prop(cust_prop, 'camera_distance')

        layout.label(text='Rotation Minimum:')
        row = layout.row(align=True)
        row.prop(cust_prop, 'camera_min_rot_x')
        row.prop(cust_prop, 'camera_min_rot_y')
        row.prop(cust_prop, 'camera_min_rot_z')

        layout.label(text='Rotation Maximum:')
        row = layout.row(align=True)
        row.prop(cust_prop, 'camera_max_rot_x')
        row.prop(cust_prop, 'camera_max_rot_y')
        row.prop(cust_prop, 'camera_max_rot_z')


# The light's sub-panel on the main panel
class LightPanel(Panel):
    bl_idname = 'SDG_PT_Light'
    bl_label = 'Light'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Synthetic Data Generator'
    bl_parent_id = 'SDG_PT_Panel'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        cust_prop = context.scene.custom_properties
        layout = self.layout

        layout.label(text='Generate:')
        layout.prop(cust_prop, 'point_lights')
        layout.prop(cust_prop, 'sun_lights')
        layout.prop(cust_prop, 'lights_count')

        layout.label(text='Power:')
        row = layout.row(align=True)
        row.prop(cust_prop, 'light_min_intensity')
        row.prop(cust_prop, 'light_max_intensity')

        layout.label(text='Position Minimum:')
        row = layout.row(align=True)
        row.prop(cust_prop, 'light_min_pos_x')
        row.prop(cust_prop, 'light_min_pos_y')
        row.prop(cust_prop, 'light_min_pos_z')

        layout.label(text='Position Maximum:')
        row = layout.row(align=True)
        row.prop(cust_prop, 'light_max_pos_x')
        row.prop(cust_prop, 'light_max_pos_y')
        row.prop(cust_prop, 'light_max_pos_z')

        layout.label(text='Rotation Minimum:')
        row = layout.row(align=True)
        row.prop(cust_prop, 'light_min_rot_x')
        row.prop(cust_prop, 'light_min_rot_y')
        row.prop(cust_prop, 'light_min_rot_z')

        layout.label(text='Rotation Maximum:')
        row = layout.row(align=True)
        row.prop(cust_prop, 'light_max_rot_x')
        row.prop(cust_prop, 'light_max_rot_y')
        row.prop(cust_prop, 'light_max_rot_z')


classes = (SDG,
           Extras,
           CameraPanel,
           LightPanel)


operator_classes = (CustomProperties,
                    CalculateObjectData,
                    Rendering,
                    Reposition,
                    GetCurrentSettings,
                    ZeroEverything,
                    ResetDefault)


# Register classes
def register():
    for cls in classes:
        register_class(cls)

    for cls in operator_classes:
        register_class(cls)

    bpy.types.Scene.custom_properties = bpy.props.PointerProperty(type=CustomProperties)


# Unregister classes
def unregister():
    for cls in classes:
        unregister_class(cls)

    for cls in operator_classes:
        unregister_class(cls)
