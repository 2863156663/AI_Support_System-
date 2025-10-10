# GitLab 工作流程指南

## 1. 初始设置

### 1.1 配置SSH密钥
```bash
# 生成SSH密钥（如果还没有）
ssh-keygen -t rsa -b 4096 -C "your.email@example.com"

# 将公钥添加到GitLab
cat ~/.ssh/id_rsa.pub
# 复制输出内容到 GitLab -> Settings -> SSH Keys
```

### 1.2 克隆项目到本地
```bash
# 克隆dev分支
git clone -b dev git@your.gitlab.server:group/project.git
cd project

# 查看当前分支
git branch -a
```

## 2. 日常开发流程

### 2.1 创建新功能分支
```bash
# 从dev分支创建新分支
git checkout dev
git pull origin dev
git checkout -b feature/your-feature-name

# 或者使用一条命令
git checkout -b feature/your-feature-name origin/dev
```

### 2.2 本地开发和测试
```bash
# 安装依赖
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r app/requirements.txt

# 启动本地服务
python app/main.py

# 在另一个终端测试API
curl http://localhost:5000/
curl http://localhost:5000/api/status
```

### 2.3 提交代码
```bash
# 查看修改状态
git status

# 添加修改的文件
git add .

# 或者添加特定文件
git add app/main.py

# 提交代码
git commit -m "feat: add new API endpoint"

# 推送到远程分支
git push origin feature/your-feature-name
```

### 2.4 创建合并请求
1. 在GitLab网页界面创建Merge Request
2. 从 `feature/your-feature-name` 合并到 `dev`
3. 添加描述和审查者
4. 等待代码审查和合并

## 3. 分支管理策略

### 3.1 分支类型
- `main/master`: 生产环境代码
- `dev`: 开发环境代码
- `feature/*`: 功能开发分支
- `hotfix/*`: 紧急修复分支

### 3.2 命名规范
```bash
# 功能分支
feature/user-authentication
feature/api-integration

# 修复分支
hotfix/critical-bug-fix
hotfix/security-patch

# 发布分支
release/v1.2.0
```

## 4. 常用Git命令

### 4.1 查看信息
```bash
# 查看提交历史
git log --oneline

# 查看分支
git branch -a

# 查看远程仓库
git remote -v

# 查看状态
git status
```

### 4.2 同步代码
```bash
# 拉取最新代码
git pull origin dev

# 获取远程更新但不合并
git fetch origin

# 合并远程分支
git merge origin/dev
```

### 4.3 撤销操作
```bash
# 撤销工作区修改
git checkout -- filename

# 撤销暂存区修改
git reset HEAD filename

# 撤销最后一次提交
git reset --soft HEAD~1
```

## 5. 最佳实践

### 5.1 提交信息规范
```
feat: 新功能
fix: 修复bug
docs: 文档更新
style: 代码格式调整
refactor: 代码重构
test: 测试相关
chore: 构建过程或辅助工具的变动

示例:
feat: add user authentication API
fix: resolve memory leak in data processing
docs: update API documentation
```

### 5.2 代码审查检查点
- [ ] 代码逻辑正确
- [ ] 没有硬编码的配置
- [ ] 包含必要的错误处理
- [ ] 添加了适当的日志
- [ ] 更新了相关文档
- [ ] 通过了所有测试

### 5.3 冲突解决
```bash
# 当出现合并冲突时
git status  # 查看冲突文件
# 手动编辑冲突文件，解决冲突标记
git add resolved-file
git commit -m "resolve merge conflict"
```

## 6. 故障排除

### 6.1 常见问题
```bash
# SSH连接问题
ssh -T git@your.gitlab.server

# 权限问题
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 大文件问题
git lfs track "*.large-file"
git add .gitattributes
```

### 6.2 重置到远程状态
```bash
# 强制重置到远程dev分支
git fetch origin
git reset --hard origin/dev

# 清理未跟踪文件
git clean -fd
```
