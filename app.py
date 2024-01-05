from flask import Flask, request, jsonify
import pandas as pd
import numpy
import requests
from bs4 import BeautifulSoup

from utils import about_fallback 

headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win 64 ; x64) Apple WeKit /537.36(KHTML , like Gecko) Chrome/80.0.3987.162 Safari/537.36'}

def get_str(offr:list):
    result = " * ".join(offr)
    return result
    

def offer(url:str):
    webpage=requests.get(url,headers = headers).text
    soup = BeautifulSoup(webpage, "lxml")
    li = soup.find_all("li",class_ = 'a-carousel-card')
    offr = []
    for i in li:
        ofr = i.find("span", class_ = "a-truncate-full")
        if ofr:
            ofr = ofr.text.strip()
            offr.append(ofr)
        else:
            pass
    if len(offr)>0:
        result = get_str(offr)
        return jsonify({"fulfillmentText":result})
    else:
        return jsonify({"fulfillmentText": "Seller not mention more details about product."})
    
    
    
def handle_url(data):
    url = data['queryResult']['queryText']
    return url

# about

def about(url:str):
    
    webpage=requests.get(url,headers = headers).text
    soup = BeautifulSoup(webpage, "lxml")
    
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
    if len(about_2)>0:
        result = get_str(about_2)
        return jsonify({"fulfillmentText":f"{result}"})
    else:
        return jsonify({"fulfillmentText": "Seller have not menstion about section of product details"})



# box content
def box_content(url:str):

    webpage=requests.get(url,headers = headers).text
    soup = BeautifulSoup(webpage, "lxml")

    id_box = soup.find_all("div", class_ = "a-section")


    box_cnt_1 = []
    for i in id_box:
        truncate = i.find_all("li", class_ = "postpurchase-included-components-list-item")
        box_cnt_1.append(truncate)

    flat_list = [item for sublist in box_cnt_1 for item in sublist if sublist]



    inbox= []
    for i in flat_list:
        truncate = i.find("span", class_ = "a-list-item").text.strip()
        inbox.append(truncate)
    if len(inbox)>0:
        result = get_str(inbox)
        # response = {"fulfillmentMessages": [{"text": {"text": [inbox]}}]}
        return jsonify({"fulfillmentText":f"You will get {result} in the box"})
    else:
        return jsonify({"fulfillmentText": "Seller have not mention box content"})

#specs

def format_as_readable_text(data_list):
    formatted_lines = [f"{entry['Key']}: {entry['Value']}" for entry in data_list]
    return "\n".join(formatted_lines)


def specs(url:str):
    
    webpage=requests.get(url,headers = headers).text
    soup = BeautifulSoup(webpage, "lxml")
    
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
    
    df = pd.DataFrame([(k, v) for dictionary in result for k, v in dictionary.items()], columns=['Key', 'Value'])
    
    if len(result)>0:
        # result = get_str(result)
        # df_json = df.to_json(orient='records')
        output_data = [{"Key": list(item.keys())[0], "Value": list(item.values())[0]} for item in result]
        formatted_text = format_as_readable_text(output_data)
        response = {"fulfillmentMessages": [{"text": {"text": [formatted_text]}}]}
        return jsonify({'fulfillmentText' : formatted_text})
    else:
        return jsonify({"fulfillmentText": "Seller have not mention specification"})

# pricez of product
def prices(url:str):
    
    webpage=requests.get(url,headers = headers).text
    soup = BeautifulSoup(webpage, "lxml")

    id = soup.find_all("div", class_ = "centerColAlign")

    all_offers = []
    for i in id:
        truncate = i.find_all("div", class_ = "a-section")
        all_offers.append(truncate)


    flat_list = [item for sublist in all_offers for item in sublist if sublist]


    snippet= []
    for i in set(flat_list):
        truncate = i.find_all('span', {'class': 'a-price'})
        snippet.append(truncate)


    flat_list_2 = [item for sublist in snippet for item in sublist if sublist]


    # offer price
    prices = []
    for i in flat_list_2:
        sp = BeautifulSoup(str(i), "html.parser")
        price_element = sp.find('span', {'class': 'a-price-whole'})
        if price_element:
            offer_price = price_element.text.strip()
            prices.append(offer_price)
        else:
            pass

    # actual price
    actual_price = []
    for i in flat_list_2:
        sp = BeautifulSoup(str(i), "html.parser")
        price_element = sp.find('span', {'class': 'a-offscreen'})
        if price_element:
            offer_price = price_element.text.strip()
            actual_price.append(offer_price)
        else:
            pass
    price_int = []
    for i in actual_price:
        price_without_symbol = i.replace("₹", "").replace(",", "")
        price = int(price_without_symbol)
        price_int.append(price)
    act_price = max(price_int)  
    return jsonify({"fulfillmentText": f"Offer price is this : ₹{prices[0]} "\
                    f"Actual price is this : ₹{act_price}"})
    
#Rating

def rating(url:str):
    webpage=requests.get(url,headers = headers).text
    soup = BeautifulSoup(webpage, "lxml")
    
    id_reviews = soup.find_all("div", class_ = "a-section")


    rating_1 = []
    for i in id_reviews:
        truncate = i.find_all("div", class_ = "a-fixed-left-grid")
        rating_1.append(truncate)


    flat_list_review = [item for sublist in rating_1 for item in sublist if sublist]


    rating_2= []
    for i in flat_list_review:
        truncate = i.find('div', class_ = "a-fixed-left-grid-col")
        rating_2.append(truncate)


    rating_3= []
    for i in rating_2:
        truncate = i.find('i', class_ = "a-icon")
        if truncate:
            rating_3.append(truncate)
        else:
            pass


    final_rating= []
    for i in rating_3:
        truncate = i.find('span', class_ = "a-icon-alt")
        if truncate:
            text = truncate.text.strip()
            final_rating.append(text)
        else:
            pass
    if len(final_rating)>0:
        result = get_str(final_rating)
        # response = {"fulfillmentMessages": [{"text": {"text": [inbox]}}]}
        return jsonify({"fulfillmentText":f"Overall rating for this product is"\
                        f"{result}"})
    else:
        return jsonify({"fulfillmentText": "No rating available for this product"})



# highly rated by cumtomer
def Highly_rated_by_customers_func(url:str):
    
    webpage=requests.get(url,headers = headers).text
    soup = BeautifulSoup(webpage, "lxml")
    
    Highly_rated_by_customers = soup.find_all("div", class_ = "a-cardui-body")
    len(Highly_rated_by_customers)

    Highly_rated_by_customers_1 = []
    for i in Highly_rated_by_customers:
        truncate = i.find_all("div", class_ = "a-container")
        Highly_rated_by_customers_1.append(truncate)



    flat_list_1 = [item for sublist in Highly_rated_by_customers_1 for item in sublist if sublist]


    Highly_rated_by_customers_2= []
    for i in flat_list_1:
        truncate = i.find('span', class_ = "a-size-small")
        if truncate:
            Highly_rated_by_customers_2.append(truncate.text.strip())
        else:
            pass
    if len(Highly_rated_by_customers_2)>0:
        result = get_str(Highly_rated_by_customers_2)
        # response = {"fulfillmentMessages": [{"text": {"text": [inbox]}}]}
        return jsonify({"fulfillmentText":f"Highly rated key points of product by customers are: {result}"})
    else:
        return jsonify({"fulfillmentText": "No rating available for this product"})


from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline

model_name = "deepset/roberta-base-squad2"
model = AutoModelForQuestionAnswering.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

nlp = pipeline('question-answering', model=model, tokenizer=tokenizer)

def fallback(url:str ,que):
    result = about_fallback(url)
    dic = nlp({
    "question":que,
    "context": result
})
    ans = dic['answer']
    score = dic['score']
    if score>0.01:
        return jsonify({"fulfillmentText": ans})
    elif score>0.005:
        return jsonify({"fulfillmentText": "Not sure exctly what your looking for but your can check her"\
                        f"{result}"})
    else:
        return jsonify({"fulfillmentText": "Seller have not mention those details"})



ul = []
app = Flask(__name__)




@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()

        # Extract the URL from the data

    intent = data["queryResult"]["intent"]["displayName"] 
    que = data["queryResult"]['queryText']
    response = {
            "fulfillmentText": "URL received and processed."
        }
    
    if intent == "url":
        url = handle_url(data)
        ul.append(url)
        return jsonify(response)
    
    elif intent == "Default-Fallback-Intent":
        result = fallback(ul[-1], que)
        return result  
    else:
         intent_handler_dict = {
	# 'price': price,
					'offer': offer,
				# 	'url': handle_url,
				#    'colours': color,
                #    "Default-Fallback-Intent": fallback,
                   "Highly_rated_by_customers":Highly_rated_by_customers_func,
				   "rating": rating,
                  "price" : prices,
				   "specs": specs,
				   "in-the-box": box_content,
				   "about-product": about
				}
         function = intent_handler_dict[intent]
         return function(ul[-1])
		

if __name__ == '__main__':
    app.run(debug=True)
    


