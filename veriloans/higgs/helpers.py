def without_keys(dict, keys, *args, **kwargs):
    return {x: dict[x] for x in dict if x not in keys}

def get_object_fields(object, dict, *args, **kwargs):
    return list(set(object.__dict__.keys()).intersection(dict.keys()))

def convert_date(date, *args, **kwargs):
    s = date.split('-')
    return F'{s[2]}-{s[1]}-{s[0]}'

def convert_date_separately(date, *args, **kwargs):
    s = date.split('-')
    return s[2], s[1], s[0]

def convert_date_from_DMY_to_YMD(date, *args, **kwargs):
    s = date.split('-')
    return f'{s[2]}-{s[1]}-{s[0]}'

def foundation(x, *args, **kwargs):
    match = {
        list: x[0],
    }
    return match.get(type(x), x)

def foundated_keys(dict, *args, **kwargs):
    return {x: foundation(dict[x]) for x in dict}
