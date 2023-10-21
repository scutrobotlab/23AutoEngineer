from plyfile import PlyData
import os
import numpy as np
model_path = os.path.join('./Linemod_preprocessed/models/obj_01.ply')
ply = PlyData.read(model_path)
data = ply.elements[0].data
x = data['x']
y = data['y']
z = data['z']
x_size = np.max(x)-np.min(x)
y_size = np.max(y)-np.min(y)
z_size = np.max(z)-np.min(z)



print("Min X:")
print(np.min(x))
print("Min Y:")
print(np.min(y))
print("Min Z:")
print(np.min(z))
print('-----------------------------------------------------------------')
print("Size X:")
print(np.max(x)-np.min(x))
print("Size Y:")
print(np.max(y)-np.min(y))
print("Size Z:")
print(np.max(z)-np.min(z))
print('-----------------------------------------------------------------')
print("Diameter:")
print( np.sqrt(x_size**2 + y_size**2 + z_size**2) ) #直径



f = open("./Linemod_preprocessed/models/models_info.txt","w")
f.write("1: {")
f.write("diameter: {}, min_x: {}, min_y: {}, min_z: {}, size_x: {}, size_y: {}, size_z: {}".format(np.sqrt(x_size**2 + y_size**2 + z_size**2) * 1000,np.min(x) * 1000,np.min(y) * 1000,np.min(z)*1000,(np.max(x)-np.min(x)) * 1000,(np.max(y)-np.min(y))*1000,(np.max(z)-np.min(z))*1000))
f.write("}")
f.close()

os.rename("./Linemod_preprocessed/models/models_info.txt","./Linemod_preprocessed/models/models_info.yml")

os.remove("compute_model_info.py")