from ast import main
import requests
import json
import time
from datetime import datetime, date
from typing import Dict, Any, Optional


class ApiTest:
    def __init__(self,base_url: str = "http://localhost:5000"):
        self.session=requests.Session()
        self.base_url=base_url
        self.session.headers.update({"Content-Type":"application/json"})
    

    def create_sample_data(self) -> Dict[str, Any]:
        return {
    "personal_info":{"name":"李洪森","age":23,"gender":"男"},
    "contact":{"email":"email@163.com","phone":"13087000000"},
    "address":{"street":"杭州市余杭区","city":"杭州","state":"浙江省","postal_code":"123456","country":"中国"},
    "skills":[{"name":"RAG","level":5,"years_experience":2,"certifications":["计算集四级","系统分析师"]}],
    "education":[{"school":"河南大学","degree":"本科","major":"人工智能","graduation_date":"2020-06-01"}],
    "work_experience": [
        {
            "company": "杭州鼎智",
            "position": "AI算法工程师",
            "start_date": "2020-07-01",
            "end_date": "2022-08-31",
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
    def check_create_user_profile(self,profile_data: Dict[str, Any]) -> Optional[str]:
        response=self.session.post(f"{self.base_url}/api/user-profile",json=profile_data)
        if response.status_code==201:
            return response.json()

def main():
    api_test=ApiTest()
    sample=api_test.create_sample_data()
    response=api_test.check_create_user_profile(sample)
    print("测试完成,响应数据:",response)

if __name__=="__main__":
    main()
