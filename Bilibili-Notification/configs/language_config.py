from defines import description

def get_string(id,*args,**kwargs):
    str_format = description.normal_desc[id]
    return str_format.format(*args,**kwargs)

