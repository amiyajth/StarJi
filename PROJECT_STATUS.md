# StarJi 项目开发进度

## 项目概述
- **项目名称**：StarJi（星迹）- 智能旅行规划助手
- **技术栈**：Vue3 + FastAPI + MySQL
- **开发者**：利兹（Lizi）
- **开发时间**：2026年1月

---

## 已完成功能

### 前端（Vue3）
- ✅ 项目初始化（Vite + Vue3 + Element Plus）
- ✅ 首页布局（导航栏、城市推荐、功能入口）
- ✅ 城市推荐页面（搜索、筛选、卡片展示）
- ✅ 旅行规划页面
- ✅ 图搜图页面
- ✅ 个人中心页面
- ✅ 响应式设计

### 后端（FastAPI）
- ✅ 项目结构规范化（MVC架构）
- ✅ MySQL数据库配置（starji数据库）
- ✅ City数据模型（SQLAlchemy ORM）
- ✅ 城市CRUD API
  - GET /api/cities - 查询城市列表
  - GET /api/cities/{id} - 查询单个城市
  - POST /api/cities - 创建城市
- ✅ 6条测试城市数据（重庆、成都、西安、杭州、厦门、青岛）
- ✅ API文档自动生成（/docs）
- ✅ 跨域配置（CORS）

---

## 项目结构

### 前端（StarJi/）
StarJi/
├── src/
│ ├── views/
│ │ ├── Home.vue
│ │ ├── CityRecommend.vue
│ │ ├── TravelPlan.vue
│ │ ├── ImageSearch.vue
│ │ └── UserCenter.vue
│ ├── components/
│ ├── router/
│ └── App.vue
├── public/
└── package.json

### 后端（StarJi/Starji1/）
Starji1/
├── api/
│ └── cities.py # 城市API路由
├── models/
│ └── city.py # 城市数据模型
├── schemas/
│ └── city.py # 数据验证Schema
├── services/
│ └── city_service.py # 业务逻辑层
├── main.py # 入口文件
├── config.py # 配置管理
├── database.py # 数据库连接
├── init_db.py # 数据库初始化
└── .env # 环境变量（不提交Git）

---

## 数据库设计

### cities表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT | 主键，自增 |
| name | VARCHAR(50) | 城市名称，唯一 |
| province | VARCHAR(50) | 所属省份 |
| description | TEXT | 城市描述 |
| image | VARCHAR(500) | 图片URL |
| tags | VARCHAR(200) | 标签（逗号分隔） |
| rating | FLOAT | 评分(0-5) |
| popularity | INT | 热度 |

---

## 环境配置

### MySQL配置
- 数据库名：starji
- 用户名：root
- 密码：存储在 `.env` 文件（不提交）
- 主机：localhost:3306

### Python虚拟环境
- 环境名：starji
- Python版本：3.11
- 激活命令：`conda activate starji`

### 依赖包（requirements.txt）
- fastapi==0.109.0
- uvicorn[standard]==0.25.0
- sqlalchemy==2.0.25
- pymysql==1.1.0
- python-dotenv==1.0.0
- pydantic==2.5.3
- pydantic-settings==2.1.0

---

## 下一步计划

### 阶段4：前端联调（未完成）
- [ ] 前端调用 /api/cities 接口
- [ ] 城市推荐页面显示真实数据
- [ ] 测试前后端完整流程

### 阶段5：用户系统
- [ ] User数据模型
- [ ] 注册/登录API
- [ ] JWT认证

### 阶段6：旅行规划
- [ ] Trip数据模型
- [ ] 行程CRUD API
- [ ] AI生成行程（RAG + Agent）

### 阶段7：图搜图
- [ ] 图片上传
- [ ] 景点识别
- [ ] 相似推荐

---

## 重要命令

### 后端运行
```bash
cd Starji1
conda activate starji
uvicorn main:app --reload
前端运行
npm run dev

Git操作
git status
git add .
git commit -m "feat: 功能描述"
git push

已解决的问题

✅ Git push慢 → 开VPN解决

✅ 数据库连接 → 配置.env文件

✅ 虚拟环境位置 → conda统一管理，不在项目里

✅ 项目结构混乱 → 规范化MVC架构

✅ 图片URL问题 → 先用假数据，以后替换

联系方式

GitHub: https://github.com/amiyajth/StarJi

邮箱: 1014805824@qq.com