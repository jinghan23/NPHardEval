import urllib.request
import json
import os
import ssl
import requests
import pandas as pd


'''
Close-source models
- GPT-4-turbo, 
- GPT-3.5-turbo, 
- Claude 2, 
- Claude 2 Instant, and 
- PaLM 2
'''

from openai import OpenAI
import anthropic

# !pip install google-cloud-aiplatform;
# from google.cloud import aiplatform
import vertexai
from vertexai.preview.language_models import TextGenerationModel, ChatModel
#get_ipython().system('gcloud auth application-default login')

### Load secrets
SECRET_FILE = '../../../secrets.txt'
with open('../../secrets.txt') as f:
    lines = f.readlines()
    for line in lines:
        if line.split(',')[0].strip() == "open_ai_key":
            open_ai_key = line.split(',')[1].strip()
        if line.split(',')[0].strip() == "anthropic_key":
            anthropic_key = line.split(',')[1].strip()

openai_client = OpenAI(api_key=open_ai_key)
claude_client = anthropic.Anthropic(api_key=anthropic_key)

### Run Models
# GPT models (GPT-3.5 and GPT-4)
def run_gpt(text_prompt, max_tokens_to_sample: int = 2000, temperature: float = 0, client=openai_client, model = "gpt-3.5-turbo"):
    # use gpt-3.5-turbo unless specify gpt-4
    response = client.chat.completions.create(
      model = model, 
      messages=[
        {"role": "user", "content": text_prompt},
      ],
      temperature=temperature,
      max_tokens=max_tokens_to_sample
    )
    return response.choices[0].message.content


# Claude 2 models (Claude 2 and Claude 2 Instant)
def run_claude(text_prompt, max_tokens_to_sample: int = 2000, temperature: float = 0, client=claude_client, model = "claude-instant-1.2"):
    # use claude-instant unless specify claude-2
    prompt = f"{anthropic.HUMAN_PROMPT} {text_prompt}{anthropic.AI_PROMPT}"
    resp = client.completions.create(
        prompt=prompt,
        stop_sequences=[anthropic.HUMAN_PROMPT],
        model=model, # model="claude-v1.3-100k",
        max_tokens_to_sample=max_tokens_to_sample,
        temperature=temperature,
    ).completion
    return resp

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

'''
Open-source models (choose from below, in total 5 models)

- [v] Vicuna
- [v] Mistral-7b
- [v] Yi-34b
- [v] Phi
- [v] baichuan
- Falcon
- Fuyu
- LlaMa 2
- LLaMa 1
- Alpaca
- UltraLM
'''

# from vllm import LLM, SamplingParams

# # TODO: add open-source models
# def run_mistral(text_prompt):
#     sampling_params = SamplingParams(temperature=0, max_tokens=512)
#     llm = LLM(
#         model='mistralai/Mistral-7B-Instruct-v0.1',
#         tensor_parallel_size=4, 
#         max_num_seqs=4,
#         max_num_batched_tokens=4 * 4096,
#     )
#     predictions = llm.generate(text_prompt, sampling_params)
#     return predictions

# def run_yi(text_prompt):
#     sampling_params = SamplingParams(temperature=0, max_tokens=512)
#     llm = LLM(
#         model='yi-ai/llm-yi-34b',
#         tensor_parallel_size=4, 
#         max_num_seqs=4,
#         max_num_batched_tokens=4 * 4096,
#     )
#     predictions = llm.generate(text_prompt, sampling_params)
#     return predictions

# def run_vicuna(text_prompt):
#     sampling_params = SamplingParams(temperature=0, max_tokens=512)
#     llm = LLM(
#         model='lmsys/vicuna-13b-v1.3',
#         tensor_parallel_size=4, 
#         max_num_seqs=4,
#         max_num_batched_tokens=4 * 4096,
#     )
#     predictions = llm.generate(text_prompt, sampling_params)
#     return predictions

# def run_phi(text_prompt):
#     sampling_params = SamplingParams(temperature=0, max_tokens=512)
#     llm = LLM(
#         model='microsoft/phi-1_5',
#         tensor_parallel_size=4, 
#         max_num_seqs=4,
#         max_num_batched_tokens=4 * 4096,
#     )
#     predictions = llm.generate(text_prompt, sampling_params)
#     return predictions

# def run_baichuan(text_prompt):
#     sampling_params = SamplingParams(temperature=0, max_tokens=512)
#     llm = LLM(
#         model='baichuan-inc/Baichuan-13B-Chat',
#         tensor_parallel_size=4, 
#         max_num_seqs=4,
#         max_num_batched_tokens=4 * 4096,
#     )
#     predictions = llm.generate(text_prompt, sampling_params)
#     return predictions

if __name__ == '__main__':
    # try claude2-instant
    resp = run_claude(text_prompt= "I am a human, and I am a", model="claude-instant-1.2") # claude-2 works
    print(resp)