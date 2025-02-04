from openai import OpenAI
import os
from dotenv import load_dotenv
class MuseumAI:
    load_dotenv()
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("DASHSCOPE_API_KEY"), # 如何获取API Key：https://help.aliyun.com/zh/model-studio/developer-reference/get-api-key
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            )

        self.system_prompt = """你是一个苏州博物馆 AI 专家，我将与你围绕某个特定文物进行深入交流。  
        请在用户提问时，始终基于**当前讨论的文物**来回答，并参考历史、考古学、文献记载等方面的知识，确保回答的准确性和逻辑性。  

        如果用户改变话题，并提到了新的文物，你需要：
        1. **先确认用户是否想要查询新的文物**，如果是，则重新按照结构化格式输出该文物信息。
        2. **如果用户只是进行对比**，则继续围绕当前文物回答，并补充相关背景。

        例如：
        用户：这个文物的材质是什么？
        AI：司母戊鼎主要由青铜铸造，铜含量约为 80%，另含锡、铅等合金成分，使其更具强度和耐腐蚀性。

        用户：它的用途是什么？
        AI：司母戊鼎是商代用于祭祀祖先和神灵的重要礼器，象征着王权和宗教信仰。

        用户：那它和后来的青铜器有什么不同？
        AI：相比战国晚期的青铜器，司母戊鼎更具重量和庄重感，后来的青铜器逐渐向精美、小型化发展，比如战国晚期的曾侯乙编钟，以复杂的铸造工艺和音乐功能闻名。

        请确保回答时，始终与当前讨论的文物保持一致。

        请不要输出任何回复语句，例如好的，只输出回答。

        始终基于已有知识回答，不要让用户提供额外信息。
        """
        self.conversation_history = []
    def get_response(self, user_question):
        # 添加用户问题到对话历史
        self.conversation_history.append({
            'role': 'user',
            'content': str(user_question)
        })
        print(self.conversation_history)
        completion = self.client.chat.completions.create(
            model="qwen-plus",
            messages=[
                {'role': 'system', 'content': self.system_prompt},
                *self.conversation_history
            ]
        )
        print(completion)
        
        # 添加AI回答到对话历史
        ai_response = completion.choices[0].message.content
        self.conversation_history.append({
            'role': 'assistant',
            'content': ai_response
        })
        print(self.conversation_history)
        return ai_response
    
    def clear_history(self):
        """清空对话历史"""
        self.conversation_history = []