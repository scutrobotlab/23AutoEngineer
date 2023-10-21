import yaml
import json
import os
from pathlib import Path
from fnmatch import fnmatchcase


class Yaml_Interconversion_Json:
    def __init__(self):
        self.filePathList = []

    # json文件内容转换成yaml格式
    def json_to_yaml(self, jsonPath):
        with open(jsonPath, encoding="utf-8") as f1:
            datas = json.load(f1)  # 将文件的内容转换为字典形式
            i = 0
            new_data = {}
            while i < 2700:
                b = str(i)
                new_data.update({i: {'cam_K': datas[b]['cam_K'], 'depth_scale': datas[b]['depth_scale']}})
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
    def modify_file_suffix(self, filePath, suffix):
        dirPath = os.path.dirname(filePath)
        fileName = 'info' + suffix
        newPath = dirPath + '/' + fileName
        # print('{}_path：{}'.format(suffix, newPath))
        return newPath

    # 原json文件同级目录下，生成yaml文件
    def generate_yaml_file(self, jsonPath, suffix='.yml'):
        yamlDatas = self.json_to_yaml(jsonPath)
        yamlPath = self.modify_file_suffix(jsonPath, suffix)
        # print('yamlPath：{}'.format(yamlPath))
        self.generate_file(yamlPath, yamlDatas)


if __name__ == "__main__":
    jsonPath = '/home/tinywolf/下载/1_渲染数据集制作/output/bop_data/lm/train_pbr/000000/scene_camera.json'##scene_camera.json的位置
    yaml_interconversion_json = Yaml_Interconversion_Json()
    yaml_interconversion_json.generate_yaml_file(jsonPath)
