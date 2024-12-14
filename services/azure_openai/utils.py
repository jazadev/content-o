import csv
import re
import json
from datetime import datetime, timedelta

def get_prompt(role):
    prompt_path = f"services/azure_openia/prompts/{role}.txt"
    with open(prompt_path, 'r', encoding="utf-8") as file:
        rfile = file.read()
    return rfile


def get_tools(role):
    prompt_path = f"services/azure_openia/tools/{role}.json"
    with open(prompt_path, 'r', encoding="utf-8") as file:
        rfile = file.read()
    return [convert_to_json(rfile), ]


def clean_data(data):
    try:
        value = data["choices"][0]["message"]["content"]
    except Exception as e:
        print(e)
        value = ''
    value_delete_list = [
        "==== START CONTENT ",
        " END ====",
        "## Task Input:",
        "```",
        "json",
    ]
    for value_delete in value_delete_list:
        value = value.replace(value_delete, "")
    return value.strip().strip('"')


def get_usage_tokens(value):
    default_ = {
        "completion_tokens": 0,
        "prompt_tokens": 0,
        "total_tokens": 0
    }
    #result = value.get("usage", None)
    if hasattr(value, 'usage'):
        return {
            "completion_tokens": value.usage.completion_tokens,
            "prompt_tokens": value.usage.prompt_tokens,
            "total_tokens": value.usage.total_tokens
        }
    #if result is None:
    #    return default_
    return default_

    try:
        return result.to_dict()
    except Exception as e:
        print(e)
        return default_


def print_error(error, mensaje):
    print("-" * 80)
    print(f"error: {str(error)}")
    print(f"mensaje: {mensaje}")
    print("-" * 80)


def convert_to_json(data):
    try:
        return json.loads(data)
    except Exception as e:
        print(f"JSON encoding error. Detail: {e}")
        return {
            "ERROR": "json encoding error"
        }
    

def get_date_from_str(date_str):
    if not date_str:
        return None
    
    possible_formats = ["%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%Y/%m/%d"]

    for formato in possible_formats:
        try:
            object_date = datetime.strptime(date_str, formato)
            return object_date
        except ValueError:
            continue  

    return date_str

def parse_json_safely(item):
    if isinstance(item, dict):
        return item
    if isinstance(item, str):
        try:
            return json.loads(item)
        except:
            if isinstance(item, list):
                return [i for i in item]
            return item
    return item


def read_csv(path):
    with open(path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)
        data = []
        for row in reader:
            data.append(row)
    return header, data

def normalize(text):
    accent_map = {
        'á': 'a',
        'é': 'e',
        'í': 'i',
        'ó': 'o',
        'ú': 'u',
        'Á': 'A',
        'É': 'E',
        'Í': 'I',
        'Ó': 'O',
        'Ú': 'U'
    }
    
    def replace_accent(match):
        char = match.group()
        if char in accent_map:
            return accent_map[char]
        else:
            return char
    
    return re.sub(r'[áéíóúÁÉÍÓÚ]', replace_accent, text)

def search_word(word, header, data):
    """
    Search a word in the CSV data and return the rows that matched the word.

    Parameters
    ----------
    word : str
        The word to search
    header : list
        The header of the CSV file
    data : list
        The data of the CSV file

    Returns
    -------
    A list of dict, where each dict is a row of the CSV file that contains the word.
    """
    word_pattern = re.compile(f'(?i)\\b{re.escape(normalize(word))}\\b')
    list_match = []
    for row in data:
        for cell in row:
            if word_pattern.search(normalize(cell)):
                list_match.append(row)
    return [dict(zip(header, row)) for row in list_match]


