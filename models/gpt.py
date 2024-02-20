from dotenv import load_dotenv
from openai import OpenAI   
import re                 
import json              
import os

load_dotenv()

class MyGPT:
    def __init__(self, role_system, role_assistant):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.client = OpenAI()
        self.role_system = role_system         
        self.role_assistant = role_assistant    
        self.requests = []    
        self.responses = []   
        self.questions = []    
        self.answers = []     
        self.token_count = []  
 
        self.add_request("system", self.role_system)
        self.add_request("assistant", self.role_assistant)
        self.count = 0

    def clean_space(self, s):
        s = re.sub('(<br>)', '\n', s)
        s = re.sub('\n+', '\n', s)
        return s
    
    def get_role_system(self):
        return self.role_system

    def get_role_assistant(self):
        return self.role_assistant

    def get_questions(self):
        return self.questions

    def get_answers(self, json_to_text=False):
        if json_to_text:
            answers_new = []
            for a in self.answers:
                try:
                    json_obj = json.loads(str(a))
                except json.decoder.JSONDecodeError as e:
                    answers_new.append(a)
                else:
                    try:
                        m_all = ""
                        for item in json_obj['result']:
                            m_author = "댓글 작성자 : " + str(item['author']) + '\n'
                            m_color = "댓글 색상 : " + str(item['color']) + '\n'
                            m_reson = "댓글 색상 판단 이유 : " + str(item['reason']) + '\n\n'
                            m_all += m_author + m_color + m_reson
                    except:
                        answers_new.append(a)
                    else:
                        a = m_all
                        answers_new.append(a)
            return answers_new
        else:
            return self.answers
        
    def get_converstation(self, json_to_text=False):
        conv = []
        for q, a in zip(self.get_questions(), self.get_answers(json_to_text)):
            conv.append([q, a])
        return conv

    def get_all(self, json_to_text=False):
        return {
            "role_system" : self.get_role_system(),
            "role_assistant" : self.get_role_assistant(),
            "questions" : self.get_questions(),
            "answers" : self.get_answers(json_to_text)
        }

    def add_request(self, role, content):
        if(role=="user"): self.questions.append(content)
        self.requests.append({"role": role, "content": content})

    def send_request(self):
        response = self.client.chat.completions.create(
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
        self.count = self.count + 1
    
    def response(self, show_response=False, show_asking=False):
        out = "\n"
        out += f"*** 토큰 사용량: {self.token_count[-1]}개 ***\n"
        if show_asking:
            out += f"질문 ----------------------------------------\n"
            out += f"{self.questions[-1]}\n"
        out += f"응답 ----------------------------------------\n"
        out += f"{self.answers[-1]}\n"
        if show_response: print(out)
        return out

    def response_json(self):
        try:
            json_obj = json.loads(str(self.answers[-1]))
            return json_obj
        except json.decoder.JSONDecodeError as e:
            print("--GPT의 응답이 JSON 문법에 맞지 않습니다.\n오류:", e, "\n")
    
    def converstation(self, show_response=False, show_asking=True):
        out = "\n"
        for z in zip(self.questions, self.answers, self.token_count):
            out += f"*** 토큰 사용량: {z[2]}개 ***\n"
            if show_asking:
                out += f"질문 ----------------------------------------\n"
                out += f"{self.questions[-1]}\n"
            out += f"응답 ----------------------------------------\n"
            out += f"{z[1]}\n"
        if show_response: print(out)
        return out


