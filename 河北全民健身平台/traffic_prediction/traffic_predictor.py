#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
客流预测模型 - 核心实现
结合知识图谱的多因素客流预测系统
"""

import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from loguru import logger
import sys
from pathlib import Path

# 配置日志
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)
logger.remove()
logger.add(sys.stderr, level="INFO")
logger.add(log_dir / "traffic_prediction.log", rotation="10 MB", level="DEBUG")


class FeatureExtractor:
    """特征提取器"""
    
    def __init__(self, kg_data_file: str):
        """初始化
        
        Args:
            kg_data_file: 知识图谱JSON文件路径
        """
        with open(kg_data_file, 'r', encoding='utf-8') as f:
            self.kg_data = json.load(f)
        
        self.entities = self.kg_data['entities']
        self.relations = self.kg_data['relations']
        logger.info("✅ 特征提取器初始化完成")
    
    def extract_time_features(self, timestamp: datetime) -> Dict:
        """提取时间特征"""
        features = {
            # 基础时间特征
            'hour': timestamp.hour,
            'day_of_week': timestamp.weekday(),
            'day_of_month': timestamp.day,
            'month': timestamp.month,
            'quarter': (timestamp.month - 1) // 3 + 1,
            
            # 周期性特征（正弦/余弦编码）
            'hour_sin': np.sin(2 * np.pi * timestamp.hour / 24),
            'hour_cos': np.cos(2 * np.pi * timestamp.hour / 24),
            'day_sin': np.sin(2 * np.pi * timestamp.weekday() / 7),
            'day_cos': np.cos(2 * np.pi * timestamp.weekday() / 7),
            'month_sin': np.sin(2 * np.pi * timestamp.month / 12),
            'month_cos': np.cos(2 * np.pi * timestamp.month / 12),
            
            # 类别特征
            'is_weekend': 1 if timestamp.weekday() >= 5 else 0,
            'is_morning': 1 if 6 <= timestamp.hour < 12 else 0,
            'is_afternoon': 1 if 12 <= timestamp.hour < 18 else 0,
            'is_evening': 1 if 18 <= timestamp.hour < 22 else 0,
            'is_peak_hour': 1 if timestamp.hour in [9, 10, 11, 18, 19, 20] else 0,
        }
        
        return features
    
    def extract_facility_features(self, facility_id: str) -> Dict:
        """从知识图谱提取场馆特征"""
        # 查找设施实体
        facility = None
        for fac_id, fac_data in self.entities['Facility'].items():
            if fac_id == facility_id:
                facility = fac_data
                break
        
        if not facility:
            logger.warning(f"未找到设施: {facility_id}")
            return {}
        
        features = {
            # 规模特征
            'site_area': facility.get('site_area', 0),
            'building_area': facility.get('building_area', 0),
            'seats': facility.get('seats', 0),
            'daily_visitors': facility.get('daily_visitors', 0),
            
            # 类型特征（One-Hot编码）
            'type_stadium': 1 if facility.get('type') == '体育场' else 0,
            'type_gymnasium': 1 if facility.get('type') == '体育馆' else 0,
            'type_fitness': 1 if facility.get('type') == '健身中心' else 0,
            'type_swimming': 1 if facility.get('type') == '游泳馆' else 0,
            
            # 时间特征
            'build_year': facility.get('build_year', 2000),
            'facility_age': 2024 - facility.get('build_year', 2000),
            
            # 设施状态
            'has_outdoor_fitness': 1 if facility.get('has_outdoor_fitness') else 0,
        }
        
        return features
    
    def extract_kg_features(self, facility_id: str) -> Dict:
        """提取知识图谱关系特征"""
        features = {}
        
        # 1. 统计关系数量
        relation_count = 0
        sports = []
        has_subsidy = 0
        city_id = None
        
        for rel in self.relations:
            if rel['subject'] == facility_id:
                relation_count += 1
                
                # 提供的运动项目
                if rel['predicate'] == '提供':
                    sports.append(rel['object'])
                
                # 政策受益
                if rel['predicate'] == '受益于':
                    has_subsidy = 1
                
                # 所在城市
                if rel['predicate'] == '位于':
                    city_id = rel['object']
        
        features['relation_count'] = relation_count
        features['sport_count'] = len(sports)
        features['has_subsidy'] = has_subsidy
        
        # 2. 城市级特征
        if city_id:
            city_facilities = self._get_city_facilities(city_id)
            features['nearby_facility_count'] = len(city_facilities)
            
            # 计算同城平均客流
            nearby_visitors = [
                f.get('daily_visitors', 0) 
                for f in city_facilities 
                if f.get('daily_visitors', 0) > 0
            ]
            features['nearby_avg_visitors'] = np.mean(nearby_visitors) if nearby_visitors else 0
        else:
            features['nearby_facility_count'] = 0
            features['nearby_avg_visitors'] = 0
        
        return features
    
    def _get_city_facilities(self, city_id: str) -> List[Dict]:
        """获取城市的所有设施"""
        facilities = []
        
        for rel in self.relations:
            if rel['predicate'] == '位于' and rel['object'] == city_id:
                fac_id = rel['subject']
                if fac_id in self.entities['Facility']:
                    facilities.append(self.entities['Facility'][fac_id])
        
        return facilities
    
    def extract_all_features(self, facility_id: str, timestamp: datetime) -> Dict:
        """提取所有特征"""
        features = {}
        
        # 时间特征
        features.update(self.extract_time_features(timestamp))
        
        # 场馆特征
        features.update(self.extract_facility_features(facility_id))
        
        # 知识图谱特征
        features.update(self.extract_kg_features(facility_id))
        
        logger.debug(f"提取特征: {facility_id} @ {timestamp}, 特征数: {len(features)}")
        
        return features


class SimpleTrafficPredictor:
    """简化的客流预测器（基于规则和统计）"""
    
    def __init__(self, feature_extractor: FeatureExtractor):
        self.feature_extractor = feature_extractor
        logger.info("✅ 客流预测器初始化完成")
    
    def predict(self, facility_id: str, timestamp: datetime) -> Dict:
        """预测客流
        
        Args:
            facility_id: 设施ID
            timestamp: 预测时间点
            
        Returns:
            预测结果字典
        """
        # 提取特征
        features = self.feature_extractor.extract_all_features(facility_id, timestamp)
        
        # 基础客流（日均客流）
        base_visitors = features.get('daily_visitors', 0)
        
        # 时间调整因子
        hour_factor = self._get_hour_factor(features['hour'])
        
        # 周末调整
        weekend_factor = 1.3 if features['is_weekend'] else 1.0
        
        # 季节调整
        season_factor = self._get_season_factor(features['month'])
        
        # 设施类型调整
        type_factor = self._get_type_factor(features)
        
        # 知识图谱调整（邻近设施影响）
        kg_factor = self._get_kg_factor(features)
        
        # 综合预测
        prediction = (
            base_visitors * 
            hour_factor * 
            weekend_factor * 
            season_factor * 
            type_factor * 
            kg_factor
        )
        
        # 容量约束
        max_capacity = features.get('seats', 1000) * 1.5
        prediction = min(prediction, max_capacity)
        
        # 置信区间（简化）
        std = prediction * 0.15
        confidence_interval = (
            max(0, prediction - 1.96 * std),
            prediction + 1.96 * std
        )
        
        result = {
            'facility_id': facility_id,
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'predicted_visitors': int(prediction),
            'confidence_interval': {
                'lower': int(confidence_interval[0]),
                'upper': int(confidence_interval[1])
            },
            'factors': {
                'base_visitors': base_visitors,
                'hour_factor': hour_factor,
                'weekend_factor': weekend_factor,
                'season_factor': season_factor,
                'type_factor': type_factor,
                'kg_factor': kg_factor
            }
        }
        
        logger.info(f"预测完成: {facility_id} @ {timestamp.hour}:00 -> {int(prediction)} 人")
        
        return result
    
    def _get_hour_factor(self, hour: int) -> float:
        """获取小时调整因子"""
        # 典型的客流分布模式
        hourly_pattern = {
            6: 0.3, 7: 0.5, 8: 0.7, 9: 0.9,
            10: 0.8, 11: 0.7, 12: 0.5, 13: 0.4,
            14: 0.5, 15: 0.7, 16: 0.9, 17: 1.2,
            18: 1.5, 19: 1.3, 20: 0.8, 21: 0.4
        }
        return hourly_pattern.get(hour, 0.1)
    
    def _get_season_factor(self, month: int) -> float:
        """获取季节调整因子"""
        # 春夏秋冬的客流差异
        if month in [3, 4, 5]:  # 春季
            return 1.1
        elif month in [6, 7, 8]:  # 夏季
            return 1.2
        elif month in [9, 10, 11]:  # 秋季
            return 1.15
        else:  # 冬季
            return 0.9
    
    def _get_type_factor(self, features: Dict) -> float:
        """获取设施类型调整因子"""
        if features.get('type_gymnasium'):
            return 1.1  # 体育馆更受欢迎
        elif features.get('type_fitness'):
            return 1.2  # 健身中心客流稳定
        elif features.get('type_swimming'):
            return 0.9  # 游泳馆季节性强
        else:
            return 1.0
    
    def _get_kg_factor(self, features: Dict) -> float:
        """获取知识图谱调整因子"""
        # 基于邻近设施的影响
        nearby_count = features.get('nearby_facility_count', 0)
        
        if nearby_count > 30:
            # 竞争激烈，分流效应
            return 0.9
        elif nearby_count > 15:
            return 0.95
        elif nearby_count < 5:
            # 独家优势
            return 1.1
        else:
            return 1.0


class ScheduleOptimizer:
    """开放时间优化器"""
    
    def __init__(self, predictor: SimpleTrafficPredictor):
        self.predictor = predictor
        logger.info("✅ 调度优化器初始化完成")
    
    def optimize_daily_schedule(self, facility_id: str, date: str) -> Dict:
        """优化一天的开放时间
        
        Args:
            facility_id: 设施ID
            date: 日期 (YYYY-MM-DD)
            
        Returns:
            优化后的时间表
        """
        logger.info(f"开始优化 {facility_id} 在 {date} 的开放时间")
        
        # 预测24小时客流
        predictions = []
        base_time = datetime.strptime(date, '%Y-%m-%d')
        
        for hour in range(24):
            timestamp = base_time + timedelta(hours=hour)
            pred = self.predictor.predict(facility_id, timestamp)
            predictions.append(pred)
        
        # 生成调度方案
        schedule = []
        for pred in predictions:
            hour = datetime.strptime(pred['timestamp'], '%Y-%m-%d %H:%M:%S').hour
            visitors = pred['predicted_visitors']
            
            # 决策规则
            if visitors < 30:
                status = 'closed'
                staff = 0
                areas = []
            elif visitors < 100:
                status = 'limited_open'
                staff = 2
                areas = ['室外场地']
            elif visitors < 200:
                status = 'normal_open'
                staff = 4
                areas = ['室内场馆', '室外场地']
            else:
                status = 'full_open'
                staff = 6
                areas = ['全部场地']
            
            schedule.append({
                'hour': f"{hour:02d}:00",
                'predicted_visitors': visitors,
                'status': status,
                'staff_count': staff,
                'open_areas': areas,
                'load_rate': self._calculate_load_rate(visitors, facility_id)
            })
        
        # 统计信息
        total_visitors = sum(p['predicted_visitors'] for p in predictions)
        total_staff_hours = sum(s['staff_count'] for s in schedule)
        peak_hour = max(predictions, key=lambda x: x['predicted_visitors'])
        
        result = {
            'facility_id': facility_id,
            'date': date,
            'schedule': schedule,
            'summary': {
                'total_predicted_visitors': total_visitors,
                'total_staff_hours': total_staff_hours,
                'peak_hour': datetime.strptime(peak_hour['timestamp'], '%Y-%m-%d %H:%M:%S').hour,
                'peak_visitors': peak_hour['predicted_visitors']
            }
        }
        
        logger.info(f"✅ 优化完成: 预计总客流 {total_visitors} 人, 高峰时段 {result['summary']['peak_hour']}:00")
        
        return result
    
    def _calculate_load_rate(self, visitors: int, facility_id: str) -> float:
        """计算负载率"""
        # 从特征提取器获取容量
        features = self.predictor.feature_extractor.extract_facility_features(facility_id)
        capacity = features.get('seats', 500) * 1.5
        
        return min(visitors / capacity, 1.0) if capacity > 0 else 0.0


class TrafficDistributor:
    """人员分流器"""
    
    def __init__(self, predictor: SimpleTrafficPredictor):
        self.predictor = predictor
        self.feature_extractor = predictor.feature_extractor
        logger.info("✅ 分流器初始化完成")
    
    def distribute(self, city: str, timestamp: datetime) -> Dict:
        """智能分流
        
        Args:
            city: 城市名称
            timestamp: 时间点
            
        Returns:
            分流建议
        """
        logger.info(f"开始分流分析: {city} @ {timestamp}")
        
        # 获取城市所有设施
        city_id = f"Area_{city}"
        facilities = self._get_city_facilities(city_id)
        
        if not facilities:
            logger.warning(f"未找到城市: {city}")
            return {'error': '未找到城市设施'}
        
        # 预测所有设施的客流
        predictions = []
        for fac in facilities:
            fac_id = fac['id']
            pred = self.predictor.predict(fac_id, timestamp)
            
            # 计算负载率
            capacity = fac.get('seats', 500) * 1.5
            load_rate = pred['predicted_visitors'] / capacity if capacity > 0 else 0
            
            predictions.append({
                'facility_id': fac_id,
                'name': fac.get('name', '未知'),
                'predicted_visitors': pred['predicted_visitors'],
                'capacity': int(capacity),
                'load_rate': load_rate,
                'status': self._get_status(load_rate)
            })
        
        # 排序：按负载率
        predictions.sort(key=lambda x: x['load_rate'])
        
        # 生成分流建议
        recommendations = []
        for pred in predictions:
            if pred['load_rate'] > 0.8:
                # 拥挤，推荐到其他场馆
                alternatives = [
                    p for p in predictions 
                    if p['facility_id'] != pred['facility_id'] and p['load_rate'] < 0.6
                ][:3]
                
                recommendations.append({
                    'facility': pred['name'],
                    'status': 'crowded',
                    'load_rate': f"{pred['load_rate']:.1%}",
                    'alternatives': [
                        {
                            'name': alt['name'],
                            'load_rate': f"{alt['load_rate']:.1%}"
                        }
                        for alt in alternatives
                    ]
                })
        
        result = {
            'city': city,
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'total_facilities': len(facilities),
            'facility_status': predictions,
            'recommendations': recommendations
        }
        
        logger.info(f"✅ 分流分析完成: {len(recommendations)} 个拥挤场馆")
        
        return result
    
    def _get_city_facilities(self, city_id: str) -> List[Dict]:
        """获取城市设施"""
        facilities = []
        
        for rel in self.feature_extractor.relations:
            if rel['predicate'] == '位于' and rel['object'] == city_id:
                fac_id = rel['subject']
                if fac_id in self.feature_extractor.entities['Facility']:
                    fac_data = self.feature_extractor.entities['Facility'][fac_id]
                    fac_data['id'] = fac_id
                    facilities.append(fac_data)
        
        return facilities
    
    def _get_status(self, load_rate: float) -> str:
        """获取状态"""
        if load_rate > 0.9:
            return 'very_crowded'
        elif load_rate > 0.7:
            return 'crowded'
        elif load_rate > 0.4:
            return 'normal'
        else:
            return 'available'


def demo():
    """演示功能"""
    logger.info("=" * 80)
    logger.info("客流预测与智能调度系统 - 演示")
    logger.info("=" * 80)
    
    # 1. 初始化
    feature_extractor = FeatureExtractor('fps_knowledge_graph.json')
    predictor = SimpleTrafficPredictor(feature_extractor)
    optimizer = ScheduleOptimizer(predictor)
    distributor = TrafficDistributor(predictor)
    
    # 2. 单点预测
    logger.info("\n" + "=" * 80)
    logger.info("演示1: 单点客流预测")
    logger.info("=" * 80)
    
    facility_id = "Facility_1"
    timestamp = datetime(2024, 10, 30, 18, 0)  # 2024-10-30 18:00
    
    prediction = predictor.predict(facility_id, timestamp)
    logger.info(f"\n预测结果:")
    logger.info(f"  设施: {facility_id}")
    logger.info(f"  时间: {prediction['timestamp']}")
    logger.info(f"  预测客流: {prediction['predicted_visitors']} 人")
    logger.info(f"  置信区间: [{prediction['confidence_interval']['lower']}, {prediction['confidence_interval']['upper']}]")
    
    # 3. 开放时间优化
    logger.info("\n" + "=" * 80)
    logger.info("演示2: 开放时间优化")
    logger.info("=" * 80)
    
    schedule = optimizer.optimize_daily_schedule(facility_id, "2024-10-30")
    logger.info(f"\n优化结果:")
    logger.info(f"  预计总客流: {schedule['summary']['total_predicted_visitors']} 人")
    logger.info(f"  高峰时段: {schedule['summary']['peak_hour']}:00")
    logger.info(f"  高峰客流: {schedule['summary']['peak_visitors']} 人")
    logger.info(f"\n时间表（部分）:")
    for item in schedule['schedule'][6:22]:  # 6:00-22:00
        logger.info(f"  {item['hour']} | {item['status']:15s} | {item['predicted_visitors']:4d}人 | 员工:{item['staff_count']}人")
    
    # 4. 智能分流
    logger.info("\n" + "=" * 80)
    logger.info("演示3: 智能分流")
    logger.info("=" * 80)
    
    distribution = distributor.distribute("石家庄市", timestamp)
    logger.info(f"\n分流分析:")
    logger.info(f"  城市: {distribution['city']}")
    logger.info(f"  总设施数: {distribution['total_facilities']}")
    logger.info(f"  拥挤场馆数: {len(distribution['recommendations'])}")
    
    if distribution['recommendations']:
        logger.info(f"\n拥挤场馆及替代建议:")
        for rec in distribution['recommendations'][:3]:
            logger.info(f"  ❌ {rec['facility']} (负载率: {rec['load_rate']})")
            for alt in rec['alternatives']:
                logger.info(f"     ✅ 推荐: {alt['name']} (负载率: {alt['load_rate']})")
    
    logger.info("\n" + "=" * 80)
    logger.info("🎉 演示完成!")
    logger.info("=" * 80)


if __name__ == "__main__":
    demo()
