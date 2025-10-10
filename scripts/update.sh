#!/bin/bash

# AI Support System - 代码更新脚本
# 用于更新服务器上的应用代码并重启服务

set -e  # 遇到错误立即退出

# 配置变量
PROJECT_NAME="AI_Support_System"
APP_DIR="/opt/$PROJECT_NAME"
VENV_DIR="$APP_DIR/venv"
LOG_FILE="$APP_DIR/update.log"
PID_FILE="$APP_DIR/app.pid"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 日志函数
log() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] $1${NC}" | tee -a $LOG_FILE
}

warn() {
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}" | tee -a $LOG_FILE
}

error() {
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}" | tee -a $LOG_FILE
    exit 1
}

# 检查应用目录是否存在
check_app_directory() {
    if [ ! -d $APP_DIR ]; then
        error "Application directory not found: $APP_DIR. Please run deploy.sh first."
    fi
    
    if [ ! -d "$APP_DIR/.git" ]; then
        error "Git repository not found in: $APP_DIR"
    fi
    
    log "Application directory verified: $APP_DIR"
}

# 备份当前版本
backup_current_version() {
    log "Creating backup of current version..."
    
    BACKUP_DIR="$APP_DIR/backups/$(date +%Y%m%d_%H%M%S)"
    mkdir -p $BACKUP_DIR
    
    # 备份应用代码（排除.git和venv）
    rsync -av --exclude='.git' --exclude='venv' --exclude='backups' --exclude='*.log' \
          $APP_DIR/ $BACKUP_DIR/
    
    log "Backup created: $BACKUP_DIR"
}

# 停止服务
stop_service() {
    log "Stopping current service..."
    
    if [ -f $PID_FILE ]; then
        PID=$(cat $PID_FILE)
        if ps -p $PID > /dev/null 2>&1; then
            log "Stopping process $PID..."
            kill $PID
            
            # 等待进程优雅退出
            for i in {1..10}; do
                if ! ps -p $PID > /dev/null 2>&1; then
                    break
                fi
                sleep 1
            done
            
            # 强制杀死如果还在运行
            if ps -p $PID > /dev/null 2>&1; then
                warn "Process still running, force killing..."
                kill -9 $PID
            fi
        fi
        rm -f $PID_FILE
        log "Service stopped successfully."
    else
        log "No running service found."
    fi
}

# 更新代码
update_code() {
    log "Updating code from GitLab..."
    
    cd $APP_DIR
    
    # 获取最新代码
    git fetch origin
    
    # 检查是否有更新
    LOCAL=$(git rev-parse HEAD)
    REMOTE=$(git rev-parse origin/dev)
    
    if [ "$LOCAL" = "$REMOTE" ]; then
        log "No updates available. Code is already up to date."
        return 0
    fi
    
    log "Updates found. Pulling latest changes..."
    
    # 拉取最新代码
    git pull origin dev
    
    # 清理未跟踪文件
    git clean -fd
    
    log "Code updated successfully."
    return 1
}

# 更新依赖
update_dependencies() {
    log "Updating Python dependencies..."
    
    if [ ! -d $VENV_DIR ]; then
        error "Virtual environment not found: $VENV_DIR"
    fi
    
    source $VENV_DIR/bin/activate
    
    # 升级pip
    pip install --upgrade pip
    
    # 安装/更新依赖
    pip install -r $APP_DIR/app/requirements.txt
    
    log "Dependencies updated successfully."
}

# 启动服务
start_service() {
    log "Starting updated service..."
    
    cd $APP_DIR
    source $VENV_DIR/bin/activate
    
    # 设置环境变量
    export FLASK_APP=app/main.py
    export FLASK_ENV=production
    export FLASK_HOST=0.0.0.0
    export FLASK_PORT=5000
    
    # 后台启动服务
    nohup python app/main.py > $APP_DIR/app.log 2>&1 &
    echo $! > $PID_FILE
    
    # 等待服务启动
    sleep 3
    
    # 检查服务是否启动成功
    if ps -p $(cat $PID_FILE) > /dev/null 2>&1; then
        log "Service started successfully. PID: $(cat $PID_FILE)"
    else
        error "Failed to start service. Check log file: $APP_DIR/app.log"
    fi
}

# 健康检查
health_check() {
    log "Performing health check..."
    
    # 等待服务完全启动
    sleep 5
    
    # 检查服务是否响应
    for i in {1..5}; do
        if curl -f http://localhost:5000/ > /dev/null 2>&1; then
            log "Health check passed. Service is responding."
            return 0
        fi
        warn "Health check attempt $i failed. Retrying..."
        sleep 2
    done
    
    error "Health check failed after 5 attempts. Service may not be working properly."
}

# 回滚功能
rollback() {
    warn "Rolling back to previous version..."
    
    # 查找最新的备份
    LATEST_BACKUP=$(ls -t $APP_DIR/backups/ | head -n1)
    
    if [ -z "$LATEST_BACKUP" ]; then
        error "No backup found for rollback."
    fi
    
    log "Rolling back to: $LATEST_BACKUP"
    
    # 停止当前服务
    stop_service
    
    # 恢复备份
    rsync -av --exclude='.git' --exclude='venv' --exclude='backups' --exclude='*.log' \
          $APP_DIR/backups/$LATEST_BACKUP/ $APP_DIR/
    
    # 重启服务
    start_service
    health_check
    
    log "Rollback completed successfully."
}

# 显示更新信息
show_update_info() {
    log "Update completed successfully!"
    echo ""
    echo "=== Update Information ==="
    echo "Application Directory: $APP_DIR"
    echo "Process ID: $(cat $PID_FILE 2>/dev/null || echo 'N/A')"
    echo "Log File: $APP_DIR/app.log"
    echo "Update Log: $LOG_FILE"
    echo "Service URL: http://$(hostname -I | awk '{print $1}'):5000"
    echo ""
    echo "=== Useful Commands ==="
    echo "View logs: tail -f $APP_DIR/app.log"
    echo "Check status: ps -p \$(cat $PID_FILE)"
    echo "View update log: tail -f $LOG_FILE"
    echo "Rollback: $0 --rollback"
    echo ""
}

# 主函数
main() {
    local rollback_mode=false
    
    # 解析命令行参数
    while [[ $# -gt 0 ]]; do
        case $1 in
            --rollback)
                rollback_mode=true
                shift
                ;;
            *)
                error "Unknown option: $1"
                ;;
        esac
    done
    
    if [ "$rollback_mode" = true ]; then
        rollback
        return
    fi
    
    log "Starting code update for $PROJECT_NAME..."
    
    check_app_directory
    backup_current_version
    stop_service
    
    # 更新代码
    if update_code; then
        log "No updates needed. Service is already running the latest version."
        return
    fi
    
    update_dependencies
    start_service
    health_check
    show_update_info
    
    log "Update completed successfully!"
}

# 脚本入口
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
