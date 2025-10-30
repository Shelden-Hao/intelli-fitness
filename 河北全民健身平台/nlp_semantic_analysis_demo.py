#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NLP语义分析演示脚本
展示如何使用自然语言处理技术将文本描述转换为量化指标
"""

import json
import sys
from pathlib import Path
from loguru import logger

# 添加模块路径
sys.path.insert(0, str(Path(__file__).parent))

from data_processing.nlp.text_analyzer import PolicyTextAnalyzer, FitnessTextProcessor

# 配置日志
log_file = "logs/semantic_analysis_demo.log"
logger.add(log_file, rotation="10 MB", level="DEBUG", encoding="utf-8")


def demo_text_to_indicators():
    """演示：文本描述转换为量化指标"""
    
    logger.info("=" * 80)
    logger.info("演示1: 文本描述转换为量化指标")
    logger.info("=" * 80)
    
    analyzer = PolicyTextAnalyzer()
    
    # 示例政策文本
    policy_texts = [
        "到2025年,经常参加体育锻炼人数比例达到38.5%",
        "人均体育场地面积达到2.6平方米",
        "县(市、区)、乡镇(街道)、行政村(社区)三级公共健身设施覆盖率达到100%",
        "新建体育场馆50座，投资金额5.2亿元"
    ]
    
    for text in policy_texts:
        logger.info(f"\n原始文本: {text}")
        indicators = analyzer.quantify_policy_indicators(text)
        logger.info(f"量化结果: {json.dumps(indicators, ensure_ascii=False, indent=2)}")


def demo_semantic_scoring():
    """演示：语义分析转评分"""
    
    logger.info("\n" + "=" * 80)
    logger.info("演示2: 语义分析转评分 (文本评价 -> 量化分数)")
    logger.info("=" * 80)
    
    analyzer = PolicyTextAnalyzer()
    
    # 不同评价的文本
    evaluation_texts = [
        ("体育设施分布非常均衡，覆盖率优秀，群众满意度很高", "accessibility"),
        ("设施分布较好，但部分地区仍需改善和加强", "balance"),
        ("设施严重不足，分布很不均衡，存在较大差距", "quality"),
        ("基本满足需求，整体尚可，有待进一步提升", "coverage")
    ]
    
    for text, indicator_type in evaluation_texts:
        logger.info(f"\n评价文本: {text}")
        logger.info(f"指标类型: {indicator_type}")
        score = analyzer.semantic_analysis_to_score(text, indicator_type)
        logger.info(f"量化分数: {score:.2f}/100")


def demo_facility_data_analysis():
    """演示：场馆数据的NLP分析"""
    
    logger.info("\n" + "=" * 80)
    logger.info("演示3: 场馆数据的NLP语义分析")
    logger.info("=" * 80)
    
    # 读取转换后的数据
    try:
        with open('fitness_facilities_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        facilities = data['facilities']
        logger.info(f"加载场馆数据: {len(facilities)} 个场馆")
        
        analyzer = PolicyTextAnalyzer()
        
        # 分析前5个场馆
        for i, facility in enumerate(facilities[:5], 1):
            logger.info(f"\n--- 场馆 {i}: {facility['name']} ---")
            
            # 构建描述文本
            desc_text = f"{facility['description']} {facility.get('remarks', '')}"
            
            # 提取关键词
            if desc_text.strip():
                keywords = analyzer.extract_keywords(desc_text, topK=5)
                logger.info(f"关键词: {[kw[0] for kw in keywords]}")
            
            # 提取数值指标
            indicators = analyzer.extract_numeric_indicators(desc_text)
            logger.info(f"提取的数值指标: {len(indicators)} 个")
            
            # 显示场馆量化指标
            logger.info(f"场地面积: {facility['indicators']['site_area']} 平方米")
            logger.info(f"日客流量: {facility['indicators']['daily_visitors']} 人次")
            logger.info(f"建成年份: {facility['build_year']}")
            
    except FileNotFoundError:
        logger.error("未找到 fitness_facilities_data.json 文件，请先运行 convert_dataset.py")


def demo_comprehensive_analysis():
    """演示：综合分析 - 基于场馆数据计算区域指标"""
    
    logger.info("\n" + "=" * 80)
    logger.info("演示4: 综合分析 - 区域体育设施指标量化")
    logger.info("=" * 80)
    
    try:
        with open('fitness_facilities_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        facilities = data['facilities']
        
        # 按城市统计
        city_stats = {}
        
        for facility in facilities:
            city = facility['location'].get('city', '未知')
            if not city:
                continue
            
            if city not in city_stats:
                city_stats[city] = {
                    'count': 0,
                    'total_area': 0,
                    'total_visitors': 0,
                    'facilities': []
                }
            
            city_stats[city]['count'] += 1
            city_stats[city]['total_area'] += facility['indicators'].get('site_area', 0)
            city_stats[city]['total_visitors'] += facility['indicators'].get('daily_visitors', 0)
            city_stats[city]['facilities'].append(facility['name'])
        
        # 输出统计结果
        logger.info("\n各城市体育设施量化指标:")
        for city, stats in sorted(city_stats.items(), key=lambda x: x[1]['count'], reverse=True)[:10]:
            logger.info(f"\n{city}:")
            logger.info(f"  场馆数量: {stats['count']} 个")
            logger.info(f"  总场地面积: {stats['total_area']:,.2f} 平方米")
            logger.info(f"  日均客流: {stats['total_visitors']:,} 人次")
            logger.info(f"  人均场地面积(假设人口100万): {stats['total_area']/1000000:.2f} 平方米/人")
            
            # 使用NLP语义分析评估
            analyzer = PolicyTextAnalyzer()
            
            # 根据数量和面积生成评价文本
            if stats['count'] >= 20:
                eval_text = "设施数量充分，分布优秀"
            elif stats['count'] >= 10:
                eval_text = "设施数量良好，分布较好"
            else:
                eval_text = "设施数量有待提升，需要加强"
            
            score = analyzer.semantic_analysis_to_score(eval_text, "facility_coverage")
            logger.info(f"  设施覆盖评分: {score:.2f}/100 (基于: {eval_text})")
        
    except FileNotFoundError:
        logger.error("未找到 fitness_facilities_data.json 文件")


def main():
    """主函数"""
    
    logger.info("🚀 开始NLP语义分析演示")
    logger.info("=" * 80)
    
    try:
        # 演示1: 文本转指标
        demo_text_to_indicators()
        
        # 演示2: 语义评分
        demo_semantic_scoring()
        
        # 演示3: 场馆数据分析
        demo_facility_data_analysis()
        
        # 演示4: 综合分析
        demo_comprehensive_analysis()
        
        logger.info("\n" + "=" * 80)
        logger.info("🎉 NLP语义分析演示完成!")
        logger.info(f"详细日志已保存到: {log_file}")
        logger.info("=" * 80)
        
    except Exception as e:
        logger.error(f"❌ 演示过程中出错: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())


if __name__ == "__main__":
    main()
