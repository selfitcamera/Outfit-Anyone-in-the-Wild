
import os
import sys
import cv2
import time
import json
import random
import argparse
import requests
import numpy as np
from urllib.request import urlretrieve


def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--OpenId", type=str, default='')
    parser.add_argument("--ApiKey", type=str, default='')
    parser.add_argument("--ApiUrl", type=str, default='', help='服务接口地址')
    parser.add_argument("--OssUrl", type=str, default='', help='图片服务器的地址')
    return parser

parser = argument_parser()
args = parser.parse_args()

ApiUrl = args.ApiUrl
OpenId = args.OpenId
ApiKey = args.ApiKey
OssUrl = args.OssUrl

if __name__ == '__main__':

    clothId = 208 # 服装的编号，可以在网站上看到
    height = 1.70 # 用户的身高，170厘米=1.7米
    weight = 65 # 用户的体重，65公斤
    fileName = 'test_input.jpg' # 不包含路径的文件名字，可以是jpg/png等
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(cur_dir, 'datas')
    pose_path = os.path.join(data_dir, fileName)
    out_dir = os.path.join(data_dir, 'test_output')
    os.makedirs(out_dir, exist_ok=True)
    out_pose_path = os.path.join(out_dir, 'pose.jpg') # 输出是jpg格式
    out_img_path = os.path.join(out_dir, 'final.jpg') # 输出是jpg格式
    

    ################### 第1步、获取一个上传链接，该链接可用于上传图片 ###################
    infId = -1
    upload_url = ''
    params = {'openId':OpenId, 'apiKey':ApiKey, 'fileName':fileName}
    session = requests.session()
    ret = requests.get(f"{ApiUrl}/api/inf/inf_upload", params=params)
    res = 0
    if ret.status_code==200:
        if 'data' in ret.json():
            print(ret.json())
            data = ret.json()['data']
            infId = data['infId']
            upload_url = data['uploadUrl']
            """
                【成功】一个示例返回结果，'data'是一个float，代表用户当前的积分
                {'code': 200, 'msg': 'ok', 'data': {'infId': 3609, 
                'uploadUrl': ''}}
            """
            print("当前任务id是: ", data['infId'], " 请一定记住这个id！否则无法查询到任务")
            print("图片上传链接是: ", data['uploadUrl'])
        else:
            """
                【失败】一个示例返回结果，积分不足
                {'code': 500, 'msg': 'You have 0.0 coins, but try-on need 5'}
            """
            print(ret.json())
            data = ret.json()
            print("失败信息为, ", data)
            exit(0)
    ################### 第1步、获取一个上传链接，该链接可用于上传图片 ###################
    

    ################### 第2步、上传图片 ###################
    with open(pose_path, 'rb') as file:
        response = requests.put(upload_url, data=file)
        if response.status_code == 200:
            print(response)
        else:
            raise Exception('上传失败！')
    ################### 第2步、上传图片 ###################


    ################### 第3步、发布任务，此时开始扣除积分 ###################
    bmi = weight/(height*height) # 计算bmi，需要调用者自行计算
    print(bmi)
    params = {'openId':OpenId, 'apiKey':ApiKey, 'infId':infId, 
        'clothId':clothId, 'bmi':bmi}
    session = requests.session()
    ret = requests.get(f"{ApiUrl}/api/inf/public_inf", params=params)
    if ret.status_code==200:
        print(ret.json())
        if 'data' in ret.json():
            """
                【成功】一个示例返回结果，'data'是一个float，代表用户当前的积分
                {'code': 200, 'msg': 'ok', 'data': True}
            """
            print('成功发布任务')
        else:
            print('发布任务失败')
            exit(0)
    else:
        exit(0)
    ################### 第3步、发布任务，此时开始扣除积分 ###################
    

    ################ 第4步、不断查询任务状态 ################
    # 任务一般在10分钟--90秒之间完成，不要查询太快
    # 冷启动时，镜像要开机，需要10分钟完成
    # 如果正好镜像是开机的，前面没有排队任务，则完成时间约90秒
    # 查询间隔建议久一些，太频繁会被防火墙封ip
    for _ in range(30):
        params = {'openId':OpenId, 'apiKey':ApiKey, 'infId':infId}
        session = requests.session()
        ret = requests.get(f"{ApiUrl}/api/inf/get_result", params=params)
        if ret.status_code==200:
            print(ret.json())
            if 'data' in ret.json():
                data = ret.json()['data']
                """
                    【成功】一个示例返回结果，'data'是一个float，代表用户当前的积分
                    {'code': 200, 'msg': 'ok', 'data': {'bmi': 0.000402367, 'body_url': '', 
                    'cost': 5.0, 'hairOcclued': 0, 'height': 0.0, 'id': 3619, 'imgUrl1': '', 
                    'imgUrl2': '', 'imgUrl3': '', 'infInfo': '', 'infInfoEn': '', 'ipId': '', 'isApi': 1, 
                    'modelBmi': 0.0, 'openId': 'ovB-x639B8QwdfF7kQYS9QKdK6u8', 'position': 0, 
                    'shareUser': -1, 'showUrl': '', 'state': 1, 'tempId': 208, 'useInfId': -1, 
                    'weight': 0.0}}
                """
                # 实际上只需要关注这3个字段
                print("当前任务排队位置是: ", data['position'])
                print("当前任务状态是: ", data['state'])

                if data['state']==2:
                    pose_url = OssUrl+data['body_url']
                    out_url = OssUrl+data['showUrl']
                    urlretrieve(pose_url, out_pose_path)
                    urlretrieve(out_url, out_img_path)
                    print(f"任务已经完成！", flush=True)
                    break
                elif data['state']==1:
                    position = data['position']
                    print(f"任务正在排队执行，排队位置:{position}", flush=True)
                elif data['state']==-1:
                    infInfoEn = data['infInfoEn']
                    print(f"任务失败，报错信息:{infInfoEn}", flush=True)
                    """
                        一个示例返回结果
                        {'code': 200, 'msg': 'ok', 'data': {'bmi': 0.000402367, 'body_url': '', 
                        'cost': 5.0, 'hairOcclued': 0, 'height': 0.0, 'id': 3653, 'imgUrl1': '', 
                        'imgUrl2': '', 'imgUrl3': '', 
                        'infInfo': '没有检测到脸部，请上传正确的人体试衣照片', 
                        'infInfoEn': 'No face was detected. Please upload the correct human fitting photo.', 
                        'ipId': '', 'isApi': 1, 'modelBmi': 0.0, 
                        'openId': 'ovB-x639B8QwdfF7kQYS9QKdK6u8', 'position': 0, 'shareUser': -1,
                         'showUrl': '', 'state': -1, 'tempId': 208, 'useInfId': -1, 'weight': 0.0}}
                    """
                    break
                elif data['state']==-2:
                    print("积分不足", flush=True)
                    break

        time.sleep(60)
    ################ 第4步、不断查询任务状态 ################
    


