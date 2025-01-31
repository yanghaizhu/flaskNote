from flask import Blueprint,request,redirect, current_app
import json
import re
import markdown
import os
from jsonFileHandler import record_load_from_file_by_uuid, appendNewItemToFile
import uuid

def str_upper_split_to_list(string):
    l = [s.strip().upper() for s in string.split(",")]
    return l
    

def search_revers_action_flag(string):
    return string.startswith("-") or string.startswith("!")


def preProcessmarkdownFile(mdString):
    mdProString = mdString
    print(mdProString)
    pat = r'\[uuid\]([0-9a-fA-F]{32})'
    matchs = re.findall(pat, mdString)
    for uuidStr in matchs:
        content = record_load_from_file_by_uuid(uuidStr)
        mdProString = mdProString.replace('[uuid]'+uuidStr,content)
    print(mdProString)
    return mdProString
    

def preProcessmarkdown_newItem(mdString):
    mdProString = mdString
    pat = r'\[newstart\]([\s\S]*?)\[newend\]'
    matchs = re.findall(pat, mdString)
    for new in matchs:
        content = new
        uuidStr = str(uuid.uuid4()).replace('-','')
        
        appendNewItemToFile(uuidStr,content)
        
        mdProString = mdProString.replace('[newstart]'+content+'[newend]','[uuid]'+uuidStr)
    return mdProString
    
    
def markdownToHtmlWithExtensions(mdPreString):
    mdString = preProcessmarkdownFile(mdPreString)
    print(mdString)
    htmlString = markdown.markdown(
        mdString,
        extensions=[
            'tables',
            'markdown.extensions.attr_list',
            'markdown.extensions.def_list',
            'markdown.extensions.fenced_code',
            'markdown.extensions.footnotes',
            'markdown.extensions.codehilite',
            "mdx_math"
        ],
        extension_configs={
            'mdx_math': {
                'enable_dollar_delimiter': True,  # 是否启用单美元符号（默认只启用双美元）
                'add_preview': True  # 在公式加载成功前是否启用预览（默认不启用）
            }
        }
    )
    return htmlString