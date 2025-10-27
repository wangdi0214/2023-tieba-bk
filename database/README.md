# 数据库设计目录

## 目录结构

```
database/
├── migrations/             # 数据库迁移文件
│   ├── user_migrations/   # 用户相关迁移
│   ├── tieba_migrations/  # 贴吧相关迁移
│   ├── post_migrations/   # 帖子相关迁移
│   └── comment_migrations/ # 评论相关迁移
├── seeds/                 # 种子数据
│   ├── users.sql          # 用户种子数据
│   ├── tiebas.sql         # 贴吧种子数据
│   ├── posts.sql          # 帖子种子数据
│   └── comments.sql       # 评论种子数据
├── schema/                # 数据库设计图
│   ├── er_diagram.png     # 实体关系图
│   ├── schema.sql         # 完整表结构
│   └── indexes.sql        # 索引设计
├── scripts/               # 数据库脚本
│   ├── backup.sh          # 备份脚本
│   ├── restore.sh         # 恢复脚本
│   └── optimize.sh        # 优化脚本
└── docs/                  # 数据库文档
    ├── design.md          # 设计思路
    ├── performance.md     # 性能优化
    └── security.md        # 安全考虑
```

## 数据库说明

### 数据库类型
- **开发环境**: SQLite3
- **生产环境**: MySQL 8.0

### 主要数据表

1. **用户相关表**
   - `user` - 用户主表
   - `user_profile` - 用户详细资料
   - `follow_relation` - 关注关系
   - `user_notification` - 用户通知

2. **贴吧相关表**
   - `tieba` - 贴吧主表
   - `tieba_member` - 贴吧成员
   - `tieba_admin` - 贴吧管理员

3. **帖子相关表**
   - `post` - 帖子主表
   - `post_like` - 帖子点赞
   - `post_view` - 帖子浏览记录

4. **评论相关表**
   - `comment` - 评论主表
   - `comment_like` - 评论点赞
   - `comment_reply` - 评论回复

## 设计原则

1. **规范化设计**: 遵循数据库第三范式
2. **性能优化**: 合理设计索引和外键
3. **安全性**: 敏感数据加密存储
4. **扩展性**: 支持水平扩展和分表

## 迁移管理

使用Django内置的迁移系统管理数据库变更。