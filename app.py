from flask import Flask, jsonify, request
from database.kv_store import DataStore
from dto.models import Hello

app = Flask(__name__)

store = DataStore()  # 创建全局实例
store.init_data()    # 初始化数据


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
            "intro": item["intro"]
        }
    }), 200

if __name__ == "__main__":
    app.run()
