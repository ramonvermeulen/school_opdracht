def cgi_field_storage_to_dict(field_storage):
    params = {}
    for key in field_storage.keys():
        params[key] = field_storage[key].value
    return params
