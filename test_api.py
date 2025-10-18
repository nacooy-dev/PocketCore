"""
测试PocketCore API功能
"""
import requests
import json

def test_api():
    """测试API功能"""
    base_url = "http://localhost:8000"
    
    print("测试PocketCore API功能...")
    
    # 测试根路径
    print("\n1. 测试根路径:")
    try:
        response = requests.get(f"{base_url}/")
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
    except Exception as e:
        print(f"错误: {e}")
    
    # 测试工具列表
    print("\n2. 测试工具列表:")
    try:
        response = requests.get(f"{base_url}/tools")
        print(f"状态码: {response.status_code}")
        tools = response.json()
        print("可用工具:")
        for tool in tools.get("tools", []):
            print(f"  - {tool['name']}: {tool['description']}")
    except Exception as e:
        print(f"错误: {e}")
    
    # 测试模型列表
    print("\n3. 测试模型列表:")
    try:
        response = requests.get(f"{base_url}/models")
        print(f"状态码: {response.status_code}")
        models = response.json()
        print("可用模型:")
        for model_info in models.get("models", []):
            print(f"  {model_info['provider'].upper()}:")
            for model in model_info['models']:
                print(f"    - {model}")
    except Exception as e:
        print(f"错误: {e}")
    
    # 测试查询功能
    print("\n4. 测试查询功能:")
    try:
        query_data = {
            "query": "你好，这是API测试"
        }
        response = requests.post(
            f"{base_url}/query",
            headers={"Content-Type": "application/json"},
            data=json.dumps(query_data)
        )
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"查询结果: {result.get('result', '无结果')}")
        else:
            print(f"错误响应: {response.text}")
    except Exception as e:
        print(f"错误: {e}")
    
    # 测试内存功能
    print("\n5. 测试内存功能:")
    try:
        response = requests.get(f"{base_url}/memory?limit=3")
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            memory = response.json()
            interactions = memory.get("interactions", [])
            if interactions:
                print("最近的交互:")
                for interaction in interactions:
                    print(f"  Q: {interaction.get('query', 'N/A')}")
                    print(f"  A: {interaction.get('response', 'N/A')}")
                    print(f"  时间: {interaction.get('timestamp', 'N/A')}")
            else:
                print("暂无交互历史")
        else:
            print(f"错误响应: {response.text}")
    except Exception as e:
        print(f"错误: {e}")
    
    print("\nAPI功能测试完成")

if __name__ == "__main__":
    test_api()