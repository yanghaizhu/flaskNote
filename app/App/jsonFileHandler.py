from flask import Blueprint,request,redirect, current_app
import json

import os

def get_json_file_list():
    file_list = []
    file_path = current_app.config["JSON_FILE_PATH"]
    for root, dirs, files in os.walk(file_path):
        for f in files:
            fname = os.path.splitext(f)[0]
            file_list.append(fname)
    current_app.log.debug(file_list)
    return file_list

def json_load_from_file(file):
    file_path = current_app.config["JSON_FILE_PATH"]
    with open(file_path+file+'.json',encoding='utf-8') as fp:
        print(file_path+file+'.json')
        itemListInJson = json.load(fp)
        
        current_app.log.debug(itemListInJson)
        return itemListInJson
        
def json_dump_to_file(file, jsonData):
    file_path = current_app.config["JSON_FILE_PATH"]
    with open(file_path+file+'.json','w',encoding='utf-8') as fp:
        json.dump(jsonData, fp, indent=2,ensure_ascii=False)
        
def record_load_from_file():
    file_path = current_app.config["RECORD_PATH_FILE"]
    with open(file_path+'.json',encoding='utf-8') as fp:
        recordData = json.load(fp)
        current_app.log.debug(recordData)
        return recordData
        
def record_dump_to_file(recordData):
    file_path = current_app.config["RECORD_PATH_FILE"]
    with open(file_path+'.json','w',encoding='utf-8') as fp:
        json.dump(recordData, fp, indent=2,ensure_ascii=False)
