import os
import cv2


root_rgb = "./JPEGImages/"
root_mask = "./mask/"
root_depth = "./depth/"

ls_rgb = os.listdir(root_rgb)
ls_mask = os.listdir(root_mask)
ls_depth = os.listdir(root_depth)

os.mkdir("rgb")

for file in ls_rgb:
    os.rename(root_rgb + file,"./rgb/" +"0" * int(4 - len(file[:-4])) + file[:-4] + ".jpg")
for file in ls_mask:
    os.rename(root_mask + file,root_mask +"0" * int(4 - len(file[:-4])) + file[:-4] + ".png")
for file in ls_depth:
    os.rename(root_depth + file,root_depth +"0" * int(4 - len(file[:-4])) + file[:-4] + ".png")

os.rmdir(root_rgb)

rgb = "./rgb"
ls__rgb = os.listdir(rgb)
i = 0
for file in ls__rgb:
    print("正在进行图片" + str(i) + "的转码")
    img = cv2.imread("./rgb/" + file)
    cv2.imwrite("./rgb/" + file[:-3] + "png",img)
    os.remove("./rgb/"+ file[:-3] + "jpg")
    i += 1