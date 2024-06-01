from flask import Blueprint,request,redirect, current_app
from .models import *
import json
import jmespath
import os
from werkzeug.utils import *
import html
import markdown

def str_upper_split_to_list(string):
    l = [s.strip().upper() for s in string.split(",")]
    current_app.log.debug(l)
    return l
    
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

def search_revers_action_flag(string):
    current_app.log.debug(string)
    return string.startswith("-") or string.startswith("!")
    
def search_in_key_list(search, key_list):
    current_app.log.debug(search)
    current_app.log.debug(key_list)
    return search in key_list

def search_res_as_expected(search, key_list):
    if search_revers_action_flag(search) and not search_in_key_list(search[1:], key_list):
        return True
    elif not search_revers_action_flag(search) and search_in_key_list(search, key_list):
        return True
    else:
        return False
    
def modify_by_id_in_list(idx, item_list, item_updated):
    for i in range(len(item_list)):
        item = item_list[i]
        if idx == item["id"]:
            item_list[i] = item_updated
    return item_list

def del_by_id_in_list(idx, item_list):
    for i in range(len(item_list)):
        item = item_list[i]
        if idx == item["id"]:
            del item_list[i]
    return item_list

# blueprint is used for route. "todo" name can be others. todoBlueprint would be used at create_app, in __init__.py. 
# We can have more blueprints, with different name, and at create_app side, register them one by one.
homeBlueprint = Blueprint('home', __name__)

        
@homeBlueprint.route('/find/<string:findStrings>/',methods=['GET','POST'])
# look up from All files, collect item content into a List.
# 遍历所有的json文件，找到关键字对于的内容列表
def findListByItem(findStrings):
    logger = current_app.log
    print(findStrings)
    findStr = findStrings
    if request.method=='POST':
        print(request.form)
        for key in request.form:
            findStr = request.form[key]
            
    ## convert seach string to list
    search_key_list = str_upper_split_to_list(findStr)
    
    ## collect file name into a list.
    ## 文件名列表
    file_list = get_json_file_list()   
    
    itemList = []
    for f in file_list:
        ## read json from json file.
        ### This file path should be based on root path.  becasue it's just included by app.py, which is in root path. 
        itemListInJson = json_load_from_file(f)
        print(f)
        ## 遍历所有item.
        for item in itemListInJson:
            allConditionMeet = True
            for search in search_key_list:
#                print(item)
                if not search_res_as_expected(search, item["keyList"]):
                    allConditionMeet = False
            if allConditionMeet:
                itemTmp = item
                itemTmp["file"] = f
                itemList.append(itemTmp)

    return  render_template('home.html', findStr=findStr, itemList=itemList, file_list=file_list)
    

@homeBlueprint.route('/show/<string:file>/',methods=['GET'])
def showFile(file):
    logger = current_app.log
    logger.critical("show file:"+file)
    ## collect file name into a list.
    ## 文件名列表
    file_list = []
    
    itemList = []
    findStr = ""

    ### assumed only one dir.
    file_list = get_json_file_list()


    f = file
    logger.debug(f)
    print(f)

    ## read json from json file.
    ### This file path should be based on root path.  becasue it's just included by app.py, which is in root path. 
    itemListInJson = json_load_from_file(f)
    ## 遍历所有item.
    for item in itemListInJson:
        logger.debug(item)
        logger.debug(findStr)
        logger.debug(item["keyList"])
        itemTmp = item
        itemTmp["file"] = f
        itemTmp["detail"] = markdown.markdown(itemTmp["detail"],extensions=['tables',
                                                                            'markdown.extensions.attr_list',
                                                                            'markdown.extensions.def_list',
                                                                            'markdown.extensions.fenced_code',
                                                                            'markdown.extensions.footnotes',
                                                                            'markdown.extensions.codehilite',
                                                                            "mdx_math"],
                                                                extension_configs={
                                                                            'mdx_math': {
                                                                                'enable_dollar_delimiter': True,  # 是否启用单美元符号（默认只启用双美元）
                                                                                'add_preview': True  # 在公式加载成功前是否启用预览（默认不启用）
                                                                            }
                                                                        })
        print(itemTmp["detail"])
        itemList.append(itemTmp)

    logger.debug(itemList)

    return  render_template('home.html', findStr=findStr, itemList=itemList, file_list=file_list)
    
        
        
@homeBlueprint.route('/form/<string:file>/<int:idx>/',methods=['GET','POST'])
# look up from All files, collect item content into a List.
# 遍历所有的json文件，找到关键字对于的内容列表
def formModify(file,idx):
    logger = current_app.log
    
    itemList = []
    findStr = ""
    file_list = []
    
    ### assumed only one dir.
    file_list = get_json_file_list()
            
    f = file

    itemListInJson = json_load_from_file(f)
    ## 遍历所有item.
    for item in itemListInJson:
        logger.debug(item)
        logger.debug(item["id"])
        if idx == item["id"]:
            itemTmp = item
            itemTmp["file"] = f

            return  render_template('ModifyForm.html', file_list=file_list, item=itemTmp)

@homeBlueprint.route('/form/new/',methods=['GET','POST'])
# look up from All files, collect item content into a List.
# 遍历所有的json文件，找到关键字对于的内容列表
def formAdd():
    logger = current_app.log
    to_file = ""
    itemList = []
    findStr = ""
    file_list = []
    
    ### assumed only one dir.
    file_list = get_json_file_list()

    return  render_template('AddForm.html', file_list = file_list, to_file = to_file)

@homeBlueprint.route('/form/new/<string:to_file>/',methods=['GET','POST'])
# look up from All files, collect item content into a List.
# 遍历所有的json文件，找到关键字对于的内容列表
def formAddToFile(to_file):
    logger = current_app.log
    
    itemList = []
    findStr = ""
    file_list = []
    
    ### assumed only one dir.
    file_list = get_json_file_list()

    return  render_template('AddForm.html', file_list=file_list,to_file = to_file)

    
@homeBlueprint.route('/modify/<string:file>/<int:idx>/',methods=['POST'])
# look up from All files, collect item content into a List.
# 遍历所有的json文件，找到关键字对于的内容列表
def modify(file,idx):
    logger = current_app.log
    file_list = []
    
    ### assumed only one dir.
    file_list = get_json_file_list()
            
    f = file
    newFile = file
    itemModify = dict()
    if request.method=='POST':
        for key in request.form:
            print(key)
            if key != "file":
                itemModify[key] = request.form[key]
            else:
                newFile = request.form[key]
        itemModify["id"] = idx
        keyList = itemModify["keyList"].split(",")
        print(keyList)
        itemModify["keyList"] = []
        for k in keyList:
            itemModify["keyList"].append(k.upper().strip())
        itemModify["keyList"] = list(filter(None,itemModify["keyList"]))
        print(request.form["detail"])
    else:
        return "not support get request !!!"
        
    if f == newFile:
        logger.critical("modify file:"+f+",id:"+str(idx))
        itemListInJson = json_load_from_file(f)
        itemListInJson = modify_by_id_in_list(idx, itemListInJson,itemModify)
        json_dump_to_file(f,itemListInJson)
    else:
        ## 增加到新的文件
        logger.critical("move item with idx:"+str(idx)+" from file："+ f +" to file:"+newFile)
        itemListInJson = json_load_from_file(newFile)
        itemListInJson.append(itemModify)
        json_dump_to_file(newFile,itemListInJson)
        ## 从旧的文件移除
        itemListInJson = json_load_from_file(f)
        del_by_id_in_list(idx, itemListInJson)
        json_dump_to_file(f,itemListInJson)
        
    im = itemModify
    im["file"] = newFile;
    return  render_template('ModifyForm.html', file_list=file_list, item=im)
    
    
@homeBlueprint.route('/add/',methods=['GET','POST'])
# look up from All files, collect item content into a List.
# 遍历所有的json文件，找到关键字对于的内容列表
def add():
    logger = current_app.log
    file_list = []
    newFile = ""
    recordFile = "record"
    record = dict()
    record = record_load_from_file()
    ### assumed only one dir.
    file_list = get_json_file_list()
            
    itemAdd = dict()
    if request.method=='POST':
        for key in request.form:
            print(key)
            if key != "file":
                itemAdd[key] = request.form[key]
            else:
                newFile = request.form[key]
        itemAdd["id"] = record["idx"]
        record["idx"] = record["idx"] + 1
        keyList = itemAdd["keyList"].split(",")
        print(keyList)
        itemAdd["keyList"] = []
        for k in keyList:
            itemAdd["keyList"].append(k.upper().strip())
            
    itemListInJson = json_load_from_file(newFile)
    
    logger.critical("add item in file:"+newFile+",id:"+str(record["idx"]-1))

        ## 增加item.
    itemListInJson.append(itemAdd)
    item = itemAdd
    item["file"] = newFile
        
    json_dump_to_file(newFile,itemListInJson)
    record_dump_to_file(record)
         
    return  render_template('ModifyForm.html', file_list=file_list, item=item)


@homeBlueprint.route('/refresh/record/',methods=['GET','POST'])
# look up from All files, collect item content into a List.
# 遍历所有的json文件，找到关键字对于的内容列表
def refresh():
    logger = current_app.log
    file_list = []
    itemList = []
    
    newFile = ""
    findStr="PDSCH"
    ### assumed only one dir.
    file_list = get_json_file_list()
            
    recordFile = "record"
    record = dict();
    record["idx"] = 0
    
    for f in file_list:
        ## read json from json file.
        ### This file path should be based on root path.  becasue it's just included by app.py, which is in root path. 
        itemListInJson = json_load_from_file(f)
        for i in range(len(itemListInJson)):
            logger.debug(i)
            itemListInJson[i]["id"] = record["idx"]
            record["idx"] += 1
            logger.debug(record["idx"])
            
        json_dump_to_file(f, itemListInJson)
    record_dump_to_file(record)

    logger.critical("refresh id in files, number:"+str(record["idx"]))

    return  render_template('home.html', findStr=findStr, itemList=itemList, file_list=file_list)
