from flask import Blueprint,request,redirect, current_app
import json
from stringHandler import *
import os
def search_in_key_list(search, key_list):
    return search in key_list

def search_in_title(search, title):
    return search.upper() in title.upper()

def search_res_as_expected(search, key_list):
    if search_revers_action_flag(search) and not search_in_title(search[1:], key_list):
        return True
    elif not search_revers_action_flag(search) and search_in_title(search, key_list):
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

