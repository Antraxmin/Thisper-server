from openai import OpenAI
import os
import re

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set")

openai_client = OpenAI(api_key=OPENAI_API_KEY)
class MyGPT:
    def __init__(self, role_system, role_assistant):
        self.role_system = role_system
        self.role_assistant = role_assistant
        self.requests = []
        self.responses = []
        self.questions = []
        self.answers = []
        self.token_count = []
        self.count = 0

        self.add_request("system", self.role_system)
        self.add_request("assistant", self.role_assistant)

    def clean_space(self, s):
        s = re.sub('(<br>)', '\n', s)
        s = re.sub('\n+', '\n', s)
        return s

    def add_request(self, role, content):
        if role == "user":
            self.questions.append(content)
        self.requests.append({"role": role, "content": content})

    def send_request(self):
        response = openai_client.chat_completions.create(
            model="gpt-3.5-turbo",
            messages=self.requests,
            temperature=0.8,
            max_tokens=2048,
            top_p=1
        )
        self.responses.append(response)
        self.answers.append(response.choices[0].message.content)
        self.add_request("assistant", response.choices[0].message.content)
        self.token_count.append(response.usage.total_tokens)

    def ask(self, content):
        self.add_request("user", content)
        self.send_request()
        self.count += 1