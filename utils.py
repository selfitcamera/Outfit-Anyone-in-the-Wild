
import os
import sys
import cv2
import json
import random
import time
import requests
import numpy as np
import gradio as gr


ApiUrl = os.environ['ApiUrl']
OpenId = os.environ['OpenId']
ApiKey = os.environ['ApiKey']


proj_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(proj_dir, 'Datas')
tmpFolder = "tmp"
os.makedirs(tmpFolder, exist_ok=True)


def get_cloth_examples():
    cloth_dir = os.path.join(data_dir, 'ClothImgs')
    examples = []
    for f in os.listdir(cloth_dir):
        cloth_id = f.split(".")[0]
        cloth_path = os.path.join(cloth_dir, f)
        examples.append([cloth_id, cloth_path])
    examples = examples[::-1]
    return examples

def get_pose_examples():
    pose_dir = os.path.join(data_dir, 'PoseImgs')
    examples = []
    for f in os.listdir(pose_dir):
        pose_id = f.split(".")[0]
        pose_path = os.path.join(pose_dir, f)
        examples.append([pose_id, pose_path])
    return examples

def get_result_example(cloth_id, pose_id):
    result_dir = os.path.join(data_dir, 'ResultImgs')
    res_path = os.path.join(result_dir, f"{cloth_id}_{pose_id}.jpg")
    return res_path

def getAllInfs(apiUrl, openId, apiKey, clientIp):
    params = {'openId':openId, 'apiKey':apiKey, 'ipId':clientIp}
    session = requests.session()
    ret = requests.get(f"{apiUrl}/api/all_infs", params=params)
    res = []
    if ret.status_code==200:
        if 'data' in ret.json():
            records = ret.json()['data']['records']
            res = [{'pose':record['body_url'], 'res':record['showUrl']} for record in records]
    return res


def upload_pose_img(apiUrl, openId, apiKey, clientIp, timeId, img):
    fileName = clientIp.replace(".", "")+str(timeId)+".jpg"
    local_path = os.path.join(tmpFolder, fileName)
    cv2.imwrite(os.path.join(tmpFolder, fileName), img[:,:,::-1])
    params = {'openId':openId, 'apiKey':apiKey, 'ipId':clientIp, 
        'timeId':str(timeId), 'fileName':fileName}
    session = requests.session()
    ret = requests.get(f"{apiUrl}/api/inf_upload", params=params)
    res = 0
    if ret.status_code==200:
        # print(ret.json())
        if 'data' in ret.json():
            upload_url = ret.json()['data']
            # print(upload_url, len(upload_url))
            if 'running' in upload_url:
                res = -1 # 存在正在进行的任务
            elif 'no_coin' in upload_url:
                res = -2 # 该ip已经用完了quota
            else:
                with open(local_path, 'rb') as file:
                    response = requests.put(upload_url, data=file)
                    if response.status_code == 200:
                        res = 1
    if os.path.exists(local_path):
        os.remove(local_path)
    return res


def publicClothSwap(apiUrl, openId, apiKey, clientIp, clothId, timeId, size):
    params = {'openId':openId, 'apiKey':apiKey, 'ipId':clientIp, 
        'timeId':timeId, 'clothId':clothId, 'bmi':size}
    session = requests.session()
    ret = requests.get(f"{apiUrl}/api/cloth_swap", params=params)
    if ret.status_code==200:
        if 'data' not in ret.json():
            print(ret.json())
            return 0
        taskId = ret.json()['data']
        return taskId
    else:
        return 0

def getInfRes(apiUrl, openId, apiKey, clientIp, timeId):
    params = {'openId':openId, 'apiKey':apiKey, 'ipId':clientIp, 'timeId':timeId}
    session = requests.session()
    ret = requests.get(f"{apiUrl}/api/getInfRes", params=params)
    if ret.status_code==200:
        if 'data' not in ret.json():
            print(ret.json())
            return 0
        return ret.json()['data']
    else:
        return 0

