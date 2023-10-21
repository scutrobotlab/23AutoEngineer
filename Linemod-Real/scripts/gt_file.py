import os
import numpy as np
import matplotlib.image


f = open("gt.txt", "w")

count = len(os.listdir("./transforms"))
for k in range(count):
    print('正在读取第'+str(k)+"张\n")
    data_load = np.load("transforms" + "/" + str(k) + ".npy")
    cam_r = []
    for i in range(3):
        for j in range(3):
            cam_r.append(data_load[i][j])      #cam_R_m2c

    cam_t = [data_load[0][3] * 1000,data_load[1][3] * 1000,data_load[2][3] * 1000]   #cam_t_m2c

    im = matplotlib.image.imread('mask/' + str(k) +'.png')
    r = []
    c = []
    ls1 = [0]
    ls2 = [0]

    for i in range(480):
        for j in range(1, 640):
            if im[i][j - 1] == 0 and im[i][j] == 1:
                r.append(i)
                c.append(j)
                break
    for i in range(480):
        for j in range(1, 640):
            if im[i][j - 1] == 1 and im[i][j] == 0:
                ls1[0] = i
                ls2[0] = j
    r.append(ls1[0])
    c.append(ls2[0])
    rmin = min(r)
    rmax = max(r)
    cmin = min(c)
    cmax = max(c)
    r.clear()
    c.clear()
    bb=[]
    bb.append(rmin)
    bb.append(rmax)
    bb.append(cmin)
    bb.append(cmax)
    print(cam_t)
    print(cam_r)
    print(bb)
    f.write("{}:\n".format(k))
    f.write("- cam_R_m2c: [{}, {}, {}, {}, {}, {}, {}, {}, {}]\n".format(cam_r[0],cam_r[1],cam_r[2],cam_r[3],cam_r[4],cam_r[5],cam_r[6],cam_r[7],cam_r[8]))
    f.write("  cam_t_m2c: [{}, {}, {}]\n".format(cam_t[0],cam_t[1],cam_t[2]))
    f.write("  obj_bb: [{}, {}, {}, {}]\n".format(bb[0],bb[1],bb[2],bb[3]))
    f.write("  obj_id: 1\n")
    cam_r.clear()
    bb.clear()
    cam_t.clear()
f.close()

os.rename("./gt.txt","./gt.yml")




