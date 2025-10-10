# 代码更新工作流程

## 1. 本地开发更新流程

### 1.1 本地修改和测试
```bash
# 1. 切换到项目目录
cd /path/to/your/local/project

# 2. 确保在dev分支
git checkout dev
git pull origin dev

# 3. 创建新功能分支
git checkout -b feature/your-new-feature

# 4. 进行代码修改
# 编辑相关文件...

# 5. 本地测试
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r app/requirements.txt
python app/main.py

# 6. 在另一个终端测试API
curl http://localhost:5000/
curl http://localhost:5000/api/status
```

### 1.2 提交和推送代码
```bash
# 1. 查看修改状态
git status

# 2. 添加修改的文件
git add .

# 3. 提交代码
git commit -m "feat: add new feature description"

# 4. 推送到远程分支
git push origin feature/your-new-feature

# 5. 在GitLab创建Merge Request
# 从 feature/your-new-feature 合并到 dev
```

### 1.3 合并到dev分支
```bash
# 1. 在GitLab网页界面合并MR
# 2. 删除功能分支（可选）
git branch -d feature/your-new-feature
git push origin --delete feature/your-new-feature

# 3. 更新本地dev分支
git checkout dev
git pull origin dev
```

## 2. 服务器代码更新流程

### 2.1 登录服务器
```bash
# SSH登录到A100服务器
ssh username@your-server-ip

# 切换到项目目录
cd /opt/AI_Support_System
```

### 2.2 手动更新流程
```bash
# 1. 停止当前服务
kill $(cat app.pid)
rm -f app.pid

# 2. 备份当前版本（可选）
cp -r . ../backup-$(date +%Y%m%d_%H%M%S)

# 3. 拉取最新代码
git fetch origin
git pull origin dev

# 4. 更新依赖（如果有新的依赖）
source venv/bin/activate
pip install -r app/requirements.txt

# 5. 启动服务
nohup python app/main.py > app.log 2>&1 &
echo $! > app.pid

# 6. 验证服务启动
sleep 3
ps -p $(cat app.pid)
curl http://localhost:5000/
```

### 2.3 使用更新脚本（推荐）
```bash
# 1. 运行更新脚本
./scripts/update.sh

# 2. 查看更新日志
tail -f update.log

# 3. 验证服务状态
ps -p $(cat app.pid)
curl http://localhost:5000/api/status
```

### 2.4 回滚操作
```bash
# 如果更新出现问题，可以回滚
./scripts/update.sh --rollback

# 或者手动回滚
git log --oneline  # 查看提交历史
git reset --hard HEAD~1  # 回滚到上一个版本
# 重启服务...
```

## 3. 自动化更新流程

### 3.1 设置GitLab Webhook
```bash
# 在GitLab项目设置中添加Webhook
# URL: http://your-server-ip:5000/webhook/update
# Secret Token: your-secret-token
# 触发事件: Push events, Merge request events
```

### 3.2 创建Webhook处理接口
```python
# 在app/main.py中添加webhook接口
@app.route('/webhook/update', methods=['POST'])
def webhook_update():
    import hmac
    import hashlib
    import subprocess
    
    # 验证webhook签名
    signature = request.headers.get('X-Gitlab-Token')
    if signature != 'your-secret-token':
        return jsonify({'error': 'Unauthorized'}), 401
    
    # 执行更新脚本
    try:
        result = subprocess.run(['./scripts/update.sh'], 
                              capture_output=True, text=True)
        return jsonify({
            'status': 'success',
            'output': result.stdout,
            'error': result.stderr
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

### 3.3 设置定时更新检查
```bash
# 添加到crontab，每小时检查一次更新
(crontab -l 2>/dev/null; echo "0 * * * * cd /opt/AI_Support_System && git fetch origin && git log HEAD..origin/dev --oneline | wc -l | xargs -I {} test {} -gt 0 && ./scripts/update.sh") | crontab -
```

## 4. 更新验证流程

### 4.1 服务健康检查
```bash
# 1. 检查进程状态
ps -p $(cat app.pid)

# 2. 检查端口监听
netstat -tlnp | grep :5000

# 3. 测试API响应
curl -f http://localhost:5000/
curl -f http://localhost:5000/api/status

# 4. 检查响应时间
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:5000/
```

### 4.2 使用Postman测试
```bash
# 1. 导入Postman集合
# 2. 设置环境变量 base_url = http://your-server-ip:5000
# 3. 运行所有测试
# 4. 检查测试结果
```

### 4.3 日志检查
```bash
# 1. 检查应用日志
tail -f app.log

# 2. 检查更新日志
tail -f update.log

# 3. 检查系统日志
journalctl -u ai-support-system -f  # 如果使用systemd
```

## 5. 更新最佳实践

### 5.1 更新前准备
- [ ] 确保本地测试通过
- [ ] 代码已合并到dev分支
- [ ] 通知相关人员更新计划
- [ ] 准备回滚方案

### 5.2 更新时机
- 选择业务低峰期进行更新
- 避免在重要活动期间更新
- 考虑时区差异

### 5.3 更新后验证
- [ ] 服务正常启动
- [ ] API响应正常
- [ ] 关键功能测试通过
- [ ] 性能指标正常
- [ ] 日志无异常错误

### 5.4 监控和告警
```bash
# 创建监控脚本
cat > /opt/AI_Support_System/health-check.sh << 'EOF'
#!/bin/bash

URL="http://localhost:5000/"
LOG_FILE="/opt/AI_Support_System/health-check.log"

if curl -f -s $URL > /dev/null; then
    echo "$(date): Health check passed" >> $LOG_FILE
else
    echo "$(date): Health check failed" >> $LOG_FILE
    # 发送告警邮件或通知
    # mail -s "Service Down" admin@example.com < $LOG_FILE
fi
EOF

chmod +x /opt/AI_Support_System/health-check.sh

# 每5分钟检查一次
(crontab -l 2>/dev/null; echo "*/5 * * * * /opt/AI_Support_System/health-check.sh") | crontab -
```

## 6. 故障处理

### 6.1 更新失败处理
```bash
# 1. 检查错误日志
tail -f update.log
tail -f app.log

# 2. 检查Git状态
git status
git log --oneline -5

# 3. 手动回滚
git reset --hard HEAD~1
./scripts/update.sh

# 4. 如果问题严重，使用备份恢复
cp -r ../backup-YYYYMMDD_HHMMSS/* .
```

### 6.2 服务无法启动
```bash
# 1. 检查端口占用
lsof -i :5000

# 2. 检查Python环境
source venv/bin/activate
python --version
pip list

# 3. 检查依赖
pip install -r app/requirements.txt

# 4. 手动启动调试
python app/main.py
```

### 6.3 性能问题
```bash
# 1. 检查系统资源
top
free -h
df -h

# 2. 检查应用性能
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:5000/

# 3. 优化配置
# 调整gunicorn worker数量
# 优化数据库连接
# 增加缓存
```

## 7. 更新记录

### 7.1 更新日志模板
```markdown
## 更新记录 - YYYY-MM-DD HH:MM

### 更新内容
- 功能1: 描述
- 功能2: 描述
- 修复: 描述

### 更新步骤
1. 停止服务
2. 拉取代码
3. 更新依赖
4. 启动服务
5. 验证功能

### 验证结果
- [ ] 服务启动正常
- [ ] API响应正常
- [ ] 功能测试通过

### 回滚方案
- 命令: git reset --hard <commit-hash>
- 备份位置: /opt/backup-YYYYMMDD_HHMMSS
```

### 7.2 版本管理
```bash
# 创建版本标签
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# 查看版本历史
git tag -l
git show v1.0.0
```
