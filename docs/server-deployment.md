# 服务器部署指南

## 1. 服务器环境准备

### 1.1 系统要求
- Ubuntu 18.04+ 或 CentOS 7+
- Python 3.7+
- Git
- 至少 2GB RAM
- 至少 10GB 可用磁盘空间

### 1.2 安装系统依赖
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y python3 python3-pip python3-venv git curl

# CentOS/RHEL
sudo yum update -y
sudo yum install -y python3 python3-pip git curl
```

### 1.3 配置SSH密钥
```bash
# 在本地生成SSH密钥（如果还没有）
ssh-keygen -t rsa -b 4096 -C "your.email@example.com"

# 将公钥复制到服务器
ssh-copy-id username@your-server-ip

# 或者手动添加
cat ~/.ssh/id_rsa.pub
# 将输出内容添加到服务器的 ~/.ssh/authorized_keys
```

## 2. 首次部署

### 2.1 登录服务器
```bash
ssh username@your-server-ip
```

### 2.2 克隆项目代码
```bash
# 克隆dev分支
git clone -b dev git@your.gitlab.server:group/project.git
cd project

# 验证代码已正确克隆
ls -la
```

### 2.3 创建虚拟环境
```bash
# 创建Python虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 升级pip
pip install --upgrade pip

# 安装项目依赖
pip install -r app/requirements.txt
```

### 2.4 配置环境变量
```bash
# 创建环境配置文件
cat > .env << EOF
FLASK_ENV=production
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
FLASK_DEBUG=False
EOF
```

### 2.5 启动服务
```bash
# 后台启动服务
nohup python app/main.py > app.log 2>&1 &

# 获取进程ID
echo $! > app.pid

# 检查服务是否启动
ps aux | grep python
curl http://localhost:5000/
```

## 3. 使用部署脚本

### 3.1 下载部署脚本
```bash
# 确保脚本有执行权限
chmod +x scripts/deploy.sh
chmod +x scripts/update.sh
```

### 3.2 运行部署脚本
```bash
# 首次部署
./scripts/deploy.sh

# 查看部署日志
tail -f /opt/AI_Support_System/deploy.log
```

### 3.3 验证部署
```bash
# 检查服务状态
ps -p $(cat /opt/AI_Support_System/app.pid)

# 测试API
curl http://localhost:5000/
curl http://localhost:5000/api/status

# 查看应用日志
tail -f /opt/AI_Support_System/app.log
```

## 4. 服务管理

### 4.1 手动服务管理
```bash
# 启动服务
cd /opt/AI_Support_System
source venv/bin/activate
nohup python app/main.py > app.log 2>&1 &
echo $! > app.pid

# 停止服务
kill $(cat app.pid)
rm -f app.pid

# 重启服务
kill $(cat app.pid) && sleep 2 && nohup python app/main.py > app.log 2>&1 & && echo $! > app.pid
```

### 4.2 使用systemd服务（推荐）
```bash
# 创建systemd服务文件
sudo tee /etc/systemd/system/ai-support-system.service > /dev/null << EOF
[Unit]
Description=AI Support System
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/opt/AI_Support_System
Environment=PATH=/opt/AI_Support_System/venv/bin
ExecStart=/opt/AI_Support_System/venv/bin/python app/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 重新加载systemd配置
sudo systemctl daemon-reload

# 启用并启动服务
sudo systemctl enable ai-support-system
sudo systemctl start ai-support-system

# 检查服务状态
sudo systemctl status ai-support-system

# 查看服务日志
sudo journalctl -u ai-support-system -f
```

## 5. 防火墙配置

### 5.1 开放端口
```bash
# Ubuntu/Debian (ufw)
sudo ufw allow 5000/tcp
sudo ufw reload

# CentOS/RHEL (firewalld)
sudo firewall-cmd --permanent --add-port=5000/tcp
sudo firewall-cmd --reload

# 或者使用iptables
sudo iptables -A INPUT -p tcp --dport 5000 -j ACCEPT
sudo iptables-save > /etc/iptables/rules.v4
```

### 5.2 配置Nginx反向代理（可选）
```bash
# 安装Nginx
sudo apt install nginx  # Ubuntu/Debian
sudo yum install nginx  # CentOS/RHEL

# 创建Nginx配置
sudo tee /etc/nginx/sites-available/ai-support-system > /dev/null << EOF
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# 启用站点
sudo ln -s /etc/nginx/sites-available/ai-support-system /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 6. 监控和日志

### 6.1 日志管理
```bash
# 查看应用日志
tail -f /opt/AI_Support_System/app.log

# 查看部署日志
tail -f /opt/AI_Support_System/deploy.log

# 查看更新日志
tail -f /opt/AI_Support_System/update.log

# 日志轮转配置
sudo tee /etc/logrotate.d/ai-support-system > /dev/null << EOF
/opt/AI_Support_System/*.log {
    daily
    missingok
    rotate 7
    compress
    delaycompress
    notifempty
    create 644 your-username your-username
}
EOF
```

### 6.2 监控脚本
```bash
# 创建监控脚本
cat > /opt/AI_Support_System/monitor.sh << 'EOF'
#!/bin/bash

PID_FILE="/opt/AI_Support_System/app.pid"
LOG_FILE="/opt/AI_Support_System/monitor.log"

if [ -f $PID_FILE ]; then
    PID=$(cat $PID_FILE)
    if ! ps -p $PID > /dev/null 2>&1; then
        echo "$(date): Process $PID not running, restarting..." >> $LOG_FILE
        cd /opt/AI_Support_System
        source venv/bin/activate
        nohup python app/main.py > app.log 2>&1 &
        echo $! > $PID_FILE
    fi
else
    echo "$(date): PID file not found, starting service..." >> $LOG_FILE
    cd /opt/AI_Support_System
    source venv/bin/activate
    nohup python app/main.py > app.log 2>&1 &
    echo $! > $PID_FILE
fi
EOF

chmod +x /opt/AI_Support_System/monitor.sh

# 添加到crontab（每分钟检查一次）
(crontab -l 2>/dev/null; echo "* * * * * /opt/AI_Support_System/monitor.sh") | crontab -
```

## 7. 故障排除

### 7.1 常见问题
```bash
# 检查端口占用
netstat -tlnp | grep :5000
lsof -i :5000

# 检查进程
ps aux | grep python
ps -p $(cat app.pid)

# 检查日志
tail -f app.log
tail -f deploy.log

# 检查权限
ls -la /opt/AI_Support_System/
```

### 7.2 性能优化
```bash
# 使用gunicorn替代Flask开发服务器
pip install gunicorn

# 启动gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app.main:app

# 或使用systemd管理gunicorn
sudo tee /etc/systemd/system/ai-support-system.service > /dev/null << EOF
[Unit]
Description=AI Support System
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/opt/AI_Support_System
Environment=PATH=/opt/AI_Support_System/venv/bin
ExecStart=/opt/AI_Support_System/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 app.main:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
```

## 8. 安全建议

### 8.1 基本安全配置
```bash
# 创建专用用户
sudo useradd -m -s /bin/bash ai-support
sudo usermod -aG sudo ai-support

# 设置SSH密钥认证
sudo nano /etc/ssh/sshd_config
# 设置: PasswordAuthentication no
sudo systemctl restart ssh

# 配置防火墙
sudo ufw enable
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 5000/tcp
```

### 8.2 SSL证书配置（可选）
```bash
# 使用Let's Encrypt
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com

# 自动续期
sudo crontab -e
# 添加: 0 12 * * * /usr/bin/certbot renew --quiet
```
