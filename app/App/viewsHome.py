from flask import Blueprint,request,redirect, current_app
from  flask import Flask, render_template, request, url_for, redirect,make_response,json, jsonify
from  wtforms import StringField, PasswordField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, EqualTo
import uuid
#str(uuid.uuid4()) to generate random string, used as unique string. like id.

#from .models import *
import json
import jmespath
import os
from werkzeug.utils import *
import html
import markdown
from mermaid import *
from .stringHandler import *
from .jsonFileHandler import *
from .actionHandler import *

# blueprint is used for route. Blueprint would be used at create_app, in __init__.py. 
# We can have more blueprints, with different name, and at create_app side, register them one by one.
homeBlueprint = Blueprint('home', __name__)

@homeBlueprint.route('/find/<string:findStrings>/',methods=['GET','POST'])
# look up from All files, collect item content into a List.
# 遍历所有的json文件,遍历字典，找到关键字对于的内容列表
def findListByItem(findStrings):
    logger = current_app.log
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
    
    ## 把之前的list结构的json文件 转换为 dict结构的json文件 需要调用的时候打开，转换完后注释掉。
    ##json_from_list_to_dict("1","2")
    
    
    uuid_to_title = dict()
    uuid_to_title = uuidTitle_load_from_file()
    itemList = []
    for f in file_list:
        ## read json from json file.
        ### This file path should be based on root path.  becasue it's just included by app.py, which is in root path. 
        itemListInJson = json_load_from_file(f)
        print(f)
        ## 遍历所有item.
        for k,item in itemListInJson.items():
            allConditionMeet = True
            for search in search_key_list:
#                print(item)
                if not search_res_as_expected(search, item["keyList"]):
                    allConditionMeet = False
            if allConditionMeet:
                itemTmp = item
                itemTmp["file"] = f
                itemTmp["detail_html"] = markdownToHtmlWithExtensions(itemTmp["detail"])
                itemList.append(itemTmp)

    return  render_template('home.html', findStr=findStr, itemList=itemList, file_list=file_list)
    

@homeBlueprint.route('/show/<string:file>/',methods=['GET'])
# 整个文件里所有的内容list都显示出来。
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


    uuid_to_title = dict();
    uuid_to_title = uuidTitle_load_from_file()

    f = file
    logger.debug(f)
    print(f)

    ## read json from json file.
    ### This file path should be based on root path.  becasue it's just included by app.py, which is in root path. 
    itemListInJson = json_load_from_file(f)
    ## 遍历所有item.
    for k,item in itemListInJson.items():
        logger.debug(item)
        logger.debug(findStr)
        logger.debug(item["keyList"])
        itemTmp = item
        itemTmp["file"] = f
        itemTmp["detail_html"] = markdownToHtmlWithExtensions(itemTmp["detail"])
        print(itemTmp["detail"])
        itemList.append(itemTmp)

    logger.debug(itemList)

    return  render_template('home.html', findStr=findStr, itemList=itemList, file_list=file_list)
    
@homeBlueprint.route('/form/<string:file>/<string:uuid>/',methods=['GET','POST'])
# look up from All files, collect item content into a List.
# 遍历所有的json文件，找到关键字对于的内容列表
def formModify(file,uuid):
    logger = current_app.log
    
    itemList = []
    findStr = ""
    file_list = []
    
    ### assumed only one dir.
    file_list = get_json_file_list()

    uuid_to_title = dict();
    uuid_to_title = uuidTitle_load_from_file()
    f = file

    itemListInJson = json_load_from_file(f)
    ## 遍历所有item.
    for k,item in itemListInJson.items():
        logger.debug(item)
        print(uuid)
        if uuid == item["uuid"]:
            itemTmp = item
            itemTmp["file"] = f
            itemTmp["detail_html"] = markdownToHtmlWithExtensions(itemTmp["detail"])
            return  render_template('ModifyForm.html', file_list=file_list, item=itemTmp)

    

@homeBlueprint.route('/modify/<string:file>/<string:uuid>/',methods=['POST'])
# look up from All files, collect item content into a List.
# 遍历所有的json文件，找到关键字对于的内容列表
def modify(file,uuid):
    logger = current_app.log
    file_list = []
    
    ### assumed only one dir.
    file_list = get_json_file_list()

    uuid_to_title = dict();
    uuid_to_title = uuidTitle_load_from_file()

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
        itemModify["uuid"] = uuid
        keyList = itemModify["keyList"].split(",")
        print(keyList)
        itemModify["keyList"] = []
        for k in keyList:
            itemModify["keyList"].append(k.upper().strip())
        itemModify["keyList"] = list(filter(None,itemModify["keyList"]))
        
        relationList = itemModify["relationList"].split(",")
        print(relationList)
        itemModify["relationList"] = []
        for k in relationList:
            itemModify["relationList"].append(k.strip())
        itemModify["relationList"] = list(filter(None,itemModify["relationList"]))
        
        itemModify["detail_html"] = markdownToHtmlWithExtensions(itemModify["detail"])
        print(itemModify["detail_html"])
    else:
        return "not support get request !!!"
        
    if f == newFile:
        logger.critical("modify file:"+f+",uuid:"+str(uuid))
        itemListInJson = json_load_from_file(f)
        #### to use uuid instead of uuid
        itemListInJson[uuid] = itemModify
        json_dump_to_file(f,itemListInJson)
    else:
        ## 目前设计中不支持新建一个文件，这部分会把内容增加到新的文件，或者移动到新文件中。
        logger.critical("move item with idx:"+str(uuid)+" from file："+ f +" to file:"+newFile)
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
    
    uuid_to_title = dict();
    uuid_to_title = uuidTitle_load_from_file()
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


@homeBlueprint.route('/refresh/uuidTitle/',methods=['GET'])
# look up from All files, collect item content into a List.
# 遍历所有的json文件，找到关键字对于的内容列表
def refreshuuidTitle():
    logger = current_app.log
    file_list = []
    itemList = []
    
    newFile = ""
    findStr="PDSCH"
    ### assumed only one dir.
    file_list = get_json_file_list()
            
    uuid_to_title = dict();
    uuid_to_title = uuidTitle_load_from_file()

    for f in file_list:
        ## read json from json file.
        ### This file path should be based on root path.  becasue it's just included by app.py, which is in root path. 
        itemListInJson = json_load_from_file(f)
        for i in range(len(itemListInJson)):
            logger.debug(i)
            uuid_to_title[itemListInJson[i]["uuid"]] = itemListInJson[i]["title"]
            
    uuidTitle_dump_to_file(uuid_to_title)


    return  render_template('home.html', findStr=findStr, itemList=itemList, file_list=file_list)



@homeBlueprint.route('/',methods=['GET'])
def index():
    logger = current_app.log
    ## collect file name into a list.
    ## 文件名列表
    file_list = []
    
    itemList = []
    findStr = ""

    uuid_to_title = dict();
    uuid_to_title = uuidTitle_load_from_file()


    logger.debug(itemList)

    return  render_template('home.html', findStr=findStr, itemList=itemList, file_list=file_list)
    
        

    
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

    uuid_to_title = dict();
    uuid_to_title = uuidTitle_load_from_file()

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
        
        keyList = list(filter(None,re.split(",",itemAdd["keyList"])))
        relationList = list(filter(None,re.split(",",itemAdd["relationList"])))
        itemAdd["keyList"] = []
        itemAdd["relationList"] = []
        for k in keyList:
            itemAdd["keyList"].append(k.upper().strip())
        for r in relationList:
            itemAdd["relationList"].append(r.strip())
        itemAdd["uuid"] = str(uuid.uuid4()).replace('-','')
            
            
    itemListInJson = json_load_from_file(newFile)
    
    logger.critical("add item in file:"+newFile+",id:"+str(record["idx"]-1))

        ## 增加item.
    itemListInJson[itemAdd["uuid"]] = itemAdd
    item = itemAdd
    item["file"] = newFile
        
    json_dump_to_file(newFile,itemListInJson)
    record_dump_to_file(record)
         
    return  render_template('ModifyForm.html', file_list=file_list, item=item)



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

@homeBlueprint.route('/uuid/<string:uuid>/',methods=['GET'])
# look up from All files, collect item content into a List.
# 遍历所有的json文件，找到关键字对于的内容列表
def searchByuuid(uuid):
    logger = current_app.log
    file_list = []
    itemList = []
            
    logger = current_app.log
    findStr = ""
                
    ## collect file name into a list.
    ## 文件名列表
    file_list = get_json_file_list()   
    im = dict()
    
    uuid_to_title = dict();
    uuid_to_title = uuidTitle_load_from_file()

    for f in file_list:
        ## read json from json file.
        ### This file path should be based on root path.  becasue it's just included by app.py, which is in root path. 
        itemListInJson = json_load_from_file(f)
        print(f)
        ## 遍历所有item.
        item = itemListInJson[uuid]
        im = item
        im["file"] = f
        im["detail_html"] = markdownToHtmlWithExtensions(im["detail"])
        itemList.append(im)
        return  render_template('home.html', findStr=findStr, itemList=itemList, file_list=file_list)

    return  render_template('home.html', findStr=findStr, itemList=itemList, file_list=file_list)
