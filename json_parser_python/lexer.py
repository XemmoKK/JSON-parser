from .constants import *

def lex_string(string):
    json_string = ''
    if string[0] == JSON_QUOTE:
        string = string[1:]
    else:
        return None, string

    for character in string:
        if character == JSON_QUOTE:
            return json_string, string[len(json_string)+1:]
        else:
            json_string += character

    raise Exception('Expected end of string quote')

def lex_number(string):
    json_number = ''
    number_characters = [str(number) for number in range(0, 10)] + ['-', 'e', '.']
    
    for character in string:
        if character in number_characters:
            json_number += character
        else:
            break

    rest = string[len(json_number):]

    if not len(json_number):
        return None, string

    if '.' in json_number:
        return float(json_number), rest

    return int(json_number), rest

def lex_bool(string):
    string_len = len(string)
    if string_len >= TRUE_LEN and string[:TRUE_LEN] == 'true':
        return True, string[TRUE_LEN:]
    elif string_len >= FALSE_LEN and string[:FALSE_LEN] == 'false':
        return False, string[FALSE_LEN:]

    return None, string

def lex_null(string):
    string_len = len(string)
    if string_len >= NULL_LEN and string[:NULL_LEN] == 'null':
        return True, string[NULL_LEN:]

    return None, string

def lex(string):
    tokens = []

    while len(string):
        json_string, string = lex_string(string)
        if json_string is not None:
            tokens.append(json_string)
            continue

        json_number, string = lex_number(string)
        if json_number is not None:
            tokens.append(json_number)
            continue

        json_bool, string = lex_bool(string)
        if json_bool is not None:
            tokens.append(json_bool)
            continue

        json_null, string = lex_null(string)
        if json_null is not None:
            tokens.append(None)
            continue

        character = string[0]
        if character in JSON_WHITESPACE:
            string = string[1:]
        elif character in JSON_SYNTAX:
            tokens.append(character)
            string = string[1:]
        else:
            raise Exception('Unexpected character: {}'.format(character))
