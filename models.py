import urllib.request
import json
import os
import ssl
import requests
import pandas as pd

import openai

# !pip install google-cloud-aiplatform;
# from google.cloud import aiplatform
import vertexai
from vertexai.preview.language_models import TextGenerationModel, ChatModel
#get_ipython().system('gcloud auth application-default login')

SECRET_FILE = '/Users/lizhouf/Documents/16_SciTechSoc/secrets.txt'

# Falcon model
class AzureFalconDeployment:
    
    def __init__(self, model_size):
        
        key = f"azure_falcon{model_size}_key"
        
        self.api_key = self.read_api_key(key)
        
        self.allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.

        self.url = f'https://huggingface-eastus-falcon{model_size}.eastus.inference.ml.azure.com/generate'
        
        self.model_deployment = f'tiiuae-falcon-{model_size}-instruct'

    def read_api_key(self, key):
        with open(SECRET_FILE) as f:
            lines = f.readlines()
            for line in lines:
                if line.split(',')[0].strip() == key:
                    api_key = line.split(',')[1].strip()
                    return api_key
        
        raise Exception('Error, unable to find the api key')
        
    def allowSelfSignedHttps(self, allowed):
        # bypass the server certificate verification on client side
        if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
            ssl._create_default_https_context = ssl._create_unverified_context

    
    def get_output_azure_falcon(self, prompt):

        data = {
                'inputs': prompt,  
                "parameters": {
                    "temperature": 0.01,
                    "max_new_tokens": 512,
                }
            }
        
        body = str.encode(json.dumps(data))

        # The azureml-model-deployment header will force the request to go to a specific deployment.
        # Remove this header to have the request observe the endpoint traffic rules
        headers = {'Content-Type':'application/json', 
                   'Authorization':('Bearer '+ self.api_key), 
                   'azureml-model-deployment': self.model_deployment }

        req = urllib.request.Request(self.url, body, headers)

        response = urllib.request.urlopen(req)

        result = response.read()

        return json.loads(result)['generated_text']

# GPT-3.5 model
class AzureGPT:
    
    def __init__(self):
        openai.api_base = "https://prompt-engineering.openai.azure.com/"
        openai.api_type = 'azure'
        openai.api_version = '2023-05-15'

        openai.api_key, self.deployment_name = self.read_secrets()
        
    def read_secrets(self):
        with open(SECRET_FILE) as f:
            lines = f.readlines()
            for line in lines:
                if line.split(',')[0].strip() == "gpt_api_key":
                    gpt_key = line.split(',')[1].strip()
                elif line.split(',')[0].strip() == "gpt_deployment_name":
                    deployment_name = line.split(',')[1].strip()
        return gpt_key, deployment_name
    
    def get_gpt_output(self, prompt):
        """Use Azure gpt model"""
        response = openai.ChatCompletion.create(
            engine = self.deployment_name, 
            messages = [{"role": "user", "content": prompt}],
            temperature = 0)
        response = response['choices'][0]['message']['content']
        return response 


# GPT-4 model

# Claude 2 model

# LLaMa 2 model

# PaLM 2 model
class GooglePaLM():
    
    def __init__(self):
        """Initiate attributes in the GooglePaLM object"""
        self.project_id = self.read_secrets()
        vertexai.init(project = self.project_id, location="us-central1")
        self.chat_model = ChatModel.from_pretrained("chat-bison@001")
        self.generation_model = TextGenerationModel.from_pretrained("text-bison@001")
    
    def read_secrets(self):
        """Read PaLM project id from secrets file"""
        project_id = None
        with open(SECRET_FILE) as f:
            lines = f.readlines()
            for line in lines:
                if line.split(',')[0].strip() == "palm_project_id":
                    project_id = line.split(',')[1].strip()
        return project_id
    
    def get_palm_generation_output(self, prompt):
        """Use Google PaLM text generation model"""
        response = self.generation_model.predict(
            prompt = prompt,
            temperature = 0
        )
        response = response.text
        return response

    def get_palm_chat_output(self, prompt):
        """Use Google PaLM chat model"""
        parameters = {
            "temperature": 0, 
            "max_output_tokens": 256
        }
        chat = self.chat_model.start_chat()
        response = chat.send_message(prompt, **parameters)
        response = response.text
        return response
