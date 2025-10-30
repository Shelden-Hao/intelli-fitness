#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全民健身公共服务（FPS）知识图谱构建模块

基于LKDF框架，构建面向河北全民健身公共服务的知识图谱
包含七个维度：时间划分(T)、区域(A)、政策法规(L)、指标(I)、个人健身信息(P)、设施(F)、运动项目(S)

本体结构：
- 实体类型：时间、区域、政策、指标、个人、设施、运动项目
- 关系类型：位于、管理、提供、参与、符合、影响等
- 属性信息：各实体的详细属性
"""

import json
import sys
from pathlib import Path
from typing import List, Dict, Optional, Set, Tuple
from loguru import logger
from datetime import datetime
from collections import defaultdict

# 配置日志
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)
log_file = log_dir / "knowledge_graph.log"

logger.remove()
logger.add(sys.stderr, level="INFO", format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>")
logger.add(log_file, rotation="10 MB", retention="30 days", level="DEBUG", encoding="utf-8")


class FPSKnowledgeGraph:
    """全民健身公共服务知识图谱"""
    
    def __init__(self):
        """初始化知识图谱"""
        # 实体存储
        self.entities = {
            'Time': {},          # 时间实体
            'Area': {},          # 区域实体
            'Law': {},           # 政策法规实体
            'Indicator': {},     # 指标实体
            'Person': {},        # 个人健身信息实体
            'Facility': {},      # 设施实体
            'Sport': {}          # 运动项目实体
        }
        
        # 关系存储
        self.relations = []
        
        # 属性存储
        self.attributes = defaultdict(dict)
        
        logger.info("✅ 初始化FPS知识图谱")
    
    def add_entity(self, entity_type: str, entity_id: str, properties: Dict):
        """添加实体
        
        Args:
            entity_type: 实体类型 (Time/Area/Law/Indicator/Person/Facility/Sport)
            entity_id: 实体唯一标识
            properties: 实体属性
        """
        if entity_type not in self.entities:
            logger.warning(f"未知实体类型: {entity_type}")
            return
        
        self.entities[entity_type][entity_id] = properties
        self.attributes[entity_id] = properties
        logger.debug(f"添加实体: {entity_type} - {entity_id}")
    
    def add_relation(self, subject: str, predicate: str, object: str, properties: Optional[Dict] = None):
        """添加关系三元组
        
        Args:
            subject: 主语实体ID
            predicate: 谓词（关系类型）
            object: 宾语实体ID
            properties: 关系属性
        """
        relation = {
            'subject': subject,
            'predicate': predicate,
            'object': object,
            'properties': properties or {}
        }
        self.relations.append(relation)
        logger.debug(f"添加关系: {subject} --[{predicate}]--> {object}")
    
    def get_entity(self, entity_id: str) -> Optional[Dict]:
        """获取实体信息"""
        return self.attributes.get(entity_id)
    
    def get_relations_by_subject(self, subject: str) -> List[Dict]:
        """获取主语为指定实体的所有关系"""
        return [r for r in self.relations if r['subject'] == subject]
    
    def get_relations_by_predicate(self, predicate: str) -> List[Dict]:
        """获取指定类型的所有关系"""
        return [r for r in self.relations if r['predicate'] == predicate]
    
    def get_statistics(self) -> Dict:
        """获取知识图谱统计信息"""
        stats = {
            'entities': {k: len(v) for k, v in self.entities.items()},
            'total_entities': sum(len(v) for v in self.entities.values()),
            'total_relations': len(self.relations),
            'relation_types': len(set(r['predicate'] for r in self.relations))
        }
        return stats
    
    def export_to_json(self, output_file: str):
        """导出知识图谱为JSON格式"""
        kg_data = {
            'metadata': {
                'name': '河北省全民健身公共服务知识图谱',
                'description': '基于LKDF框架构建的FPS领域知识图谱',
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'dimensions': ['时间(T)', '区域(A)', '政策法规(L)', '指标(I)', '个人(P)', '设施(F)', '运动项目(S)']
            },
            'entities': self.entities,
            'relations': self.relations,
            'statistics': self.get_statistics()
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(kg_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"✅ 知识图谱已导出到: {output_file}")
    
    def export_to_owl(self, output_file: str):
        """导出为OWL本体格式（用于Protege）"""
        owl_content = self._generate_owl_content()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(owl_content)
        
        logger.info(f"✅ OWL本体已导出到: {output_file}")
    
    def _generate_owl_content(self) -> str:
        """生成OWL格式内容"""
        owl = ['<?xml version="1.0"?>']
        owl.append('<rdf:RDF xmlns="http://www.fps-hebei.org/ontology#"')
        owl.append('     xml:base="http://www.fps-hebei.org/ontology"')
        owl.append('     xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"')
        owl.append('     xmlns:owl="http://www.w3.org/2002/07/owl#"')
        owl.append('     xmlns:xml="http://www.w3.org/XML/1998/namespace"')
        owl.append('     xmlns:xsd="http://www.w3.org/2001/XMLSchema#"')
        owl.append('     xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#">')
        owl.append('')
        owl.append('    <owl:Ontology rdf:about="http://www.fps-hebei.org/ontology">')
        owl.append('        <rdfs:label>河北省全民健身公共服务知识图谱</rdfs:label>')
        owl.append('        <rdfs:comment>基于LKDF框架的FPS领域本体</rdfs:comment>')
        owl.append('    </owl:Ontology>')
        owl.append('')
        
        # 定义类
        owl.append('    <!-- 实体类定义 -->')
        for entity_type in self.entities.keys():
            owl.append(f'    <owl:Class rdf:about="#{entity_type}">')
            owl.append(f'        <rdfs:label>{entity_type}</rdfs:label>')
            owl.append('    </owl:Class>')
            owl.append('')
        
        # 定义属性
        owl.append('    <!-- 对象属性定义 -->')
        predicates = set(r['predicate'] for r in self.relations)
        for predicate in predicates:
            owl.append(f'    <owl:ObjectProperty rdf:about="#{predicate}">')
            owl.append(f'        <rdfs:label>{predicate}</rdfs:label>')
            owl.append('    </owl:ObjectProperty>')
            owl.append('')
        
        # 定义实例（示例部分）
        owl.append('    <!-- 实例定义（部分示例） -->')
        for entity_type, entities in self.entities.items():
            for entity_id, props in list(entities.items())[:5]:  # 只导出前5个示例
                safe_id = entity_id.replace(' ', '_').replace('/', '_')
                owl.append(f'    <{entity_type} rdf:about="#{safe_id}">')
                owl.append(f'        <rdfs:label>{entity_id}</rdfs:label>')
                for key, value in props.items():
                    if isinstance(value, (str, int, float)):
                        owl.append(f'        <{key}>{value}</{key}>')
                owl.append(f'    </{entity_type}>')
                owl.append('')
        
        owl.append('</rdf:RDF>')
        
        return '\n'.join(owl)


class FPSKnowledgeGraphBuilder:
    """FPS知识图谱构建器"""
    
    def __init__(self):
        """初始化构建器"""
        self.kg = FPSKnowledgeGraph()
        logger.info("✅ 初始化FPS知识图谱构建器")
    
    def build_from_facilities_data(self, data_file: str):
        """从场馆数据构建知识图谱
        
        Args:
            data_file: 场馆数据JSON文件路径
        """
        logger.info(f"开始从数据文件构建知识图谱: {data_file}")
        
        # 加载数据
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        facilities = data['facilities']
        logger.info(f"加载 {len(facilities)} 个场馆数据")
        
        # 1. 构建时间维度实体 (Time)
        self._build_time_entities(facilities)
        
        # 2. 构建区域维度实体 (Area)
        self._build_area_entities(facilities)
        
        # 3. 构建设施实体 (Facility)
        self._build_facility_entities(facilities)
        
        # 4. 构建运动项目实体 (Sport)
        self._build_sport_entities(facilities)
        
        # 5. 构建指标实体 (Indicator)
        self._build_indicator_entities(facilities)
        
        # 6. 构建政策法规实体 (Law) - 基于补助状态
        self._build_law_entities(facilities)
        
        # 7. 构建关系
        self._build_relations(facilities)
        
        # 统计信息
        stats = self.kg.get_statistics()
        logger.info("=" * 80)
        logger.info("知识图谱构建完成!")
        logger.info(f"总实体数: {stats['total_entities']}")
        logger.info(f"总关系数: {stats['total_relations']}")
        logger.info(f"实体分布: {stats['entities']}")
        logger.info("=" * 80)
        
        return self.kg
    
    def _build_time_entities(self, facilities: List[Dict]):
        """构建时间维度实体"""
        logger.info("构建时间维度实体...")
        
        # 提取所有年份
        years = set()
        for facility in facilities:
            if facility.get('build_year'):
                years.add(facility['build_year'])
        
        # 创建年份实体
        for year in sorted(years):
            entity_id = f"Year_{year}"
            properties = {
                'year': year,
                'type': '年份',
                'decade': f"{year//10*10}年代"
            }
            self.kg.add_entity('Time', entity_id, properties)
        
        # 创建时间段实体
        time_periods = [
            {'id': 'Period_1980s', 'name': '1980年代', 'start': 1980, 'end': 1989},
            {'id': 'Period_1990s', 'name': '1990年代', 'start': 1990, 'end': 1999},
            {'id': 'Period_2000s', 'name': '2000年代', 'start': 2000, 'end': 2009},
            {'id': 'Period_2010s', 'name': '2010年代', 'start': 2010, 'end': 2019},
            {'id': 'Period_2020s', 'name': '2020年代', 'start': 2020, 'end': 2029}
        ]
        
        for period in time_periods:
            self.kg.add_entity('Time', period['id'], period)
        
        logger.info(f"✅ 创建 {len(years)} 个年份实体和 {len(time_periods)} 个时间段实体")
    
    def _build_area_entities(self, facilities: List[Dict]):
        """构建区域维度实体"""
        logger.info("构建区域维度实体...")
        
        # 省级实体
        province_id = "Area_河北省"
        self.kg.add_entity('Area', province_id, {
            'name': '河北省',
            'level': '省级',
            'type': '行政区域'
        })
        
        # 市级实体
        cities = set()
        districts = set()
        
        for facility in facilities:
            location = facility.get('location', {})
            city = location.get('city')
            district = location.get('district')
            
            if city:
                cities.add(city)
            if district:
                districts.add(district)
        
        # 创建市级实体
        for city in cities:
            if city:
                city_id = f"Area_{city}"
                self.kg.add_entity('Area', city_id, {
                    'name': city,
                    'level': '市级',
                    'province': '河北省',
                    'type': '行政区域'
                })
                
                # 添加省市关系
                self.kg.add_relation(city_id, '属于', province_id)
        
        # 创建区县级实体
        for district in districts:
            if district and district not in cities:
                district_id = f"Area_{district}"
                self.kg.add_entity('Area', district_id, {
                    'name': district,
                    'level': '区县级',
                    'type': '行政区域'
                })
        
        logger.info(f"✅ 创建 1 个省级、{len(cities)} 个市级、{len(districts)} 个区县级实体")
    
    def _build_facility_entities(self, facilities: List[Dict]):
        """构建设施实体"""
        logger.info("构建设施实体...")
        
        for facility in facilities:
            facility_id = f"Facility_{facility['id']}"
            
            properties = {
                'name': facility.get('name', ''),
                'type': facility.get('facility_type', ''),
                'operator': facility.get('operator', ''),
                'build_year': facility.get('build_year', 0),
                'address': facility.get('description', ''),
                'subsidy_status': facility.get('subsidy_status', ''),
                'image_url': facility.get('image_url', ''),
                # 指标数据
                'building_area': facility['indicators'].get('building_area', 0),
                'site_area': facility['indicators'].get('site_area', 0),
                'land_area': facility['indicators'].get('land_area', 0),
                'seats': facility['indicators'].get('seats', 0),
                'daily_visitors': facility['indicators'].get('daily_visitors', 0),
                'has_outdoor_fitness': facility['indicators'].get('has_outdoor_fitness', False)
            }
            
            self.kg.add_entity('Facility', facility_id, properties)
        
        logger.info(f"✅ 创建 {len(facilities)} 个设施实体")
    
    def _build_sport_entities(self, facilities: List[Dict]):
        """构建运动项目实体"""
        logger.info("构建运动项目实体...")
        
        # 收集所有运动项目
        sports = set()
        for facility in facilities:
            sports.update(facility.get('sports_types', []))
        
        # 运动项目分类
        sport_categories = {
            '足球': '球类运动', '篮球': '球类运动', '排球': '球类运动',
            '羽毛球': '球类运动', '乒乓球': '球类运动', '网球': '球类运动',
            '游泳': '水上运动', '跑步': '田径运动', '健身': '力量训练',
            '瑜伽': '柔韧性训练', '太极拳': '传统运动', '广场舞': '群众运动',
            '滑冰': '冰雪运动', '滑雪': '冰雪运动'
        }
        
        for sport in sports:
            if sport:
                sport_id = f"Sport_{sport}"
                self.kg.add_entity('Sport', sport_id, {
                    'name': sport,
                    'category': sport_categories.get(sport, '其他运动'),
                    'type': '运动项目'
                })
        
        logger.info(f"✅ 创建 {len(sports)} 个运动项目实体")
    
    def _build_indicator_entities(self, facilities: List[Dict]):
        """构建指标实体"""
        logger.info("构建指标实体...")
        
        # 定义指标类型
        indicators = [
            {'id': 'Indicator_场地面积', 'name': '场地面积', 'unit': '平方米', 'category': '设施指标'},
            {'id': 'Indicator_建筑面积', 'name': '建筑面积', 'unit': '平方米', 'category': '设施指标'},
            {'id': 'Indicator_用地面积', 'name': '用地面积', 'unit': '平方米', 'category': '设施指标'},
            {'id': 'Indicator_座位数', 'name': '座位数', 'unit': '座', 'category': '设施指标'},
            {'id': 'Indicator_日客流量', 'name': '日客流量', 'unit': '人次', 'category': '使用指标'},
            {'id': 'Indicator_人均场地面积', 'name': '人均体育场地面积', 'unit': '平方米/人', 'category': '区域指标'},
            {'id': 'Indicator_参与率', 'name': '经常参加体育锻炼人数比例', 'unit': '%', 'category': '人口指标'},
            {'id': 'Indicator_覆盖率', 'name': '公共健身设施覆盖率', 'unit': '%', 'category': '区域指标'},
            {'id': 'Indicator_设施密度', 'name': '每万人拥有体育设施数', 'unit': '个/万人', 'category': '区域指标'}
        ]
        
        for indicator in indicators:
            self.kg.add_entity('Indicator', indicator['id'], indicator)
        
        # 计算区域级指标
        city_stats = defaultdict(lambda: {'total_area': 0, 'facility_count': 0, 'total_visitors': 0})
        
        for facility in facilities:
            city = facility.get('location', {}).get('city')
            if city:
                city_stats[city]['total_area'] += facility['indicators'].get('site_area', 0)
                city_stats[city]['facility_count'] += 1
                city_stats[city]['total_visitors'] += facility['indicators'].get('daily_visitors', 0)
        
        # 为每个城市创建指标实例
        for city, stats in city_stats.items():
            city_id = f"Area_{city}"
            
            # 人均场地面积指标实例（假设人口100万）
            per_capita_area = stats['total_area'] / 1000000
            indicator_id = f"IndicatorValue_{city}_人均场地面积"
            self.kg.add_entity('Indicator', indicator_id, {
                'indicator_type': '人均体育场地面积',
                'value': round(per_capita_area, 2),
                'unit': '平方米/人',
                'area': city,
                'year': 2025
            })
            
            # 添加指标关系
            self.kg.add_relation(city_id, '具有指标', indicator_id)
        
        logger.info(f"✅ 创建 {len(indicators)} 个指标类型和区域指标实例")
    
    def _build_law_entities(self, facilities: List[Dict]):
        """构建政策法规实体"""
        logger.info("构建政策法规实体...")
        
        # 定义政策法规
        policies = [
            {
                'id': 'Law_全民健身计划',
                'title': '全民健身计划（2021-2025年）',
                'level': '国家级',
                'department': '国务院',
                'publish_year': 2021,
                'type': '规划'
            },
            {
                'id': 'Law_河北省全民健身条例',
                'title': '河北省全民健身条例',
                'level': '省级',
                'department': '河北省人大',
                'publish_year': 2020,
                'type': '法规'
            },
            {
                'id': 'Law_体育场馆补助政策',
                'title': '公共体育场馆向社会免费或低收费开放补助资金管理办法',
                'level': '国家级',
                'department': '财政部、体育总局',
                'publish_year': 2014,
                'type': '管理办法'
            }
        ]
        
        for policy in policies:
            self.kg.add_entity('Law', policy['id'], policy)
        
        logger.info(f"✅ 创建 {len(policies)} 个政策法规实体")
    
    def _build_relations(self, facilities: List[Dict]):
        """构建实体间关系"""
        logger.info("构建实体间关系...")
        
        relation_count = 0
        
        for facility in facilities:
            facility_id = f"Facility_{facility['id']}"
            
            # 1. 设施-区域关系
            city = facility.get('location', {}).get('city')
            if city:
                city_id = f"Area_{city}"
                self.kg.add_relation(facility_id, '位于', city_id)
                relation_count += 1
            
            # 2. 设施-时间关系
            build_year = facility.get('build_year')
            if build_year:
                year_id = f"Year_{build_year}"
                self.kg.add_relation(facility_id, '建成于', year_id)
                relation_count += 1
            
            # 3. 设施-运动项目关系
            for sport in facility.get('sports_types', []):
                if sport:
                    sport_id = f"Sport_{sport}"
                    self.kg.add_relation(facility_id, '提供', sport_id)
                    relation_count += 1
            
            # 4. 设施-政策关系（基于补助状态）
            if '补助' in facility.get('subsidy_status', ''):
                self.kg.add_relation(facility_id, '受益于', 'Law_体育场馆补助政策')
                relation_count += 1
            
            # 5. 设施-指标关系
            # 每个设施都符合场地面积指标
            self.kg.add_relation(facility_id, '符合指标', 'Indicator_场地面积', {
                'value': facility['indicators'].get('site_area', 0)
            })
            relation_count += 1
        
        logger.info(f"✅ 创建 {relation_count} 个关系")
    
    def export_knowledge_graph(self, json_file: str = 'fps_knowledge_graph.json', 
                               owl_file: str = 'fps_ontology.owl'):
        """导出知识图谱"""
        logger.info("导出知识图谱...")
        
        # 导出JSON格式
        self.kg.export_to_json(json_file)
        
        # 导出OWL格式（用于Protege）
        self.kg.export_to_owl(owl_file)
        
        logger.info("✅ 知识图谱导出完成")


def main():
    """主函数"""
    logger.info("=" * 80)
    logger.info("开始构建河北省全民健身公共服务知识图谱")
    logger.info("=" * 80)
    
    # 创建构建器
    builder = FPSKnowledgeGraphBuilder()
    
    # 从数据文件构建知识图谱
    kg = builder.build_from_facilities_data('fitness_facilities_data.json')
    
    # 导出知识图谱
    builder.export_knowledge_graph(
        json_file='fps_knowledge_graph.json',
        owl_file='fps_ontology.owl'
    )
    
    # 显示统计信息
    stats = kg.get_statistics()
    logger.info("\n" + "=" * 80)
    logger.info("知识图谱统计信息")
    logger.info("=" * 80)
    logger.info(f"总实体数: {stats['total_entities']}")
    logger.info(f"总关系数: {stats['total_relations']}")
    logger.info(f"关系类型数: {stats['relation_types']}")
    logger.info("\n实体分布:")
    for entity_type, count in stats['entities'].items():
        logger.info(f"  {entity_type}: {count} 个")
    logger.info("=" * 80)
    
    logger.info("\n🎉 知识图谱构建完成!")
    logger.info("输出文件:")
    logger.info("  - fps_knowledge_graph.json (JSON格式)")
    logger.info("  - fps_ontology.owl (OWL本体格式，可用Protege打开)")
    logger.info("  - logs/knowledge_graph.log (日志文件)")


if __name__ == "__main__":
    main()
