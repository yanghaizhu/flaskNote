from flask import Blueprint,request,redirect, current_app

import os
def str_upper_split_to_list(string):
    l = [s.strip().upper() for s in string.split(",")]
    current_app.log.debug(l)
    return l
    

def search_revers_action_flag(string):
    current_app.log.debug(string)
    return string.startswith("-") or string.startswith("!")
    
    