import os
import math
import mathutils as mu
from datetime import datetime
from .installer import install_modules

try:
    import bpy
    import numpy as np
    import random
    from . import construct
    from . import calc
except ImportError:
    install_modules()

    import bpy
    import numpy as np
    import random
    from . import construct
    from . import calc

cam = None

cam_rot_x = 0.0
cam_rot_y = 0.0
cam_rot_z = 0.0
cam_dist = 0.0

light_pos_x = 0.0
light_pos_y = 0.0
light_pos_z = 0.0

light_rot_x = 0.0
light_rot_y = 0.0
light_rot_z = 0.0

light_intensity = 0.0

light_radius = 0.0

output_path = ''
scale = 0


def get_key(val):
    for key, value in construct.id_dict.items():
        if val == value:
            return key

    return 'key doesn\'t exist'


def get_current_units():
    length_unit = bpy.context.scene.unit_settings.length_unit

    if length_unit == 'KILOMETERS':
        return 'km', 1000
    elif length_unit == 'METERS':
        return 'm', 1
    elif length_unit == 'CENTIMETERS':
        return 'cm', 1/100
    elif length_unit == 'MILLIMETERS':
        return 'mm', 1/1000
    elif length_unit == 'MICROMETERS':
        return 'mcm', 1/1000000
    elif length_unit == 'MILES':
        return 'mi', 1760
    elif length_unit == 'FEET':
        return 'ft', 1/3
    elif length_unit == 'INCHES':
        return 'in', 1/36
    elif length_unit == 'THOU':
        return 'thou', 1/36000
    else:
        return 'bu', 1


def save_current_objects_in_scene():
    target_file = os.path.expanduser('~/Desktop/saved_objs.blend')
    bpy.ops.wm.save_as_mainfile(filepath=target_file)


def reset_saved_objects():
    target_file = os.path.expanduser('~/Desktop/saved_objs.blend')
    bpy.ops.wm.open_mainfile(filepath=target_file)

    os.remove(target_file)


# Get the eyedropped objects
def get_objects(context):
    cust_props = context.scene.custom_properties

    global cam

    if cust_props.camera is not None:
        cam = bpy.data.objects.get(cust_props.camera.name)

    if cam is None:
        return None
    else:
        return cam


# Get every setting from objects
def get_current_settings(context):
    cust_props = context.scene.custom_properties

    cust_props.camera_distance = np.linalg.norm(np.array(cam.location)-np.array([0, 0, 0]))

    cust_props.camera_min_rot_x = cam.rotation_euler[0]
    cust_props.camera_min_rot_y = cam.rotation_euler[1]
    cust_props.camera_min_rot_z = cam.rotation_euler[2]
    cust_props.camera_max_rot_x = cam.rotation_euler[0]
    cust_props.camera_max_rot_y = cam.rotation_euler[1]
    cust_props.camera_max_rot_z = cam.rotation_euler[2]


# Set every value in the addon to 0
def zero_everything(context):
    cust_props = context.scene.custom_properties

    global cam
    cam = None

    cust_props.render_count = 1
    cust_props.return_to_original = False

    cust_props.depth_max_distance = 0

    cust_props.ids_filepath = ''
    cust_props.obj_data_filepath = ''

    cust_props.camera = None
    cust_props.camera_distance = 0.0

    cust_props.camera_min_rot_x = 0.0
    cust_props.camera_min_rot_y = 0.0
    cust_props.camera_min_rot_z = 0.0
    cust_props.camera_max_rot_x = 0.0
    cust_props.camera_max_rot_y = 0.0
    cust_props.camera_max_rot_z = 0.0

    cust_props.point_lights = False
    cust_props.sun_lights = False
    cust_props.lights_count = 0

    cust_props.light_min_intensity = 0.0
    cust_props.light_max_intensity = 0.0

    cust_props.light_min_rot_x = 0.0
    cust_props.light_min_rot_y = 0.0
    cust_props.light_min_rot_z = 0.0
    cust_props.light_max_rot_x = 0.0
    cust_props.light_max_rot_y = 0.0
    cust_props.light_max_rot_z = 0.0

    cust_props.light_min_pos_x = 0.0
    cust_props.light_min_pos_y = 0.0
    cust_props.light_min_pos_z = 0.0
    cust_props.light_max_pos_x = 0.0
    cust_props.light_max_pos_y = 0.0
    cust_props.light_max_pos_z = 0.0


# Return to default values
def reset_default(context):
    cust_props = context.scene.custom_properties

    global cam
    cam = None

    cust_props.render_count = 1
    cust_props.return_to_original = False

    cust_props.depth_max_distance = 100.0

    cust_props.ids_filepath = ''
    cust_props.obj_data_filepath = ''

    cust_props.camera = None
    cust_props.camera_distance = 10.0

    cust_props.camera_min_rot_x = -0.3490658504
    cust_props.camera_min_rot_y = 0.0
    cust_props.camera_min_rot_z = 0.0
    cust_props.camera_max_rot_x = -1.4835298642
    cust_props.camera_max_rot_y = 6.2831853072
    cust_props.camera_max_rot_z = 0.0

    cust_props.point_lights = False
    cust_props.sun_lights = False
    cust_props.lights_count = 1

    cust_props.light_min_intensity = 1.0
    cust_props.light_max_intensity = 2.0

    cust_props.light_min_rot_x = -1.308996939
    cust_props.light_min_rot_y = -1.308996939
    cust_props.light_min_rot_z = 0.0
    cust_props.light_max_rot_x = 1.308996939
    cust_props.light_max_rot_y = 1.308996939
    cust_props.light_max_rot_z = 0.0

    cust_props.light_min_pos_x = -5.0
    cust_props.light_min_pos_y = -5.0
    cust_props.light_min_pos_z = 5.0
    cust_props.light_max_pos_x = 5.0
    cust_props.light_max_pos_y = 5.0
    cust_props.light_max_pos_z = 5.0


# Set settings to the set amounts or the object's original setting
def set_variables(cust_props):

    global cam_dist
    cam_dist = cust_props.camera_distance

    global cam_rot_x
    if cust_props.camera_min_rot_x == 0.0 and cust_props.camera_max_rot_x == 0.0:
        if cam_dist == 0.0:
            cam_rot_x = cam.rotation_euler[0]
        else:
            cam_rot_x = 0.0
    else:
        cam_rot_x = random.uniform(cust_props.camera_min_rot_x, cust_props.camera_max_rot_x)

    global cam_rot_y
    if cust_props.camera_min_rot_y == 0.0 and cust_props.camera_max_rot_y == 0.0:
        if cam_dist == 0.0:
            cam_rot_y = cam.rotation_euler[1]
        else:
            cam_rot_y = 0.0
    else:
        cam_rot_y = random.uniform(cust_props.camera_min_rot_y, cust_props.camera_max_rot_y)

    global cam_rot_z
    if cust_props.camera_min_rot_z == 0.0 and cust_props.camera_max_rot_z == 0.0:
        if cam_dist == 0.0:
            cam_rot_z = cam.rotation_euler[2]
        else:
            cam_rot_z = 0.0
    else:
        cam_rot_z = random.uniform(cust_props.camera_min_rot_z, cust_props.camera_max_rot_z)

    global light_pos_x
    if cust_props.light_min_pos_x == 0.0 and cust_props.light_max_pos_x == 0.0:
        light_pos_x = 0
    else:
        light_pos_x = random.uniform(cust_props.light_min_pos_x, cust_props.light_max_pos_x)

    global light_pos_y
    if cust_props.light_min_pos_y == 0.0 and cust_props.light_max_pos_y == 0.0:
        light_pos_y = 0
    else:
        light_pos_y = random.uniform(cust_props.light_min_pos_y, cust_props.light_max_pos_y)

    global light_pos_z
    if cust_props.light_min_pos_z == 0.0 and cust_props.light_max_pos_z == 0.0:
        light_pos_z = 10
    else:
        light_pos_z = random.uniform(cust_props.light_min_pos_z, cust_props.light_max_pos_z)

    global light_rot_x
    if cust_props.light_min_rot_x == 0.0 and cust_props.light_max_rot_x == 0.0:
        light_rot_x = 0
    else:
        light_rot_x = random.uniform(cust_props.light_min_rot_x, cust_props.light_max_rot_x)

    global light_rot_y
    if cust_props.light_min_rot_y == 0.0 and cust_props.light_max_rot_y == 0.0:
        light_rot_y = 0
    else:
        light_rot_y = random.uniform(cust_props.light_min_rot_y, cust_props.light_max_rot_y)

    global light_rot_z
    if cust_props.light_min_rot_z == 0.0 and cust_props.light_max_rot_z == 0.0:
        light_rot_z = 0
    else:
        light_rot_z = random.uniform(cust_props.light_min_rot_z, cust_props.light_max_rot_z)


# Show a message box
def show_message_box(message='', title='Message Box', icon='NONE'):
    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)


def save_positions():
    cam_pos = cam.location.copy()

    for i in range(0, len(bpy.data.objects)):
        print(f'{i}. object relative camera pos: {cam_pos - bpy.data.objects[i].location}')


# Handles the placement of all objects in the scene and renders images
def rotate_and_render(context):
    cust_props = context.scene.custom_properties

    construct.construct_id_dictionary()

    global scale
    scale = calc.get_scale(context)

    for obj in bpy.data.objects:
        obj.pass_index = 0

    if cust_props.return_to_original:
        save_current_objects_in_scene()

    now = datetime.datetime.now()
    dt_string = now.strftime('%d-%m-%Y_%H-%M-%S')
    global output_path
    output_path = os.path.expanduser(f'~/Desktop/Renders/{dt_string}/')

    for scene in bpy.data.scenes:
        scene.render.engine = 'CYCLES'

    bpy.context.scene.frame_set(1)

    construct.construct_object_layers()
    construct.construct_node_tree()

    os.mkdir(output_path)

    with open(output_path + 'camera_gt.json', 'a') as camera_gt:
        with open(output_path + 'scene_camera.json', 'a') as scene_camera:
            camera_gt.write('{\n')
            scene_camera.write('{\n')

            for i in range(cust_props.render_count):

                set_variables(cust_props)
                construct.construct_lights()

                if cam_dist != 0.0:
                    cam.location = mu.Vector((0, 0, 0))
                    cam.rotation_euler = [math.radians(90) + cam_rot_x, cam_rot_z, cam_rot_y]

                    bpy.ops.object.select_all(action='DESELECT')
                    cam.select_set(True)
                    bpy.ops.transform.translate(value=[0, 0, cam_dist], orient_type='LOCAL')

                context.scene.render.filepath = output_path + f'rgb/{str(i + 1).zfill(6)}{bpy.context.scene.render.file_extension}'

                print(f'Rendering Set {i+1}...')
                bpy.ops.render.render(write_still=True)

                for o in bpy.data.objects:
                    if o.type == 'MESH':
                        if o.name in construct.id_dict.values():
                            os.rename(output_path + f'mask/{o.name}0001.png',
                                      output_path + f'mask/{str(i).zfill(6)}_{str(get_key(o.name)).zfill(6)}.png')
                            os.rename(output_path + f'mask_visib/{o.name}0001.png',
                                      output_path + f'mask_visib/{str(i).zfill(6)}_{str(get_key(o.name)).zfill(6)}.png')

                os.rename(output_path + 'depth/Image0001.png',
                          output_path + f'depth/{str(i+1).zfill(6)}.png')

                last = (i == cust_props.render_count - 1)
                construct.construct_scene_gt_json(last, camera_gt, i, bpy.data.objects, cam)
                construct.construct_scene_camera_json(last, scene_camera, i, cam)

            camera_gt.write('}')
            scene_camera.write('}')

    if cust_props.return_to_original:
        reset_saved_objects()


def reposition(context):
    cust_props = context.scene.custom_properties

    if cust_props.return_to_original:
        save_current_objects_in_scene()

    for i in range(cust_props.render_count):
        set_variables(cust_props)
        construct.construct_lights()

        if cam_dist != 0.0:
            cam.location = mu.Vector((0, 0, 0))
            cam.rotation_euler = [math.radians(90) + cam_rot_x, cam_rot_z, cam_rot_y]

            bpy.ops.object.select_all(action='DESELECT')
            cam.select_set(True)
            bpy.ops.transform.translate(value=[0, 0, cam_dist], orient_type='LOCAL')

    if cust_props.return_to_original:
        reset_saved_objects()
