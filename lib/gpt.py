from openai import OpenAI

models = [
    "gpt-4-1106-preview",
    "gpt-3.5-turbo-1106"
]

def call(api_key, system, user, model_name="gpt-3.5-turbo"):
    try:
        client = OpenAI(api_key=api_key)
        completion = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user}
            ]
        )
    except Exception as e:
        return f"{e}"
    return completion.choices[0].message.content
    
