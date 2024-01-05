import pandas as pd
import numpy
import requests
from bs4 import BeautifulSoup

from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline

headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win 64 ; x64) Apple WeKit /537.36(KHTML , like Gecko) Chrome/80.0.3987.162 Safari/537.36'}


model_name = "deepset/roberta-base-squad2"
model = AutoModelForQuestionAnswering.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

nlp = pipeline('question-answering', model=model, tokenizer=tokenizer)

# def specs_fallback(url:str):
    
#     webpage=requests.get(url,headers = headers).text
#     soup = BeautifulSoup(webpage, "lxml")
    
#     id_spec = soup.find_all("div", class_ = "a-expander-content")
#     len(id_spec)

#     all_spec = []
#     for i in id_spec:
#         truncate = i.find_all("table", class_ = "a-keyvalue")
#         all_spec.append(truncate)


#     flat_list_spec = [item for sublist in all_spec for item in sublist if sublist]


#     tr = []
#     for i in flat_list_spec:
#         rows = i.find_all('tr')
#         tr.append(rows)



#     data_list= []
#     for i in tr:
#         for j in i:
#             truncate_1 = j.find("th", class_ = "a-color-secondary").text.strip()
#             truncate_2 = j.find("td", class_ = "a-size-base").text.strip().strip('\u200e')
#             data_list.append({
#                 truncate_1: truncate_2
#             })
#     unique_keys = set()
#     result = []

#     for item in data_list:
#         keys = set(item.keys())
#         if not keys.intersection(unique_keys):  # Check if any key has already been seen
#             result.append(item)
#             unique_keys.update(keys)
#     return result

# def name(url:str):
    
#     webpage=requests.get(url,headers = headers).text
#     soup = BeautifulSoup(webpage, "lxml")
    
    
#     product_name = []
#     for i in range(1):
#         text = soup.find_all('span', {'class': 'a-size-large product-title-word-break', 'id': 'productTitle'})[i].text
#         product_name.append(text)
#     #     print(text.strip())
#     return product_name

def about_fallback(url:str):
    
    webpage=requests.get(url,headers = headers).text
    soup = BeautifulSoup(webpage, "lxml")

    # product_name
    product_name = []
    for i in range(1):
        text = soup.find_all('span', {'class': 'a-size-large product-title-word-break', 'id': 'productTitle'})[i].text
        product_name.append(text)
    
    # specs
        id_spec = soup.find_all("div", class_ = "a-expander-content")
    len(id_spec)

    all_spec = []
    for i in id_spec:
        truncate = i.find_all("table", class_ = "a-keyvalue")
        all_spec.append(truncate)


    flat_list_spec = [item for sublist in all_spec for item in sublist if sublist]


    tr = []
    for i in flat_list_spec:
        rows = i.find_all('tr')
        tr.append(rows)



    data_list= []
    for i in tr:
        for j in i:
            truncate_1 = j.find("th", class_ = "a-color-secondary").text.strip()
            truncate_2 = j.find("td", class_ = "a-size-base").text.strip().strip('\u200e')
            data_list.append({
                truncate_1: truncate_2
            })
    unique_keys = set()
    result = []

    for item in data_list:
        keys = set(item.keys())
        if not keys.intersection(unique_keys):  # Check if any key has already been seen
            result.append(item)
            unique_keys.update(keys)
    specs = []
    for dic in result:
        x = dic
        specs.append(f"{list(x.keys())[0]} is {list(x.values())[0]}")

    
    # about info
    id_about = soup.find_all("div", class_ = "centerColAlign")
    len(id_about)

    about_1 = []
    for i in id_about:
        truncate = i.find_all("li", class_ = "a-spacing-mini")
        about_1.append(truncate)



    flat_list_abt = [item for sublist in about_1 for item in sublist if sublist]


    about_2= []
    for i in flat_list_abt:
        truncate = i.find('span', class_ = "a-list-item").text.strip()
        about_2.append(truncate)

    

    # product_name = name(url)
    # s = specs_fallback(url)
    # specs = []
    # for dic in s:
    #     x = dic
    #     specs.append(f"{list(x.keys())[0]} is {list(x.values())[0]}")
    
    content = product_name + about_2 + specs
    result =get_str_fallback(content)
    return result





def get_str_fallback(offr:list):
    result = "   ".join(offr)
    return result



# def fallback(url:str, que):
#     result = about_fallback(url)
#     dic = nlp({
#     "question":que,
#     "context": result
# })
#     ans = dic['answer']
#     score = dic['score']
#     if score>0.01:
#         pass
#     elif score>0.005:
#         pass
#     else:
#         pass


# product name
    
# product name



