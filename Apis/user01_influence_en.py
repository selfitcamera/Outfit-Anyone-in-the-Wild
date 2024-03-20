
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

    clothId = 208 # The clothId can be seen on the website
    height = 1.70 # User's height, 170 cm = 1.7 meters
    weight = 65 # User's weight, 65 kg
    fileName = 'test_input.png' # File name without path, can be jpg/png, etc.
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(cur_dir, 'datas')
    pose_path = os.path.join(data_dir, fileName)
    out_dir = os.path.join(data_dir, 'test_output')
    os.makedirs(out_dir, exist_ok=True)
    out_pose_path = os.path.join(out_dir, 'pose.jpg') # The output is in jpg format
    out_img_path = os.path.join(out_dir, 'final.jpg') # The output is in jpg format
    

    ################### Step 1. Get an upload link, which can be used to upload images ###################
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
                [Success] An example returns the result. 'data' is a float, representing the user's current points.
                {'code': 200, 'msg': 'ok', 'data': {'infId': 3609, 
                'uploadUrl': ''}}
            """
            print("当前任务id是: ", data['infId'], " Please remember this ID! Otherwise, the task cannot be queried")
            print("图片上传链接是: ", data['uploadUrl'])
        else:
            """
                [Failure] An example returns a result with insufficient points.
                {'code': 500, 'msg': 'You have 0.0 coins, but try-on need 5'}
            """
            print(ret.json())
            data = ret.json()
            print("失败信息为, ", data)
            exit(0)
    ################### Step 1. Get an upload link, which can be used to upload images ###################
    

    ################### Step 2. Upload pictures ###################
    with open(pose_path, 'rb') as file:
        response = requests.put(upload_url, data=file)
        if response.status_code == 200:
            print(response)
        else:
            raise Exception('upload failed！')
    ################### Step 2. Upload pictures ###################


    ################### Step 3: Publish the task, and points will start to be deducted at this time ###################
    bmi = weight/(height*height) # To calculate bmi, the caller needs to calculate it by himself
    print(bmi)
    params = {'openId':OpenId, 'apiKey':ApiKey, 'infId':infId, 
        'clothId':clothId, 'bmi':bmi}
    session = requests.session()
    ret = requests.get(f"{ApiUrl}/api/inf/public_inf", params=params)
    if ret.status_code==200:
        print(ret.json())
        if 'data' in ret.json():
            """
                [Success] An example returns the result
                {'code': 200, 'msg': 'ok', 'data': True}
            """
            print('成功发布任务')
        else:
            print('发布任务失败')
            exit(0)
    else:
        exit(0)
    ################### Step 3: Publish the task, and points will start to be deducted at this time ###################
    

    ################ Step 4: Continuously query task status ################
    # Tasks are usually completed between 10 minutes and 90 seconds. Do not query too quickly.
    # During cold start, it takes 10 minutes to start the image.
    # If the mirror is powered on and there are no queued tasks in front of it, the completion time will be about 90 seconds.
    # It is recommended that the query interval be longer. If it is too frequent, the IP address will be blocked by the firewall.
    for _ in range(30):
        params = {'openId':OpenId, 'apiKey':ApiKey, 'infId':infId}
        session = requests.session()
        ret = requests.get(f"{ApiUrl}/api/inf/get_result", params=params)
        if ret.status_code==200:
            print(ret.json())
            if 'data' in ret.json():
                data = ret.json()['data']
                """
                    [Success] An example returns the result. 'data' is a float, representing the user's current points.
                    {'code': 200, 'msg': 'ok', 'data': {'bmi': 0.000402367, 'body_url': '', 
                    'cost': 5.0, 'hairOcclued': 0, 'height': 0.0, 'id': 3619, 'imgUrl1': '', 
                    'imgUrl2': '', 'imgUrl3': '', 'infInfo': '', 'infInfoEn': '', 'ipId': '', 'isApi': 1, 
                    'modelBmi': 0.0, 'openId': 'xxxx', 'position': 0, 
                    'shareUser': -1, 'showUrl': '', 'state': 1, 'tempId': 208, 'useInfId': -1, 
                    'weight': 0.0}}
                """
                # In fact, you only need to pay attention to these 3 fields
                print("The current task queue position is: ", data['position'])
                print("The current task status is: ", data['state'])

                if data['state']==2:
                    pose_url = OssUrl+data['body_url']
                    out_url = OssUrl+data['showUrl']
                    urlretrieve(pose_url, out_pose_path)
                    urlretrieve(out_url, out_img_path)
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

        time.sleep(60)
    ################ Step 4: Continuously query task status ################
    


