import streamlit as st
import asyncio
import threading

import lib.gpt as gpt
import lib.bedrock as bedrock
from lib.memory import gpt_load, gpt_save
from lib.memory import model_load, model_save
from lib.memory import system_load, system_save
from lib.memory import access_key_load, access_key_save
from lib.memory import secret_access_key_load, secret_access_key_save
from lib.threads import BaseThreading
from streamlit.runtime.scriptrunner import add_script_run_ctx


st.set_page_config(page_title="GenAI Quickstart")
st.title('GenAI Quickstart')

# APIキーの読み込み
_openai_api_key = gpt_load()

openai_api_key = st.sidebar.text_input('OpenAI API Key', value=_openai_api_key, type="password")

if openai_api_key!="" and openai_api_key:
  gpt_save(openai_api_key)


# AWS Access keyの読み込み
_access_key = access_key_load()

access_key = st.sidebar.text_input('AWS アクセスキー', value=_access_key, type="password", help="AWSアカウントでアクセスキーを発行してください。以下のリンクから作成可能です。https://ap-northeast-1.console.aws.amazon.com/cloudformation/home?region=ap-northeast-1#/stacks/quickcreate?templateURL=https%3A%2F%2Fmorita-chikara-ai-quick.s3.ap-northeast-1.amazonaws.com%2Frole.yml&stackName=ai-quick-user")

if access_key!="" and access_key:
  access_key_save(access_key)

# AWS Secret Access keyの読み込み
_secret_access_key = secret_access_key_load()

secret_access_key = st.sidebar.text_input('AWS シークレットアクセスキー', value=_secret_access_key, type="password")

if secret_access_key!="" and secret_access_key:
  secret_access_key_save(secret_access_key)


# モデル有効化の読み込み
_models = model_load(access_key, secret_access_key)
models = st.sidebar.text_area('モデル一覧（カンマ区切り）', value=_models, help="生成したいモデルのIDを入力してください。 例: gpt-3.5-turboなど　https://platform.openai.com/docs/models/overview")
if models!="" and models:
  model_save(models)

if st.sidebar.button('モデルの自動読み込み', type="primary"):
  print(access_key, secret_access_key)
  models = model_load(access_key, secret_access_key ,True)
  # print(models)
  model_save(models)

# systemの読み込み
_system  = system_load()

system = st.sidebar.text_input('システムプロンプト', value=_system)

if system!="" and system:
  system_save(system)


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
    execute_func = lambda : render(openai_api_key, system, text, model_name)
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
      # asyncio.run(model_multiple_request(text))
      # message = gpt.call(openai_api_key, system, text)
      # with st.chat_message("ChatGPT", avatar="🤖"):
      #   st.caption("ChatGPT")
      #   st.write(message)


