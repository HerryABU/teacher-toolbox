import requests
import json

# 测试API端点
BASE_URL = "http://localhost:5000"

def test_api_endpoints():
    print("🧪 测试API端点...")
    
    # 测试获取工具配置
    print("\n1. 测试获取工具配置...")
    try:
        response = requests.get(f"{BASE_URL}/api/config/tools")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 获取工具配置成功，共{len(data.get('categories', []))}个分类")
        else:
            print(f"❌ 获取工具配置失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 请求失败: {e}")
    
    # 测试添加分类
    print("\n2. 测试添加分类...")
    try:
        category_data = {
            "operation": "category",
            "category_id": "test_category",
            "category_name": "测试分类",
            "category_icon": "DocumentAdd"
        }
        response = requests.post(f"{BASE_URL}/api/tools", json=category_data)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 添加分类成功: {result['message']}")
        else:
            print(f"❌ 添加分类失败: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"❌ 请求失败: {e}")
    
    # 测试添加工具
    print("\n3. 测试添加工具...")
    try:
        tool_data = {
            "operation": "tool",
            "category_id": "test_category",
            "tool_id": "test_tool",
            "tool_name": "测试工具",
            "tool_description": "这是一个测试工具",
            "tool_icon": "Aim"
        }
        response = requests.post(f"{BASE_URL}/api/tools", json=tool_data)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 添加工具成功: {result['message']}")
        else:
            print(f"❌ 添加工具失败: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"❌ 请求失败: {e}")
    
    # 测试删除工具
    print("\n4. 测试删除工具...")
    try:
        response = requests.delete(f"{BASE_URL}/api/tools/test_category/test_tool")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 删除工具成功: {result['message']}")
        else:
            print(f"❌ 删除工具失败: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"❌ 请求失败: {e}")
    
    # 测试删除分类
    print("\n5. 测试删除分类...")
    try:
        response = requests.delete(f"{BASE_URL}/api/categories/test_category")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 删除分类成功: {result['message']}")
        else:
            print(f"❌ 删除分类失败: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"❌ 请求失败: {e}")
    
    print("\n🧪 API测试完成！")

if __name__ == "__main__":
    test_api_endpoints()