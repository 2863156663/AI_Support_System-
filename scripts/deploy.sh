#!/bin/bash
# AI Support System 自动部署脚本
# 使用方法: ./deploy.sh [环境] [分支]
# 示例: ./deploy.sh production main

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

# 配置变量
PROJECT_DIR="/var/www/ai-support-system"
APP_DIR="$PROJECT_DIR/test"
VENV_DIR="$APP_DIR/venv"
SERVICE_NAME="ai-support-system"
BACKUP_DIR="/var/backups/ai-support-system"

# 默认参数
ENVIRONMENT=${1:-production}
BRANCH=${2:-main}

log_info "开始部署 AI Support System"
log_info "环境: $ENVIRONMENT"
log_info "分支: $BRANCH"
log_info "项目目录: $PROJECT_DIR"

# 检查是否为root用户
if [[ $EUID -eq 0 ]]; then
   log_error "请不要使用root用户运行此脚本"
   exit 1
fi

# 检查项目目录是否存在
if [ ! -d "$PROJECT_DIR" ]; then
    log_error "项目目录不存在: $PROJECT_DIR"
    exit 1
fi

# 进入项目目录
cd "$PROJECT_DIR"

# 1. 备份当前版本
log_info "创建备份..."
BACKUP_FILE="$BACKUP_DIR/backup_$(date +%Y%m%d_%H%M%S).tar.gz"
mkdir -p "$BACKUP_DIR"
tar -czf "$BACKUP_FILE" . --exclude='venv' --exclude='__pycache__' --exclude='*.pyc'
log_success "备份完成: $BACKUP_FILE"

# 2. 拉取最新代码
log_info "拉取最新代码..."
git fetch origin
git checkout "$BRANCH"
git pull origin "$BRANCH"
log_success "代码更新完成"

# 3. 检查虚拟环境
if [ ! -d "$VENV_DIR" ]; then
    log_info "创建Python虚拟环境..."
    python3 -m venv "$VENV_DIR"
    log_success "虚拟环境创建完成"
fi

# 4. 激活虚拟环境并安装依赖
log_info "安装/更新依赖..."
source "$VENV_DIR/bin/activate"
pip install --upgrade pip
pip install -r "$APP_DIR/app/requirements.txt"
log_success "依赖安装完成"

# 5. 运行测试（可选）
if [ "$ENVIRONMENT" = "production" ]; then
    log_info "运行测试..."
    cd "$APP_DIR"
    if [ -f "test_complex_api.py" ]; then
        python test_complex_api.py || log_warning "测试失败，但继续部署"
    fi
    cd "$PROJECT_DIR"
fi

# 6. 重启服务
log_info "重启服务..."
sudo systemctl restart "$SERVICE_NAME"

# 等待服务启动
sleep 5

# 7. 检查服务状态
log_info "检查服务状态..."
if sudo systemctl is-active --quiet "$SERVICE_NAME"; then
    log_success "服务启动成功"
else
    log_error "服务启动失败"
    sudo systemctl status "$SERVICE_NAME"
    exit 1
fi

# 8. 健康检查
log_info "执行健康检查..."
HEALTH_URL="http://localhost:5000/"
if curl -f -s "$HEALTH_URL" > /dev/null; then
    log_success "健康检查通过"
else
    log_error "健康检查失败"
    exit 1
fi

# 9. 清理旧备份（保留最近7天）
log_info "清理旧备份..."
find "$BACKUP_DIR" -name "backup_*.tar.gz" -mtime +7 -delete

log_success "部署完成！"
log_info "服务状态: $(sudo systemctl is-active $SERVICE_NAME)"
log_info "服务日志: sudo journalctl -u $SERVICE_NAME -f"