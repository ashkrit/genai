import json
import requests


def ask_local(model:str,conversation:[]) -> str:
    url = "http://0.0.0.0:11434/api/chat"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages":conversation,
        "stream":True
    }
    reply = requests.post(url, headers=headers, data=json.dumps(data))
    reply.raise_for_status()

    buffer=""

    for line in reply.iter_lines():
       body = json.loads(line)
       message = body["message"]
       buffer+=message["content"]
    
    return buffer

if __name__ == "__main__":
    messages = []

    while True:
        question = input("Ask me something >: ")
        if question == "exit":
            break
        messages.append({"role": "user", "content": question})
        print("Reply >:")
        reply = ask_local("llama3", messages)
        print(reply)
        messages.append({"role": "assistant", "content": reply})
    

