# 矿物晶体收藏管理系统 (Mineral Collection Management System)

专为矿物、化石收藏圈打造的藏品管理系统，支持标本档案管理、照片上传、鉴定流程和多维度统计分析。

## ✨ 功能特性

### 📋 标本档案管理
- 完整的矿物信息录入：矿种、产地、莫氏硬度、晶系、颜色、光泽等专业字段
- 自动生成标本编号，支持自定义编号
- 入手途径、价格、交易商等收藏信息管理
- 多条件组合检索：按矿种、产地、晶系、鉴定状态等快速筛选

### 📷 照片管理
- 批量上传照片，支持拖拽上传
- **容错机制**：单张照片上传失败不影响其他照片
- 自动设置封面照片，支持手动调整
- 照片说明文字管理

### 🔍 鉴定流程
- 三级鉴定状态：待鉴定 → 已确认 → 存疑
- **状态机流转**：严格控制状态变更规则，支持后续扩展
- **权限分离**：仅管理员可执行鉴定操作
- 完整的鉴定历史记录，包含鉴定意见、置信度

### 📊 统计分析
- 馆藏总量、总价值等核心指标
- 按矿种、产地、晶系、获取方式多维度统计
- 鉴定状态分布统计
- ECharts 可视化图表展示

### 🔐 用户系统
- 角色分离：藏家（普通用户）、管理员（鉴定师）
- JWT 认证，Token 自动续期
- 数据权限隔离：藏家仅可见自己的藏品

## 🏗️ 技术架构

### 后端
- **框架**: FastAPI 0.115
- **数据库**: MySQL 8.0
- **ORM**: SQLAlchemy 2.0
- **认证**: JWT + Passlib
- **分层架构**: Router → Service → Model → Schema

### 前端
- **框架**: Vue 3 + Vite
- **UI 组件**: Element Plus
- **状态管理**: Pinia
- **路由**: Vue Router 4
- **HTTP 客户端**: Axios
- **图表**: ECharts 5

### 部署
- **容器化**: Docker + docker-compose
- **反向代理**: Nginx
- **文件存储**: 本地文件系统

## 📁 项目结构

```
.
├── backend/                 # 后端 FastAPI 项目
│   ├── app/
│   │   ├── main.py         # 应用入口
│   │   ├── config.py       # 配置管理
│   │   ├── database.py     # 数据库连接
│   │   ├── models/         # 数据模型
│   │   │   ├── user.py
│   │   │   ├── specimen.py
│   │   │   ├── photo.py
│   │   │   └── identification.py
│   │   ├── schemas/        # 请求/响应 DTO
│   │   ├── services/       # 业务逻辑层
│   │   │   ├── user_service.py
│   │   │   ├── specimen_service.py
│   │   │   ├── photo_service.py
│   │   │   ├── identification_service.py
│   │   │   └── stats_service.py
│   │   ├── routers/        # API 路由
│   │   └── utils/          # 工具函数
│   ├── init_db.py          # 数据库初始化脚本
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/               # 前端 Vue3 项目
│   ├── src/
│   │   ├── views/          # 页面组件
│   │   ├── components/     # 公共组件
│   │   ├── api/            # API 接口
│   │   ├── stores/         # Pinia 状态
│   │   ├── router/         # 路由配置
│   │   └── utils/          # 工具函数
│   ├── nginx.conf
│   └── Dockerfile
├── docker-compose.yml      # 生产编排
├── start.bat               # Windows 启动脚本
└── stop.bat                # Windows 停止脚本
```

## 🚀 快速开始

### 方式一：Docker 一键启动（推荐）

#### 前置要求
- Docker Desktop 4.0+
- Windows 10/11 或 macOS/Linux

#### 启动步骤

1. **克隆或下载项目到本地**

2. **双击运行 `start.bat`**（Windows）或执行命令：
   ```bash
   docker-compose up -d --build
   ```

3. **等待服务启动完成**（约 2-5 分钟）

4. **访问应用**：
   - 前端：http://localhost
   - API 文档：http://localhost:8000/docs

### 方式二：本地开发运行

#### 启动后端
```bash
cd backend
pip install -r requirements.txt

# 先启动 MySQL（可用 docker-compose.dev.yml）
docker-compose -f docker-compose.dev.yml up -d

# 修改 .env 中 MYSQL_HOST 为 localhost
# 然后启动后端
uvicorn app.main:app --reload --port 8000

# 初始化数据
python init_db.py
```

#### 启动前端
```bash
cd frontend
npm install
npm run dev
```

访问 http://localhost:5173

## 👤 演示账号

| 角色 | 用户名 | 密码 | 说明 |
|------|--------|------|------|
| 管理员 | admin | admin123 | 可执行鉴定操作，查看所有数据 |
| 藏家 | collector1 | 123456 | 普通藏家，管理自己的藏品 |
| 藏家 | collector2 | 123456 | 普通藏家，管理自己的藏品 |
| 藏家 | collector3 | 123456 | 普通藏家，管理自己的藏品 |

## 📊 预置示例数据

系统启动后自动灌入 20 块示例标本，涵盖：

**矿种**：萤石、黄铁矿、电气石、石英（烟晶/紫晶）、蓝铜矿、雄黄、辰砂、方解石、文石、黄玉（托帕石）、绿柱石（海蓝宝/祖母绿）、石榴子石、刚玉（红宝石）、石膏、锡石、自然铜、辉锑矿等

**产地**：湖南、新疆、山东、湖北、贵州、江西、内蒙古、青海、云南、江苏、安徽等多个省份

**鉴定状态**：已确认 14 块，待鉴定 4 块，存疑 2 块

## 🔌 API 接口

### 认证接口
- `POST /api/v1/auth/register` - 用户注册
- `POST /api/v1/auth/login` - 用户登录

### 标本接口
- `GET /api/v1/specimens` - 获取标本列表（支持多条件筛选）
- `GET /api/v1/specimens/{id}` - 获取标本详情
- `POST /api/v1/specimens` - 创建标本
- `PUT /api/v1/specimens/{id}` - 更新标本
- `DELETE /api/v1/specimens/{id}` - 删除标本
- `GET /api/v1/specimens/mineral-types` - 获取所有矿种
- `GET /api/v1/specimens/provinces` - 获取所有省份

### 照片接口
- `GET /api/v1/photos/specimen/{specimen_id}` - 获取标本照片
- `POST /api/v1/photos/specimen/{specimen_id}` - 单张上传
- `POST /api/v1/photos/specimen/{specimen_id}/bulk` - 批量上传
- `PUT /api/v1/photos/{id}/primary` - 设为封面
- `DELETE /api/v1/photos/{id}` - 删除照片

### 鉴定接口
- `GET /api/v1/identifications/specimen/{specimen_id}` - 获取鉴定历史
- `GET /api/v1/identifications/pending` - 获取待鉴定列表
- `POST /api/v1/identifications` - 提交鉴定意见（仅管理员）
- `GET /api/v1/identifications/allowed-transitions/{status}` - 获取允许的状态流转

### 统计接口
- `GET /api/v1/stats` - 获取综合统计数据

## 🔄 鉴定状态流转图

```
┌─────────┐    确认    ┌───────────┐
│ PENDING │ ─────────► │ CONFIRMED │
│ 待鉴定  │            │  已确认   │
└─────────┘ ◄───────── └───────────┘
     │    退回             │
     │  存疑               │ 存疑
     ▼                     ▼
┌─────────┐    确认    ┌───────────┐
│ DISPUTED│ ─────────► │ CONFIRMED │
│  存疑   │ ◄───────── │  已确认   │
└─────────┘    退回     └───────────┘
```

## 🔧 核心设计要点

### 1. 分层架构
业务逻辑全部封装在 Service 层，Router 仅负责参数校验和响应格式化，便于后续扩展。

### 2. 状态机模式
鉴定状态流转规则在 `IdentificationService.ALLOWED_TRANSITIONS` 中统一定义，后续如需增加状态（如"专家复核中"），只需修改此处配置。

### 3. 批量上传容错
`PhotoService.bulk_upload()` 中每张照片独立处理，失败时记录错误信息但继续处理下一张，最终返回详细的成功/失败清单。

### 4. 权限控制
通过 FastAPI Depends 机制实现三层权限控制：
- `get_current_user` - 认证校验
- `get_current_active_user` - 活跃用户校验
- `get_current_admin_user` - 管理员权限校验

### 5. 数据权限隔离
所有查询接口自动根据用户角色过滤数据，普通用户仅可见自己的藏品，管理员可见全部数据。

## 📝 后续扩展建议

1. **产地地图分布**：集成 ECharts 地图组件，在统计页面展示各省藏品分布热力图
2. **藏品估值统计**：增加估值模型，支持按年代、稀有度自动估算藏品价值
3. **导出功能**：支持导出标本卡片、收藏证书 PDF
4. **移动端适配**：开发微信小程序或响应式移动端界面
5. **社交功能**：藏家之间分享、交流藏品
6. **AI 辅助鉴定**：接入图像识别 AI，自动识别矿物种类

## 🛠️ 常用命令

```bash
# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f

# 重启服务
docker-compose restart

# 进入后端容器
docker exec -it mineral-backend bash

# 进入 MySQL
docker exec -it mineral-mysql mysql -uroot -pmineral123 mineral_db

# 重新初始化数据（慎用！会清空现有数据）
docker-compose down -v
docker-compose up -d --build
```

## 📄 开源协议

MIT License

## 🤝 联系方式

如有问题或建议，欢迎提交 Issue。
