from flask import Flask, jsonify, request
from database.kv_store import DataStore
from dto.models import Hello
from llm.ali_ai import MuseumAI

app = Flask(__name__)

store = DataStore()  # 创建全局实例
store.init_data()    # 初始化数据
museum_ai = MuseumAI()
@app.route("/hello")
def hello_world():
    return jsonify({"status": "success", "data": Hello(id="123", content="world").model_dump()}), 200

@app.route("/items/<int:item_id>")
def get_item(item_id):
    item = store.find_by_id(item_id)
    if item is None:
        return jsonify({"status": "error", "message": "未找到对应的物品"}), 404
        
    return jsonify({
        "status": "success",
        "data": {
            "name": item["name"],
            "intro": item["intro"],
        }
    }), 200

@app.route("/questions", methods=['POST'])
def ask_question():
    question = request.json.get('question')
    item_id = request.json.get('item_id')
    
    if not question:
        return jsonify({"status": "error", "message": "请提供问题内容"}), 400
        
    if item_id is None:
        return jsonify({"status": "error", "message": "请提供物品ID"}), 400
    
    item = store.find_by_id(item_id)
    if item is None:
        return jsonify({"status": "error", "message": "未找到对应的物品"}), 404
        
    # 将物品信息作为上下文提供给 AI
    context = {
        "item_name": item["name"],
        "item_intro": item["intro"],
        "question": question
    }
    
    response = museum_ai.get_response(context)
    return jsonify({"status": "success", "data": response}), 200

@app.route("/chat_history", methods=['DELETE'])
def delete_chat_history():
    museum_ai.clear_history()
    return jsonify({"status": "success", "message": "对话历史已清空"}), 200

if __name__ == "__main__":
    app.run()
