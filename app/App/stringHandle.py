
def str_upper_split_to_list(string):
    l = [s.strip().upper() for s in string.split(",")]
    current_app.log.debug(l)
    return l
    