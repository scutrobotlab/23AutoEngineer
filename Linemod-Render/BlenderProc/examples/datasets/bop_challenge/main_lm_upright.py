import blenderproc as bproc
import argparse
import os
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('bop_parent_path', default="..", help="Path to the bop datasets parent directory")
parser.add_argument('cc_textures_path', default="resources/cctextures", help="Path to downloaded cc textures")
parser.add_argument('output_dir', default="examples/datasets/bop_challenge/output", help="Path to where the final files will be saved ")
parser.add_argument('--num_scenes', type=int, default=2000, help="How many scenes with 25 images each to generate")
args = parser.parse_args()

bproc.init()

# load bop objects into the scene
target_bop_objs = bproc.loader.load_bop_objs(bop_dataset_path = os.path.join(args.bop_parent_path, 'lm'), mm2m = True,obj_ids = [9])


# load BOP datset intrinsics
bproc.loader.load_bop_intrinsics(bop_dataset_path = os.path.join(args.bop_parent_path, 'lm'))
    
# create room
room_planes = [bproc.object.create_primitive('PLANE', scale=[2, 2, 1]),
               bproc.object.create_primitive('PLANE', scale=[2, 2, 1], location=[0, -2, 2], rotation=[-1.570796, 0, 0]),
               bproc.object.create_primitive('PLANE', scale=[2, 2, 1], location=[0, 2, 2], rotation=[1.570796, 0, 0]),
               bproc.object.create_primitive('PLANE', scale=[2, 2, 1], location=[2, 0, 2], rotation=[0, -1.570796, 0]),
               bproc.object.create_primitive('PLANE', scale=[2, 2, 1], location=[-2, 0, 2], rotation=[0, 1.570796, 0])]

# sample light color and strenght from ceiling
light_plane = bproc.object.create_primitive('PLANE', scale=[3, 3, 1], location=[0, 0, 10])
light_plane.set_name('light_plane')
light_plane_material = bproc.material.create('light_material')

# sample point light on shell
light_point = bproc.types.Light()
light_point.set_energy(200)

# load cc_textures
print(args.cc_textures_path)
cc_textures = bproc.loader.load_ccmaterials(args.cc_textures_path)
print(cc_textures)

# Define a function that samples 6-DoF poses 定义一个对 6-DoF 姿势进行采样的函数
def sample_pose_func(obj: bproc.types.MeshObject):
    min = np.random.uniform([-0.3, -0.3, 0.0], [-0.2, -0.2, 0.0])
    max = np.random.uniform([0.2, 0.2, 0.4], [0.3, 0.3, 0.6])
    obj.set_location(np.random.uniform(min, max))
    obj.set_rotation_euler(bproc.sampler.uniformSO3())
    
# activate depth rendering without antialiasing and set amount of samples for color rendering
bproc.renderer.enable_depth_output(activate_antialiasing=False)
bproc.renderer.set_max_amount_of_samples(50)

# Set intrinsics via K matrix
bproc.camera.set_intrinsics_from_K_matrix(
    [[498.55382294 ,  0.   ,      322.61057961]
 [  0.     ,    498.59901606 ,233.90011395]
 [  0.        ,   0.       ,    1.        ]], 640, 480
)
k=0
while k< 12:
    j = 0
    while j< 9:
        for i in range(args.num_scenes):

    # Sample bop objects for a scene
            sampled_target_bop_objs = list(np.random.choice(target_bop_objs, size=1, replace=False))

    # Randomize materials and set physics
            for obj in (sampled_target_bop_objs ):        
                mat = obj.get_materials()[0]     
                mat.set_principled_shader_value("Roughness", np.random.uniform(0, 1.0))
                mat.set_principled_shader_value("Specular", np.random.uniform(0, 1.0))
                obj.hide(False)
    
    # Sample two light sources
            light_plane_material.make_emissive(emission_strength=np.random.uniform(3,6), 
                                        emission_color=np.random.uniform([0.5, 0.5, 0.5, 1.0], [1.0, 1.0, 1.0, 1.0]))  
            light_plane.replace_materials(light_plane_material)
            light_point.set_color(np.random.uniform([0.5,0.5,0.5],[1,1,1]))
            location = bproc.sampler.shell(center = [0, 0, 0], radius_min = 1, radius_max = 1.5,
                                elevation_min = 5, elevation_max = 89)
            light_point.set_location(location)

    # sample CC Texture and assign to room planes
            random_cc_texture = np.random.choice(cc_textures)
            print(room_planes)
            for plane in room_planes:
                plane.replace_materials(random_cc_texture)

            #room_planes[0].replace_materials(random_cc_texture)

    # Sample object poses and check collisions 
            bproc.object.sample_poses(objects_to_sample = sampled_target_bop_objs ,
                                sample_pose_func = sample_pose_func, 
                                max_tries = 20000)
            
    # Define a function that samples the initial pose of a given object above the ground
            def sample_initial_pose(obj: bproc.types.MeshObject):
                obj.set_location(bproc.sampler.upper_region(objects_to_sample_on=room_planes[0:1],
                                                        min_height=1, max_height=4, face_sample_range=[0.5, 0.5]))
        #小鸭子的位子信息
                #卫星到T
                if k == 0: 
                   obj.set_rotation_euler([0, 0, 0])
                if k == 1: 
                   obj.set_rotation_euler([-np.pi/4, 0, 0])
                #卫星平躺下
                if k == 2: 
                   obj.set_rotation_euler([-np.pi/2, 0, 0])
                if k == 3: 
                   obj.set_rotation_euler([-np.pi*3/4, 0, 0])
                #卫星正T
                if k == 4: 
                   obj.set_rotation_euler([-np.pi, 0, 0])
                if k == 5: 
                   obj.set_rotation_euler([-np.pi*5/4, 0, 0])
                if k == 6: 
                   obj.set_rotation_euler([-np.pi/2, -np.pi/2, 0])
                if k == 7: 
                   obj.set_rotation_euler([-np.pi/2, np.pi/2, 0])
                if k == 8: 
                   obj.set_rotation_euler([-np.pi/4, -np.pi/2, 0])
                if k == 9: 
                   obj.set_rotation_euler([-np.pi/4, np.pi/2, 0])
                if k == 10: 
                   obj.set_rotation_euler([-np.pi*3/4, -np.pi/2, 0])
                if k == 11: 
                   obj.set_rotation_euler([-np.pi*3/4, np.pi/2, 0])
	#小鸭子倒立
	#obj.set_rotation_euler(np.random.uniform([-np.pi, 0, 0], [-np.pi, 0, 0]))
	#obj.set_rotation_euler(np.random.uniform([-np.pi*4, 0, 0], [-np.pi*4, 0, np.pi * 2]))

    # Sample objects on the given surface
            placed_objects = bproc.object.sample_poses_on_surface(objects_to_sample=sampled_target_bop_objs ,
                                                              surface=room_planes[0],
                                                              sample_pose_func=sample_initial_pose,
                                                                  min_distance=0.01,
                                                          max_distance=0.02)

    # BVH tree used for camera obstacle checks
            bop_bvh_tree = bproc.object.create_bvh_tree_multi_objects(sampled_target_bop_objs )

            cam_poses = 0
            while cam_poses < 25:
        # Sample location
                location = bproc.sampler.shell(center = [0, 0, 0],
                                    radius_min = 0.3,
                                    radius_max = 0.65,
                                    elevation_min = (8+10*j),
                                    elevation_max = (9+10*j),
                                    azimuth_min = -180, 
                                    azimuth_max = 180,
                                    uniform_volume=True)
        # Determine point of interest in scene as the object closest to the mean of a subset of objects
                poi = bproc.object.compute_poi(np.random.choice(sampled_target_bop_objs, size=1, replace=False))
        # Compute rotation based on vector going from location towards poi
                rotation_matrix = bproc.camera.rotation_from_forward_vec(poi - location, inplane_rot=np.random.uniform(-0.2, 0.2))
        # Add homog cam pose based on location an rotation
                cam2world_matrix = bproc.math.build_transformation_mat(location, rotation_matrix)
        
        # Check that obstacles are at least 0.3 meter away from the camera and make sure the view interesting enough
                if bproc.camera.perform_obstacle_in_view_check(cam2world_matrix,{"min": 0.1}, bop_bvh_tree):
            # Persist camera pose
                    bproc.camera.add_camera_pose(cam2world_matrix, frame=cam_poses)
                    cam_poses += 1

    # render the whole pipeline
            data = bproc.renderer.render()

    # Write data in bop format
            bproc.writer.write_bop(os.path.join(args.output_dir, 'bop_data'),
                           target_objects = sampled_target_bop_objs,
                           dataset = 'lm',
                           depth_scale = 1.0,
                           depths = data["depth"],
                           colors = data["colors"], 
                           color_file_format = "JPEG",
                           ignore_dist_thres = 10,
                           frames_per_chunk = 200000)
        j=j+1
    k=k+1
