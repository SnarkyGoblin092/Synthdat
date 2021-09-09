from os.path import splitext
import bpy
from bpy import props
from bpy.types import PropertyGroup
from . import construct
from . import calc
from .utils import show_message_box


class CustomProperties(PropertyGroup):

    def update_object_ids_filepath(self, context):
        extension = splitext(self.ids_filepath)[1]
        if extension != '.txt' and self.ids_filepath != '':
            self.ids_filepath = ''
            show_message_box('Only .txt files are allowed!', 'Warning!', 'ERROR')
        else:
            construct.object_ids_filepath = bpy.path.abspath(self.ids_filepath)

    def update_object_data_filepath(self, context):
        calc.object_data_filepath = f'{bpy.path.abspath(self.obj_data_filepath)}object_data.json'

    render_count: props.IntProperty(
        name='Number of renders',
        description='Specifies how many images Blender will render',
        default=1,
        min=1
    )

    return_to_original: props.BoolProperty(
        name='Return to original',
        description='Return objects to their original positions with their original rotations',
        default=False
    )

    depth_max_distance: props.FloatProperty(
        name='Max Distance',
        description='The depth map\'s maximum distance. If both min and max values are 0, min will be 0 and max will be 100',
        subtype='DISTANCE',
        default=100.0,
        min=0.0
    )

    ids_filepath: props.StringProperty(
        name='',
        description='The file containing object IDs',
        subtype='FILE_PATH',
        update=update_object_ids_filepath
    )

    obj_data_filepath: props.StringProperty(
        name='',
        description='The folder which the object data will be exported to',
        subtype='DIR_PATH',
        update=update_object_data_filepath
    )

    # Camera properties
    camera: props.PointerProperty(
        type=bpy.types.Camera,
        name='Camera',
        description='Select the camera'
    )

    camera_distance: props.FloatProperty(
        name='Distance from object',
        description='The Camera\'s distance from the object.\nIf set to 0, the camera won\'t change positions',
        default=10.0,
        subtype='DISTANCE',
        min=0.0
    )

    camera_min_rot_x: props.FloatProperty(
        name='X',
        description='The amount the camera can rotate on it\'s local X axis in the negative direction.\n'
                    'Set it to -90° to point the camera down, or 90° to point it up',
        default=-0.3490658504,
        subtype='ANGLE',
        min=-90,
        max=90
    )

    camera_min_rot_y: props.FloatProperty(
        name='Y',
        description='The amount the camera can rotate on it\'s local Y axis in the negative direction',
        default=0.0,
        subtype='ANGLE',
        min=-360.0,
        max=360.0
    )

    camera_min_rot_z: props.FloatProperty(
        name='Z',
        description='The amount the camera can rotate on it\'s local Z axis in the negative direction',
        default=0.0,
        subtype='ANGLE',
        min=-360.0,
        max=360.0
    )

    camera_max_rot_x: props.FloatProperty(
        name='X',
        description='The amount the camera can rotate on it\'s local X axis in the positive direction.\n'
                    'Set it to 90° to point the camera up, or -90° to point it down',
        default=-1.4835298642,
        subtype='ANGLE',
        min=-90.0,
        max=90.0
    )

    camera_max_rot_y: props.FloatProperty(
        name='Y',
        description='The amount the camera can rotate on it\'s local Y axis in the positive direction',
        default=6.2831853072,
        subtype='ANGLE',
        min=-360.0,
        max=360.0
    )

    camera_max_rot_z: props.FloatProperty(
        name='Z',
        description='The amount the camera can rotate on it\'s local Z axis in the positive direction',
        default=0.0,
        subtype='ANGLE',
        min=-360.0,
        max=360.0
    )

    # Light properties

    point_lights: props.BoolProperty(
        name='Point Lights',
        description='Generate point lights',
        default=False
    )

    sun_lights: props.BoolProperty(
        name='Sun Lights',
        description='Generate sun lights',
        default=False
    )

    lights_count: props.IntProperty(
        name='Lights Count',
        description='Number of lights to be generated',
        default=1,
        min=1
    )

    light_min_intensity: props.FloatProperty(
        name='Min',
        description='Light\'s minimum intensity.\n'
                    'If both min and max are set to 0, the current intensity will be used',
        default=1.0
    )

    light_max_intensity: props.FloatProperty(
        name='Max',
        description='Light\'s maximum intensity.\n'
                    'If both min and max are set to 0, the current intensity will be used',
        default=2.0
    )

    light_min_rot_x: props.FloatProperty(
        name='X',
        description='The amount the light can rotate on it\'s local X axis in the negative direction',
        default=-1.308996939,
        subtype='ANGLE',
        min=-90.0,
        max=90.0
    )

    light_min_rot_y: props.FloatProperty(
        name='Y',
        description='The amount the light can rotate on it\'s local Y axis in the negative direction',
        default=-1.308996939,
        subtype='ANGLE',
        min=-90.0,
        max=90.0
    )

    light_min_rot_z: props.FloatProperty(
        name='Z',
        description='The amount the light can rotate on it\'s local Z axis in the negative direction',
        default=0.0,
        subtype='ANGLE',
        min=-360.0,
        max=360.0
    )

    light_max_rot_x: props.FloatProperty(
        name='X',
        description='The amount the light can rotate on it\'s local X axis in the positive direction',
        default=1.308996939,
        subtype='ANGLE',
        min=-90.0,
        max=90.0
    )

    light_max_rot_y: props.FloatProperty(
        name='Y',
        description='The amount the light can rotate on it\'s local Y axis in the positive direction',
        default=1.308996939,
        subtype='ANGLE',
        min=-90.0,
        max=90.0
    )

    light_max_rot_z: props.FloatProperty(
        name='Z',
        description='The amount the light can rotate on it\'s local Z axis in the positive direction',
        default=0.0,
        subtype='ANGLE',
        min=-360.0,
        max=360.0
    )

    light_min_pos_x: props.FloatProperty(
        name='X',
        description='The amount the light can move on the X axis in the negative direction',
        default=-5.0,
        subtype='DISTANCE'
    )

    light_min_pos_y: props.FloatProperty(
        name='Y',
        description='The amount the light can move on the Y axis in the negative direction',
        default=-5,
        subtype='DISTANCE'
    )

    light_min_pos_z: props.FloatProperty(
        name='Z',
        description='The amount the light can move on the Z axis in the negative direction',
        default=5.0,
        subtype='DISTANCE',
    )

    light_max_pos_x: props.FloatProperty(
        name='X',
        description='The amount the light can move on the X axis in the positive direction',
        default=5.0,
        subtype='DISTANCE'
    )

    light_max_pos_y: props.FloatProperty(
        name='Y',
        description='The amount the light can move on the Y axis in the positive direction',
        default=5.0,
        subtype='DISTANCE'
    )

    light_max_pos_z: props.FloatProperty(
        name='Z',
        description='The amount the light can move on the Z axis in the positive direction',
        default=5.0,
        subtype='DISTANCE',
    )
