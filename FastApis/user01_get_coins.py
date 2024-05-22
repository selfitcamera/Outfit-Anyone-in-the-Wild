
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
    return parser

parser = argument_parser()
args = parser.parse_args()

ApiUrl = args.ApiUrl
OpenId = args.OpenId
ApiKey = args.ApiKey

if __name__ == '__main__':

    params = {'openId':OpenId, 'apiKey':ApiKey}
    session = requests.session()
    ret = requests.post(f"{ApiUrl}/api/inf/get_coins", data=json.dumps(params))
    if ret.status_code==200:
        print(ret.json())
        if 'data' in ret.json():
            """
                [Success] An example returns the result
                { "code": 200,  "msg": "ok",  "data": 0.3}
            """
            """
                [Success] An example returns the result
                { "code": 500, "msg": "no coins!"}
            """            
            print('successfully!')
    
