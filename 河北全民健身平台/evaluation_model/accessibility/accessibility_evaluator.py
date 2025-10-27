"""
可及性评价模块 - GIS空间分析、距离计算、时间可及性
"""
import numpy as np
import pandas as pd
from typing import List, Dict, Tuple
from loguru import logger
import json
from math import radians, cos, sin, asin, sqrt


class AccessibilityEvaluator:
    """可及性评价器"""
    
    def __init__(self):
        logger.info("初始化可及性评价器")
    
    def haversine_distance(self, lon1: float, lat1: float, 
                          lon2: float, lat2: float) -> float:
        """
        计算两点间的球面距离 (Haversine公式)
        返回距离单位: 公里
        """
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        r = 6371  # 地球平均半径，单位为公里
        
        return c * r
    
    def calculate_nearest_facility(self, user_location: Tuple[float, float],
                                   facilities: List[Dict]) -> Dict:
        """计算最近的健身设施"""
        user_lon, user_lat = user_location
        
        min_distance = float('inf')
        nearest_facility = None
        
        for facility in facilities:
            facility_lon = facility.get('longitude', 0)
            facility_lat = facility.get('latitude', 0)
            
            distance = self.haversine_distance(user_lon, user_lat, facility_lon, facility_lat)
            
            if distance < min_distance:
                min_distance = distance
                nearest_facility = facility
        
        return {
            "facility": nearest_facility,
            "distance_km": min_distance,
            "walking_time_min": min_distance / 5 * 60,  # 假设步行速度5km/h
            "cycling_time_min": min_distance / 15 * 60,  # 假设骑行速度15km/h
            "driving_time_min": min_distance / 40 * 60   # 假设驾车速度40km/h
        }
    
    def calculate_service_coverage(self, facilities: List[Dict], 
                                   service_radius_km: float = 2.0) -> Dict:
        """
        计算服务覆盖率
        service_radius_km: 服务半径(公里)
        """
        logger.info(f"计算服务覆盖率 (服务半径: {service_radius_km}km)...")
        
        # 模拟居民点
        residential_points = self._generate_residential_points()
        
        covered_points = 0
        coverage_details = []
        
        for point in residential_points:
            point_lon, point_lat = point['longitude'], point['latitude']
            
            # 检查是否在任何设施的服务范围内
            is_covered = False
            nearest_distance = float('inf')
            
            for facility in facilities:
                distance = self.haversine_distance(
                    point_lon, point_lat,
                    facility['longitude'], facility['latitude']
                )
                
                if distance < nearest_distance:
                    nearest_distance = distance
                
                if distance <= service_radius_km:
                    is_covered = True
            
            if is_covered:
                covered_points += 1
            
            coverage_details.append({
                "point_id": point['id'],
                "is_covered": is_covered,
                "nearest_distance_km": nearest_distance
            })
        
        coverage_rate = covered_points / len(residential_points)
        
        result = {
            "total_points": len(residential_points),
            "covered_points": covered_points,
            "coverage_rate": coverage_rate,
            "service_radius_km": service_radius_km,
            "interpretation": self._interpret_coverage(coverage_rate)
        }
        
        logger.info(f"覆盖率: {coverage_rate:.2%}")
        return result
    
    def _generate_residential_points(self, count: int = 100) -> List[Dict]:
        """生成模拟居民点"""
        # 河北省大致范围
        lon_range = (113.5, 119.5)
        lat_range = (36.0, 42.5)
        
        points = []
        for i in range(count):
            points.append({
                "id": i,
                "longitude": np.random.uniform(*lon_range),
                "latitude": np.random.uniform(*lat_range)
            })
        
        return points
    
    def calculate_15min_fitness_circle(self, facilities: List[Dict]) -> Dict:
        """
        计算15分钟健身圈覆盖率
        15分钟步行距离约为1.25公里
        """
        logger.info("计算15分钟健身圈覆盖率...")
        
        service_radius = 1.25  # 公里
        result = self.calculate_service_coverage(facilities, service_radius)
        
        result["circle_type"] = "15分钟健身圈"
        result["walking_time_min"] = 15
        
        return result
    
    def evaluate_time_accessibility(self, facilities: List[Dict]) -> Dict:
        """评价时间可及性"""
        logger.info("评价时间可及性...")
        
        # 分析开放时间
        open_hours_analysis = []
        
        for facility in facilities:
            open_hours = facility.get('open_hours', '')
            
            # 解析开放时间
            if '全天' in open_hours:
                daily_hours = 24
            elif '-' in open_hours:
                # 简化处理: 06:00-22:00 -> 16小时
                parts = open_hours.split('-')
                if len(parts) == 2:
                    start_hour = int(parts[0].split(':')[0])
                    end_hour = int(parts[1].split(':')[0])
                    daily_hours = end_hour - start_hour
                else:
                    daily_hours = 12  # 默认值
            else:
                daily_hours = 12
            
            open_hours_analysis.append({
                "facility": facility['name'],
                "open_hours": open_hours,
                "daily_hours": daily_hours,
                "accessibility_score": daily_hours / 24
            })
        
        avg_daily_hours = np.mean([item['daily_hours'] for item in open_hours_analysis])
        avg_accessibility = avg_daily_hours / 24
        
        result = {
            "facilities_analysis": open_hours_analysis,
            "average_daily_hours": avg_daily_hours,
            "average_accessibility_score": avg_accessibility,
            "interpretation": self._interpret_time_accessibility(avg_accessibility)
        }
        
        logger.info(f"平均每日开放时长: {avg_daily_hours:.1f}小时")
        return result
    
    def calculate_comprehensive_accessibility(self, facilities: List[Dict],
                                             population_data: List[Dict]) -> Dict:
        """计算综合可及性指数"""
        logger.info("计算综合可及性指数...")
        
        # 地理可及性 (15分钟健身圈覆盖率)
        geo_accessibility = self.calculate_15min_fitness_circle(facilities)
        
        # 时间可及性
        time_accessibility = self.evaluate_time_accessibility(facilities)
        
        # 设施密度
        total_population = sum(city['total_population'] for city in population_data)
        facility_density = len(facilities) / (total_population / 10000)  # 每万人设施数
        
        # 综合可及性指数 (加权平均)
        weights = {
            'geographic': 0.4,
            'temporal': 0.3,
            'density': 0.3
        }
        
        comprehensive_score = (
            geo_accessibility['coverage_rate'] * weights['geographic'] +
            time_accessibility['average_accessibility_score'] * weights['temporal'] +
            min(facility_density / 2, 1.0) * weights['density']  # 归一化密度指标
        )
        
        result = {
            "geographic_accessibility": geo_accessibility['coverage_rate'],
            "temporal_accessibility": time_accessibility['average_accessibility_score'],
            "facility_density_per_10k": facility_density,
            "comprehensive_score": comprehensive_score,
            "weights": weights,
            "interpretation": self._interpret_comprehensive(comprehensive_score)
        }
        
        logger.info(f"综合可及性指数: {comprehensive_score:.4f}")
        return result
    
    def _interpret_coverage(self, rate: float) -> str:
        """解释覆盖率"""
        if rate >= 0.9:
            return "优秀 - 覆盖率很高"
        elif rate >= 0.75:
            return "良好 - 覆盖率较高"
        elif rate >= 0.6:
            return "中等 - 覆盖率一般"
        else:
            return "较差 - 覆盖率偏低"
    
    def _interpret_time_accessibility(self, score: float) -> str:
        """解释时间可及性"""
        if score >= 0.75:
            return "优秀 - 开放时间充足"
        elif score >= 0.6:
            return "良好 - 开放时间较好"
        elif score >= 0.45:
            return "中等 - 开放时间一般"
        else:
            return "较差 - 开放时间不足"
    
    def _interpret_comprehensive(self, score: float) -> str:
        """解释综合可及性"""
        if score >= 0.8:
            return "优秀"
        elif score >= 0.65:
            return "良好"
        elif score >= 0.5:
            return "中等"
        else:
            return "需要改进"


if __name__ == "__main__":
    # 测试示例
    evaluator = AccessibilityEvaluator()
    
    # 加载设施数据
    with open('data/raw/facilities.json', 'r', encoding='utf-8') as f:
        facilities = json.load(f)
    
    # 加载人口数据
    with open('data/raw/population.json', 'r', encoding='utf-8') as f:
        population = json.load(f)
    
    # 计算综合可及性
    accessibility_result = evaluator.calculate_comprehensive_accessibility(facilities, population)
    
    # 保存结果
    with open('data/processed/accessibility_evaluation.json', 'w', encoding='utf-8') as f:
        json.dump(accessibility_result, f, ensure_ascii=False, indent=2)
    
    logger.info("✅ 可及性评价完成!")
    print(json.dumps(accessibility_result, ensure_ascii=False, indent=2))
