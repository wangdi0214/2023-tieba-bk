# 百度贴吧毕业设计项目

基于Veaury(Vue 3 + React 18混合开发)和Django REST Framework的完整Web项目

## 项目结构

```
2023-tieba-bk/
├── frontend/                 # Veaury前端项目
│   ├── src/
│   │   ├── components/      # 组件目录
│   │   ├── pages/          # 页面目录
│   │   ├── stores/         # 状态管理
│   │   ├── utils/          # 工具函数
│   │   └── main.js         # 入口文件
│   ├── public/             # 静态资源
│   ├── package.json        # 前端依赖配置
│   └── vite.config.js      # Vite配置
├── backend/                 # Django后端项目
│   ├── tieba_project/      # Django项目配置
│   ├── tieba_app/          # 主应用
│   ├── user_app/           # 用户应用
│   ├── post_app/           # 帖子应用
│   ├── comment_app/        # 评论应用
│   ├── manage.py           # Django管理脚本
│   └── requirements.txt    # Python依赖
├── docs/                   # 项目文档
│   ├── api/               # API文档
│   ├── database/          # 数据库设计
│   └── deployment/        # 部署文档
├── database/              # 数据库相关
│   ├── migrations/        # 数据库迁移文件
│   ├── seeds/            # 种子数据
│   └── schema/           # 数据库设计图
└── config/               # 配置文件
    ├── development.py    # 开发环境配置
    ├── production.py     # 生产环境配置
    └── settings.py       # 主配置文件
```

## 技术栈

### 前端
- **框架**: Veaury (Vue 3 + React 18)
- **构建工具**: Vite
- **状态管理**: Pinia + Zustand
- **UI组件**: Element Plus + Ant Design
- **路由**: Vue Router + React Router

### 后端
- **框架**: Django 4.x + Django REST Framework
- **数据库**: MySQL 8.0
- **缓存**: Redis
- **认证**: JWT
- **文件存储**: 本地存储 + CDN

## 快速开始

### 前端开发
```bash
cd frontend
npm install
npm run dev
```

### 后端开发
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## 功能模块

- 用户管理（注册、登录、个人中心）
- 贴吧管理（创建、浏览、管理）
- 帖子管理（发布、浏览、评论）
- 搜索功能（全文搜索、用户搜索）
- 消息系统（通知、私信）

## 开发团队

毕业设计项目 - 百度贴吧仿制版