import json
from itertools import combinations
from .installer import install_modules

try:
    import bpy
    import numpy as np
    from scipy.spatial import ConvexHull
    from . import utils
    from . import construct
except ImportError:
    install_modules()

    import bpy
    import numpy as np
    from scipy.spatial import ConvexHull
    from . import utils
    from . import construct

object_data_filepath = ''


def get_relative_rotation_matrix(rot_origin, rot_target):
    a = np.cos(rot_origin[0])
    b = np.sin(rot_origin[0])
    c = np.cos(rot_origin[1])
    d = np.sin(rot_origin[1])
    e = np.cos(rot_origin[2])
    f = np.sin(rot_origin[2])

    ad = a * d
    bd = b * d

    origin_matrix = [[c * e, -c * f, d],
                     [bd * e + a * f, -bd * f + a * e, -b * c],
                     [-ad * e + b * f, ad * f + b * e, a * c]]

    a = np.cos(rot_target[0])
    b = np.sin(rot_target[0])
    c = np.cos(rot_target[1])
    d = np.sin(rot_target[1])
    e = np.cos(rot_target[2])
    f = np.sin(rot_target[2])

    ad = a * d
    bd = b * d

    target_matrix = [[c * e, -c * f, d],
                     [bd * e + a * f, -bd * f + a * e, -b * c],
                     [-ad * e + b * f, ad * f + b * e, a * c]]

    origin_matrix = np.array(origin_matrix)
    target_matrix = np.array(target_matrix)
    rotation_matrix = origin_matrix @ target_matrix.transpose()
    return rotation_matrix


def bu_to_unit(value, scale):
    return value / scale


def unit_to_bu(value, scale):
    return value * scale


def get_scale(context):
    cust_props = context.scene.custom_properties

    if cust_props.depth_max_distance == 0:
        cust_props.depth_max_distance = 100.0

    value_range = cust_props.depth_max_distance

    if value_range < 0:
        value_range *= -1

    return bu_to_unit(value_range / 65536, utils.get_current_units()[1])


def calc_cam_k():
    scene = bpy.context.scene

    scale = scene.render.resolution_percentage / 100
    width = scene.render.resolution_x * scale  # px
    height = scene.render.resolution_y * scale  # px

    cam_data = scene.camera.data

    focal = cam_data.lens  # mm
    sensor_width = cam_data.sensor_width  # mm
    sensor_height = cam_data.sensor_height  # mm
    pixel_aspect_ratio = scene.render.pixel_aspect_x / scene.render.pixel_aspect_y

    if cam_data.sensor_fit == 'VERTICAL':
        # the sensor height is fixed (sensor fit is horizontal),
        # the sensor width is effectively changed with the pixel aspect ratio
        s_u = width / sensor_width / pixel_aspect_ratio
        s_v = height / sensor_height
    else:  # 'HORIZONTAL' and 'AUTO'
        # the sensor width is fixed (sensor fit is horizontal),
        # the sensor height is effectively changed with the pixel aspect ratio
        pixel_aspect_ratio = scene.render.pixel_aspect_x / scene.render.pixel_aspect_y
        s_u = width / sensor_width
        s_v = height * pixel_aspect_ratio / sensor_height

    # parameters of intrinsic calibration matrix K
    alpha_u = focal * s_u
    alpha_v = focal * s_v
    u_0 = width / 2
    v_0 = height / 2
    skew = 0  # only use rectangular pixels

    k = np.array([
        [alpha_u, skew, u_0],
        [0, alpha_v, v_0],
        [0, 0, 1]
    ], dtype=np.float32)

    return k


def calc_diameter_of_objects():
    objects = bpy.data.objects
    data = {}
    for obj in objects:
        if obj.name in construct.id_dict.values():
            verts = np.array([v.co for v in obj.data.vertices])
            hull = ConvexHull(points=verts)
            points = [hull.points[i] for i in hull.vertices]

            def calc_dist(p):
                return np.linalg.norm(np.subtract(p[0], p[1]))

            diameter = 0

            for pair in combinations(points, 2):
                dist = calc_dist(pair)
                if diameter < dist:
                    diameter = dist

            min_x = 0 - (obj.dimensions.x / 2)
            min_y = 0 - (obj.dimensions.y / 2)
            min_z = 0 - (obj.dimensions.z / 2)
            size_x = obj.dimensions.x
            size_y = obj.dimensions.y
            size_z = obj.dimensions.z

            data[f'{utils.get_key(obj.name)}'] = {
                "_comment": obj.name,
                "diameter": diameter,
                "min_x": min_x,
                "min_y": min_y,
                "min_z": min_z,
                "size_x": size_x,
                "size_y": size_y,
                "size_z": size_z
            }

    with open(object_data_filepath, 'w') as file:
        data_str = json.dumps(data, indent=4, sort_keys=True)
        file.write(data_str)
