from database import engine, Base, SessionLocal
from models.city import City

def init_database():
    """初始化数据库：创建所有表"""
    print("开始创建数据库表...")
    
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    
    print("✅ 数据库表创建成功！")
    
    # 插入测试数据
    print("开始插入测试数据...")
    insert_test_data()
    print("✅ 测试数据插入完成！")

def insert_test_data():
    """插入测试城市数据"""
    db = SessionLocal()
    
    try:
        # 检查是否已有数据
        existing = db.query(City).first()
        if existing:
            print("数据库已有数据，跳过插入")
            return
        
        # 测试城市数据
        cities = [
            City(
                name="重庆",
                province="重庆市",
                description="山城重庆，以壮丽的夜景、麻辣火锅和独特的立体交通闻名。洪崖洞、解放碑、磁器口古镇都是必游之地。",
                image="https://images.unsplash.com/photo-1508804185872-d7badad00f7d",
                tags="火锅,夜景,山城,网红",
                rating=4.6,
                popularity=9500
            ),
            City(
                name="成都",
                province="四川省",
                description="天府之国成都，悠闲慢生活的代表。大熊猫基地、宽窄巷子、锦里古街让你感受巴蜀文化的魅力。",
                image="https://images.unsplash.com/photo-1590735213920-68192a487bc2",
                tags="熊猫,美食,休闲,古镇",
                rating=4.7,
                popularity=10200
            ),
            City(
                name="西安",
                province="陕西省",
                description="十三朝古都西安，拥有世界闻名的兵马俑、古城墙、大雁塔。在回民街品尝地道陕西美食。",
                image="https://images.unsplash.com/photo-1565967511849-76a60a516170",
                tags="古都,历史,兵马俑,美食",
                rating=4.5,
                popularity=8800
            ),
            City(
                name="杭州",
                province="浙江省",
                description="人间天堂杭州，以西湖美景、江南园林、龙井茶闻名。春天赏樱，夏天观荷，四季皆美。",
                image="https://images.unsplash.com/photo-1589448271919-a5b0e4635e5c",
                tags="西湖,江南,茶文化,园林",
                rating=4.8,
                popularity=9800
            ),
            City(
                name="厦门",
                province="福建省",
                description="海上花园厦门，鼓浪屿的钢琴之音、曾厝垵的文艺气息、环岛路的海风，构成完美的海滨假期。",
                image="https://images.unsplash.com/photo-1590735213920-68192a487bc2",
                tags="海滨,文艺,鼓浪屿,小清新",
                rating=4.6,
                popularity=8500
            ),
            City(
                name="青岛",
                province="山东省",
                description="帆船之都青岛，红瓦绿树、碧海蓝天。栈桥、八大关、啤酒博物馆，感受中西合璧的独特魅力。",
                image="https://images.unsplash.com/photo-1548919973-5cef591cdbc9",
                tags="海滨,啤酒,欧式建筑,海鲜",
                rating=4.5,
                popularity=7800
            ),
        ]
        
        db.add_all(cities)
        db.commit()
        print(f"成功插入 {len(cities)} 条城市数据")
        
    except Exception as e:
        print(f"插入数据失败: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_database()
