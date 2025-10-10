#!/bin/bash
# 阿里云服务器初始化配置脚本
# 使用方法: ./setup-server.sh

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_info "开始配置阿里云服务器..."

# 1. 系统更新
log_info "更新系统包..."
apt update && apt upgrade -y
log_success "系统更新完成"

# 2. 安装基础工具
log_info "安装基础工具..."
apt install -y curl wget git vim htop tree unzip software-properties-common
log_success "基础工具安装完成"

# 3. 安装Python3和pip
log_info "安装Python3和pip..."
apt install -y python3 python3-pip python3-venv python3-dev
log_success "Python3安装完成"

# 4. 安装Nginx
log_info "安装Nginx..."
apt install -y nginx
systemctl start nginx
systemctl enable nginx
log_success "Nginx安装完成"

# 5. 配置防火墙
log_info "配置防火墙..."
ufw --force enable
ufw allow ssh
ufw allow 'Nginx Full'
ufw allow 5000/tcp
log_success "防火墙配置完成"

# 6. 创建应用用户
log_info "创建应用用户..."
if ! id "ai-support" &>/dev/null; then
    useradd -m -s /bin/bash ai-support
    usermod -aG sudo ai-support
    log_success "应用用户创建完成"
else
    log_info "应用用户已存在"
fi

# 7. 创建项目目录
log_info "创建项目目录..."
mkdir -p /var/www/ai-support-system
chown ai-support:ai-support /var/www/ai-support-system
log_success "项目目录创建完成"

# 8. 安装Node.js（如果需要前端构建）
log_info "安装Node.js..."
curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
apt install -y nodejs
log_success "Node.js安装完成"

# 9. 安装PM2（进程管理器）
log_info "安装PM2..."
npm install -g pm2
log_success "PM2安装完成"

# 10. 配置SSH安全
log_info "配置SSH安全..."
sed -i 's/#PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
systemctl restart ssh
log_success "SSH安全配置完成"

# 11. 安装监控工具
log_info "安装监控工具..."
apt install -y htop iotop nethogs
log_success "监控工具安装完成"

# 12. 配置时区
log_info "配置时区..."
timedatectl set-timezone Asia/Shanghai
log_success "时区配置完成"

# 13. 创建备份目录
log_info "创建备份目录..."
mkdir -p /var/backups/ai-support-system
chown ai-support:ai-support /var/backups/ai-support-system
log_success "备份目录创建完成"

# 14. 安装Docker（可选）
read -p "是否安装Docker? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    log_info "安装Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    usermod -aG docker ai-support
    systemctl start docker
    systemctl enable docker
    log_success "Docker安装完成"
fi

# 15. 安装Certbot（SSL证书）
log_info "安装Certbot..."
apt install -y certbot python3-certbot-nginx
log_success "Certbot安装完成"

# 16. 配置系统优化
log_info "配置系统优化..."
cat >> /etc/sysctl.conf << EOF
# 网络优化
net.core.rmem_max = 16777216
net.core.wmem_max = 16777216
net.ipv4.tcp_rmem = 4096 65536 16777216
net.ipv4.tcp_wmem = 4096 65536 16777216
net.core.netdev_max_backlog = 5000
net.ipv4.tcp_window_scaling = 1
EOF

sysctl -p
log_success "系统优化配置完成"

# 17. 创建部署脚本
log_info "创建部署脚本..."
cat > /home/ai-support/deploy.sh << 'EOF'
#!/bin/bash
cd /var/www/ai-support-system
git pull origin main
source test/venv/bin/activate
pip install -r test/app/requirements.txt
sudo systemctl restart ai-support-system
EOF

chmod +x /home/ai-support/deploy.sh
chown ai-support:ai-support /home/ai-support/deploy.sh
log_success "部署脚本创建完成"

# 18. 显示系统信息
log_info "系统配置完成！"
echo "=================================="
echo "系统信息:"
echo "操作系统: $(lsb_release -d | cut -f2)"
echo "内核版本: $(uname -r)"
echo "Python版本: $(python3 --version)"
echo "Node.js版本: $(node --version)"
echo "Nginx版本: $(nginx -v 2>&1)"
echo "=================================="

log_success "服务器初始化配置完成！"
log_info "下一步请按照部署指南进行应用部署"
