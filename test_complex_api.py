#!/usr/bin/env python3
"""
测试复杂API接口的脚本
"""

import requests
import json
from datetime import datetime

# 服务器地址
BASE_URL = "http://localhost:5000"

def test_health_check():
    """测试健康检查接口"""
    print("=== 测试健康检查接口 ===")
    response = requests.get(f"{BASE_URL}/")
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()

def test_create_user_profile():
    """测试创建用户档案接口"""
    print("=== 测试创建用户档案接口 ===")
    
    # 读取示例数据
    with open('sample_user_profile.json', 'r', encoding='utf-8') as f:
        profile_data = json.load(f)
    
    response = requests.post(
        f"{BASE_URL}/api/user-profile",
        json=profile_data,
        headers={'Content-Type': 'application/json'}
    )
    
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()
    
    return response.json().get('data', {}).get('user_id') if response.status_code == 201 else None

def test_get_user_profile(user_id):
    """测试获取用户档案接口"""
    if not user_id:
        print("=== 跳过获取用户档案测试（没有有效的user_id）===")
        return
    
    print("=== 测试获取用户档案接口 ===")
    response = requests.get(f"{BASE_URL}/api/user-profile/{user_id}")
    
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()

def test_validate_user_profile():
    """测试验证用户档案接口"""
    print("=== 测试验证用户档案接口 ===")
    
    # 读取示例数据
    with open('sample_user_profile.json', 'r', encoding='utf-8') as f:
        profile_data = json.load(f)
    
    response = requests.post(
        f"{BASE_URL}/api/user-profile/test_user/validate",
        json=profile_data,
        headers={'Content-Type': 'application/json'}
    )
    
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()

def test_invalid_data():
    """测试无效数据"""
    print("=== 测试无效数据 ===")
    
    # 测试缺少必填字段
    invalid_data = {
        "personal_info": {
            "name": "测试用户",
            "age": 25
            # 缺少gender字段
        },
        "contact": {
            "email": "invalid-email",  # 无效邮箱
            "phone": "123"  # 无效手机号
        }
    }
    
    response = requests.post(
        f"{BASE_URL}/api/user-profile",
        json=invalid_data,
        headers={'Content-Type': 'application/json'}
    )
    
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()

def main():
    """主测试函数"""
    print("开始测试复杂API接口...")
    print(f"测试时间: {datetime.now()}")
    print("=" * 50)
    
    try:
        # 测试健康检查
        test_health_check()
        
        # 测试创建用户档案
        user_id = test_create_user_profile()
        
        # 测试获取用户档案
        test_get_user_profile(user_id)
        
        # 测试验证用户档案
        test_validate_user_profile()
        
        # 测试无效数据
        test_invalid_data()
        
        print("=" * 50)
        print("所有测试完成！")
        
    except requests.exceptions.ConnectionError:
        print("错误: 无法连接到服务器，请确保Flask应用正在运行")
        print("运行命令: python app/main.py")
    except Exception as e:
        print(f"测试过程中出现错误: {e}")

if __name__ == "__main__":
    main()
