
# coding: utf-8

# **Задание.**
# 
# На основе `public_table.csv` составьте новую таблицу с колонками `nct_id`, `min_age_days`, `max_age_days`, `is_for_man`, `is_for_woman`, `criteria`, `number_of_inclusion_criteria`, `number_of_exclusion_criteria`.
# 
# В колонке `min_age_days` и `max_age_days` необходимо записать число - количество дней. Если не указан минимальный возраст - указать 0 дней, если не указан максимальный возраст, указать 73000 (200 лет - считаем, что до такого возраста человек не живет). Единицы, меньше дня, округлять вниз (например 26 часов - это 1 день).
# 
# В колонке `is_for_man` и `is_for_woman` необходимо указать True или False - определить подходит ли испытания для мужчины или женщины сооветственно. Если в оригинальной таблице описание гендера пусто - считаем, что подходит всем.
# 
# В колонке `criteria` необходимо указать исправленный текст критериев - в этом тексте должны быть исправлены проблемы кодировки, а также нормализован unicode.
# 
# Для колонки `number_of_inclusion_criteria` и `number_of_exclusion_criteria` необходимо подсчитать количество критериев включения и исключения соответственно. Это число необходимо посчитать, применив смекалку и распарсив текст критериев. Обратите внимание, что формат описания этих критериев может слегка отличаться. Если информация вообще не представлена, то нужно выставить 0.
# 
# Учитывая неоднозначность задания, ваша задача - максимизировать процент правильных значнией в финальной таблице, а не пытаться составить идеальную правильную таблицу. Значения, близкие к правильным, также будут засчитываться, но с соответствующим штрафом.
# 
# Итоговую таблицу нужно положить в формате csv в файл `result.csv`.

# In[1]:


import pandas as pd


# In[10]:


data = pd.read_csv('public_table.csv', index_col=0)


# In[11]:


data.head()


# # Age

# In[29]:


import re
from math import floor

def age_to_days(s: str, fill_value: int=0) -> int:
    if pd.isna(s):
        return fill_value
    age_pattern = re.compile(r'([0-9]+) (\w+)')
    match = re.match(age_pattern, s)
    
    number = int(match.group(1))
    unit = match.group(2)
    
    convert_map = {
        "Years": 365,
        "Year": 365,
        "Months": 30,
        "Month": 30,
        "Weeks": 7,
        "Week": 7,
        "Day": 1,
        "Days": 1,
        "Hour": 1. / 24,
        "Hours": 1. / 24,
        "Minute": 1. / (24 * 60),
        "Minutes": 1. / (24 * 60),
    }
    days = floor(number * convert_map[unit])
    return days


# In[30]:


from functools import partial

min_age_to_days = partial(age_to_days, fill_value=0)
max_age_to_days = partial(age_to_days, fill_value=73000)


# In[31]:


data['min_age_days'] = data['minimum_age'].apply(min_age_to_days)
data['max_age_days'] = data['maximum_age'].apply(max_age_to_days)


# # Gender

# In[40]:


def is_appropriate_to_man(value) -> bool:
    if pd.isna(value):
        return True
    man_patterns = [
        r'(?!wo)m[ae]n',
        r'(?!fe)males?',
        r'boy',
        r'prostate',
        r'erectile',
    ]
    for pattern in man_patterns:
        if re.search(pattern, value):
            return True
    return False

def is_for_woman(value) -> bool:
    if pd.isna(value):
        return True
    return not is_appropriate_to_man(value)


# In[41]:


data['is_for_man'] = data['gender_description'].apply(is_appropriate_to_man)
data['is_for_woman'] = data['gender_description'].apply(is_for_woman)


# # Criteria

# In[47]:


import ftfy
import unicodedata


def normalize_text(s:str) -> str:
    if pd.isna(s):
        return ''
    return unicodedata.normalize('NFKD', ftfy.fix_text(s))


# In[48]:


data['criteria'] = data['criteria'].apply(normalize_text)


# # Inclusion/exclusion criteria

#     Proposed heuristic for counting number of criterias: "-" followed by capital letter

# In[137]:


def calc_incl_num(s: str):
    s = s.replace('Inclusion', 'BEGIN')
    s = s.replace('Exclusion', 'END')
    substr = s[s.find('BEGIN'):s.find('END')]
    num = len(re.findall(r'\s-\s*[A-Z]', substr))
    return num

def calc_excl_num(s: str):
    s = s.replace('Exclusion', 'BEGIN')
    substr = s[s.find('BEGIN'):]
    num = len(re.findall(r'\s-\s*[A-Z]', substr))
    return num


# In[138]:


data['number_of_inclusion_criteria'] = data['criteria'].apply(calc_incl_num)


# In[139]:


data['number_of_exclusion_criteria'] = data['criteria'].apply(calc_excl_num)


# # Result

# In[143]:


data[['nct_id', 'min_age_days', 'max_age_days', 'is_for_man', 'is_for_woman', 'criteria', 'number_of_inclusion_criteria', 'number_of_exclusion_criteria']].to_csv('result.csv')

