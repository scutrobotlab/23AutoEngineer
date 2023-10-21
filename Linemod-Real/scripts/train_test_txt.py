import os

files = len(os.listdir("./Linemod_preprocessed/data/01/depth/"))

_train = open("./Linemod_preprocessed/data/01/train.txt","w")
_test = open("./Linemod_preprocessed/data/01/test.txt","w")
for i in range(files):
    num = (4-len(str(i))) * '0' + str(i)
    if i % 5 == 4:
        _test.write(num + "\n")
    else:
        _train.write(num + "\n")
_train.close()
_test.close()