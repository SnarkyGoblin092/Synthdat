import bpy
from bpy.types import Operator, Panel
from bpy.utils import register_class, unregister_class
from . import utils
from .properties import CustomProperties

# Information about the addon
bl_info = {
    'name': 'Synthetic Data Generator',
    'author': 'Orsós Emil István',
    'version': (0, 3),
    'blender': (2, 80, 0),
    'location': '3D View > Toolbar > Synthetic Data Generator',
    'description': 'Generates synthetic images for machine learning.'
}


class Rendering(Operator):
    bl_idname = 'render.render_images'
    bl_label = 'Render'
    """ 
        Starts the rendering process. 
        Note that this will rebuild your compositor node tree!
    """

    def execute(self, context):

        cam = utils.get_objects(context)

        if cam is None:
            utils.show_message_box('Select all objects objects using the eyedroppers!',
                                   'Objects not found!', 'ERROR')
        else:
            utils.rotate_and_render(context)

        return {'FINISHED'}


class Reposition(Operator):
    bl_idname = 'render.reposition'
    bl_label = 'Reposition'
    """ 
        Repositions objects in the scene with random lighting.
    """

    def execute(self, context):

        cam = utils.get_objects(context)

        if cam is None:
            utils.show_message_box('Select all objects objects using the eyedroppers!',
                                   'Objects not found!', 'ERROR')
        else:
            utils.reposition(context)

        return {'FINISHED'}


class GetCurrentSettings(Operator):
    bl_idname = 'render.get_current_settings'
    bl_label = 'Get Current Settings'
    """ 
        Get the current settings of all eyedropped objects.
    """

    def execute(self, context):
        cam = utils.get_objects(context)

        if cam is None:
            utils.show_message_box('Select all objects objects using the eyedroppers!',
                                   'Objects not found!', 'ERROR')
        else:
            utils.get_current_settings(context)

        return {'FINISHED'}


class ZeroEverything(Operator):
    bl_idname = 'render.zero_everything'
    bl_label = 'Zero Everything'
    """ 
        Set everything to zero.
    """

    def execute(self, context):
        utils.zero_everything(context)
        return {'FINISHED'}


class ResetDefault(Operator):
    bl_idname = 'render.reset_default'
    bl_label = 'Reset Default'
    """ 
        Return to default values.
    """

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
        layout.row().label(text='')
        layout.operator('render.get_current_settings', text='Get Current Settings')
        layout.operator('render.reset_default', text='Reset Default Values')
        layout.operator('render.zero_everything', text='Zero Everything')
        layout.row().label(text='')
        layout.row().label(text='Depth map distance settings')
        row = layout.row(align=True)
        row.prop(cust_prop, 'depth_max_distance')


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

        layout.label(text="Rotation Minimum:")
        row = layout.row(align=True)
        row.prop(cust_prop, 'camera_min_rot_x')
        row.prop(cust_prop, 'camera_min_rot_y')
        row.prop(cust_prop, 'camera_min_rot_z')

        layout.label(text="Rotation Maximum:")
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

        layout.label(text="Position Minimum:")
        row = layout.row(align=True)
        row.prop(cust_prop, 'light_min_pos_x')
        row.prop(cust_prop, 'light_min_pos_y')
        row.prop(cust_prop, 'light_min_pos_z')

        layout.label(text="Position Maximum:")
        row = layout.row(align=True)
        row.prop(cust_prop, 'light_max_pos_x')
        row.prop(cust_prop, 'light_max_pos_y')
        row.prop(cust_prop, 'light_max_pos_z')

        layout.label(text="Rotation Minimum:")
        row = layout.row(align=True)
        row.prop(cust_prop, 'light_min_rot_x')
        row.prop(cust_prop, 'light_min_rot_y')
        row.prop(cust_prop, 'light_min_rot_z')

        layout.label(text="Rotation Maximum:")
        row = layout.row(align=True)
        row.prop(cust_prop, 'light_max_rot_x')
        row.prop(cust_prop, 'light_max_rot_y')
        row.prop(cust_prop, 'light_max_rot_z')


# Register classes
def register():
    register_class(CustomProperties)
    register_class(SDG)
    register_class(CameraPanel)
    register_class(LightPanel)
    register_class(Rendering)
    register_class(Reposition)
    register_class(ResetDefault)
    register_class(ZeroEverything)
    register_class(GetCurrentSettings)
    bpy.types.Scene.custom_properties = bpy.props.PointerProperty(type=CustomProperties)


# Unregister classes
def unregister():
    unregister_class(CustomProperties)
    unregister_class(GetCurrentSettings)
    unregister_class(ZeroEverything)
    unregister_class(ResetDefault)
    unregister_class(Reposition)
    unregister_class(Rendering)
    unregister_class(LightPanel)
    unregister_class(CameraPanel)
    unregister_class(SDG)

