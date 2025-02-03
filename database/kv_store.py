from tinydb import TinyDB, Query

class DataStore:
    def __init__(self, db_path='db.json'):
        self.db = TinyDB(db_path)
        self.table = self.db.table('items')
        
    def init_data(self):
        # 初始化一些示例数据
        initial_data = [
            {'id': 1, 'name': '【宋】瓷三足炉', 'intro': '苏州市娄药镇新苏大队开河工地出土。龙泉窑青瓷。方唇直口，深直腹，设三足。外壁施豆青釉，釉不及底，内壁近口处施釉。'},
            {'id': 2, 'name': '【宋】瓷圈足炉', 'intro': '苏州市娄药镇新苏大队开河工地出土。龙泉窑青瓷。方唇直口，深直腹，圈足。外壁施豆青釉，釉不及底，内壁近口处施釉。'},
            {'id': 3, 'name': '【宋】黄釉瓷虎子', 'intro': '苏州市货场指挥部虎丘分团工地出土。横置圆筒状，口倾斜向上，光素无纹，背有半环形提梁，平底。整体施酱黄釉，釉不及底。'}
        ]
        self.table.truncate()  # 清空现有数据
        self.table.insert_multiple(initial_data)
        
    def find_by_id(self, item_id):
        Item = Query()
        return self.table.get(Item.id == item_id)





