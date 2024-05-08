import json
import requests
import os


def ask_groq(model:str,message:[]) -> str:
    url = "https://api.groq.com/openai/v1/chat/completions"
    api_key = os.getenv('gorq_key')
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": model,
        "messages":message,
        "stream":False,
        "temperature": 1,
        "max_tokens": 1024,
        "top_p": 1
    }
    reply = requests.post(url, headers=headers, data=json.dumps(data))
    reply_json = json.loads(reply.text)
    choice = reply_json["choices"]
    reply_message= choice[0]["message"]    
    return reply_message["content"]

if __name__ == "__main__":
    messages = []

    while True:
        question = input("Ask me something >: ")
        if question == "exit":
            break
        messages.append({"role": "user", "content": question})
        print("Reply >:")
        reply = ask_groq("llama3-8b-8192", messages)
        print(reply)
        messages.append({"role": "assistant", "content": reply})
    

