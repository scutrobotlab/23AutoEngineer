import os
import shutil

os.mkdir("./data")
os.mkdir("./data/01")
os.mkdir("./models")
os.mkdir("./segnet_results")
os.mkdir("./segnet_results/01_label")

msk = os.listdir("./mask")
for file in msk:
    shutil.copy("./mask/" + file,"./segnet_results/01_label/")


shutil.move("./rgb","./data/01/")
shutil.move("./mask","./data/01/")
shutil.move("./depth","./data/01/")
shutil.move("./gt.yml","./data/01/")
shutil.move("./info.yml","./data/01/")

os.rename("./Gold.ply","./obj_01.ply")   ##记得改成自己那个ply的文件名
shutil.move("obj_01.ply","./models")

shutil.rmtree("./labels")
shutil.rmtree("./transforms")
os.remove("intrinsics.json")
os.remove("registeredScene.ply")
os.remove("transforms.npy")

root = os.listdir("./")
for file in root:
    if file[-2:] == "py":
        if file == "compute_model_info.py":
            continue
        os.remove(file)

os.mkdir("./Linemod_preprocessed")
shutil.move("data","./Linemod_preprocessed/")
shutil.move("models","./Linemod_preprocessed/")
shutil.move("segnet_results","./Linemod_preprocessed/")