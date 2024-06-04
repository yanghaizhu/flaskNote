from flask import Blueprint,request,redirect, current_app
import json

import markdown
import os
def str_upper_split_to_list(string):
    l = [s.strip().upper() for s in string.split(",")]
    current_app.log.debug(l)
    return l
    

def search_revers_action_flag(string):
    current_app.log.debug(string)
    return string.startswith("-") or string.startswith("!")
    
def markdownToHtmlWithExtensions(mdString):
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