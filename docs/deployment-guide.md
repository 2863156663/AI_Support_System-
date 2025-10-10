# AI Support System 部署指南

## 📋 目录
- [1. 环境准备](#1-环境准备)
- [2. 使用SourceTree上传代码到GitHub](#2-使用sourcetree上传代码到github)
- [3. 阿里云服务器准备](#3-阿里云服务器准备)
- [4. 服务器环境配置](#4-服务器环境配置)
- [5. 应用部署](#5-应用部署)
- [6. 域名配置与SSL证书](#6-域名配置与ssl证书)
- [7. 监控与维护](#7-监控与维护)
- [8. 故障排除](#8-故障排除)

---

## 1. 环境准备

### 1.1 必需软件
- **SourceTree** (Git GUI工具)
- **Git** (版本控制)
- **Python 3.8+** (开发环境)
- **阿里云账号** (服务器资源)

### 1.2 GitHub准备
1. 注册GitHub账号
2. 创建新的Repository
3. 获取Repository的SSH或HTTPS地址

---

## 2. 使用SourceTree上传代码到GitHub

### 2.1 安装和配置SourceTree

#### 下载安装
1. 访问 [SourceTree官网](https://www.sourcetreeapp.com/)
2. 下载并安装SourceTree
3. 首次启动时选择Git作为版本控制系统

#### 配置Git用户信息
```bash
git config --global user.name "你的用户名"
git config --global user.email "你的邮箱@example.com"
```

### 2.2 创建本地Git仓库

#### 方法一：在现有项目目录中初始化
```bash
# 进入项目目录
cd F:\1DZ\AI_Support_System

# 初始化Git仓库
git init

# 添加所有文件到暂存区
git add .

# 创建首次提交
git commit -m "Initial commit: AI Support System"
```

#### 方法二：使用SourceTree GUI
1. 打开SourceTree
2. 点击 "Create" → "Create Local Repository"
3. 选择项目目录：`F:\1DZ\AI_Support_System`
4. 点击 "Create"

### 2.3 配置远程仓库

#### 在SourceTree中配置远程仓库
1. 在SourceTree中打开项目
2. 点击 "Repository" → "Repository Settings"
3. 在 "Remotes" 标签页中点击 "Add"
4. 填写远程仓库信息：
   - **Remote name**: `origin`
   - **URL/Path**: `https://github.com/你的用户名/AI_Support_System.git`
   - **Authentication**: 选择 "HTTPS" 并输入GitHub用户名和密码

#### 使用命令行配置
```bash
# 添加远程仓库
git remote add origin https://github.com/你的用户名/AI_Support_System.git

# 验证远程仓库配置
git remote -v
```

### 2.4 推送代码到GitHub

#### 使用SourceTree推送
1. 在SourceTree中确保所有更改都已提交
2. 点击 "Push" 按钮
3. 选择远程仓库：`origin`
4. 选择分支：`master` 或 `main`
5. 点击 "Push"

#### 使用命令行推送
```bash
# 推送到远程仓库
git push -u origin master

# 如果远程仓库使用main分支
git push -u origin main
```

### 2.5 创建.gitignore文件

在项目根目录创建 `.gitignore` 文件：

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Environment variables
.env
.env.local
.env.production

# Database
*.db
*.sqlite3

# Temporary files
*.tmp
*.temp
```

---

## 3. 阿里云服务器准备

### 3.1 购买ECS实例

#### 推荐配置
- **实例规格**: 2核4GB (ecs.t5-lc1m2.large)
- **操作系统**: Ubuntu 20.04 LTS
- **存储**: 40GB SSD
- **网络**: 专有网络VPC
- **安全组**: 开放22(SSH), 80(HTTP), 443(HTTPS), 5000(Flask)端口

#### 购买步骤
1. 登录阿里云控制台
2. 进入 "云服务器ECS"
3. 点击 "创建实例"
4. 选择配置并完成购买

### 3.2 配置安全组

#### 入方向规则
| 协议类型 | 端口范围 | 授权对象 | 描述 |
|---------|---------|---------|------|
| SSH(22) | 22/22 | 0.0.0.0/0 | SSH登录 |
| HTTP(80) | 80/80 | 0.0.0.0/0 | HTTP访问 |
| HTTPS(443) | 443/443 | 0.0.0.0/0 | HTTPS访问 |
| 自定义TCP | 5000/5000 | 0.0.0.0/0 | Flask应用 |

---

## 4. 服务器环境配置

### 4.1 连接服务器

#### 使用SSH连接
```bash
# 使用密码连接
ssh root@你的服务器公网IP

# 使用密钥连接
ssh -i 你的密钥文件.pem root@你的服务器公网IP
```

### 4.2 系统更新和基础软件安装

```bash
# 更新系统包
sudo apt update && sudo apt upgrade -y

# 安装基础工具
sudo apt install -y curl wget git vim htop

# 安装Python3和pip
sudo apt install -y python3 python3-pip python3-venv

# 验证安装
python3 --version
pip3 --version
```

### 4.3 安装Nginx

```bash
# 安装Nginx
sudo apt install -y nginx

# 启动Nginx服务
sudo systemctl start nginx
sudo systemctl enable nginx

# 检查状态
sudo systemctl status nginx
```

### 4.4 安装和配置Git

```bash
# 安装Git
sudo apt install -y git

# 配置Git用户信息
git config --global user.name "服务器用户名"
git config --global user.email "服务器邮箱@example.com"

# 生成SSH密钥（可选）
ssh-keygen -t rsa -b 4096 -C "服务器邮箱@example.com"
```

---

## 5. 应用部署

### 5.1 克隆代码到服务器

```bash
# 创建应用目录
sudo mkdir -p /var/www/ai-support-system
sudo chown $USER:$USER /var/www/ai-support-system

# 进入目录
cd /var/www/ai-support-system

# 克隆代码
git clone https://github.com/你的用户名/AI_Support_System.git .

# 或者使用SSH（如果配置了SSH密钥）
git clone git@github.com:你的用户名/AI_Support_System.git .
```

### 5.2 创建Python虚拟环境

```bash
# 进入项目目录
cd /var/www/ai-support-system/test

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 升级pip
pip install --upgrade pip

# 安装依赖
pip install -r app/requirements.txt
```

### 5.3 配置环境变量

```bash
# 创建环境变量文件
sudo nano /var/www/ai-support-system/.env
```

添加以下内容：
```env
# Flask配置
FLASK_APP=app/main.py
FLASK_ENV=production
FLASK_DEBUG=False
FLASK_HOST=0.0.0.0
FLASK_PORT=5000

# 数据库配置（如果需要）
DATABASE_URL=sqlite:///app.db

# 其他配置
SECRET_KEY=your-secret-key-here
```

### 5.4 创建systemd服务文件

```bash
# 创建服务文件
sudo nano /etc/systemd/system/ai-support-system.service
```

添加以下内容：
```ini
[Unit]
Description=AI Support System Flask App
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/ai-support-system/test
Environment="PATH=/var/www/ai-support-system/test/venv/bin"
ExecStart=/var/www/ai-support-system/test/venv/bin/python app/main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

### 5.5 配置Nginx反向代理

```bash
# 创建Nginx配置文件
sudo nano /etc/nginx/sites-available/ai-support-system
```

添加以下内容：
```nginx
server {
    listen 80;
    server_name 你的域名.com www.你的域名.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 静态文件处理
    location /static {
        alias /var/www/ai-support-system/test/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

### 5.6 启用配置并启动服务

```bash
# 启用Nginx站点
sudo ln -s /etc/nginx/sites-available/ai-support-system /etc/nginx/sites-enabled/

# 测试Nginx配置
sudo nginx -t

# 重载Nginx配置
sudo systemctl reload nginx

# 启动Flask应用服务
sudo systemctl start ai-support-system
sudo systemctl enable ai-support-system

# 检查服务状态
sudo systemctl status ai-support-system
```

---

## 6. 域名配置与SSL证书

### 6.1 域名解析配置

#### 在阿里云DNS中配置
1. 登录阿里云控制台
2. 进入 "云解析DNS"
3. 添加域名解析记录：
   - **记录类型**: A
   - **主机记录**: @ 和 www
   - **解析线路**: 默认
   - **记录值**: 你的服务器公网IP
   - **TTL**: 600

### 6.2 安装SSL证书

#### 使用Let's Encrypt免费证书

```bash
# 安装Certbot
sudo apt install -y certbot python3-certbot-nginx

# 获取SSL证书
sudo certbot --nginx -d 你的域名.com -d www.你的域名.com

# 设置自动续期
sudo crontab -e
```

添加以下行：
```cron
0 12 * * * /usr/bin/certbot renew --quiet
```

---

## 7. 监控与维护

### 7.1 日志管理

#### 查看应用日志
```bash
# 查看Flask应用日志
sudo journalctl -u ai-support-system -f

# 查看Nginx日志
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### 7.2 性能监控

#### 安装监控工具
```bash
# 安装htop和iotop
sudo apt install -y htop iotop

# 查看系统资源使用情况
htop
```

### 7.3 自动部署脚本

创建部署脚本 `deploy.sh`：

```bash
#!/bin/bash
# 部署脚本

echo "开始部署AI Support System..."

# 进入项目目录
cd /var/www/ai-support-system

# 拉取最新代码
git pull origin main

# 激活虚拟环境
source test/venv/bin/activate

# 安装/更新依赖
pip install -r test/app/requirements.txt

# 重启服务
sudo systemctl restart ai-support-system

# 检查服务状态
sudo systemctl status ai-support-system

echo "部署完成！"
```

### 7.4 备份策略

#### 创建备份脚本
```bash
#!/bin/bash
# 备份脚本

BACKUP_DIR="/var/backups/ai-support-system"
DATE=$(date +%Y%m%d_%H%M%S)

# 创建备份目录
mkdir -p $BACKUP_DIR

# 备份代码
tar -czf $BACKUP_DIR/code_$DATE.tar.gz /var/www/ai-support-system

# 备份数据库（如果有）
# mysqldump -u username -p database_name > $BACKUP_DIR/db_$DATE.sql

# 删除7天前的备份
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "备份完成: $BACKUP_DIR/code_$DATE.tar.gz"
```

---

## 8. 故障排除

### 8.1 常见问题

#### 问题1：无法访问网站
**检查步骤：**
```bash
# 检查服务状态
sudo systemctl status ai-support-system
sudo systemctl status nginx

# 检查端口是否监听
sudo netstat -tlnp | grep :80
sudo netstat -tlnp | grep :5000

# 检查防火墙
sudo ufw status
```

#### 问题2：502 Bad Gateway
**解决方案：**
```bash
# 检查Flask应用是否运行
sudo systemctl status ai-support-system

# 检查应用日志
sudo journalctl -u ai-support-system -f

# 重启服务
sudo systemctl restart ai-support-system
```

#### 问题3：SSL证书问题
**解决方案：**
```bash
# 检查证书状态
sudo certbot certificates

# 手动续期
sudo certbot renew

# 测试SSL配置
sudo nginx -t
```

### 8.2 性能优化

#### Nginx优化
```nginx
# 在nginx.conf中添加
worker_processes auto;
worker_connections 1024;

# 启用gzip压缩
gzip on;
gzip_types text/plain text/css application/json application/javascript text/xml application/xml;

# 设置缓存
location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

#### Flask应用优化
```python
# 在main.py中添加
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,
        threaded=True  # 启用多线程
    )
```

---

## 📞 技术支持

如果在部署过程中遇到问题，可以：

1. 查看本文档的故障排除部分
2. 检查服务器日志文件
3. 联系技术支持团队

---

**文档版本**: v1.0  
**最后更新**: 2024年10月  
**维护者**: AI Support System Team
