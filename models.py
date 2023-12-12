import urllib.request
import json
import os
import ssl
import requests
import time
import pandas as pd


'''
Close-source models
Included:
- GPT-4-turbo, 
- GPT-3.5-turbo, 
- Claude 2, 
- Claude 2 Instant, and 
- PaLM 2
TODO:
- Gemini
'''

from openai import OpenAI
import anthropic
from google.cloud import aiplatform
import vertexai
from vertexai.preview.language_models import TextGenerationModel, ChatModel

### Load secrets
SECRET_FILE = '../../secrets.txt'
with open('../../secrets.txt') as f:
    lines = f.readlines()
    for line in lines:
        if line.split(',')[0].strip() == "open_ai_key":
            open_ai_key = line.split(',')[1].strip()
        elif line.split(',')[0].strip() == "anthropic_key":
            anthropic_key = line.split(',')[1].strip()
        elif line.split(',')[0].strip() == "palm_project_id":
            palm_project_id = line.split(',')[1].strip()

openai_client = OpenAI(api_key=open_ai_key)
claude_client = anthropic.Anthropic(api_key=anthropic_key)
# vertexai.init(project = palm_project_id, location="us-central1")
# chat_model = ChatModel.from_pretrained("chat-bison@001")
### Run Models


# GPT models (GPT-3.5 and GPT-4)
def run_gpt(text_prompt, max_tokens_to_sample: int = 3000, temperature: float = 0, client=openai_client, model = "gpt-3.5-turbo"):
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
def run_claude(text_prompt, max_tokens_to_sample: int = 3000, temperature: float = 0, client=claude_client, model = "claude-instant-1.2"):
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

def run_palm(text_prompt, max_tokens_to_sample: int = 1000, temperature: float = 0, model = "chat-bison@001"):
    """Use Google PaLM chat model"""
    parameters = {
        "temperature": temperature, 
        "max_output_tokens": max_tokens_to_sample
    }
    chat = chat_model.start_chat()
    response = chat.send_message(text_prompt, **parameters)
    response = response.text
    time.sleep(2)
    return response

'''
Open-source models (choose from below, in total 5 models)
Inbcluded:
- [v] Vicuna
- [v] Mistral-7b
- [v] Yi-34b
- [v] Phi
- [v] baichuan
TODO:
- Falcon
- Fuyu
- LlaMa 2
- LLaMa 1
- Alpaca
- UltraLM
'''

# from vllm import LLM, SamplingParams

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

# if __name__ == '__main__':
#     # try claude2-instant
#     resp = run_palm(text_prompt= "I am a human, and I am a", model="chat-bison@001") # claude-2 works claude-instant-1.2
#     print(resp)
