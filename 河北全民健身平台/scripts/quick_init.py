"""
快速数据初始化脚本 - 无需额外依赖
"""
import os
import json
from datetime import datetime

def create_directories():
    """创建必要的目录"""
    directories = [
        'data/raw',
        'data/processed',
        'data/knowledge_graph',
        'data/models',
        'ml_models/saved_models',
        'uploads'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ 创建目录: {directory}")

def generate_facilities_data():
    """生成健身设施数据"""
    facilities = [
        {
            "id": 1,
            "name": "石家庄市体育馆",
            "type": "综合体育馆",
            "city": "石家庄市",
            "district": "长安区",
            "address": "中山东路318号",
            "area": 15000,
            "capacity": 8000,
            "facilities": ["篮球场", "羽毛球场", "游泳馆", "健身房"],
            "open_hours": "06:00-22:00",
            "latitude": 38.0428,
            "longitude": 114.5149,
            "build_year": 2010,
            "investment": 50000000,
            "annual_visitors": 500000
        },
        {
            "id": 2,
            "name": "保定市全民健身中心",
            "type": "健身中心",
            "city": "保定市",
            "district": "竞秀区",
            "address": "朝阳南大街",
            "area": 12000,
            "capacity": 5000,
            "facilities": ["健身房", "游泳池", "乒乓球馆", "瑜伽室"],
            "open_hours": "06:00-21:00",
            "latitude": 38.8738,
            "longitude": 115.4645,
            "build_year": 2015,
            "investment": 30000000,
            "annual_visitors": 300000
        },
        {
            "id": 3,
            "name": "唐山市体育公园",
            "type": "体育公园",
            "city": "唐山市",
            "district": "路南区",
            "address": "南新道",
            "area": 50000,
            "capacity": 10000,
            "facilities": ["足球场", "篮球场", "跑道", "健身器材区"],
            "open_hours": "全天开放",
            "latitude": 39.6304,
            "longitude": 118.1803,
            "build_year": 2018,
            "investment": 80000000,
            "annual_visitors": 800000
        }
    ]
    
    with open('data/raw/facilities.json', 'w', encoding='utf-8') as f:
        json.dump(facilities, f, ensure_ascii=False, indent=2)
    
    print(f"✓ 生成健身设施数据: {len(facilities)} 条")
    return facilities

def generate_population_data():
    """生成人口数据"""
    population_data = [
        {
            "city": "石家庄市",
            "total_population": 11000000,
            "urban_population": 6500000,
            "rural_population": 4500000,
            "age_0_14": 1800000,
            "age_15_64": 7500000,
            "age_65_plus": 1700000,
            "year": 2024
        },
        {
            "city": "保定市",
            "total_population": 9400000,
            "urban_population": 4200000,
            "rural_population": 5200000,
            "age_0_14": 1500000,
            "age_15_64": 6400000,
            "age_65_plus": 1500000,
            "year": 2024
        },
        {
            "city": "唐山市",
            "total_population": 7700000,
            "urban_population": 4500000,
            "rural_population": 3200000,
            "age_0_14": 1200000,
            "age_15_64": 5300000,
            "age_65_plus": 1200000,
            "year": 2024
        }
    ]
    
    with open('data/raw/population.json', 'w', encoding='utf-8') as f:
        json.dump(population_data, f, ensure_ascii=False, indent=2)
    
    print(f"✓ 生成人口数据: {len(population_data)} 条")
    return population_data

def generate_participation_data():
    """生成参与数据"""
    participation_data = [
        {
            "city": "石家庄市",
            "year": 2024,
            "regular_participants": 3500000,
            "participation_rate": 0.318,
            "weekly_frequency": 3.5,
            "avg_duration": 45,
            "popular_activities": ["跑步", "健走", "广场舞", "羽毛球", "游泳"]
        },
        {
            "city": "保定市",
            "year": 2024,
            "regular_participants": 2800000,
            "participation_rate": 0.298,
            "weekly_frequency": 3.2,
            "avg_duration": 42,
            "popular_activities": ["健走", "跑步", "太极拳", "篮球", "乒乓球"]
        },
        {
            "city": "唐山市",
            "year": 2024,
            "regular_participants": 2400000,
            "participation_rate": 0.312,
            "weekly_frequency": 3.4,
            "avg_duration": 43,
            "popular_activities": ["跑步", "健走", "羽毛球", "篮球", "游泳"]
        }
    ]
    
    with open('data/raw/participation.json', 'w', encoding='utf-8') as f:
        json.dump(participation_data, f, ensure_ascii=False, indent=2)
    
    print(f"✓ 生成参与数据: {len(participation_data)} 条")
    return participation_data

def generate_policy_data():
    """生成政策数据"""
    policies = [
        {
            "title": "河北省全民健身实施计划(2021-2025年)",
            "level": "省级",
            "department": "河北省人民政府",
            "publish_date": "2021-12-15",
            "effective_date": "2022-01-01",
            "key_points": [
                "到2025年,经常参加体育锻炼人数比例达到38.5%",
                "人均体育场地面积达到2.6平方米",
                "县(市、区)、乡镇(街道)、行政村(社区)三级公共健身设施和社区15分钟健身圈全覆盖"
            ],
            "url": "http://example.com/policy1"
        },
        {
            "title": "关于构建更高水平的全民健身公共服务体系的意见",
            "level": "国家级",
            "department": "中共中央办公厅、国务院办公厅",
            "publish_date": "2022-03-23",
            "effective_date": "2022-03-23",
            "key_points": [
                "推动全民健身公共服务城乡区域均衡发展",
                "提升全民健身公共服务智慧化水平",
                "完善全民健身激励机制"
            ],
            "url": "http://example.com/policy2"
        }
    ]
    
    with open('data/raw/policies.json', 'w', encoding='utf-8') as f:
        json.dump(policies, f, ensure_ascii=False, indent=2)
    
    print(f"✓ 生成政策数据: {len(policies)} 条")
    return policies

def generate_report():
    """生成数据报告"""
    report = {
        "data_summary": {
            "facilities_count": 3,
            "cities_count": 3,
            "policies_count": 2,
            "total_population": 28100000,
            "total_participants": 8700000,
            "avg_participation_rate": 0.309
        },
        "data_sources": [
            "国家统计局",
            "河北省统计局",
            "国家体育总局",
            "河北省体育局"
        ],
        "status": "completed",
        "timestamp": datetime.now().isoformat()
    }
    
    with open('data/processed/data_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"✓ 生成数据报告")
    return report

def main():
    print("=" * 60)
    print("河北全民健身平台 - 快速数据初始化")
    print("=" * 60)
    print()
    
    # 创建目录
    print("📁 创建目录结构...")
    create_directories()
    print()
    
    # 生成数据
    print("📊 生成示例数据...")
    facilities = generate_facilities_data()
    population = generate_population_data()
    participation = generate_participation_data()
    policies = generate_policy_data()
    print()
    
    # 生成报告
    print("📈 生成数据报告...")
    report = generate_report()
    print()
    
    # 总结
    print("=" * 60)
    print("✅ 数据初始化完成!")
    print("=" * 60)
    print(f"健身设施: {len(facilities)} 条")
    print(f"城市数据: {len(population)} 条")
    print(f"参与数据: {len(participation)} 条")
    print(f"政策文件: {len(policies)} 条")
    print()
    print("数据文件位置:")
    print("  - data/raw/facilities.json")
    print("  - data/raw/population.json")
    print("  - data/raw/participation.json")
    print("  - data/raw/policies.json")
    print("  - data/processed/data_report.json")
    print()
    print("=" * 60)

if __name__ == "__main__":
    main()
