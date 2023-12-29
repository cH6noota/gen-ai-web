import boto3 
import json
import streamlit as st

def client_get(service_name, access_key, secret_access_key):
    if st.session_state["local_mode"]:
        print("Local")
        client = boto3.client(
                    service_name=service_name,
                    region_name="us-east-1"
        )
    else:
        client = boto3.client(
                    service_name=service_name,
                    region_name="us-east-1",
                    aws_access_key_id=access_key,
                    aws_secret_access_key=secret_access_key
        )
    return client



def list_model(access_key, secret_access_key):

    bedrock = client_get('bedrock', access_key, secret_access_key)
    try:
        res = bedrock.list_foundation_models()['modelSummaries']
    except Exception as e:
        print(e)
        return []        
    # 'modelId', 'inputModalities', 'modelLifecycle'
    res = filter(
        lambda x: 'TEXT' in x['inputModalities'] and 'TEXT' in x['outputModalities'], res
    )
    res = filter(
        lambda x: x['modelLifecycle']['status'] == 'ACTIVE', res
    )
    res = filter(
        lambda x: x['inferenceTypesSupported'] == ['ON_DEMAND'], res
    )
    res = map(lambda x:x["modelId"], res)
    return res

def call(access_key, secret_access_key, system, user, model_id):
    
    client = client_get('bedrock-runtime', access_key, secret_access_key)

    if "anthropic" in model_id:
        enclosed_prompt = system + "\nHuman: " + user + "\n\nAssistant:"
        body = {
            "prompt": enclosed_prompt,
            "max_tokens_to_sample": 512,
            "temperature": 0.5,
            "stop_sequences": ["\n\nHuman:"],
        }
        # model_id = model['modelArn']
    elif "llama" in model_id:
        body = {
                "prompt": system + "\n" + user,
                "temperature": 0.5,
                "top_p": 0.9,
                "max_gen_len": 512,
        }
    elif "titan" in model_id:
        # model_id = model["modelId"].split(":")[0]
        body = {
            "inputText": system + "\n" + user ,
            "textGenerationConfig": {
                "maxTokenCount": 512,
                "stopSequences": ["User:"],
                "temperature": 0.5,
                "topP":0.9
            }
        }
    elif "cohere" in model_id:
        body = {
            "prompt": system + "\n" + user ,
            "max_tokens": 512,
            "temperature": 0.5,
        }       
    else:
        body = {
            "prompt": system + "\n" + user ,
            "maxTokens": 512,
            "temperature": 0.5,
        }
    try:
        response = client.invoke_model(
            modelId=model_id,
            body=json.dumps(body),
            contentType="application/json",
            accept="application/json",
        )
    except Exception as e:
        print(e)
        return f"{e}"
    response_body = json.loads(response.get('body').read())
    # print(response_body)
    if response_body.get('completions'):
        outputText = response_body.get('completions')[0].get('data')["text"]
    elif response_body.get('generations'):
        outputText = response_body.get('generations')[0].get('text')
    elif response_body.get('generation'):
        outputText = response_body.get('generation')
    else:
        outputText = response_body.get('results')[0].get('outputText')
    return outputText
    

# for model in list_model():
#     print(model["modelId"])
#     print(call("", "", model))
    # if "anthropic.claude" in model["modelId"]:
    #     print(model)
        