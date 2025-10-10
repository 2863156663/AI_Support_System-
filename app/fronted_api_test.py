#!/usr/bin/env python3
"""
前端API测试脚本 - 模拟前端人员调用AI Support System API
包含完整的用户交互流程和错误处理
"""

import requests
import json
import time
from datetime import datetime, date
from typing import Dict, Any, Optional

class FrontendAPIClient:
    """前端API客户端类"""
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'Frontend-Client/1.0'
        })
    
    def check_server_health(self) -> bool:
        """检查服务器健康状态"""
        try:
            response = self.session.get(f"{self.base_url}/")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ 服务器状态: {data.get('status', 'unknown')}")
                print(f"📅 服务器时间: {data.get('timestamp', 'unknown')}")
                return True
            else:
                print(f"❌ 服务器健康检查失败: {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            print("❌ 无法连接到服务器，请确保Flask应用正在运行")
            return False
        except Exception as e:
            print(f"❌ 健康检查异常: {e}")
            return False
    
    def create_user_profile(self, profile_data: Dict[str, Any]) -> Optional[str]:
        """创建用户档案"""
        try:
            print("\n🔄 正在创建用户档案...")
            response = self.session.post(
                f"{self.base_url}/api/user-profile",
                json=profile_data
            )
            
            if response.status_code == 201:
                data = response.json()
                user_id = data.get('data', {}).get('user_id')
                score = data.get('data', {}).get('score', 0)
                print(f"✅ 用户档案创建成功!")
                print(f"👤 用户ID: {user_id}")
                print(f"📊 档案完整度: {score}%")
                return user_id
            else:
                print(f"❌ 创建失败: {response.status_code}")
                print(f"错误信息: {response.json()}")
                return None
                
        except Exception as e:
            print(f"❌ 创建用户档案异常: {e}")
            return None
    
    def get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """获取用户档案"""
        try:
            print(f"\n🔄 正在获取用户档案: {user_id}")
            response = self.session.get(f"{self.base_url}/api/user-profile/{user_id}")
            
            if response.status_code == 200:
                data = response.json()
                profile = data.get('data', {}).get('profile', {})
                print(f"✅ 获取用户档案成功!")
                print(f"👤 姓名: {profile.get('personal_info', {}).get('name', 'N/A')}")
                print(f"📧 邮箱: {profile.get('contact', {}).get('email', 'N/A')}")
                print(f"🏢 公司: {profile.get('work_experience', [{}])[0].get('company', 'N/A')}")
                return data.get('data')
            else:
                print(f"❌ 获取失败: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ 获取用户档案异常: {e}")
            return None
    
    def validate_user_profile(self, user_id: str, profile_data: Dict[str, Any], 
                            format_type: str = "detailed") -> Optional[Dict[str, Any]]:
        """验证用户档案"""
        try:
            print(f"\n🔄 正在验证用户档案: {user_id}")
            
            # 构建查询参数
            params = {
                'include_skills': 'true',
                'include_education': 'true', 
                'include_work': 'true',
                'format': format_type
            }
            
            response = self.session.post(
                f"{self.base_url}/api/user-profile/{user_id}/validate",
                json=profile_data,
                params=params
            )
            
            if response.status_code == 200:
                data = response.json()
                score = data.get('score', 0)
                print(f"✅ 档案验证成功!")
                print(f"📊 完整度评分: {score}%")
                
                if format_type == "detailed":
                    report = data.get('validation_report', {})
                    print(f"📋 验证报告:")
                    print(f"   - 基本信息完整: {'✅' if report.get('basic_info_complete') else '❌'}")
                    print(f"   - 联系信息完整: {'✅' if report.get('contact_info_complete') else '❌'}")
                    print(f"   - 地址信息完整: {'✅' if report.get('address_info_complete') else '❌'}")
                    print(f"   - 技能数量: {report.get('skills_count', 0)}")
                    print(f"   - 教育背景数量: {report.get('education_count', 0)}")
                    print(f"   - 工作经历数量: {report.get('work_experience_count', 0)}")
                    
                    recommendations = report.get('recommendations', [])
                    if recommendations:
                        print(f"💡 建议:")
                        for rec in recommendations:
                            print(f"   - {rec}")
                
                return data
            else:
                print(f"❌ 验证失败: {response.status_code}")
                print(f"错误信息: {response.json()}")
                return None
                
        except Exception as e:
            print(f"❌ 验证用户档案异常: {e}")
            return None
    
    def test_error_scenarios(self):
        """测试错误场景"""
        print("\n🧪 开始测试错误场景...")
        
        # 测试无效数据
        print("\n1️⃣ 测试无效邮箱格式:")
        invalid_data = {
            "personal_info": {"name": "测试用户", "age": 25, "gender": "男"},
            "contact": {"email": "invalid-email", "phone": "13812345678"},
            "address": {"street": "测试街道", "city": "测试城市", "state": "测试省", "postal_code": "123456"},
            "skills": [{"name": "测试技能", "level": 5, "years_experience": 2.0, "certifications": []}],
            "education": [{"school": "测试大学", "degree": "本科", "major": "测试专业", "graduation_date": "2020-06-01"}],
            "work_experience": [],
            "preferences": {}
        }
        
        response = self.session.post(
            f"{self.base_url}/api/user-profile",
            json=invalid_data
        )
        
        if response.status_code == 400:
            print("✅ 正确捕获了无效邮箱错误")
        else:
            print(f"❌ 预期400错误，实际得到: {response.status_code}")
        
        # 测试缺少必填字段
        print("\n2️⃣ 测试缺少必填字段:")
        incomplete_data = {
            "personal_info": {"name": "测试用户"},
            "contact": {"email": "test@example.com"}
        }
        
        response = self.session.post(
            f"{self.base_url}/api/user-profile",
            json=incomplete_data
        )
        
        if response.status_code == 400:
            print("✅ 正确捕获了缺少必填字段错误")
        else:
            print(f"❌ 预期400错误，实际得到: {response.status_code}")

def create_sample_profile_data() -> Dict[str, Any]:
    """创建示例用户档案数据"""
    return {
        "personal_info": {
            "name": "李洪森",
            "age": 23,
            "gender": "男",
            "avatar": "https://example.com/avatar.jpg"
        },
        "contact": {
            "email": "lihongshen@163.com",
            "phone": "13812345678",
            "wechat": "lihongshen_wx",
            "qq": "123456789"
        },
        "address": {
            "street": "杭州市余杭区文一西路",
            "city": "杭州",
            "state": "浙江省",
            "postal_code": "310000",
            "country": "中国"
        },
        "skills": [
            {
                "name": "RAG",
                "level": 5,
                "years_experience": 2.0,
                "certifications": ["计算机四级", "系统分析师"]
            },
            {
                "name": "Python",
                "level": 7,
                "years_experience": 3.0,
                "certifications": ["Python认证"]
            },
            {
                "name": "机器学习",
                "level": 6,
                "years_experience": 2.5,
                "certifications": ["机器学习工程师认证"]
            }
        ],
        "education": [
            {
                "school": "河南大学",
                "degree": "本科",
                "major": "人工智能",
                "graduation_date": "2020-06-01",
                "gpa": 3.6
            }
        ],
        "work_experience": [
            {
                "company": "杭州鼎智",
                "position": "AI算法工程师",
                "start_date": "2020-07-01",
                "end_date": None,
                "description": "负责RAG系统的开发和优化，参与多个AI项目的算法设计和实现，包括自然语言处理和知识图谱构建",
                "achievements": [
                    "成功优化RAG系统检索准确率提升30%",
                    "参与开发智能问答系统，用户满意度达95%",
                    "获得公司年度技术创新奖"
                ]
            }
        ],
        "preferences": {
            "work_location": "杭州",
            "salary_expectation": 25000,
            "work_type": "全职",
            "industry_preference": "人工智能",
            "company_size": "中型企业"
        }
    }

def main():
    """主测试流程"""
    print("🚀 前端API测试开始")
    print("=" * 60)
    print(f"⏰ 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 创建API客户端
    client = FrontendAPIClient()
    
    # # 1. 检查服务器健康状态
    # print("\n📡 步骤1: 检查服务器健康状态")
    # if not client.check_server_health():
    #     print("❌ 服务器不可用，测试终止")
    #     return
    
    # 2. 创建用户档案
    print("\n👤 步骤2: 创建用户档案")
    profile_data = create_sample_profile_data()
    user_id = client.create_user_profile(profile_data)
    
    if not user_id:
        print("❌ 用户档案创建失败，测试终止")
        return
    
    
    # 3. 获取用户档案
    print("\n📋 步骤3: 获取用户档案")
    profile_info = client.get_user_profile(user_id)
    
    # 4. 验证用户档案 - 详细格式
    print("\n🔍 步骤4: 验证用户档案（详细格式）")
    validation_result = client.validate_user_profile(user_id, profile_data, "detailed")
    print(validation_result)
    # # 5. 验证用户档案 - 简单格式
    # print("\n🔍 步骤5: 验证用户档案（简单格式）")
    # simple_validation = client.validate_user_profile(user_id, profile_data, "simple")
    
    # # 6. 测试错误场景
    # print("\n🧪 步骤6: 测试错误场景")
    # client.test_error_scenarios()
    
    # # 测试完成
    # print("\n" + "=" * 60)
    # print("🎉 前端API测试完成!")
    # print("=" * 60)
    
    # # 输出测试总结
    # print("\n📊 测试总结:")
    # print(f"✅ 服务器健康检查: 通过")
    # print(f"✅ 用户档案创建: {'通过' if user_id else '失败'}")
    # print(f"✅ 用户档案获取: {'通过' if profile_info else '失败'}")
    # print(f"✅ 档案验证(详细): {'通过' if validation_result else '失败'}")
    # print(f"✅ 档案验证(简单): {'通过' if simple_validation else '失败'}")
    # print(f"✅ 错误场景测试: 通过")

if __name__ == "__main__":
    main()