# SourceTree 详细操作指南

## 📋 目录
- [1. SourceTree 安装与配置](#1-sourcetree-安装与配置)
- [2. 创建和克隆仓库](#2-创建和克隆仓库)
- [3. 日常操作流程](#3-日常操作流程)
- [4. 分支管理](#4-分支管理)
- [5. 冲突解决](#5-冲突解决)
- [6. 高级功能](#6-高级功能)

---

## 1. SourceTree 安装与配置

### 1.1 下载和安装

#### Windows 安装
1. 访问 [SourceTree官网](https://www.sourcetreeapp.com/)
2. 点击 "Download for Windows"
3. 下载完成后运行安装程序
4. 按照向导完成安装

#### 首次启动配置
1. **选择Git版本**：选择 "Use bundled Git" 或 "Use system Git"
2. **配置用户信息**：
   ```
   Full Name: 你的姓名
   Email Address: 你的邮箱@example.com
   ```
3. **SSH密钥配置**（推荐）：
   - 点击 "Tools" → "Create or Import SSH Keys"
   - 生成新的SSH密钥对
   - 将公钥添加到GitHub账户

### 1.2 GitHub 集成配置

#### 添加GitHub账户
1. 点击 "Tools" → "Options"
2. 选择 "Authentication" 标签
3. 点击 "Add" 添加GitHub账户
4. 选择认证方式：
   - **HTTPS**: 使用用户名和密码/令牌
   - **SSH**: 使用SSH密钥（推荐）

#### SSH密钥配置详细步骤
```bash
# 1. 生成SSH密钥
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

# 2. 启动ssh-agent
eval "$(ssh-agent -s)"

# 3. 添加私钥到ssh-agent
ssh-add ~/.ssh/id_rsa

# 4. 复制公钥内容
cat ~/.ssh/id_rsa.pub
```

在GitHub中添加SSH密钥：
1. 登录GitHub → Settings → SSH and GPG keys
2. 点击 "New SSH key"
3. 粘贴公钥内容并保存

---

## 2. 创建和克隆仓库

### 2.1 创建新仓库

#### 方法一：在GitHub上创建后克隆
1. 登录GitHub，点击 "New repository"
2. 填写仓库信息：
   - **Repository name**: `AI_Support_System`
   - **Description**: `AI Support System API`
   - **Visibility**: Public 或 Private
   - **Initialize**: 勾选 "Add a README file"
3. 点击 "Create repository"

#### 在SourceTree中克隆
1. 打开SourceTree
2. 点击 "Clone" 按钮
3. 填写克隆信息：
   - **Source URL**: `git@github.com:你的用户名/AI_Support_System.git`
   - **Destination Path**: `F:\1DZ\AI_Support_System`
   - **Name**: `AI_Support_System`
4. 点击 "Clone"

### 2.2 初始化本地仓库

#### 如果已有项目代码
1. 在SourceTree中点击 "Create" → "Create Local Repository"
2. 选择项目目录：`F:\1DZ\AI_Support_System`
3. 点击 "Create"
4. 添加远程仓库：
   - 点击 "Repository" → "Repository Settings"
   - 在 "Remotes" 标签中点击 "Add"
   - 填写远程仓库信息

---

## 3. 日常操作流程

### 3.1 提交代码的标准流程

#### 步骤1：查看更改
1. 在SourceTree中打开项目
2. 在左侧面板选择 "Working Copy"
3. 查看 "Unstaged files" 中的更改
4. 双击文件查看具体修改内容

#### 步骤2：暂存文件
1. 选择要提交的文件
2. 点击 "Stage" 按钮或双击文件
3. 文件会移动到 "Staged files" 区域
4. 可以使用 "Stage All" 暂存所有更改

#### 步骤3：编写提交信息
1. 在底部 "Commit message" 区域输入提交信息
2. 遵循提交信息规范：
   ```
   类型(范围): 简短描述
   
   详细描述（可选）
   
   相关Issue: #123
   ```
   
   示例：
   ```
   feat(api): 添加用户档案验证接口
   
   - 实现POST /api/user-profile/{id}/validate接口
   - 支持详细和简单两种验证格式
   - 添加Query参数支持
   
   相关Issue: #15
   ```

#### 步骤4：提交代码
1. 点击 "Commit" 按钮
2. 提交成功后，更改会显示在历史记录中

#### 步骤5：推送到远程仓库
1. 点击 "Push" 按钮
2. 选择远程仓库和分支
3. 点击 "Push"

### 3.2 拉取最新代码

#### 从远程仓库拉取
1. 点击 "Pull" 按钮
2. 选择远程仓库和分支
3. 点击 "Pull"

#### 处理拉取冲突
如果出现冲突，SourceTree会显示冲突文件：
1. 双击冲突文件
2. 在编辑器中解决冲突
3. 保存文件
4. 在SourceTree中标记为已解决
5. 提交合并结果

---

## 4. 分支管理

### 4.1 创建分支

#### 创建新分支
1. 点击 "Branch" 按钮
2. 输入分支名称：`feature/user-profile-validation`
3. 选择基于哪个分支创建（通常是master/main）
4. 点击 "Create Branch"

#### 分支命名规范
- **功能分支**: `feature/功能描述`
- **修复分支**: `fix/问题描述`
- **发布分支**: `release/版本号`
- **热修复分支**: `hotfix/问题描述`

### 4.2 切换分支

#### 切换本地分支
1. 在左侧面板选择 "Branches"
2. 双击要切换的分支
3. 或者右键点击分支 → "Checkout"

#### 创建远程分支跟踪
1. 右键点击远程分支
2. 选择 "Checkout"
3. 输入本地分支名称
4. 点击 "OK"

### 4.3 合并分支

#### 合并到主分支
1. 切换到目标分支（如master）
2. 点击 "Merge" 按钮
3. 选择要合并的分支
4. 点击 "Merge"

#### 创建Pull Request
1. 推送功能分支到远程仓库
2. 在GitHub上创建Pull Request
3. 等待代码审查
4. 合并后删除功能分支

---

## 5. 冲突解决

### 5.1 识别冲突

#### 冲突标识
SourceTree会在以下情况显示冲突：
- 文件状态显示为 "Conflicted"
- 历史记录中显示合并冲突
- 拉取时提示冲突

### 5.2 解决冲突

#### 使用SourceTree内置编辑器
1. 双击冲突文件
2. 在编辑器中查看冲突标记：
   ```
   <<<<<<< HEAD
   你的更改
   =======
   其他人的更改
   >>>>>>> branch-name
   ```
3. 编辑文件，删除冲突标记，保留需要的代码
4. 保存文件

#### 使用外部工具
1. 配置合并工具：
   - "Tools" → "Options" → "Diff"
   - 选择外部合并工具（如Beyond Compare, VS Code等）
2. 右键冲突文件 → "Resolve Conflicts" → "Launch External Merge Tool"

#### 标记冲突已解决
1. 解决所有冲突后
2. 在SourceTree中右键冲突文件
3. 选择 "Resolve Conflicts" → "Mark Resolved"
4. 提交合并结果

---

## 6. 高级功能

### 6.1 历史记录管理

#### 查看提交历史
1. 在左侧面板选择 "History"
2. 查看提交历史树
3. 点击提交查看详细信息
4. 双击文件查看具体更改

#### 回滚更改
1. 右键点击要回滚的提交
2. 选择 "Reset current branch to this commit"
3. 选择回滚类型：
   - **Soft**: 保留更改在暂存区
   - **Mixed**: 保留更改在工作区
   - **Hard**: 完全删除更改

### 6.2 标签管理

#### 创建标签
1. 右键点击要标记的提交
2. 选择 "Tag"
3. 输入标签名称：`v1.0.0`
4. 添加标签描述
5. 点击 "Create Tag"

#### 推送标签
1. 点击 "Push" 按钮
2. 勾选 "Push tags"
3. 点击 "Push"

### 6.3 子模块管理

#### 添加子模块
1. "Repository" → "Submodules" → "Add Submodule"
2. 填写子模块信息
3. 点击 "Add"

#### 更新子模块
1. "Repository" → "Submodules" → "Update Submodules"
2. 选择要更新的子模块
3. 点击 "Update"

### 6.4 工作流管理

#### 创建书签
1. 右键点击提交
2. 选择 "Bookmark this commit"
3. 输入书签名称
4. 用于标记重要的提交点

#### 使用Stash
1. 点击 "Stash" 按钮
2. 输入Stash描述
3. 点击 "Stash"
4. 稍后可以通过 "Stash" 面板恢复

---

## 7. 最佳实践

### 7.1 提交规范

#### 提交信息格式
```
<type>(<scope>): <subject>

<body>

<footer>
```

#### 类型说明
- **feat**: 新功能
- **fix**: 修复bug
- **docs**: 文档更新
- **style**: 代码格式调整
- **refactor**: 代码重构
- **test**: 测试相关
- **chore**: 构建过程或辅助工具的变动

### 7.2 分支策略

#### Git Flow 模型
```
master (生产环境)
├── develop (开发环境)
├── feature/功能名 (功能开发)
├── release/版本号 (发布准备)
└── hotfix/问题名 (紧急修复)
```

#### GitHub Flow 模型
```
main (主分支)
└── feature/功能名 (功能开发)
```

### 7.3 代码审查

#### Pull Request 最佳实践
1. **小批量提交**: 每次PR包含一个完整功能
2. **详细描述**: 说明更改内容和原因
3. **测试验证**: 确保代码经过测试
4. **代码审查**: 至少一人审查通过

---

## 8. 故障排除

### 8.1 常见问题

#### 问题1：无法推送到远程仓库
**可能原因**：
- 没有推送权限
- 远程仓库地址错误
- 网络连接问题

**解决方案**：
1. 检查远程仓库地址：`git remote -v`
2. 验证SSH密钥配置
3. 检查网络连接

#### 问题2：合并冲突频繁
**解决方案**：
1. 经常拉取最新代码
2. 使用功能分支开发
3. 及时合并小改动

#### 问题3：提交历史混乱
**解决方案**：
1. 使用 `git rebase` 整理历史
2. 使用 `git reset` 回滚提交
3. 重新创建分支

### 8.2 性能优化

#### 大仓库优化
1. 使用 `.gitignore` 排除不必要文件
2. 定期清理历史记录
3. 使用浅克隆：`git clone --depth 1`

#### SourceTree 性能优化
1. 关闭不必要的插件
2. 定期清理缓存
3. 使用命令行处理大文件

---

## 📞 技术支持

如果在使用SourceTree过程中遇到问题：

1. 查看SourceTree官方文档
2. 访问GitHub帮助中心
3. 搜索相关错误信息
4. 联系技术支持团队

---

**文档版本**: v1.0  
**最后更新**: 2024年10月  
**适用版本**: SourceTree 4.x
