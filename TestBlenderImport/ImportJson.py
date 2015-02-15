'''
Created on 03 февр. 2015 г.

@author: Mihail
'''

"""
Blender importer for Three.js (ASCII JSON format).
"""

import os
import time
import json
import bpy
import mathutils
import math
from mathutils import Matrix, Vector
from mathutils.geometry import tessellate_polygon
from bpy_extras.image_utils import load_image
from bpy_extras.io_utils import unpack_list, unpack_face_list

from urllib import request
# #####################################################
# Generators
# #####################################################

def load_remote_image(url):
    # Load image file from url.    
    try:
        #make a temp filename that is valid on your machine
        path_base ="C:/test/tmp/"
        tmp_filename = path_base + url.split('/')[-1]
        #fetch the image in this file
        request.urlretrieve(url, tmp_filename)
        #create a blender datablock of it
        img = bpy.data.images.load(tmp_filename)
        #pack the image in the blender file so...
        img.pack()
        #...we can delete the temp image
        #os.remove(tmp_filename)
    except Exception as e:
        raise NameError("Cannot load image: {0}".format(e))
    return img
    
def setColor(c, cInHex):
    rgbArr = hexToTuple(cInHex)
    c.r = rgbArr[0]
    c.g = rgbArr[1]
    c.b = rgbArr[2]

def create_texture(textureName, data, isLocalImage = True):
    name = textureName
    texture = bpy.data.textures.new(name, type='IMAGE')

    textures_data = data.get("textures", [])
    
    if not textures_data:
        raise  ValueError('textures_data not found')
    
    for t in enumerate(textures_data):
        if t[1].get("name") == textureName:
            texture_data = t[1]
            break
        
    if not texture_data:
        raise NameError("Cannot load texture data %s" % textureName)
    
    imageRealPathOrUrl = texture_data.get("url", "")
    image = load_image (imageRealPathOrUrl) if isLocalImage else load_remote_image(imageRealPathOrUrl)

    if not image:
        raise NameError("Cannot load image %s" % imageRealPathOrUrl)
    
    texture.image = image
    texture.use_mirror_y = texture_data.get("mirrorY")
    texture.use_mirror_x = texture_data.get("mirrorX")

    return texture

def create_materials(data):
    materials = []
    materials_data = data.get("materials", [])

    for i, m in enumerate(materials_data):

        name = m.get("DbgName", "material_%d" % i)
        
        diffuseColor = m.get("diffuseColor", None)    # ok
        diffuseMap = m.get("diffuseMap", None)        # ok 
        ambientColor = m.get("ambientColor", None)    # ok        
        specularColor = m.get("specularColor", None)  # ok 
        specularMap = m.get("specularMap", None)  #TODO ???
        shininess = m.get("shininess", 0.0)       # TODO probably is specular_intensity
        alpha = m.get("transparency", 1.0)        # ok 
        #TODO????? 
        reflectivity = m.get("reflectivity", 0)   # TODO
        bumpMap = m.get("bumpMap", None)          # TODO
        bumpScale = m.get("bumpScale", 1)        
        emissive = m.get("emissive", 0) # TODO not sure  
        
        """TODO what is it?"""  
        specular_hardness = 0  

        material = bpy.data.materials.new(name)

        material.use_vertex_color_light = False
        if diffuseColor:
            setColor(material.diffuse_color, diffuseColor)
        
        """I am not sure of the this """
#         if reflectivity < 1.0:
#             material.diffuse_intensity = reflectivity 

        if specularColor:
            setColor(material.specular_color, specularColor)
            
        """I am not sure of the this """
        if shininess >= 0 and shininess <= 100:            
            material.specular_intensity = shininess / 100.0
            
        if ambientColor < 1.0:
            material.ambient = ambientColor

        if alpha < 1.0:
            material.alpha = alpha
            material.use_transparency = True

        if specular_hardness:
            material.specular_hardness = specular_hardness

        if diffuseMap:
            texture = create_texture(diffuseMap, data, False)
            mtex = material.texture_slots.add()
            mtex.texture = texture
            mtex.texture_coords = 'UV'
            mtex.use = True
            mtex.use_map_color_diffuse = True

            material.active_texture = texture
        
        """I am not sure of the this """
        if emissive < 1.0:
            material.emit = emissive
          
        materials.append(material)

    return materials

def update_mesh_object(mesh):
        print("TEST before update me.tessfaces len", len(mesh.tessfaces))
        #mesh.update(calc_tessface = True)
        #mesh.update(calc_edges= True)
        mesh.update(calc_edges= False, calc_tessface = False)
        print("TEST me.tessfaces len", len(mesh.tessfaces))
        
def create_mesh_object(name, vertices, materials, face_data, flipYZ, recalculate_normals, matrix, parrent):

    faces         = face_data["faces"]
    vertexNormals = face_data["vertexNormals"]
    vertexColors  = face_data["vertexColors"] # not used
    vertexUVs     = face_data["vertexUVs"]
    faceMaterials = face_data["materials"]
    faceColors    = face_data["faceColors"] # not used

    # Create a new mesh
    me = bpy.data.meshes.new(name)
    
    if not parrent:
        ob = bpy.data.objects.new(name, None)
    else :
        ob = bpy.data.objects.new(name, me)
        ob.data = me  
    
    ob.matrix_world = matrix
    scene = bpy.context.scene                   # get the current scene
    scene.objects.link(ob)
    #scene.update()    
    
    if parrent:
        ob.parent = parrent
        #bpy.context.scene.objects.active = parrent    
        #ob.select = True # select  object
        #ob.select = True
        #bpy.ops.object.parent_set( type = 'OBJECT', xmirror = False, keep_transform = True )
    
    me.vertices.add(len(vertices))
    me.tessfaces.add(len(faces))
    # verts_loc is a list of (x, y, z) tuples
    me.vertices.foreach_set("co", unpack_list(vertices))
    me.tessfaces.foreach_set("vertices_raw", unpack_face_list([f for f in faces]))

    # Handle normals
    if not recalculate_normals:
        update_mesh_object(me)

    if face_data["hasVertexNormals"]:     
        print("setting vertex normals")

        for fi in range(len(faces)):
            #print("setting face %i with %i vertices" % (fi, len(normals[fi])))
            me.tessfaces[fi].use_smooth = True
            if vertexNormals[fi]:
                if not recalculate_normals:
                    for j in range(len(vertexNormals[fi])):
                        vertexNormal = vertexNormals[fi][j]
                        x = vertexNormal[0]
                        y = vertexNormal[1]
                        z = vertexNormal[2]
                        vi = me.tessfaces[fi].vertices[j]
                        me.vertices[vi].normal.x = x
                        me.vertices[vi].normal.y = y
                        me.vertices[vi].normal.z = z                

    # Handle colors TODO:we have colors?

    if face_data["hasVertexColors"]:

        print("setting vertex colors")

        me.vertex_colors.new("vertex_color_layer_0")

        for fi in range(len(faces)):

            if vertexColors[fi]:

                face_colors = me.vertex_colors[0].data[fi]
                face_colors = face_colors.color1, face_colors.color2, face_colors.color3, face_colors.color4

                for vi in range(len(vertexColors[fi])):

                    r = vertexColors[fi][vi][0]
                    g = vertexColors[fi][vi][1]
                    b = vertexColors[fi][vi][2]

                    face_colors[vi].r = r
                    face_colors[vi].g = g
                    face_colors[vi].b = b

    elif face_data["hasFaceColors"]:

        print("setting vertex colors from face colors")

        me.vertex_colors.new("vertex_color_layer_0")

        for fi in range(len(faces)):

            if faceColors[fi]:

                r = faceColors[fi][0]
                g = faceColors[fi][1]
                b = faceColors[fi][2]

                face_colors = me.vertex_colors[0].data[fi]
                face_colors = face_colors.color1, face_colors.color2, face_colors.color3, face_colors.color4

                for vi in range(len(faces[fi])):

                    face_colors[vi].r = r
                    face_colors[vi].g = g
                    face_colors[vi].b = b

    # Handle uvs

    if face_data["hasVertexUVs"]:

        print("setting vertex uvs")

        for fi in range(len(faces)):

            me.tessface_uv_textures.new()
            uv_tess_tex = me.tessface_uv_textures[0]
            if vertexUVs[fi]:

                uv_face = uv_tess_tex.data[fi] # we have only one layer
                face_uvs = uv_face.uv1, uv_face.uv2, uv_face.uv3, uv_face.uv4

                for vi in range(len(vertexUVs[fi])):

                    u = vertexUVs[fi][vi][0]
                    v = vertexUVs[fi][vi][1]

                    face_uvs[vi].x = u
                    face_uvs[vi].y = v

                active_texture = materials[faceMaterials[fi]].active_texture

                if active_texture:
                    active_texture.use_alpha = True
    # Handle materials # 1

    if face_data["hasMaterials"]:
        print("setting materials (mesh)")

        for m in materials:
            me.materials.append(m)

        print("setting materials (faces)")

        for fi in range(len(faces)):
            if faceMaterials[fi] >= 0:
                print("TEST MATERIALS index %r" % (faceMaterials[fi]))                
                me.tessfaces[fi].material_index = faceMaterials[fi]
                
    # Create a new object
    
    if recalculate_normals:
        update_mesh_object(me)
    
    return  ob

# #####################################################
# Faces
# #####################################################

def empty_facedata():
    return  {
    "faces"         : [],
    "materials"     : [],
    "faceUVs"       : [],
    "vertexUVs"     : [],
    "faceNormals"   : [],
    "vertexNormals" : [],
    "faceColors"    : [],
    "vertexColors"  : [],

    "hasVertexNormals"  : False,
    "hasVertexUVs"      : False,
    "hasVertexColors"   : False,
    "hasFaceColors"     : False,
    "hasMaterials"      : False
    }
    
def extract_faces(data, material_index):
    result = empty_facedata()
    faces = data.get("faces", [])
    normals = data.get("normals", [])
    uvs = data.get("uvs", [])         

    offset = 0
    zLength = len(faces)

    hasMaterial         = material_index != -1
    hasFaceUv           = False
    hasFaceVertexUv     = True if uvs else False 
    hasFaceVertexNormal = True if normals else False
    hasFaceColor        = False
    hasFaceVertexColor  = False

    print("Data: hasMaterial:", hasMaterial, "hasFaceUv:", hasFaceUv,"hasFaceVertexUv:", hasFaceVertexUv, "hasFaceVertexNormal", hasFaceVertexNormal, "hasFaceVertexColor:", hasFaceVertexColor)

    result["hasVertexUVs"] = result["hasVertexUVs"] or hasFaceVertexUv
    result["hasVertexNormals"] = result["hasVertexNormals"] or hasFaceVertexNormal
    result["hasVertexColors"] = result["hasVertexColors"] or hasFaceVertexColor
    result["hasFaceColors"] = result["hasFaceColors"] or hasFaceColor
    result["hasMaterials"] = result["hasMaterials"] or hasMaterial    

    while ( offset < zLength ):
        """ 
        vertices
        faces format [Ai Bi Ci ...] if no normals
                     [Ai nAi Bi nBi Ci nCi ...]
        """
        faceNormals = []
        face = []
        
        offsetIncrement = 3;
        indexFactor = 1
        
        if hasFaceVertexNormal:
            offsetIncrement = 6
            indexFactor = 2

        a = faces[ offset ]            
        b = faces[ offset + indexFactor ] 
        c = faces[ offset + indexFactor * 2 ]
        face = [a, b, c]
        
        if hasFaceVertexNormal:
            an = faces[ offset  + 1 ]            
            bn = faces[ offset + indexFactor + 1 ] 
            cn = faces[ offset + indexFactor * 2 + 1 ]
            faceNormals = [an, bn, cn]                    

        nVertices = 3
        offset += offsetIncrement
        result["faces"].append(face)

        #normals
        if hasFaceVertexNormal:

            vertexNormals = []

            for j in range(nVertices):

                normalIndex = faceNormals[ j ] * 3

                x = normals[ normalIndex ]
                y = normals[ normalIndex + 1 ]
                z = normals[ normalIndex + 2 ]

                vertexNormals.append( [x, y, z] )
        else:
            vertexNormals = None
        print("TESt vertex Normals: ", vertexNormals)
        result["vertexNormals"].append(vertexNormals)

        # uvs
        if hasFaceVertexUv:
            vertexUvs = []

            for j in range(nVertices): # nVertices is alvays 3 in our case

                uvIndex = face[ j ] * 2

                u = uvs[ uvIndex ]
                v = uvs[ uvIndex + 1 ]

                vertexUvs.append([u, v])

            result["vertexUVs"].append(vertexUvs)
            
        # material
        if hasMaterial:

            materialIndex = material_index

        else:
            materialIndex = -1

        result["materials"].append(materialIndex)
    
    return result

# #####################################################
# Camera
# #####################################################
"""
    "camera":
    {
        "fov": "58",
        "aspectRatio": 1.8975225225225225,
        "near": 1,
        "far": 100000,
        "matrix":
        [
            0.8744340538978577,
            -0.06514564156532288,
            0.48075059056282043,
            1575.3531494140625,
            -3.0619268232001673e-10,
            0.9909433126449585,
            0.13428093492984772,
            899.5685424804688,
            -0.48514437675476074,
            -0.11741982400417328,
            0.8665145635604858,
            3857.8896484375,
            0,
            0,
            0,
            1
        ]
    }
"""

def add_camera(camera_data, parent):
    nearClipDistance = camera_data.get("near",0)  
    farClipDistance  = camera_data.get("far",0)
    aspectRatio = camera_data.get("aspectRatio",0)
    fieldOfViewInDegrees = camera_data.get("fov", 0)
    matrix_data = camera_data.get("matrix", [])

    cam = bpy.data.cameras.new("Camera")
    
    cam.type = 'PERSP'
    cam.lens_unit = 'FOV'
    cam.lens = fieldOfViewInDegrees
    cam.clip_start = nearClipDistance
    cam.clip_end = farClipDistance
    cam["Ratio"] = aspectRatio
     
    
    cam_ob = bpy.data.objects.new("Camera", cam)
    cam_ob.data = cam    
    cam_ob.matrix_world = arrayToMatrix(matrix_data)
    if parent:
        cam_ob.parent = parent
    
    bpy.context.scene.objects.link(cam_ob)
    
# #####################################################
# Utils
# #####################################################

def hexToTuple( hexColor ):
    r = (( hexColor >> 16 ) & 0xff) / 255.0
    g = (( hexColor >> 8 ) & 0xff) / 255.0
    b = ( hexColor & 0xff) / 255.0
    return (r, g, b)

def isBitSet(value, position):
    return value & ( 1 << position )

def splitArray(data, chunkSize):
    result = []
    chunk = []
    for i in range(len(data)):
        if i > 0 and i % chunkSize == 0:
            result.append(chunk)
            chunk = []
        chunk.append(data[i])
    result.append(chunk)
    return result

def arrayToMatrix(arrMatrix):
    matrix1 = [[arrMatrix[0], arrMatrix[1], arrMatrix[2],  arrMatrix[3]],
            [arrMatrix[4], arrMatrix[5], arrMatrix[6],  arrMatrix[7]],
            [arrMatrix[8], arrMatrix[9], arrMatrix[10], arrMatrix[11]],
            [arrMatrix[12], arrMatrix[13], arrMatrix[14], arrMatrix[15]]]
    matrix = Matrix(matrix1)
    return matrix

def extract_json_string(text):
    marker_begin = "scene:"

    start = text.find(marker_begin) + len(marker_begin)
    end = text.rfind("}", start)
    return text[start:end+1].strip()

def get_name(filepath):
    return os.path.splitext(os.path.basename(filepath))[0]

def get_path(filepath):
    return os.path.dirname(filepath)

# #####################################################
# Parser
# #####################################################
"""
Default Settings
"""
def setting_target_rotation():
    return [-90, 0, 0]

def setting_target_scale():
    return [0.01, 0.01, 00.01]

def apply_default_transform(bpy_ob):
    target_rotation = setting_target_rotation()
    
    t_rot = (math.radians(target_rotation[0]*-1),
    math.radians(target_rotation[1]*-1), 
    math.radians(target_rotation[2]*-1))

    bpy_ob.rotation_mode = 'XYZ'
    bpy_ob.rotation_euler = (t_rot)
    
    bpy_ob.scale = setting_target_scale()
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False) #apply rotation
    
"""
=========================================================
"""
  
"""
"name": "object_0",
"material": "worktop",
"geometry": "worktop_geometry_2",
matrix
"""
def load_data(data,  option_flip_yz, recalculate_normals, option_worker):
    print("\n\tloading data...")
    
    #TODO: add null checks        
    geometries = data.get("geometries")
    root_data = data.get("root")
    nodes = root_data.get("nodes")
    materials_data = data.get("materials", [])
    camera_data = data.get("camera")
   
    #create root
    rawmatrix = root_data.get("matrix", [])
    root_matrix = arrayToMatrix(rawmatrix)
    empty_root_faces = empty_facedata()
    root_me = create_mesh_object('root', [], [], empty_root_faces, option_flip_yz, False, root_matrix, None)
    apply_default_transform(root_me)
    
    # Add camera
    add_camera(camera_data, root_me)
    # Create materials
    print("\n\tloading materials...")
    materials = create_materials(data)

    # Create nodes
    print("\n\tloading nodes...")
    for i in enumerate(nodes):
        print("\n\tloading node: ", i[1])
        nd_name = i[1].get("name", "")
        nd_geometryName = i[1].get("geometry", "")
        
        rawmatrix =i[1].get("matrix", [])
        if len(rawmatrix) > 16:
            raise ValueError("Matrix shold be 4x4")
       
        nd_matrix = arrayToMatrix(rawmatrix)        
        
        for g_i in enumerate(geometries):
            if g_i[1].get("name","") == nd_geometryName:
                nd_data = g_i[1]
                break
        
        nd_materialname = nd_data.get("material", "")
        
        material_index = -1;
        for m_i in enumerate(materials_data):
            if m_i[1].get("name","") == nd_materialname:
                material_index = m_i[0]
                break
                        
        print("Build node... \nInfo: name %r geometry %r material name %r material index %r matrix %r\n\n" % (nd_name, nd_geometryName, nd_materialname, material_index, nd_matrix))
        #TODO: check data
        # flip YZ
        vertices = splitArray(nd_data["positions"], 3)
    
        if option_flip_yz:
            vertices[:] = [(v[0], -v[2], v[1]) for v in vertices]
    
        # extract faces
    
        face_data = extract_faces(nd_data, material_index)
    
        # deselect all
    
        bpy.ops.object.select_all(action='DESELECT')
    
        nfaces = len(face_data["faces"])
        nvertices = len(vertices)
        nnormals = len(face_data.get("vertexNormals", []))
        ncolors = -1 #TODO: doe we need it len(data.get("colors", [])) / 3
        nuvs = len(face_data.get("vertexUVs", []))
        nmaterials = len(data.get("materials", []))
    
        print('\tbuilding geometry for node %r...\n\tfaces:%r, vertices:%r, vertex normals: %r, vertex uvs: %r, vertex colors: %r, materials: %r ...' % (
            nd_name, nfaces, nvertices, nnormals, nuvs, ncolors, nmaterials ))
        print("faces ",face_data["faces"])
    
        # Create new obj
        ob = create_mesh_object(nd_name, vertices, materials, face_data, option_flip_yz, recalculate_normals, nd_matrix, root_me)    
    print("\n\t objects loaded")
    
    
    
def load(operator, context, filepath, option_flip_yz = False, recalculate_normals = True, option_worker = False):

    print('\nimporting %r' % filepath)

    time_main = time.time()

    print("\tparsing JSON file...")

    time_sub = time.time()

    file = open(filepath, 'rU')
    rawcontent = file.read()
    file.close()

    if option_worker:
        json_string = extract_json_string(rawcontent)
    else:
        json_string = rawcontent

    data = json.loads( json_string )

    time_new = time.time()

    print('parsing %.4f sec' % (time_new - time_sub))

    time_sub = time_new

    load_data(data, option_flip_yz, recalculate_normals, option_worker)
    
    scene = bpy.context.scene
    scene.update()

    time_new = time.time()

    print('finished importing: %r in %.4f sec.' % (filepath, (time_new - time_main)))
    return {'FINISHED'}


if __name__ == "__main__":
    #register()
    print('Started...')
    #load(None, None, "C:/test/CubColTest.json")
    load(None, None, "C:/test/Json.json")
    #load(None, None, "C:/test/Cubic.json")
    print('Finished')
