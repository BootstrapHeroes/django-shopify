def slice(objects, prop):
    """
        slice objects in sublist sharing a common propery
    """
    if not objects:
        return []

    def get_prop(obj, prop):
        if not isinstance(objects[0], dict):
            return obj.__dict__[prop]
        return obj[prop]
    
    set_objects = set([get_prop(o, prop) for o in objects])
    return [[o for o in objects if get_prop(o, prop) == obj] for obj in set_objects]


def convert_to_bool(data, params):

    for param in params:
        if not data[param]:
            data[param] = False
        else:
            if data[param] == "on":
                data[param] = True
            else:
                data[param] = bool(int(data[param]))


def normalize_url(url):

    if not url.startswith("http://") and not url.startswith("https://"):
        return "http://%s" % url
    return url