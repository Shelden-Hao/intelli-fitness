#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FPS知识图谱查询演示脚本
展示知识图谱的查询和推理功能
"""

import json
import sys
from pathlib import Path
from typing import List, Dict, Set
from loguru import logger
from collections import defaultdict

# 配置日志
logger.remove()
logger.add(sys.stderr, level="INFO", format="<green>{time:HH:mm:ss}</green> | <level>{message}</level>")


class KnowledgeGraphQuery:
    """知识图谱查询器"""
    
    def __init__(self, kg_file: str):
        """加载知识图谱"""
        with open(kg_file, 'r', encoding='utf-8') as f:
            self.kg_data = json.load(f)
        
        self.entities = self.kg_data['entities']
        self.relations = self.kg_data['relations']
        
        # 构建索引
        self._build_indexes()
        
        logger.info(f"✅ 加载知识图谱: {self.kg_data['metadata']['name']}")
        logger.info(f"   实体数: {self.kg_data['statistics']['total_entities']}")
        logger.info(f"   关系数: {self.kg_data['statistics']['total_relations']}")
    
    def _build_indexes(self):
        """构建查询索引"""
        # 主语索引
        self.subject_index = defaultdict(list)
        # 宾语索引
        self.object_index = defaultdict(list)
        # 谓词索引
        self.predicate_index = defaultdict(list)
        
        for relation in self.relations:
            self.subject_index[relation['subject']].append(relation)
            self.object_index[relation['object']].append(relation)
            self.predicate_index[relation['predicate']].append(relation)
    
    def get_entity(self, entity_id: str) -> Dict:
        """获取实体信息"""
        for entity_type, entities in self.entities.items():
            if entity_id in entities:
                return {'type': entity_type, **entities[entity_id]}
        return None
    
    def find_entities_by_type(self, entity_type: str) -> List[Dict]:
        """按类型查找实体"""
        if entity_type not in self.entities:
            return []
        
        return [{'id': k, **v} for k, v in self.entities[entity_type].items()]
    
    def find_relations_by_subject(self, subject: str) -> List[Dict]:
        """查找主语为指定实体的关系"""
        return self.subject_index.get(subject, [])
    
    def find_relations_by_object(self, obj: str) -> List[Dict]:
        """查找宾语为指定实体的关系"""
        return self.object_index.get(obj, [])
    
    def find_relations_by_predicate(self, predicate: str) -> List[Dict]:
        """查找指定类型的关系"""
        return self.predicate_index.get(predicate, [])
    
    def query_city_facilities(self, city_name: str) -> List[Dict]:
        """查询城市的所有设施"""
        city_id = f"Area_{city_name}"
        
        # 查找所有位于该城市的设施
        relations = self.find_relations_by_object(city_id)
        facilities = []
        
        for rel in relations:
            if rel['predicate'] == '位于':
                facility_id = rel['subject']
                facility = self.get_entity(facility_id)
                if facility:
                    facilities.append({'id': facility_id, **facility})
        
        return facilities
    
    def query_facility_sports(self, facility_id: str) -> List[str]:
        """查询设施提供的运动项目"""
        relations = self.find_relations_by_subject(facility_id)
        sports = []
        
        for rel in relations:
            if rel['predicate'] == '提供':
                sport_id = rel['object']
                sport = self.get_entity(sport_id)
                if sport:
                    sports.append(sport.get('name', ''))
        
        return sports
    
    def query_facilities_by_year(self, year: int) -> List[Dict]:
        """查询指定年份建成的设施"""
        year_id = f"Year_{year}"
        
        relations = self.find_relations_by_object(year_id)
        facilities = []
        
        for rel in relations:
            if rel['predicate'] == '建成于':
                facility_id = rel['subject']
                facility = self.get_entity(facility_id)
                if facility:
                    facilities.append({'id': facility_id, **facility})
        
        return facilities
    
    def query_policy_beneficiaries(self, policy_id: str) -> List[Dict]:
        """查询受某政策影响的设施"""
        relations = self.find_relations_by_object(policy_id)
        facilities = []
        
        for rel in relations:
            if rel['predicate'] == '受益于':
                facility_id = rel['subject']
                facility = self.get_entity(facility_id)
                if facility:
                    facilities.append({'id': facility_id, **facility})
        
        return facilities
    
    def get_city_statistics(self, city_name: str) -> Dict:
        """获取城市统计信息"""
        facilities = self.query_city_facilities(city_name)
        
        if not facilities:
            return None
        
        stats = {
            'city': city_name,
            'total_facilities': len(facilities),
            'total_site_area': sum(f.get('site_area', 0) for f in facilities),
            'total_visitors': sum(f.get('daily_visitors', 0) for f in facilities),
            'facility_types': defaultdict(int),
            'avg_build_year': 0
        }
        
        # 统计设施类型
        for f in facilities:
            ftype = f.get('type', '未知')
            stats['facility_types'][ftype] += 1
        
        # 平均建成年份
        years = [f.get('build_year', 0) for f in facilities if f.get('build_year', 0) > 0]
        if years:
            stats['avg_build_year'] = int(sum(years) / len(years))
        
        return stats


def demo_basic_queries(kg: KnowledgeGraphQuery):
    """演示基本查询"""
    logger.info("\n" + "=" * 80)
    logger.info("演示1: 基本实体查询")
    logger.info("=" * 80)
    
    # 查询所有城市
    cities = kg.find_entities_by_type('Area')
    city_names = [c['name'] for c in cities if c.get('level') == '市级']
    logger.info(f"\n河北省城市列表 ({len(city_names)}个):")
    for city in sorted(city_names):
        logger.info(f"  - {city}")
    
    # 查询所有运动项目
    sports = kg.find_entities_by_type('Sport')
    logger.info(f"\n运动项目列表 ({len(sports)}个):")
    for sport in sports:
        logger.info(f"  - {sport['name']} ({sport.get('category', '未分类')})")
    
    # 查询所有政策
    policies = kg.find_entities_by_type('Law')
    logger.info(f"\n政策法规列表 ({len(policies)}个):")
    for policy in policies:
        logger.info(f"  - {policy['title']} ({policy.get('level', '')})")


def demo_city_queries(kg: KnowledgeGraphQuery):
    """演示城市相关查询"""
    logger.info("\n" + "=" * 80)
    logger.info("演示2: 城市设施查询")
    logger.info("=" * 80)
    
    # 查询石家庄市的设施
    city = "石家庄市"
    facilities = kg.query_city_facilities(city)
    
    logger.info(f"\n{city}的体育设施 (共{len(facilities)}个):")
    for i, f in enumerate(facilities[:5], 1):
        logger.info(f"  {i}. {f['name']}")
        logger.info(f"     类型: {f.get('type', '未知')}")
        logger.info(f"     场地面积: {f.get('site_area', 0):,.0f} 平方米")
        logger.info(f"     日客流: {f.get('daily_visitors', 0):,} 人次")
    
    if len(facilities) > 5:
        logger.info(f"  ... 还有 {len(facilities) - 5} 个设施")


def demo_statistics_queries(kg: KnowledgeGraphQuery):
    """演示统计查询"""
    logger.info("\n" + "=" * 80)
    logger.info("演示3: 城市统计分析")
    logger.info("=" * 80)
    
    # 获取主要城市的统计信息
    major_cities = ["石家庄市", "唐山市", "保定市", "邯郸市", "承德市"]
    
    city_stats_list = []
    for city in major_cities:
        stats = kg.get_city_statistics(city)
        if stats:
            city_stats_list.append(stats)
    
    # 按设施数量排序
    city_stats_list.sort(key=lambda x: x['total_facilities'], reverse=True)
    
    logger.info("\n主要城市体育设施统计:")
    logger.info(f"{'城市':<12} {'设施数':<8} {'总面积(万㎡)':<15} {'日客流(万人次)':<15} {'平均建成年份':<12}")
    logger.info("-" * 80)
    
    for stats in city_stats_list:
        logger.info(
            f"{stats['city']:<12} "
            f"{stats['total_facilities']:<8} "
            f"{stats['total_site_area']/10000:<15.2f} "
            f"{stats['total_visitors']/10000:<15.2f} "
            f"{stats['avg_build_year']:<12}"
        )


def demo_time_queries(kg: KnowledgeGraphQuery):
    """演示时间维度查询"""
    logger.info("\n" + "=" * 80)
    logger.info("演示4: 时间维度分析")
    logger.info("=" * 80)
    
    # 按年代统计设施建设
    decade_stats = defaultdict(int)
    
    all_facilities = kg.find_entities_by_type('Facility')
    for f in all_facilities:
        year = f.get('build_year', 0)
        if year > 0:
            decade = (year // 10) * 10
            decade_stats[decade] += 1
    
    logger.info("\n各年代设施建设数量:")
    for decade in sorted(decade_stats.keys()):
        count = decade_stats[decade]
        bar = "█" * (count // 5)
        logger.info(f"  {decade}年代: {count:3d} 个 {bar}")
    
    # 查询最近建成的设施
    recent_year = 2020
    recent_facilities = kg.query_facilities_by_year(recent_year)
    
    if recent_facilities:
        logger.info(f"\n{recent_year}年建成的设施 ({len(recent_facilities)}个):")
        for f in recent_facilities[:3]:
            logger.info(f"  - {f['name']} ({f.get('type', '未知')})")


def demo_policy_queries(kg: KnowledgeGraphQuery):
    """演示政策相关查询"""
    logger.info("\n" + "=" * 80)
    logger.info("演示5: 政策影响分析")
    logger.info("=" * 80)
    
    # 查询受补助政策影响的设施
    policy_id = "Law_体育场馆补助政策"
    beneficiaries = kg.query_policy_beneficiaries(policy_id)
    
    logger.info(f"\n受补助政策影响的设施 (共{len(beneficiaries)}个):")
    
    # 按城市统计
    city_count = defaultdict(int)
    for f in beneficiaries:
        # 查找设施所在城市
        relations = kg.find_relations_by_subject(f['id'])
        for rel in relations:
            if rel['predicate'] == '位于':
                city_entity = kg.get_entity(rel['object'])
                if city_entity:
                    city_count[city_entity.get('name', '未知')] += 1
    
    logger.info("\n按城市分布:")
    for city, count in sorted(city_count.items(), key=lambda x: x[1], reverse=True)[:10]:
        logger.info(f"  {city}: {count} 个")


def demo_complex_queries(kg: KnowledgeGraphQuery):
    """演示复杂查询"""
    logger.info("\n" + "=" * 80)
    logger.info("演示6: 复杂关联查询")
    logger.info("=" * 80)
    
    # 查询：石家庄市 + 2015年后建成 + 有室外健身器材
    city = "石家庄市"
    facilities = kg.query_city_facilities(city)
    
    filtered = [
        f for f in facilities
        if f.get('build_year', 0) >= 2015 and f.get('has_outdoor_fitness', False)
    ]
    
    logger.info(f"\n{city}2015年后建成且有室外健身器材的设施 ({len(filtered)}个):")
    for f in filtered[:5]:
        logger.info(f"  - {f['name']} (建于{f.get('build_year')}年)")
    
    # 计算人均场地面积
    logger.info("\n人均场地面积指标:")
    indicators = kg.find_entities_by_type('Indicator')
    per_capita_indicators = [
        ind for ind in indicators
        if ind.get('indicator_type') == '人均体育场地面积'
    ]
    
    for ind in sorted(per_capita_indicators, key=lambda x: x.get('value', 0), reverse=True)[:5]:
        logger.info(f"  {ind.get('area', '未知')}: {ind.get('value', 0):.2f} 平方米/人")


def main():
    """主函数"""
    logger.info("=" * 80)
    logger.info("FPS知识图谱查询演示")
    logger.info("=" * 80)
    
    # 加载知识图谱
    kg = KnowledgeGraphQuery('fps_knowledge_graph.json')
    
    # 运行演示
    demo_basic_queries(kg)
    demo_city_queries(kg)
    demo_statistics_queries(kg)
    demo_time_queries(kg)
    demo_policy_queries(kg)
    demo_complex_queries(kg)
    
    logger.info("\n" + "=" * 80)
    logger.info("🎉 演示完成!")
    logger.info("=" * 80)


if __name__ == "__main__":
    main()
