def replace_in_keys(d, str1, str2):
    if isinstance(d, dict):
        return {k.replace(str1, str2): replace_in_keys(v, str1, str2) for k, v in d.items()}
    elif isinstance(d, list):
        return [replace_in_keys(item, str1, str2) for item in d]  # Handle lists by applying replace_keys to each item
    return d  # Return other data types unchanged

def list_elems_to_string(col):
    return col.apply(lambda x: ','.join(map(str, x)) if isinstance(x, list) else x)