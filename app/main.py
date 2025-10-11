#!/usr/bin/env python3
"""
AI Support System - 主应用文件
一个简单的Flask API服务，用于测试部署流程
"""

from flask import Flask, jsonify, request
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime, date
import os
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# 配置
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
app.config['HOST'] = os.environ.get('FLASK_HOST', '0.0.0.0')
app.config['PORT'] = int(os.environ.get('FLASK_PORT', 5000))

# Pydantic 模型定义
class Address(BaseModel):
    """地址信息模型"""
    street: str = Field(..., description="街道地址", min_length=1, max_length=200)
    city: str = Field(..., description="城市", min_length=1, max_length=50)
    state: str = Field(..., description="省份/州", min_length=1, max_length=50)
    postal_code: str = Field(..., description="邮政编码", min_length=5, max_length=10)
    country: str = Field(default="中国", description="国家")
    

class ContactInfo(BaseModel):
    """联系信息模型"""
    email: EmailStr = Field(..., description="邮箱地址")
    phone: str = Field(..., description="电话号码", pattern=r'^1[3-9]\d{9}$')
    wechat: Optional[str] = Field(None, description="微信号", max_length=50)
    qq: Optional[str] = Field(None, description="QQ号", max_length=20)
    

class Skill(BaseModel):
    """技能信息模型"""
    name: str = Field(..., description="技能名称", min_length=1, max_length=50)
    level: int = Field(..., description="技能等级", ge=1, le=10)
    years_experience: float = Field(..., description="经验年数", ge=0, le=50)
    certifications: List[str] = Field(default_factory=list, description="相关认证")
    

class Education(BaseModel):
    """教育背景模型"""
    school: str = Field(..., description="学校名称", min_length=1, max_length=100)
    degree: str = Field(..., description="学位", min_length=1, max_length=50)
    major: str = Field(..., description="专业", min_length=1, max_length=50)
    graduation_date: date = Field(..., description="毕业日期")
    gpa: Optional[float] = Field(None, description="GPA", ge=0, le=4.0)
    

class WorkExperience(BaseModel):
    """工作经历模型"""
    company: str = Field(..., description="公司名称", min_length=1, max_length=100)
    position: str = Field(..., description="职位", min_length=1, max_length=50)
    start_date: date = Field(..., description="开始日期")
    end_date: Optional[date] = Field(None, description="结束日期")
    description: str = Field(..., description="工作描述", min_length=10, max_length=1000)
    achievements: List[str] = Field(default_factory=list, description="主要成就")
    

class UserProfile(BaseModel):
    """用户档案模型"""
    personal_info: Dict[str, Any] = Field(..., description="个人信息")
    contact: ContactInfo = Field(..., description="联系信息")
    address: Address = Field(..., description="地址信息")
    skills: List[Skill] = Field(..., description="技能列表", min_items=1)
    education: List[Education] = Field(..., description="教育背景", min_items=1)
    work_experience: List[WorkExperience] = Field(default_factory=list, description="工作经历")
    preferences: Dict[str, Any] = Field(default_factory=dict, description="个人偏好")
    

class UserProfileResponse(BaseModel):
    """用户档案响应模型"""
    user_id: str = Field(..., description="用户ID")
    profile: UserProfile = Field(..., description="用户档案")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    status: str = Field(..., description="状态")
    score: float = Field(..., description="档案完整度评分", ge=0, le=100)

@app.route('/', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        'status': 'healthy',
        'message': 'AI Support System is running',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.route('/api/status', methods=['GET'])
def get_status():
    """获取系统状态"""
    return jsonify({
        'status': 'running',
        'uptime': 'N/A',  # 实际项目中可以计算运行时间
        'environment': os.environ.get('ENVIRONMENT', 'development'),
        'server_info': {
            'host': app.config['HOST'],
            'port': app.config['PORT'],
            'debug': app.config['DEBUG']
        }
    })

@app.route('/api/echo', methods=['POST'])
def echo():
    """回显接口，用于测试POST请求"""
    data = request.get_json()
    return jsonify({
        'message': 'Echo received',
        'received_data': data,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/user-profile', methods=['POST'])
def create_user_profile():
    """创建用户档案接口 - 使用复杂的嵌套Pydantic模型"""
    try:
        # 获取请求数据
        data = request.get_json()
        
        # 验证数据是否符合UserProfile模型
        user_profile = UserProfile(**data)
        
        # 计算档案完整度评分
        score = calculate_profile_score(user_profile)
        
        # 生成用户ID（实际项目中应该从数据库生成）
        user_id = f"user_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # 创建响应数据
        response_data = UserProfileResponse(
            user_id=user_id,
            profile=user_profile,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            status="active",
            score=score
        )
        
        logger.info(f"Created user profile for user_id: {user_id}")
        
        return jsonify({
            'success': True,
            'message': '用户档案创建成功',
            'data': response_data.dict(),
            'timestamp': datetime.now().isoformat()
        }), 201
        
    except Exception as e:
        logger.error(f"Error creating user profile: {str(e)}")
        return jsonify({
            'success': False,
            'message': '用户档案创建失败',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 400

@app.route('/api/user-profile/<user_id>', methods=['GET'])
def get_user_profile(user_id):
    """获取用户档案接口"""
    try:
        # 模拟从数据库获取用户档案（实际项目中应该查询数据库）
        sample_profile = create_sample_profile()
        
        response_data = UserProfileResponse(
            user_id=user_id,
            profile=sample_profile,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            status="active",
            score=calculate_profile_score(sample_profile)
        )
        
        return jsonify({
            'success': True,
            'message': '获取用户档案成功',
            'data': response_data.dict(),
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting user profile: {str(e)}")
        return jsonify({
            'success': False,
            'message': '获取用户档案失败',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/user-profile/<user_id>/validate', methods=['POST'])
def validate_user_profile(user_id):
    """验证用户档案数据接口 - 支持Query Params"""
    try:
        # 获取请求数据
        data = request.get_json()
        
        # 获取Query Params
        include_skills = request.args.get('include_skills', 'true').lower() == 'true'
        include_education = request.args.get('include_education', 'true').lower() == 'true'
        include_work = request.args.get('include_work', 'true').lower() == 'true'
        format_type = request.args.get('format', 'detailed')  # simple 或 detailed
        print('现在有请求参数：', request.args)
        # 验证数据
        user_profile = UserProfile(**data)
        print('现在有用户档案：', user_profile)
        # 计算评分
        score = calculate_profile_score(user_profile)
        
        # 生成验证报告
        validation_report = generate_validation_report(user_profile)
        
        # 根据format参数决定返回格式
        if format_type == 'simple':
            response_data = {
                'success': True,
                'message': '数据验证成功',
                'user_id': user_id,
                'score': score,
                'timestamp': datetime.now().isoformat()
            }
        else:  # detailed
            response_data = {
                'success': True,
                'message': '数据验证成功',
                'user_id': user_id,
                'validation_report': validation_report,
                'score': score,
                'query_params': {
                    'include_skills': include_skills,
                    'include_education': include_education,
                    'include_work': include_work,
                    'format': format_type
                },
                'timestamp': datetime.now().isoformat()
            }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        logger.error(f"Error validating user profile: {str(e)}")
        return jsonify({
            'success': False,
            'message': '数据验证失败',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 400

@app.route('/api/test', methods=['GET'])
def test_endpoint():
    """测试接口"""
    return jsonify({
        'message': 'Test endpoint working',
        'test_data': {
            'string': 'Hello World',
            'number': 42,
            'boolean': True,
            'array': [1, 2, 3, 4, 5]
        },
        'timestamp': datetime.now().isoformat()
    })

@app.errorhandler(404)
def not_found(error):
    """404错误处理"""
    return jsonify({
        'error': 'Not Found',
        'message': 'The requested resource was not found',
        'status_code': 404
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """500错误处理"""
    return jsonify({
        'error': 'Internal Server Error',
        'message': 'An internal server error occurred',
        'status_code': 500
    }), 500

# 辅助函数
def calculate_profile_score(profile: UserProfile) -> float:
    """计算用户档案完整度评分"""
    score = 0.0
    max_score = 100.0
    
    # 个人信息 (20分)
    if profile.personal_info:
        score += 20.0
    
    # 联系信息 (20分)
    if profile.contact:
        score += 20.0
    
    # 地址信息 (15分)
    if profile.address:
        score += 15.0
    
    # 技能信息 (20分)
    if profile.skills:
        score += min(20.0, len(profile.skills) * 5.0)
    
    # 教育背景 (15分)
    if profile.education:
        score += min(15.0, len(profile.education) * 7.5)
    
    # 工作经历 (10分)
    if profile.work_experience:
        score += min(10.0, len(profile.work_experience) * 3.0)
    
    return round(score, 2)

def generate_validation_report(profile: UserProfile) -> Dict[str, Any]:
    """生成验证报告"""
    report = {
        "basic_info_complete": bool(profile.personal_info),
        "contact_info_complete": bool(profile.contact),
        "address_info_complete": bool(profile.address),
        "skills_count": len(profile.skills),
        "education_count": len(profile.education),
        "work_experience_count": len(profile.work_experience),
        "recommendations": []
    }
    
    # 生成建议
    if len(profile.skills) < 3:
        report["recommendations"].append("建议添加更多技能信息")
    
    if len(profile.education) < 1:
        report["recommendations"].append("请添加教育背景信息")
    
    if not profile.work_experience:
        report["recommendations"].append("建议添加工作经历")
    
    if not profile.contact.wechat and not profile.contact.qq:
        report["recommendations"].append("建议添加微信或QQ联系方式")
    
    return report

def create_sample_profile() -> UserProfile:
    """创建示例用户档案"""
    return UserProfile(
        personal_info={
            "name": "张三",
            "age": 28,
            "gender": "男",
            "avatar": "https://example.com/avatar.jpg"
        },
        contact=ContactInfo(
            email="zhangsan@example.com",
            phone="13812345678",
            wechat="zhangsan_wx",
            qq="123456789"
        ),
        address=Address(
            street="中关村大街1号",
            city="北京市",
            state="北京市",
            postal_code="100080",
            country="中国"
        ),
        skills=[
            Skill(
                name="Python",
                level=8,
                years_experience=5.0,
                certifications=["Python认证", "Django认证"]
            ),
            Skill(
                name="JavaScript",
                level=7,
                years_experience=3.0,
                certifications=["React认证"]
            ),
            Skill(
                name="数据库设计",
                level=6,
                years_experience=2.0,
                certifications=[]
            )
        ],
        education=[
            Education(
                school="清华大学",
                degree="学士",
                major="计算机科学与技术",
                graduation_date=date(2018, 6, 1),
                gpa=3.8
            )
        ],
        work_experience=[
            WorkExperience(
                company="腾讯科技",
                position="高级软件工程师",
                start_date=date(2018, 7, 1),
                end_date=date(2021, 6, 30),
                description="负责后端服务开发，使用Python和Django框架开发Web应用",
                achievements=["优化系统性能50%", "带领团队完成3个重要项目"]
            ),
            WorkExperience(
                company="字节跳动",
                position="技术专家",
                start_date=date(2021, 7, 1),
                end_date=None,
                description="负责AI相关产品的技术架构设计和开发",
                achievements=["设计并实现AI推荐系统", "获得公司技术创新奖"]
            )
        ],
        preferences={
            "work_location": "北京",
            "salary_expectation": 50000,
            "work_type": "全职"
        }
    )

if __name__ == '__main__':
    logger.info(f"Starting AI Support System on {app.config['HOST']}:{app.config['PORT']}")
    logger.info(f"Debug mode: {app.config['DEBUG']}")
    
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )
