# AI Support System 快速启动指南

## 🚀 5分钟快速部署

### 本地开发环境

#### Windows 用户
1. **运行环境设置脚本**
   ```cmd
   cd test\scripts
   setup-windows.bat
   ```

2. **启动应用**
   ```cmd
   cd test\app
   start-app.bat
   ```

3. **测试API**
   ```cmd
   cd test\app
   test-api.bat
   ```

#### Linux/Mac 用户
1. **设置环境**
   ```bash
   cd test/scripts
   chmod +x setup-server.sh
   ./setup-server.sh
   ```

2. **启动应用**
   ```bash
   cd test/app
   python main.py
   ```

### 生产环境部署

#### 1. 上传代码到GitHub
```bash
# 使用SourceTree或命令行
git add .
git commit -m "Initial commit"
git push origin main
```

#### 2. 服务器部署
```bash
# 在阿里云服务器上执行
cd /var/www
git clone https://github.com/你的用户名/AI_Support_System.git
cd AI_Support_System/test/scripts
chmod +x *.sh
./setup-server.sh
./deploy.sh production main
```

---

## 📋 详细步骤

### 步骤1: 环境准备
- [ ] 安装Python 3.8+
- [ ] 安装Git
- [ ] 安装SourceTree（可选）
- [ ] 注册GitHub账号
- [ ] 购买阿里云ECS实例

### 步骤2: 代码管理
- [ ] 克隆或创建项目
- [ ] 配置Git用户信息
- [ ] 创建.gitignore文件
- [ ] 提交初始代码

### 步骤3: 本地测试
- [ ] 创建虚拟环境
- [ ] 安装依赖包
- [ ] 运行应用
- [ ] 执行API测试

### 步骤4: 服务器部署
- [ ] 配置服务器环境
- [ ] 克隆代码到服务器
- [ ] 配置Nginx反向代理
- [ ] 设置systemd服务
- [ ] 配置SSL证书

### 步骤5: 验证部署
- [ ] 健康检查
- [ ] API功能测试
- [ ] 性能测试
- [ ] 安全配置检查

---

## 🔧 常用命令

### 开发环境
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 启动应用
python main.py

# 运行测试
python fronted_api_test.py
```

### 生产环境
```bash
# 部署应用
./deploy.sh production main

# 备份数据
./backup.sh full

# 查看服务状态
sudo systemctl status ai-support-system

# 查看日志
sudo journalctl -u ai-support-system -f

# 重启服务
sudo systemctl restart ai-support-system
```

---

## 🆘 故障排除

### 常见问题

#### 1. 端口被占用
```bash
# 查看端口占用
netstat -tlnp | grep :5000

# 杀死占用进程
sudo kill -9 PID
```

#### 2. 权限问题
```bash
# 修改文件权限
sudo chown -R www-data:www-data /var/www/ai-support-system
sudo chmod -R 755 /var/www/ai-support-system
```

#### 3. 依赖安装失败
```bash
# 更新pip
pip install --upgrade pip

# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

#### 4. 服务启动失败
```bash
# 查看详细错误
sudo journalctl -u ai-support-system -n 50

# 检查配置文件
sudo nginx -t
```

---

## 📞 获取帮助

### 文档资源
- [部署指南](deployment-guide.md)
- [SourceTree操作指南](sourcetree-guide.md)
- [部署检查清单](deployment-checklist.md)

### 技术支持
- 查看项目README.md
- 检查GitHub Issues
- 联系开发团队

---

**快速启动指南版本**: v1.0  
**最后更新**: 2024年10月  
**适用环境**: Windows, Linux, macOS
