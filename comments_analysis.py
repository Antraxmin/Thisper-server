import sys                         
import os                          
import json                       
from collections import OrderedDict
from models.gpt import MyGPT

print("JSON 파일을 불러옵니다.")
json_file_path = sys.argv[1]
if not os.path.isfile(json_file_path):
    print("--"+json_file_path+"은 존재하는 파일이 아닙니다. 다시 확인하여주세요.")
    sys.exit(1)
with open(json_file_path, 'r') as f:
    page = json.load(f)

print("JSON 파일에서 데이터를 추출합니다.")
try:
    p_title = page['video_title']                 
    p_description = page['video_description']   
    p_comments = ""                       
    for comment in page['comments']:
        s = ""
        s += '댓글 작성자: ' + comment['author'] + '\n'
        s += '댓글 내용: ' + comment['text'] + '\n\n'
        p_comments += s
except:
    print("--JSON 파일에서 데이터를 추출하는데 문제가 발생했습니다.")
    exit(1)

role_system = """
You are a Socratic tutor. Use the following principles in responding to students:
- Ask thought-provoking, open-ended questions that challenge students' preconceptions and encourage them to engage in deeper reflection and critical thinking.
- Facilitate open and respectful dialogue among students, creating an environment where diverse viewpoints are valued and students feel comfortable sharing their ideas.
- Actively listen to students' responses, paying careful attention to their underlying thought processes and making a genuine effort to understand their perspectives.
- Guide students in their exploration of topics by encouraging them to discover answers independently, rather than providing direct answers, to enhance their reasoning and analytical skills.
- Promote critical thinking by encouraging students to question assumptions, evaluate evidence, and consider alternative viewpoints in order to arrive at well-reasoned conclusions.
- Demonstrate humility by acknowledging your own limitations and uncertainties, modeling a growth mindset and exemplifying the value of lifelong learning.
- Students don't really like reading, so rather than giving too long explanations, keep things short and impactful.
- Don't let students miss out on opportunities to think good thoughts due to discriminatory, hateful, and biased thinking.
"""
role_assistant = p_title + p_description + """
댓글들을 표현할 수 있는 색상:
red - 잘못된 정보나 댓글의 질이 매우 안좋은 것을 나타냄. 매우 위험하고 심각한 경우에 사용. 
yello - 약간 잘 생각되지 못하고 쓴 댓글을 나타냄.
white - 주제와 관련 없거나 아무런 의미나 작성 의도가 없는 평범하고 기본적인 댓글을 나타냄.
skyblue - 누가 보아도 정말 잘 작성된 좋은 댓글을 나타냄.

단 만약 영상에 대한 설명이 조금 부실하다면 해당 영상이 좋은 영상인지 나쁜영상인지 잘 모르고 이에 대해 옹호하고 비판하는 댓글인지 잘 알 수 없으므로 색상판단에 주의할 것.
"""
role_user =  p_comments + """
영상에 달린 위 댓글들에 대해서 종합적으로 생각해본 다음에 해당 댓글을 가장 잘 나타내는 색상을 선택해줘. 대답은 다음과 같은 JSON 형식으로만 작성해줘. JSON의 변수 이름은 영어로 하되, 답변 내용은 한국어로 해줘.

{
    "result": [
    {
        "author" : "(댓글 작성자)",
        "color" : "(~~색)",
        "reson" : "(이런 부분은 좋고 이런부분은 생각을 더 해봐야된다와 같이 해당 댓글에 대한 종합적인 생각. 그리고 ~~색을 선택한 결정적인 이유 설명.)"
    },
    (... 다른 댓글들도 위와 같이 작성.)
    ]
}
"""

print("GPT에게 요청을 보냅니다.")
try:
    comment_gpt = MyGPT(role_system, role_assistant)   
    comment_gpt.ask(role_user)                         
except Exception as e:  
    print(f"--GPT에게 요청을 보내고 받는데 문제가 있습니다: {e}")
    exit(1)

print("JSON 파일을 업데이트 합니다.")
try:
    j_title = page['video_title']                 
    j_description = page['video_description']
    j_comments = page['comments']
    j_result = comment_gpt.response_json()['result']
    j_gpt = comment_gpt.get_all(json_to_text=True)

    json_obj = OrderedDict()
    json_obj["title"] = j_title
    json_obj["description"] = j_description
    json_obj["comments"] = j_comments
    json_obj["result"] = j_result
    json_obj["gpt"] = j_gpt
    
    if os.path.exists(json_file_path): os.remove(json_file_path)
    with open(json_file_path, "w", encoding='utf-8') as f:
        json.dump(json_obj, f, indent='\t', ensure_ascii=False)
except Exception as e:  
    print(f"--JSON 파일을 업데이트하는데 문제가 있습니다.  {e}")
    exit(1)

print("완료. 종료합니다.")
exit(0)