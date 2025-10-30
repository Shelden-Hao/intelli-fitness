#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FPS知识图谱可视化脚本
生成知识图谱的统计图表和网络图
"""

import json
import sys
from pathlib import Path
from collections import defaultdict, Counter
from loguru import logger

# 配置日志
logger.remove()
logger.add(sys.stderr, level="INFO")


def load_knowledge_graph(kg_file: str) -> dict:
    """加载知识图谱"""
    with open(kg_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def generate_statistics_report(kg_data: dict):
    """生成统计报告"""
    logger.info("=" * 80)
    logger.info("河北省全民健身公共服务知识图谱 - 统计报告")
    logger.info("=" * 80)
    
    metadata = kg_data['metadata']
    entities = kg_data['entities']
    relations = kg_data['relations']
    stats = kg_data['statistics']
    
    # 基本信息
    logger.info(f"\n📊 基本信息")
    logger.info(f"  名称: {metadata['name']}")
    logger.info(f"  创建时间: {metadata['created_at']}")
    logger.info(f"  数据来源: fitness_facilities_data.json")
    
    # 维度信息
    logger.info(f"\n🎯 知识维度 ({len(metadata['dimensions'])}个)")
    for i, dim in enumerate(metadata['dimensions'], 1):
        logger.info(f"  {i}. {dim}")
    
    # 实体统计
    logger.info(f"\n📦 实体统计")
    logger.info(f"  总实体数: {stats['total_entities']}")
    for entity_type, count in stats['entities'].items():
        percentage = (count / stats['total_entities'] * 100) if stats['total_entities'] > 0 else 0
        bar = "█" * int(percentage / 5)
        logger.info(f"  {entity_type:12s}: {count:4d} ({percentage:5.1f}%) {bar}")
    
    # 关系统计
    logger.info(f"\n🔗 关系统计")
    logger.info(f"  总关系数: {stats['total_relations']}")
    logger.info(f"  关系类型数: {stats['relation_types']}")
    
    # 统计各类关系数量
    relation_types = Counter(r['predicate'] for r in relations)
    logger.info(f"\n  关系类型分布:")
    for rel_type, count in relation_types.most_common():
        percentage = (count / stats['total_relations'] * 100) if stats['total_relations'] > 0 else 0
        bar = "█" * int(percentage / 5)
        logger.info(f"    {rel_type:12s}: {count:4d} ({percentage:5.1f}%) {bar}")


def analyze_facilities(kg_data: dict):
    """分析设施数据"""
    logger.info("\n" + "=" * 80)
    logger.info("设施维度分析")
    logger.info("=" * 80)
    
    facilities = kg_data['entities']['Facility']
    
    # 按类型统计
    type_count = Counter(f.get('type', '未知') for f in facilities.values())
    logger.info(f"\n设施类型分布 (共{len(facilities)}个):")
    for ftype, count in type_count.most_common():
        percentage = (count / len(facilities) * 100)
        logger.info(f"  {ftype:12s}: {count:3d} ({percentage:5.1f}%)")
    
    # 面积统计
    total_area = sum(f.get('site_area', 0) for f in facilities.values())
    avg_area = total_area / len(facilities) if facilities else 0
    logger.info(f"\n场地面积统计:")
    logger.info(f"  总面积: {total_area:,.0f} 平方米")
    logger.info(f"  平均面积: {avg_area:,.0f} 平方米/个")
    
    # 客流统计
    total_visitors = sum(f.get('daily_visitors', 0) for f in facilities.values())
    avg_visitors = total_visitors / len(facilities) if facilities else 0
    logger.info(f"\n客流统计:")
    logger.info(f"  总日客流: {total_visitors:,} 人次")
    logger.info(f"  平均日客流: {avg_visitors:,.0f} 人次/个")


def analyze_areas(kg_data: dict):
    """分析区域数据"""
    logger.info("\n" + "=" * 80)
    logger.info("区域维度分析")
    logger.info("=" * 80)
    
    areas = kg_data['entities']['Area']
    relations = kg_data['relations']
    
    # 统计各城市的设施数量
    city_facilities = defaultdict(int)
    for rel in relations:
        if rel['predicate'] == '位于':
            # 获取城市名称
            area_id = rel['object']
            if area_id in areas:
                area = areas[area_id]
                if area.get('level') == '市级':
                    city_facilities[area['name']] += 1
    
    logger.info(f"\n各城市设施数量排名:")
    for i, (city, count) in enumerate(sorted(city_facilities.items(), key=lambda x: x[1], reverse=True), 1):
        bar = "█" * (count // 2)
        logger.info(f"  {i:2d}. {city:12s}: {count:3d} 个 {bar}")


def analyze_time_dimension(kg_data: dict):
    """分析时间维度"""
    logger.info("\n" + "=" * 80)
    logger.info("时间维度分析")
    logger.info("=" * 80)
    
    facilities = kg_data['entities']['Facility']
    
    # 按年代统计
    decade_count = defaultdict(int)
    for f in facilities.values():
        year = f.get('build_year', 0)
        if year > 0:
            decade = (year // 10) * 10
            decade_count[decade] += 1
    
    logger.info(f"\n各年代设施建设数量:")
    for decade in sorted(decade_count.keys()):
        count = decade_count[decade]
        bar = "█" * (count // 3)
        logger.info(f"  {decade}年代: {count:3d} 个 {bar}")
    
    # 最新设施
    recent_facilities = sorted(
        [(f.get('name', ''), f.get('build_year', 0)) for f in facilities.values()],
        key=lambda x: x[1],
        reverse=True
    )[:5]
    
    logger.info(f"\n最新建成的设施:")
    for name, year in recent_facilities:
        if year > 0:
            logger.info(f"  {year}年: {name}")


def analyze_indicators(kg_data: dict):
    """分析指标维度"""
    logger.info("\n" + "=" * 80)
    logger.info("指标维度分析")
    logger.info("=" * 80)
    
    indicators = kg_data['entities']['Indicator']
    
    # 人均场地面积指标
    per_capita_indicators = [
        ind for ind in indicators.values()
        if ind.get('indicator_type') == '人均体育场地面积'
    ]
    
    if per_capita_indicators:
        logger.info(f"\n人均体育场地面积指标 (假设人口100万):")
        sorted_indicators = sorted(per_capita_indicators, key=lambda x: x.get('value', 0), reverse=True)
        for ind in sorted_indicators:
            city = ind.get('area', '未知')
            value = ind.get('value', 0)
            bar = "█" * int(value * 50)
            logger.info(f"  {city:12s}: {value:.2f} 平方米/人 {bar}")


def generate_network_structure(kg_data: dict):
    """生成网络结构描述"""
    logger.info("\n" + "=" * 80)
    logger.info("知识图谱网络结构")
    logger.info("=" * 80)
    
    stats = kg_data['statistics']
    relations = kg_data['relations']
    
    # 计算网络密度
    total_entities = stats['total_entities']
    total_relations = stats['total_relations']
    
    # 最大可能关系数 = n * (n-1) / 2
    max_relations = total_entities * (total_entities - 1) / 2
    density = (total_relations / max_relations * 100) if max_relations > 0 else 0
    
    logger.info(f"\n网络特征:")
    logger.info(f"  节点数: {total_entities}")
    logger.info(f"  边数: {total_relations}")
    logger.info(f"  网络密度: {density:.4f}%")
    logger.info(f"  平均度: {total_relations * 2 / total_entities:.2f}")
    
    # 统计出度和入度
    out_degree = defaultdict(int)
    in_degree = defaultdict(int)
    
    for rel in relations:
        out_degree[rel['subject']] += 1
        in_degree[rel['object']] += 1
    
    # 找出度最高的节点
    if out_degree:
        max_out = max(out_degree.items(), key=lambda x: x[1])
        logger.info(f"  最大出度: {max_out[1]} ({max_out[0]})")
    
    if in_degree:
        max_in = max(in_degree.items(), key=lambda x: x[1])
        logger.info(f"  最大入度: {max_in[1]} ({max_in[0]})")


def export_summary(kg_data: dict, output_file: str):
    """导出摘要信息"""
    summary = {
        'name': kg_data['metadata']['name'],
        'created_at': kg_data['metadata']['created_at'],
        'dimensions': kg_data['metadata']['dimensions'],
        'statistics': kg_data['statistics'],
        'top_cities': [],
        'facility_types': {},
        'time_periods': {}
    }
    
    # 城市排名
    areas = kg_data['entities']['Area']
    relations = kg_data['relations']
    
    city_facilities = defaultdict(int)
    for rel in relations:
        if rel['predicate'] == '位于':
            area_id = rel['object']
            if area_id in areas:
                area = areas[area_id]
                if area.get('level') == '市级':
                    city_facilities[area['name']] += 1
    
    summary['top_cities'] = [
        {'city': city, 'count': count}
        for city, count in sorted(city_facilities.items(), key=lambda x: x[1], reverse=True)[:10]
    ]
    
    # 设施类型
    facilities = kg_data['entities']['Facility']
    type_count = Counter(f.get('type', '未知') for f in facilities.values())
    summary['facility_types'] = dict(type_count)
    
    # 保存
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    logger.info(f"\n✅ 摘要已导出到: {output_file}")


def main():
    """主函数"""
    logger.info("=" * 80)
    logger.info("FPS知识图谱可视化分析")
    logger.info("=" * 80)
    
    # 加载知识图谱
    kg_data = load_knowledge_graph('fps_knowledge_graph.json')
    
    # 生成各类分析
    generate_statistics_report(kg_data)
    analyze_facilities(kg_data)
    analyze_areas(kg_data)
    analyze_time_dimension(kg_data)
    analyze_indicators(kg_data)
    generate_network_structure(kg_data)
    
    # 导出摘要
    export_summary(kg_data, 'fps_kg_summary.json')
    
    logger.info("\n" + "=" * 80)
    logger.info("🎉 分析完成!")
    logger.info("=" * 80)
    logger.info("\n输出文件:")
    logger.info("  - fps_kg_summary.json (摘要信息)")
    logger.info("\n可视化建议:")
    logger.info("  - 使用Protege打开 fps_ontology.owl 查看本体结构")
    logger.info("  - 使用Neo4j导入数据进行图可视化")
    logger.info("  - 使用Gephi进行网络分析")


if __name__ == "__main__":
    main()
