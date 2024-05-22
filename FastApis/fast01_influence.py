
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
    parser.add_argument("--ApiUrl", type=str, default='', help='api interface address')
    parser.add_argument("--OssUrl", type=str, default='', help='Image server address')
    return parser

parser = argument_parser()
args = parser.parse_args()

ApiUrl = args.ApiUrl
OpenId = args.OpenId
ApiKey = args.ApiKey
OssUrl = args.OssUrl

if __name__ == '__main__':

    poseName = '1_pose.jpg'
    clothName = '2_cloth.jpg'
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(cur_dir, 'datas/fastinfs')
    pose_path = os.path.join(data_dir, poseName)
    cloth_path = os.path.join(data_dir, clothName)

    out_pose_path = os.path.join(data_dir, 'out_pose.jpg') # The output is in jpg format
    out_img_path = os.path.join(data_dir, 'out_img.jpg') # The output is in jpg format
    out_mask_path = os.path.join(data_dir, 'out_mask.jpg') # The output is in jpg format

    ################### Step 1. Get an upload link, which can be used to upload images ###################
    infId = -1
    clothUrl = ''
    maskUrl = ''
    poseUrl = ''
    params = {'openId':OpenId, 'apiKey':ApiKey, 
        'ipId':'', 'poseFileName':poseName, 'maskFileName':'', 
        'clothFileName':clothName}
    session = requests.session()
    ret = requests.post(f"{ApiUrl}/api/inf/fastinf_upload", data=json.dumps(params))

    res = 0
    if ret.status_code==200:
        if 'data' in ret.json():
            print(ret.json())
            data = ret.json()['data']
            infId = data['infId']
            clothUrl = data['clothUrl']
            maskUrl = data['maskUrl']
            poseUrl = data['poseUrl']
            """
                {
                    "code": 200,
                    "msg": "ok",
                    "data": {
                        "clothUrl": "",
                        "cod": 1,
                        "infId": 6622,
                        "maskUrl": "",
                        "poseUrl": "h"
                    }
                }
            """
            print("currnet infId: ", data['infId'], " Please remember this ID! Otherwise, the task cannot be queried")
        else:
            """
            {
                "code": 500,
                "msg": "Hacker access detected！"
            }
            """
            print(ret.json())
            data = ret.json()
            print("fail info is, ", data)
            exit(0)
    ################### Step 1. Get an upload link, which can be used to upload images ###################
    

    ################### Step 2. Upload pictures ###################
    with open(cloth_path, 'rb') as file:
        response = requests.put(clothUrl, data=file)
        if response.status_code == 200:
            print(response)
        else:
            raise Exception('upload failed！')
    with open(pose_path, 'rb') as file:
        response = requests.put(poseUrl, data=file)
        if response.status_code == 200:
            print(response)
        else:
            raise Exception('upload failed！')
    ################### Step 2. Upload pictures ###################
    
    
    ################### Step 3: Publish the task, and coins will start to be consumed at this time ###################
    denoise_steps = 20
    auto_mask = 1
    auto_crop = 1
    category = 2
    caption = ""

    params = {'openId':OpenId, 'apiKey':ApiKey, 'infId':infId, 
        'denoise_steps':denoise_steps, 'auto_mask':auto_mask, 
        'auto_crop':auto_crop, 'category':category, 'caption':caption}
    session = requests.session()
    ret = requests.post(f"{ApiUrl}/api/inf/public_fastinf", data=json.dumps(params))
    if ret.status_code==200:
        print(ret.json())
        if 'data' in ret.json():
            """
                [Success] An example returns the result
                {'code': 200, 'msg': 'ok', 'data': True}
            """
            print('public task successfully!')
        else:
            print('public task failed')
            exit(0)
    else:
        exit(0)
    ################### Step 3: Publish the task, and points will start to be deducted at this time ###################
    
    
    out_pose_path = os.path.join(data_dir, 'out_pose.jpg') # The output is in jpg format
    out_img_path = os.path.join(data_dir, 'out_img.jpg') # The output is in jpg format
    out_mask_path = os.path.join(data_dir, 'out_mask.jpg') # The output is in jpg format
    
    
    ################ Step 4: Continuously query task status ################
    # task is supported to finished in 20 seconds at most time
    # Sometimes you need to queue, which may take more than 40 seconds
    # Sometimes the computer does not turn on, and it takes 10 minutes to complete.
    time.sleep(20)
    for _ in range(30):
        params = {'openId':OpenId, 'apiKey':ApiKey, 'infId':infId}
        session = requests.session()
        ret = requests.post(f"{ApiUrl}/api/inf/get_fast_result", data=json.dumps(params))
        if ret.status_code==200:
            print(ret.json())
            if 'data' in ret.json():
                data = ret.json()['data']
                """
                    {
                        "code": 200,
                        "msg": "ok",
                        "data": {
                            "auto_crop": 0,
                            "auto_mask": 0,
                            "bodyUrl": "ClothData/Publics/Users/ovB-x639B8QwdfF7kQYS9QKdK6u8/FastInfs/QKGBFQ6618/res_src.jpg",
                            "caption": "",
                            "category": 2,
                            "cost": 0.0,
                            "denoise_steps": 0,
                            "id": 6618,
                            "infInfo": "result 0",
                            "infInfoEn": "result 0",
                            "ipId": "",
                            "isApi": 1,
                            "maskUrl": "ClothData/Publics/Users/ovB-x639B8QwdfF7kQYS9QKdK6u8/FastInfs/QKGBFQ6618/res_mask.jpg",
                            "openId": "ovB-x639B8QwdfF7kQYS9QKdK6u8",
                            "position": 0,
                            "showUrl": "ClothData/Publics/Users/ovB-x639B8QwdfF7kQYS9QKdK6u8/FastInfs/QKGBFQ6618/res_img.jpg",
                            "state": 2,
                            "suffix": "QKGBFQ"
                        }
                    }
                """
                # In fact, you only need to pay attention to these 3 fields
                print("The current task queue position is: ", data['position'])
                print("The current task status is: ", data['state'])

                if data['state']==2:
                    urlretrieve(OssUrl+data['bodyUrl'], out_pose_path)
                    urlretrieve(OssUrl+data['showUrl'], out_img_path)
                    urlretrieve(OssUrl+data['maskUrl'], out_mask_path)
                    print(f"The task has been completed！", flush=True)
                    break
                elif data['state']==1:
                    position = data['position']
                    print(f"The task is being queued for execution, and the queue position:{position}", flush=True)
                elif data['state']==-1:
                    infInfoEn = data['infInfoEn']
                    print(f"Task failed, error message reported:{infInfoEn}", flush=True)
                    """
                        An example returns results
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
                    print("no coins", flush=True)
                    break
    ################ Step 4: Continuously query task status ################
    


