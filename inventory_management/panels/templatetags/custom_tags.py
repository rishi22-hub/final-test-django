from django import template

register = template.Library()

@register.filter(name='split_email')
def split_email(email):
    return email.split('@')[0]

@register.filter(name='split')
def split(input_string, char):
    return input_string.split(char)


@register.filter(name='path_matches')
def path_matches(path, paths_list):
    return path in paths_list


@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter(name='multiplied_by')
def multiplied_by(value, arg):
    return float(value) * int(arg)
