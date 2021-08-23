import bpy
import json
import numpy as np


class NumpyArrayEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NumpyArrayEncoder, self).default(obj)


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


def add_to_scene_json(last, file, it, objects, camera):
    data = {}
    data["{}".format(it)] = []
    i = 0
    for obj in objects:
        if obj.type == 'MESH' and obj.name[0] != '_':
            rot_matrix = get_relative_rotation_matrix(obj.rotation_euler, camera.rotation_euler)
            rot_matrix = np.ravel(rot_matrix)
            loc_diff = np.array(obj.location - camera.location)

            data["{}".format(it)].append({
                "cam_R_m2c": rot_matrix,
                "cam_t_m2c": loc_diff,
                "obj_id": i
            })
            i += 1
    data_str = json.dumps(data, cls=NumpyArrayEncoder)[1:-1]
    if not last:
        data_str += ','
    file.write("{}\n".format(data_str))
