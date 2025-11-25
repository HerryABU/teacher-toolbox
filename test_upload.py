import requests

# 测试Excel上传功能
BASE_URL = "http://localhost:5000"

def test_excel_upload():
    print("🧪 测试Excel上传功能...")
    
    # 测试上传Excel文件
    print("\n1. 测试上传Excel文件...")
    try:
        with open('test_class.xlsx', 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{BASE_URL}/api/upload/class", files=files)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 上传成功: {result['message']}")
            print(f"📊 数据统计:")
            print(f"   - 总行数: {result['data']['total_rows']}")
            print(f"   - 列数: {len(result['data']['columns'])}")
            print(f"   - 文件名: {result['data']['file_name']}")
            print(f"   - 列名: {result['data']['columns']}")
        else:
            print(f"❌ 上传失败: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"❌ 请求失败: {e}")

if __name__ == "__main__":
    test_excel_upload()