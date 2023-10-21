import yaml
import json
import os
from pathlib import Path
from fnmatch import fnmatchcase


class Yaml_Interconversion_Json:
    def __init__(self):
        self.filePathList = []

    # json文件内容转换成yaml格式
    def json_to_yaml(self, jsonPath1, jsonPath2):
        with open(jsonPath1, encoding="utf-8") as f1:
            datas1 = json.load(f1)  # 将文件的内容转换为字典形式
        with open(jsonPath2, encoding="utf-8") as f2:
            datas2 = json.load(f2)  # 将文件的内容转换为字典形式
            i = 0
            new_data = {}
            while (i < 2700):
                b = str(i)
                new_data.update({i: [{'cam_R_m2c': datas1[b][0]['cam_R_m2c'], 'cam_t_m2c': datas1[b][0]['cam_t_m2c'],
                                      'obj_bb': datas2[b][0]['bbox_obj'], 'obj_id': datas1[b][0]['obj_id']}]})

                print(i)
                i = i + 1
            yamlDatas = yaml.dump(new_data, indent=5, sort_keys=False)  # 将字典的内容转换为yaml格式的字符串
        return yamlDatas

    #    # json文件内容转换成yaml格式
    # def json_to_yaml(self, jsonPath):
    #     with open(jsonPath, encoding="utf-8") as f:
    #         datas = json.load(f)
    #     yamlDatas = yaml.dump(datas, indent=5, sort_keys=False)
    #     # print(yamlDatas)
    #     return yamlDatas

    # 生成文件
    def generate_file(self, filePath, datas):
        if os.path.exists(filePath):
            os.remove(filePath)
        with open(filePath, 'w') as f:
            f.write(datas)

    # 清空列表
    def clear_list(self):
        self.filePathList.clear()

    # 修改文件后缀
    def modify_file_suffix(self, filePath1, suffix):
        dirPath = os.path.dirname(filePath1)
        fileName = 'gt' + suffix
        newPath = dirPath + '/' + fileName
        # print('{}_path：{}'.format(suffix, newPath))
        return newPath

    # 原json文件同级目录下，生成yaml文件
    def generate_yaml_file(self, jsonPath1, jsonPath2, suffix='.yml'):
        yamlDatas = self.json_to_yaml(jsonPath1, jsonPath2)
        yamlPath = self.modify_file_suffix(jsonPath1, suffix)
        # print('yamlPath：{}'.format(yamlPath))
        self.generate_file(yamlPath, yamlDatas)


if __name__ == "__main__":
    jsonPath1 = '/home/tinywolf/下载/1_渲染数据集制作/output/bop_data/lm/train_pbr/000000/scene_gt.json'##scene_gt.json位置
    jsonPath2 = '/home/tinywolf/下载/1_渲染数据集制作/output/bop_data/lm/train_pbr/000000/scene_gt_info.json'##scene_gt_info.json位置
    yaml_interconversion_json = Yaml_Interconversion_Json()
    yaml_interconversion_json.generate_yaml_file(jsonPath1, jsonPath2)
