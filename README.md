<h1>SALESMAN CHATBOT </h1>

## Overview

This project aims to create a chatbot that assists users in extracting product details from Amazon URLs. By simply pasting the product URL, the chatbot will fetch and display the necessary product information.

I have used deep learning pretrained Question-Answering model called ['deepset/roberta-base-squad2'](https://huggingface.co/deepset/roberta-base-squad2-covid) which is available on hugging face for free. For more details refer my [Blog](https://medium.com/@rajputharshal2002/unveiling-the-prototype-of-amazon-sales-assistant-chatbot-%EF%B8%8F-7fe6c1aaeb55)

## Technologies 

* Deep learning pretrained Question-Answering model called ['deepset/roberta-base-squad2'](https://huggingface.co/deepset/roberta-base-squad2-covid)

* [Dialogflow](https://dialogflow.cloud.google.com) provides basic framwork for chatbot

* [ngrok](https://ngrok.com/download) to get https url to connect dialogflow with backend

## Features

* Automated Information Extraction: Simply provide the product URL, and the chatbot will retrieve and display the relevant product details.
* Dialogflow Integration: Built using Dialogflow for smooth and natural conversational experiences.

## Future improvments

* Create a chrome extention

## Requirements

* [Dialogflow](https://dialogflow.cloud.google.com) account and agent set up using dialogflow.txt.
* Create account on ngrok and download [ngrok](https://ngrok.com/download)
* Python environment to handle backend processing (if applicable).

## Setup & Usage

* Dialogflow Setup:
Create a new agent or import the provided dialogflow.txt file.
Ensure that you have turned on webhook call for all intent by going into each intent scroll dwon and turn on webhook call
Train the agent with necessary intents and entities.

* Backend Setup (if applicable):
Clone the repository.
Install required Python packages.
Set up the backend server and link it with Dialogflow using appropriate webhooks i.e ngrok.
Step1: First clone the repository using
```sh
git clone https://github.com/harshayr/SALESMAN-CHATBOT.git
```

Step2: go into current working directory and move ngrok file manualy to this folder
```sh
cd SALESMAN_CHATTBOT
```

Step3: Install prerequisites by pasting below command to your terminal
```sh
pip install -r requirment.txt
```

Step4: Open terminal and go into current working directory using step2 command and after use 
```sh
ngrok http 5000
```

Step5: Copy forwarding https url which will look like (Forwarding = https://7280-103-199-193-46ngrok-free.app)
 
Step6: Past that url into dialogflow fulfillment webhook section and save

step7: Go to integrations and select web demo copy url and paste in other tab and now you can see a chatbot interface where you can paste a link and get information about product according to your need 

* Usage:
Access the chatbot via the provided interface or platform.
Provide the product URL when prompted.
Interact with the chatbot to receive product details which will save your time and energy.
Enhance user shopping experience


For more details refer my [Blog](https://medium.com/@rajputharshal2002/unveiling-the-prototype-of-amazon-sales-assistant-chatbot-%EF%B8%8F-7fe6c1aaeb55)


