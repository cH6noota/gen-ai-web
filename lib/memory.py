import streamlit as st
from lib.bedrock import list_model
from lib.gpt import models

gpt_key = []

@st.cache_resource
def gpt_data():
    return []

def gpt_load():
    global gpt_key
    gpt_key = gpt_data()
    return gpt_key[0] if len(gpt_key)==1 else ""

def gpt_save(value):
    global gpt_key
    if len(gpt_key)!=0:
        gpt_key.clear()
    gpt_key.append(value)


model_data = []

@st.cache_resource
def model_data_get():
    return []

def model_load(access_key, secret_access_key, reload=False):
    global model_data
    model_data = model_data_get()
    if len(model_data)==1 and reload==False:
        if model_data[0].replace(" ","").replace("　","") != "":
            return model_data[0]
    data = list(list_model(access_key, secret_access_key))+ models
    text = ",".join(data)
    return text
    

def model_save(value):
    global model_data
    if len(model_data)!=0:
        model_data.clear()
    model_data.append(value)

system_data = []

@st.cache_resource
def system_data_get():
    return []

def system_load():
    global system_data
    system_data = system_data_get()
    return system_data[0] if len(system_data)==1 else "あなたは優秀なAIアシスタントです"

def system_save(value):
    global system_data
    if len(system_data)!=0:
        system_data.clear()
    system_data.append(value)

# アクセスキー
access_key = []

@st.cache_resource
def access_key_get():
    return []

def access_key_load():
    global access_key
    access_key = access_key_get()
    return access_key[0] if len(access_key)==1 else ""

def access_key_save(value):
    global access_key
    if len(access_key)!=0:
        access_key.clear()
    access_key.append(value)


# シークレットアクセスキー
secret_access_key = []

@st.cache_resource
def secret_access_key_get():
    return []

def secret_access_key_load():
    global secret_access_key
    secret_access_key = secret_access_key_get()
    return secret_access_key[0] if len(secret_access_key)==1 else ""

def secret_access_key_save(value):
    global secret_access_key
    if len(secret_access_key)!=0:
        secret_access_key.clear()
    secret_access_key.append(value)
