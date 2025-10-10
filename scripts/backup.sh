#!/bin/bash
# AI Support System 备份脚本
# 使用方法: ./backup.sh [备份类型]
# 示例: ./backup.sh full

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

# 配置变量
PROJECT_DIR="/var/www/ai-support-system"
BACKUP_DIR="/var/backups/ai-support-system"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_TYPE=${1:-full}

# 创建备份目录
mkdir -p "$BACKUP_DIR"

log_info "开始备份 AI Support System"
log_info "备份类型: $BACKUP_TYPE"
log_info "备份时间: $(date)"

case $BACKUP_TYPE in
    "full")
        log_info "执行完整备份..."
        
        # 备份代码
        CODE_BACKUP="$BACKUP_DIR/code_$DATE.tar.gz"
        tar -czf "$CODE_BACKUP" \
            -C "$PROJECT_DIR" \
            --exclude='venv' \
            --exclude='__pycache__' \
            --exclude='*.pyc' \
            --exclude='.git' \
            .
        log_success "代码备份完成: $CODE_BACKUP"
        
        # 备份配置文件
        CONFIG_BACKUP="$BACKUP_DIR/config_$DATE.tar.gz"
        tar -czf "$CONFIG_BACKUP" \
            /etc/nginx/sites-available/ai-support-system \
            /etc/systemd/system/ai-support-system.service \
            /var/www/ai-support-system/.env 2>/dev/null || true
        log_success "配置备份完成: $CONFIG_BACKUP"
        
        # 备份数据库（如果有）
        if command -v mysqldump &> /dev/null; then
            DB_BACKUP="$BACKUP_DIR/database_$DATE.sql"
            mysqldump -u root -p --all-databases > "$DB_BACKUP" 2>/dev/null || log_warning "数据库备份跳过"
            log_success "数据库备份完成: $DB_BACKUP"
        fi
        
        ;;
        
    "code")
        log_info "执行代码备份..."
        CODE_BACKUP="$BACKUP_DIR/code_$DATE.tar.gz"
        tar -czf "$CODE_BACKUP" \
            -C "$PROJECT_DIR" \
            --exclude='venv' \
            --exclude='__pycache__' \
            --exclude='*.pyc' \
            --exclude='.git' \
            .
        log_success "代码备份完成: $CODE_BACKUP"
        ;;
        
    "config")
        log_info "执行配置备份..."
        CONFIG_BACKUP="$BACKUP_DIR/config_$DATE.tar.gz"
        tar -czf "$CONFIG_BACKUP" \
            /etc/nginx/sites-available/ai-support-system \
            /etc/systemd/system/ai-support-system.service \
            /var/www/ai-support-system/.env 2>/dev/null || true
        log_success "配置备份完成: $CONFIG_BACKUP"
        ;;
        
    "database")
        log_info "执行数据库备份..."
        if command -v mysqldump &> /dev/null; then
            DB_BACKUP="$BACKUP_DIR/database_$DATE.sql"
            mysqldump -u root -p --all-databases > "$DB_BACKUP" 2>/dev/null || log_warning "数据库备份跳过"
            log_success "数据库备份完成: $DB_BACKUP"
        else
            log_warning "MySQL未安装，跳过数据库备份"
        fi
        ;;
        
    *)
        log_error "未知的备份类型: $BACKUP_TYPE"
        log_info "支持的备份类型: full, code, config, database"
        exit 1
        ;;
esac

# 清理旧备份（保留最近30天）
log_info "清理旧备份..."
find "$BACKUP_DIR" -name "*.tar.gz" -mtime +30 -delete
find "$BACKUP_DIR" -name "*.sql" -mtime +30 -delete

# 显示备份信息
log_info "备份完成！"
log_info "备份目录: $BACKUP_DIR"
log_info "备份文件:"
ls -lh "$BACKUP_DIR"/*$DATE* 2>/dev/null || log_warning "未找到备份文件"

# 计算备份大小
BACKUP_SIZE=$(du -sh "$BACKUP_DIR" | cut -f1)
log_info "总备份大小: $BACKUP_SIZE"
