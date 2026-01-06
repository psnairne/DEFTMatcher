import json
from ollama import chat, ChatResponse


class OllamaClient:

    model_name: str

    def __init__(self, model_name: str):

        self.model_name = model_name

    def query(self, system_message: str, user_input: str) -> str:
        resp: ChatResponse = chat(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_input},
            ],
        )
        resp_json: dict = json.loads(resp.model_dump_json())
        return resp_json.get("message", {}).get("content", "")
