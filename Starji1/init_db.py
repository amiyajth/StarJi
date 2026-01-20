from database import engine, Base, SessionLocal
from models.city import City
from models.user import User
from models.trip import Trip


def init_database():
    """初始化数据库：创建所有表"""
    print("开始创建数据库表...")
    Base.metadata.create_all(bind=engine)
    print("✅ 数据库表创建成功！")
    
    print("开始插入测试数据...")
    insert_test_data()
    print("✅ 测试数据插入完成！")


def insert_test_data():
    """插入测试城市数据"""
    db = SessionLocal()
    
    try:
        existing = db.query(City).first()
        if existing:
            print("数据库已有数据，跳过插入")
            return
        
        cities = get_all_cities_data()
        db.add_all(cities)
        db.commit()
        print(f"成功插入 {len(cities)} 条城市数据")
        
    except Exception as e:
        print(f"插入数据失败: {e}")
        db.rollback()
    finally:
        db.close()


def get_all_cities_data():
    """✨ 完整的城市数据（20+热门城市）"""
    return [
        # ==================== 华东 ====================
        City(
            name="上海",
            province="上海市",
            description="东方明珠，国际大都市。外滩的万国建筑、陆家嘴的摩天大楼、老城厢的石库门，传统与现代在这里完美交融。",
            image="https://images.unsplash.com/photo-1474181487882-5abf3f0ba6c2?w=800&q=80",
            tags="都市,购物,美食,夜景",
            rating=4.7,
            popularity=12000
        ),
        City(
            name="杭州",
            province="浙江省",
            description="人间天堂杭州，以西湖美景、江南园林、龙井茶闻名。春天赏樱，夏天观荷，四季皆美。",
            image="https://images.unsplash.com/photo-1528164344705-47542687000d?w=800&q=80",
            tags="西湖,江南,茶文化,园林",
            rating=4.8,
            popularity=9800
        ),
        City(
            name="苏州",
            province="江苏省",
            description="上有天堂，下有苏杭。苏州园林甲天下，拙政园、留园尽显江南韵味，平江路的小桥流水让人流连忘返。",
            image="https://images.unsplash.com/photo-1530922335919-e8c2db7c4f6e?w=800&q=80",
            tags="园林,古镇,江南,昆曲",
            rating=4.6,
            popularity=8200
        ),
        City(
            name="南京",
            province="江苏省",
            description="六朝古都南京，中山陵的庄严、夫子庙的繁华、玄武湖的宁静，承载着厚重的历史文化。",
            image="https://images.unsplash.com/photo-1599661046289-e31897846e41?w=800&q=80",
            tags="历史,古都,民国,美食",
            rating=4.5,
            popularity=8500
        ),
        City(
            name="厦门",
            province="福建省",
            description="海上花园厦门，鼓浪屿的钢琴之音、曾厝垵的文艺气息、环岛路的海风，构成完美的海滨假期。",
            image="https://images.unsplash.com/photo-1504681869696-d977211a5f4c?w=800&q=80",
            tags="海滨,文艺,鼓浪屿,小清新",
            rating=4.6,
            popularity=8500
        ),
        City(
            name="青岛",
            province="山东省",
            description="帆船之都青岛，红瓦绿树、碧海蓝天。栈桥、八大关、啤酒博物馆，感受中西合璧的独特魅力。",
            image="https://images.unsplash.com/photo-1569074187119-c87815b476da?w=800&q=80",
            tags="海滨,啤酒,欧式建筑,海鲜",
            rating=4.5,
            popularity=7800
        ),
        City(
            name="黄山",
            province="安徽省",
            description="五岳归来不看山，黄山归来不看岳。奇松怪石云海温泉，被誉为天下第一奇山。",
            image="https://images.unsplash.com/photo-1518173946687-a4c3cbecd067?w=800&q=80",
            tags="山岳,云海,日出,自然",
            rating=4.8,
            popularity=7500
        ),
        
        # ==================== 华南 ====================
        City(
            name="广州",
            province="广东省",
            description="千年商都广州，早茶文化、骑楼老街、珠江夜游，在现代都市中品味岭南风情。",
            image="https://images.unsplash.com/photo-1536599018102-9f803c979853?w=800&q=80",
            tags="美食,早茶,都市,岭南",
            rating=4.5,
            popularity=9200
        ),
        City(
            name="深圳",
            province="广东省",
            description="创新之城深圳，从小渔村到国际大都市，世界之窗、欢乐谷、大梅沙，年轻活力的代名词。",
            image="https://images.unsplash.com/photo-1518623489648-a173ef7824f3?w=800&q=80",
            tags="都市,科技,主题公园,海滨",
            rating=4.4,
            popularity=8800
        ),
        City(
            name="三亚",
            province="海南省",
            description="东方夏威夷三亚，椰风海韵、碧海蓝天。亚龙湾的细沙、天涯海角的浪漫，是度假的天堂。",
            image="https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&q=80",
            tags="海滨,度假,热带,浪漫",
            rating=4.6,
            popularity=9500
        ),
        City(
            name="桂林",
            province="广西壮族自治区",
            description="桂林山水甲天下，漓江两岸的喀斯特地貌如诗如画，阳朔西街的慢生活让人沉醉。",
            image="https://images.unsplash.com/photo-1537531383496-f4749b8032cf?w=800&q=80",
            tags="山水,漓江,自然,摄影",
            rating=4.7,
            popularity=8800
        ),
        
        # ==================== 华北 ====================
        City(
            name="北京",
            province="北京市",
            description="千年古都北京，故宫的红墙黄瓦、长城的雄伟壮观、胡同的京味儿生活，历史与现代在这里交汇。",
            image="https://images.unsplash.com/photo-1508804185872-d7badad00f7d?w=800&q=80",
            tags="古都,故宫,长城,文化",
            rating=4.8,
            popularity=15000
        ),
        City(
            name="天津",
            province="天津市",
            description="近代百年看天津，五大道的洋楼、意式风情街的浪漫、狗不理包子的滋味，海河之滨风情万种。",
            image="https://images.unsplash.com/photo-1577086664693-894d8a9e644d?w=800&q=80",
            tags="洋楼,美食,相声,海河",
            rating=4.3,
            popularity=6500
        ),
        
        # ==================== 西南 ====================
        City(
            name="重庆",
            province="重庆市",
            description="山城重庆，以壮丽的夜景、麻辣火锅和独特的立体交通闻名。洪崖洞、解放碑、磁器口古镇都是必游之地。",
            image="https://images.unsplash.com/photo-1599571234909-29ed5d1321d6?w=800&q=80",
            tags="火锅,夜景,山城,网红",
            rating=4.6,
            popularity=9500
        ),
        City(
            name="成都",
            province="四川省",
            description="天府之国成都，悠闲慢生活的代表。大熊猫基地、宽窄巷子、锦里古街让你感受巴蜀文化的魅力。",
            image="https://images.unsplash.com/photo-1494783367193-149034c05e8f?w=800&q=80",
            tags="熊猫,美食,休闲,古镇",
            rating=4.7,
            popularity=10200
        ),
        City(
            name="大理",
            province="云南省",
            description="风花雪月大理，苍山洱海的壮美、古城的悠闲、白族的风情，是无数人心中的诗和远方。",
            image="https://images.unsplash.com/photo-1513415564515-763d91423bdd?w=800&q=80",
            tags="古城,洱海,文艺,慢生活",
            rating=4.6,
            popularity=8600
        ),
        City(
            name="丽江",
            province="云南省",
            description="浪漫丽江，古城的小桥流水、玉龙雪山的巍峨、纳西古乐的悠扬，让人沉醉在时光里。",
            image="https://images.unsplash.com/photo-1547981609-4b6bfe67ca0b?w=800&q=80",
            tags="古城,雪山,浪漫,纳西",
            rating=4.5,
            popularity=8200
        ),
        City(
            name="拉萨",
            province="西藏自治区",
            description="日光之城拉萨，布达拉宫的庄严、大昭寺的虔诚、八廓街的转经筒，离天堂最近的地方。",
            image="https://images.unsplash.com/photo-1559628233-100c798642d4?w=800&q=80",
            tags="藏传佛教,高原,神圣,朝圣",
            rating=4.9,
            popularity=7200
        ),
        City(
            name="昆明",
            province="云南省",
            description="春城昆明，四季如春的气候、滇池的波光、石林的奇观，是通往云南各地的门户。",
            image="https://images.unsplash.com/photo-1470004914212-05527e49370b?w=800&q=80",
            tags="春城,滇池,石林,鲜花",
            rating=4.4,
            popularity=7000
        ),
        
        # ==================== 西北 ====================
        City(
            name="西安",
            province="陕西省",
            description="十三朝古都西安，拥有世界闻名的兵马俑、古城墙、大雁塔。在回民街品尝地道陕西美食。",
            image="https://images.unsplash.com/photo-1545893835-abaa50cbe628?w=800&q=80",
            tags="古都,历史,兵马俑,美食",
            rating=4.5,
            popularity=8800
        ),
        City(
            name="敦煌",
            province="甘肃省",
            description="丝路明珠敦煌，莫高窟的千年壁画、鸣沙山的大漠风光、月牙泉的神奇，是一场穿越时空的旅行。",
            image="https://images.unsplash.com/photo-1516496636080-14fb876e029d?w=800&q=80",
            tags="丝路,石窟,沙漠,历史",
            rating=4.7,
            popularity=6800
        ),
        City(
            name="兰州",
            province="甘肃省",
            description="黄河穿城而过的兰州，一碗牛肉面温暖人心，中山桥见证百年沧桑，是西北之旅的重要一站。",
            image="https://images.unsplash.com/photo-1516466723877-e4ec1d736c8a?w=800&q=80",
            tags="黄河,牛肉面,丝路,西北",
            rating=4.2,
            popularity=5500
        ),
        
        # ==================== 东北 ====================
        City(
            name="哈尔滨",
            province="黑龙江省",
            description="冰城哈尔滨，冬季的冰雪大世界、中央大街的俄式风情、马迭尔冰棍的甜蜜，是北国的浪漫之都。",
            image="https://images.unsplash.com/photo-1516398810611-ed42ccfabb7f?w=800&q=80",
            tags="冰雪,俄式风情,冬季,滑雪",
            rating=4.5,
            popularity=7800
        ),
        City(
            name="大连",
            province="辽宁省",
            description="浪漫之都大连，星海广场的开阔、老虎滩的海洋世界、俄罗斯风情街的异域风情，北方明珠名不虚传。",
            image="https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=800&q=80",
            tags="海滨,广场,海鲜,浪漫",
            rating=4.4,
            popularity=7200
        ),
        City(
            name="长春",
            province="吉林省",
            description="北国春城长春，伪满皇宫的历史、净月潭的森林、长影世纪城的光影，东北老工业基地的新魅力。",
            image="https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?w=800&q=80",
            tags="历史,森林,电影,冰雪",
            rating=4.2,
            popularity=5800
        ),
        
        # ==================== 中部 ====================
        City(
            name="武汉",
            province="湖北省",
            description="九省通衢武汉，黄鹤楼的诗意、长江大桥的壮观、热干面的滋味、樱花季的浪漫，江城魅力无限。",
            image="https://images.unsplash.com/photo-1564352969782-d30e66f0970e?w=800&q=80",
            tags="黄鹤楼,樱花,美食,长江",
            rating=4.5,
            popularity=8200
        ),
        City(
            name="长沙",
            province="湖南省",
            description="娱乐之都长沙，橘子洲头的伟人足迹、岳麓山的红枫、太平老街的烟火气、茶颜悦色的奶茶，快乐无处不在。",
            image="https://images.unsplash.com/photo-1590559899683-0b3b3ab7b6c1?w=800&q=80",
            tags="美食,娱乐,红色,夜生活",
            rating=4.5,
            popularity=8500
        ),
        City(
            name="张家界",
            province="湖南省",
            description="人间仙境张家界，阿凡达取景地的奇峰异石、玻璃栈道的惊险刺激、天门山的云海翻涌，如入画中世界。",
            image="https://images.unsplash.com/photo-1518255190200-3bdaf0069c2e?w=800&q=80",
            tags="山岳,奇观,玻璃桥,自然",
            rating=4.7,
            popularity=7600
        ),
    ]


def update_city_images():
    """✨ 更新现有城市的图片（用于修复已有数据）"""
    db = SessionLocal()
    
    city_images = {
        "上海": "https://images.unsplash.com/photo-1474181487882-5abf3f0ba6c2?w=800&q=80",
        "杭州": "https://images.unsplash.com/photo-1528164344705-47542687000d?w=800&q=80",
        "苏州": "https://images.unsplash.com/photo-1545893835-abaa50cbe628?w=800&q=80",
        "南京": "https://images.unsplash.com/photo-1599661046289-e31897846e41?w=800&q=80",
        "厦门": "https://images.unsplash.com/photo-1504681869696-d977211a5f4c?w=800&q=80",
        "青岛": "https://images.unsplash.com/photo-1569074187119-c87815b476da?w=800&q=80",
        "黄山": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=800&q=80",
        "广州": "https://images.unsplash.com/photo-1583395838144-09af17bc2b70?w=800&q=80",
        "深圳": "https://images.unsplash.com/photo-1518623489648-a173ef7824f3?w=800&q=80",
        "三亚": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&q=80",
        "桂林": "https://images.unsplash.com/photo-1537531383496-f4749b8032cf?w=800&q=80",
        "北京": "https://images.unsplash.com/photo-1508804185872-d7badad00f7d?w=800&q=80",
        "天津": "https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b?w=800&q=80",
        "重庆": "https://images.unsplash.com/photo-1599571234909-29ed5d1321d6?w=800&q=80",
        "成都": "https://images.unsplash.com/photo-1494783367193-149034c05e8f?w=800&q=80",
        "大理": "https://images.unsplash.com/photo-1513415564515-763d91423bdd?w=800&q=80",
        "丽江": "https://images.unsplash.com/photo-1547981609-4b6bfe67ca0b?w=800&q=80",
        "拉萨": "https://images.unsplash.com/photo-1559628233-100c798642d4?w=800&q=80",
        "昆明": "https://images.unsplash.com/photo-1470004914212-05527e49370b?w=800&q=80",
        "西安": "https://images.unsplash.com/photo-1545893835-abaa50cbe628?w=800&q=80",
        "敦煌": "https://images.unsplash.com/photo-1516496636080-14fb876e029d?w=800&q=80",
        "兰州": "https://images.unsplash.com/photo-1516466723877-e4ec1d736c8a?w=800&q=80",
        "哈尔滨": "https://images.unsplash.com/photo-1477346611705-65d1883cee1e?w=800&q=80",
        "大连": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=800&q=80",
        "长春": "https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?w=800&q=80",
        "武汉": "https://images.unsplash.com/photo-1522083165195-3424ed129620?w=800&q=80",
        "长沙": "https://images.unsplash.com/photo-1517048676732-d65bc937f952?w=800&q=80",
        "张家界": "https://images.unsplash.com/photo-1494500764479-0c8f2919a3d8?w=800&q=80",
    }
    
    try:
        for city_name, image_url in city_images.items():
            city = db.query(City).filter(City.name == city_name).first()
            if city:
                city.image = image_url
                print(f"✅ 更新 {city_name} 的图片")
            else:
                print(f"⚠️ 未找到城市: {city_name}")
        
        db.commit()
        print("✅ 所有城市图片更新完成！")
        
    except Exception as e:
        print(f"更新失败: {e}")
        db.rollback()
    finally:
        db.close()
def add_more_cities():
    """✨ 添加更多城市（不删除现有数据）"""
    db = SessionLocal()
    
    # 需要添加的新城市 (name, province, description, image, tags, rating, popularity)
    new_cities_data = [
        ("上海", "上海市", "东方明珠，国际大都市。外滩的万国建筑、陆家嘴的摩天大楼、老城厢的石库门，传统与现代在这里完美交融。", "https://images.unsplash.com/photo-1474181487882-5abf3f0ba6c2?w=800&q=80", "都市,购物,美食,夜景", 4.7, 12000),
        ("苏州", "江苏省", "上有天堂，下有苏杭。苏州园林甲天下，拙政园、留园尽显江南韵味，平江路的小桥流水让人流连忘返。", "https://images.unsplash.com/photo-1530922335919-e8c2db7c4f6e?w=800&q=80", "园林,古镇,江南,昆曲", 4.6, 8200),
        ("南京", "江苏省", "六朝古都南京，中山陵的庄严、夫子庙的繁华、玄武湖的宁静，承载着厚重的历史文化。", "https://images.unsplash.com/photo-1599661046289-e31897846e41?w=800&q=80", "历史,古都,民国,美食", 4.5, 8500),
        ("黄山", "安徽省", "五岳归来不看山，黄山归来不看岳。奇松怪石云海温泉，被誉为天下第一奇山。", "https://images.unsplash.com/photo-1518173946687-a4c3cbecd067?w=800&q=80", "山岳,云海,日出,自然", 4.8, 7500),
        ("广州", "广东省", "千年商都广州，早茶文化、骑楼老街、珠江夜游，在现代都市中品味岭南风情。", "https://images.unsplash.com/photo-1536599018102-9f803c979853?w=800&q=80", "美食,早茶,都市,岭南", 4.5, 9200),
        ("深圳", "广东省", "创新之城深圳，从小渔村到国际大都市，世界之窗、欢乐谷、大梅沙，年轻活力的代名词。", "https://images.unsplash.com/photo-1518623489648-a173ef7824f3?w=800&q=80", "都市,科技,主题公园,海滨", 4.4, 8800),
        ("三亚", "海南省", "东方夏威夷三亚，椰风海韵、碧海蓝天。亚龙湾的细沙、天涯海角的浪漫，是度假的天堂。", "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&q=80", "海滨,度假,热带,浪漫", 4.6, 9500),
        ("桂林", "广西壮族自治区", "桂林山水甲天下，漓江两岸的喀斯特地貌如诗如画，阳朔西街的慢生活让人沉醉。", "https://images.unsplash.com/photo-1537531383496-f4749b8032cf?w=800&q=80", "山水,漓江,自然,摄影", 4.7, 8800),
        ("北京", "北京市", "千年古都北京，故宫的红墙黄瓦、长城的雄伟壮观、胡同的京味儿生活，历史与现代在这里交汇。", "https://images.unsplash.com/photo-1508804185872-d7badad00f7d?w=800&q=80", "古都,故宫,长城,文化", 4.8, 15000),
        ("天津", "天津市", "近代百年看天津，五大道的洋楼、意式风情街的浪漫、狗不理包子的滋味，海河之滨风情万种。", "https://images.unsplash.com/photo-1577086664693-894d8a9e644d?w=800&q=80", "洋楼,美食,相声,海河", 4.3, 6500),
        ("大理", "云南省", "风花雪月大理，苍山洱海的壮美、古城的悠闲、白族的风情，是无数人心中的诗和远方。", "https://images.unsplash.com/photo-1513415564515-763d91423bdd?w=800&q=80", "古城,洱海,文艺,慢生活", 4.6, 8600),
        ("丽江", "云南省", "浪漫丽江，古城的小桥流水、玉龙雪山的巍峨、纳西古乐的悠扬，让人沉醉在时光里。", "https://images.unsplash.com/photo-1547981609-4b6bfe67ca0b?w=800&q=80", "古城,雪山,浪漫,纳西", 4.5, 8200),
        ("拉萨", "西藏自治区", "日光之城拉萨，布达拉宫的庄严、大昭寺的虔诚、八廓街的转经筒，离天堂最近的地方。", "https://images.unsplash.com/photo-1559628233-100c798642d4?w=800&q=80", "藏传佛教,高原,神圣,朝圣", 4.9, 7200),
        ("昆明", "云南省", "春城昆明，四季如春的气候、滇池的波光、石林的奇观，是通往云南各地的门户。", "https://images.unsplash.com/photo-1470004914212-05527e49370b?w=800&q=80", "春城,滇池,石林,鲜花", 4.4, 7000),
        ("敦煌", "甘肃省", "丝路明珠敦煌，莫高窟的千年壁画、鸣沙山的大漠风光、月牙泉的神奇，是一场穿越时空的旅行。", "https://images.unsplash.com/photo-1516496636080-14fb876e029d?w=800&q=80", "丝路,石窟,沙漠,历史", 4.7, 6800),
        ("兰州", "甘肃省", "黄河穿城而过的兰州，一碗牛肉面温暖人心，中山桥见证百年沧桑，是西北之旅的重要一站。", "https://images.unsplash.com/photo-1516466723877-e4ec1d736c8a?w=800&q=80", "黄河,牛肉面,丝路,西北", 4.2, 5500),
        ("哈尔滨", "黑龙江省", "冰城哈尔滨，冬季的冰雪大世界、中央大街的俄式风情、马迭尔冰棍的甜蜜，是北国的浪漫之都。", "https://images.unsplash.com/photo-1516398810611-ed42ccfabb7f?w=800&q=80", "冰雪,俄式风情,冬季,滑雪", 4.5, 7800),
        ("大连", "辽宁省", "浪漫之都大连，星海广场的开阔、老虎滩的海洋世界、俄罗斯风情街的异域风情，北方明珠名不虚传。", "https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=800&q=80", "海滨,广场,海鲜,浪漫", 4.4, 7200),
        ("长春", "吉林省", "北国春城长春，伪满皇宫的历史、净月潭的森林、长影世纪城的光影，东北老工业基地的新魅力。", "https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?w=800&q=80", "历史,森林,电影,冰雪", 4.2, 5800),
        ("武汉", "湖北省", "九省通衢武汉，黄鹤楼的诗意、长江大桥的壮观、热干面的滋味、樱花季的浪漫，江城魅力无限。", "https://images.unsplash.com/photo-1564352969782-d30e66f0970e?w=800&q=80", "黄鹤楼,樱花,美食,长江", 4.5, 8200),
        ("长沙", "湖南省", "娱乐之都长沙，橘子洲头的伟人足迹、岳麓山的红枫、太平老街的烟火气、茶颜悦色的奶茶，快乐无处不在。", "https://images.unsplash.com/photo-1590559899683-0b3b3ab7b6c1?w=800&q=80", "美食,娱乐,红色,夜生活", 4.5, 8500),
        ("张家界", "湖南省", "人间仙境张家界，阿凡达取景地的奇峰异石、玻璃栈道的惊险刺激、天门山的云海翻涌，如入画中世界。", "https://images.unsplash.com/photo-1518255190200-3bdaf0069c2e?w=800&q=80", "山岳,奇观,玻璃桥,自然", 4.7, 7600),
    ]
    
    try:
        added_count = 0
        updated_count = 0
        
        for name, province, description, image, tags, rating, popularity in new_cities_data:
            # 检查城市是否已存在
            existing = db.query(City).filter(City.name == name).first()
            
            if existing:
                # 更新现有城市的信息
                existing.province = province
                existing.description = description
                existing.image = image
                existing.tags = tags
                existing.rating = rating
                existing.popularity = popularity
                updated_count += 1
                print(f"🔄 更新城市: {name}")
            else:
                # 添加新城市
                new_city = City(
                    name=name,
                    province=province,
                    description=description,
                    image=image,
                    tags=tags,
                    rating=rating,
                    popularity=popularity
                )
                db.add(new_city)
                added_count += 1
                print(f"✅ 添加城市: {name}")
        
        db.commit()
        print(f"\n🎉 操作完成！新增 {added_count} 个城市，更新 {updated_count} 个城市")
        
    except Exception as e:
        print(f"操作失败: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    # 根据需要选择执行的函数：
    
    # 1. 初始化数据库（首次使用）
    # init_database()
    
    # 2. 只更新图片
    # update_city_images()
    
    # 3. 添加/更新所有城市（推荐）
    add_more_cities()
