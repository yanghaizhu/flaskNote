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

def json_from_list_to_dict(file,toFile):
    dataList = json_load_from_file(file)
    dataDict = {}
    for item in dataList:
        dataDict[item["uuid"]] = item
    json_dump_to_file(toFile,dataDict)


def record_load_from_file():
    file_path = current_app.config["RECORD_PATH_FILE"]
    with open(file_path+'.json',encoding='utf-8') as fp:
        recordData = json.load(fp)
        current_app.log.debug(recordData)
        return recordData

def record_load_from_file_by_uuid(uuid):
    print(uuid)
    content = "# ["+uuid+"](http://127.0.0.1:5000/uuid/4f72b351467a400aa018a0243d993b37/)\r\n#"
    recordData = json_load_from_file("2")
    item = recordData[uuid]
    content = content + item["detail"]
    return content
    

def record_dump_to_file(recordData):
    file_path = current_app.config["RECORD_PATH_FILE"]
    print(recordData)
    print("file_path")
    print(file_path)
    with open(file_path+'.json','w',encoding='utf-8') as fp:
        json.dump(recordData, fp, indent=2,ensure_ascii=False)
    


def appendNewItemToFile(uuid, content):
    recordData = json_load_from_file("2")
    print(uuid)
    itemAdd = dict()
    keyList = list()
    relationList = list()
    itemAdd["keyList"] = []
    itemAdd["relationList"] = []
    itemAdd["uuid"] = uuid
    itemAdd["detail"] = content
    recordData[uuid] = itemAdd

        
    json_dump_to_file("2",recordData)


def uuidTitle_dump_to_file(uuid_to_title):
    file_path = current_app.config["UUID_TITLE_PATH_FILE"]
    with open(file_path+'.json','w',encoding='utf-8') as fp:
        json.dump(uuid_to_title, fp, indent=2,ensure_ascii=False)

def uuidTitle_load_from_file():
    file_path = current_app.config["UUID_TITLE_PATH_FILE"]
    with open(file_path+'.json',encoding='utf-8') as fp:
        uuid_to_title = json.load(fp)
        current_app.log.debug(uuid_to_title)
        return uuid_to_title