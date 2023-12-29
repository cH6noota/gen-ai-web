import streamlit as st
import asyncio
import threading

import lib.gpt as gpt
import lib.bedrock as bedrock
from lib.memory import model_load
from lib.threads import BaseThreading
from streamlit.runtime.scriptrunner import add_script_run_ctx


st.set_page_config(page_title="GenAI Quickstart")
st.title('GenAI Quickstart')

# ローカルモードの読み込み
if 'local_mode' not in st.session_state:
    st.session_state["local_mode"] = False

# APIキーの読み込み
if 'openai_api_key' not in st.session_state:
    st.session_state['openai_api_key'] = ''

openai_api_key = st.sidebar.text_input('OpenAI API Key', value=st.session_state['openai_api_key'], type="password")

if openai_api_key!="" and openai_api_key:
  st.session_state['openai_api_key'] = openai_api_key


# AWS Access keyの読み込み
if 'access_key' not in st.session_state:
    st.session_state['access_key'] = ''

access_key = st.sidebar.text_input('AWS アクセスキー', value=st.session_state['access_key'], type="password", help="AWSアカウントでアクセスキーを発行してください。以下のリンクから作成可能です。https://ap-northeast-1.console.aws.amazon.com/cloudformation/home?region=ap-northeast-1#/stacks/quickcreate?templateURL=https%3A%2F%2Fmorita-chikara-ai-quick.s3.ap-northeast-1.amazonaws.com%2Frole.yml&stackName=ai-quick-user")

if access_key!="" and access_key:
  st.session_state['access_key'] = access_key

# AWS Secret Access keyの読み込み
if 'secret_access_key' not in st.session_state:
    st.session_state["secret_access_key"] = ''

secret_access_key = st.sidebar.text_input('AWS シークレットアクセスキー', value=st.session_state["secret_access_key"], type="password")

if secret_access_key!="" and secret_access_key:
  st.session_state["secret_access_key"] = secret_access_key


# モデル有効化の読み込み
if 'models' not in st.session_state:
    st.session_state["models"] = model_load(access_key, secret_access_key)
models = st.sidebar.text_area('モデル一覧（カンマ区切り）', value=st.session_state["models"], help="生成したいモデルのIDを入力してください。 例: gpt-3.5-turboなど　https://platform.openai.com/docs/models/overview")
if models!="" and models:
  st.session_state["models"] = models

if st.sidebar.button('モデルの自動読み込み', type="primary"):
  print(access_key, secret_access_key)
  models = model_load(access_key, secret_access_key ,True)
  st.session_state["models"] = models

# systemの読み込み
if 'system' not in st.session_state:
    st.session_state["system"] = "あなたは優秀なAIアシスタントです"
system = st.sidebar.text_input('システムプロンプト', value=st.session_state["system"])

if system!="" and system:
  st.session_state["system"] = system

# localmode 
local_mode = st.sidebar.checkbox('ローカルモード', value=st.session_state["local_mode"])
if local_mode:
  st.session_state["local_mode"] = True



def render(openai_api_key, system, text, model_name):
  if "gpt" in  model_name:
    print("GPT", model_name,"実行開始")
    message = gpt.call(openai_api_key, system, text, model_name)
  else:
    print("Bedrock", model_name,"実行開始")
    message = bedrock.call(access_key, secret_access_key, system, text, model_name)
  # print(message)
  with st.chat_message(model_name):
    st.caption(model_name)
    st.write(message)
    print(model_name,"実行完了")


def model_multiple_request(text):
  # モデル名を取り出し
  threads = []
  for model_name in models.split(","):
    model_name = model_name.replace(" ","").replace("　","").replace("	","")
    execute_func = lambda : render(openai_api_key, st.session_state["system"], text, model_name)
    thread = BaseThreading(model_name, execute_func)
    add_script_run_ctx(thread)
    thread.start()
    threads.append(thread)
  for thread in threads:
    thread.join()


with st.form('my_form'):
  text = st.text_area('テキストを入力してください:', '')
  submitted = st.form_submit_button('Submit')
  if submitted:
    with st.spinner('しばらくお待ちください'):
      model_multiple_request(text)


