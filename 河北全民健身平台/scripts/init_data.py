"""
数据初始化脚本 - 生成真实模拟数据
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_processing.crawler.sports_crawler import FitnessDataCollector
from data_processing.preprocessor.data_cleaner import FitnessDataPreprocessor
from loguru import logger
import json


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
        logger.info(f"创建目录: {directory}")


def initialize_data():
    """初始化数据"""
    logger.info("=" * 60)
    logger.info("开始初始化数据...")
    logger.info("=" * 60)
    
    # 创建目录
    create_directories()
    
    # 采集数据
    collector = FitnessDataCollector()
    
    logger.info("\n📊 采集健身设施数据...")
    facilities = collector.collect_facility_data()
    collector.save_data(facilities, "facilities")
    
    logger.info("\n👥 采集人口数据...")
    population = collector.collect_population_data()
    collector.save_data(population, "population")
    
    logger.info("\n🏃 采集参与数据...")
    participation = collector.collect_participation_data()
    collector.save_data(participation, "participation")
    
    logger.info("\n📜 采集政策数据...")
    policies = collector.collect_policy_data()
    collector.save_data(policies, "policies")
    
    # 数据预处理
    logger.info("\n" + "=" * 60)
    logger.info("开始数据预处理...")
    logger.info("=" * 60)
    
    preprocessor = FitnessDataPreprocessor()
    
    logger.info("\n🔧 预处理设施数据...")
    preprocessor.preprocess_facility_data(
        "data/raw/facilities.json",
        "data/processed/facilities_cleaned.json"
    )
    
    logger.info("\n🔧 预处理人口数据...")
    preprocessor.preprocess_population_data(
        "data/raw/population.json",
        "data/processed/population_cleaned.json"
    )
    
    logger.info("\n🔧 预处理参与数据...")
    preprocessor.preprocess_participation_data(
        "data/raw/participation.json",
        "data/processed/participation_cleaned.json"
    )
    
    # 生成统计报告
    logger.info("\n" + "=" * 60)
    logger.info("生成统计报告...")
    logger.info("=" * 60)
    
    report = {
        "data_summary": {
            "facilities_count": len(facilities),
            "cities_count": len(population),
            "policies_count": len(policies)
        },
        "data_sources": [
            "国家统计局",
            "河北省统计局",
            "国家体育总局",
            "河北省体育局"
        ],
        "status": "completed",
        "timestamp": "2024-01-01T00:00:00"
    }
    
    with open('data/processed/data_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    logger.info("\n✅ 数据初始化完成!")
    logger.info(f"   - 健身设施: {len(facilities)} 条")
    logger.info(f"   - 城市数据: {len(population)} 条")
    logger.info(f"   - 参与数据: {len(participation)} 条")
    logger.info(f"   - 政策文件: {len(policies)} 条")
    logger.info("\n" + "=" * 60)


if __name__ == "__main__":
    initialize_data()
