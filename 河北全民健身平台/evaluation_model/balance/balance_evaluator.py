"""
均衡性评价模块 - 基尼系数、集中指数、区位商
"""
import numpy as np
import pandas as pd
from typing import List, Dict, Tuple
from loguru import logger
import json


class BalanceEvaluator:
    """均衡性评价器"""
    
    def __init__(self):
        logger.info("初始化均衡性评价器")
    
    def calculate_gini_coefficient(self, data: np.ndarray) -> float:
        """
        计算基尼系数
        Gini = (2 * Σ(i * x_i)) / (n * Σx_i) - (n + 1) / n
        """
        sorted_data = np.sort(data)
        n = len(data)
        index = np.arange(1, n + 1)
        
        gini = (2 * np.sum(index * sorted_data)) / (n * np.sum(sorted_data)) - (n + 1) / n
        
        logger.info(f"基尼系数: {gini:.4f}")
        return gini
    
    def calculate_concentration_index(self, facilities: np.ndarray, 
                                     population: np.ndarray) -> float:
        """
        计算集中指数 (Concentration Index)
        CI = Σ|f_i - p_i|
        其中 f_i 是设施比例, p_i 是人口比例
        """
        # 归一化
        facility_ratio = facilities / np.sum(facilities)
        population_ratio = population / np.sum(population)
        
        # 计算集中指数
        ci = np.sum(np.abs(facility_ratio - population_ratio))
        
        logger.info(f"集中指数: {ci:.4f}")
        return ci
    
    def calculate_location_quotient(self, local_facilities: float, 
                                   local_population: float,
                                   total_facilities: float, 
                                   total_population: float) -> float:
        """
        计算区位商 (Location Quotient)
        LQ = (local_facilities / local_population) / (total_facilities / total_population)
        """
        if local_population == 0 or total_population == 0:
            return 0.0
        
        lq = (local_facilities / local_population) / (total_facilities / total_population)
        
        logger.info(f"区位商: {lq:.4f}")
        return lq
    
    def evaluate_facility_balance(self, cities_data: List[Dict]) -> Dict:
        """评价设施分布均衡性"""
        logger.info("开始评价设施分布均衡性...")
        
        # 提取数据
        cities = [city['city'] for city in cities_data]
        populations = np.array([city['total_population'] for city in cities_data])
        
        # 假设设施数据
        facilities_count = np.array([150, 120, 100])  # 石家庄、保定、唐山
        facilities_area = np.array([500000, 380000, 420000])  # 平方米
        
        # 计算人均设施面积
        per_capita_area = facilities_area / populations
        
        # 基尼系数 - 设施面积分布
        gini_area = self.calculate_gini_coefficient(facilities_area)
        
        # 基尼系数 - 人均设施面积
        gini_per_capita = self.calculate_gini_coefficient(per_capita_area)
        
        # 集中指数
        ci = self.calculate_concentration_index(facilities_area, populations)
        
        # 区位商
        location_quotients = []
        total_facilities = np.sum(facilities_count)
        total_population = np.sum(populations)
        
        for i, city in enumerate(cities):
            lq = self.calculate_location_quotient(
                facilities_count[i], populations[i],
                total_facilities, total_population
            )
            location_quotients.append({
                "city": city,
                "location_quotient": lq,
                "interpretation": self._interpret_lq(lq)
            })
        
        result = {
            "gini_coefficient": {
                "total_area": gini_area,
                "per_capita_area": gini_per_capita,
                "interpretation": self._interpret_gini(gini_per_capita)
            },
            "concentration_index": {
                "value": ci,
                "interpretation": self._interpret_ci(ci)
            },
            "location_quotients": location_quotients,
            "per_capita_areas": [
                {"city": cities[i], "area": per_capita_area[i]}
                for i in range(len(cities))
            ]
        }
        
        logger.info("✅ 设施分布均衡性评价完成")
        return result
    
    def _interpret_gini(self, gini: float) -> str:
        """解释基尼系数"""
        if gini < 0.2:
            return "高度均衡"
        elif gini < 0.3:
            return "相对均衡"
        elif gini < 0.4:
            return "基本均衡"
        elif gini < 0.5:
            return "不够均衡"
        else:
            return "严重不均衡"
    
    def _interpret_ci(self, ci: float) -> str:
        """解释集中指数"""
        if ci < 0.2:
            return "设施分布与人口分布高度匹配"
        elif ci < 0.4:
            return "设施分布与人口分布较为匹配"
        elif ci < 0.6:
            return "设施分布与人口分布存在一定偏差"
        else:
            return "设施分布与人口分布严重不匹配"
    
    def _interpret_lq(self, lq: float) -> str:
        """解释区位商"""
        if lq > 1.2:
            return "设施相对集中,高于平均水平"
        elif lq > 0.8:
            return "设施分布适中,接近平均水平"
        else:
            return "设施相对不足,低于平均水平"
    
    def calculate_resource_balance(self, investment_data: List[Dict]) -> Dict:
        """计算资源投入均衡性"""
        logger.info("计算资源投入均衡性...")
        
        cities = [item['city'] for item in investment_data]
        investments = np.array([item['investment'] for item in investment_data])
        populations = np.array([item['population'] for item in investment_data])
        
        # 人均投入
        per_capita_investment = investments / populations
        
        # 基尼系数
        gini = self.calculate_gini_coefficient(per_capita_investment)
        
        # 变异系数
        cv = np.std(per_capita_investment) / np.mean(per_capita_investment)
        
        result = {
            "gini_coefficient": gini,
            "coefficient_of_variation": cv,
            "per_capita_investments": [
                {"city": cities[i], "investment": per_capita_investment[i]}
                for i in range(len(cities))
            ],
            "interpretation": {
                "gini": self._interpret_gini(gini),
                "cv": "高度分散" if cv > 0.5 else "相对集中" if cv > 0.3 else "高度集中"
            }
        }
        
        logger.info("✅ 资源投入均衡性计算完成")
        return result


class ServiceBalanceAnalyzer:
    """服务项目均衡性分析器"""
    
    def __init__(self):
        self.evaluator = BalanceEvaluator()
    
    def analyze_activity_distribution(self, facilities_data: List[Dict]) -> Dict:
        """分析运动项目分布均衡性"""
        logger.info("分析运动项目分布均衡性...")
        
        # 统计各类运动项目数量
        activity_counts = {}
        for facility in facilities_data:
            for activity in facility.get('facilities', []):
                activity_counts[activity] = activity_counts.get(activity, 0) + 1
        
        # 计算分布均衡度
        counts = np.array(list(activity_counts.values()))
        
        # 香农熵 - 衡量多样性
        probabilities = counts / np.sum(counts)
        shannon_entropy = -np.sum(probabilities * np.log2(probabilities + 1e-10))
        max_entropy = np.log2(len(counts))
        diversity_index = shannon_entropy / max_entropy if max_entropy > 0 else 0
        
        # 基尼系数
        gini = self.evaluator.calculate_gini_coefficient(counts)
        
        result = {
            "activity_counts": activity_counts,
            "diversity_index": diversity_index,
            "gini_coefficient": gini,
            "interpretation": {
                "diversity": "高度多样" if diversity_index > 0.8 else "较为多样" if diversity_index > 0.6 else "多样性不足",
                "balance": self.evaluator._interpret_gini(gini)
            }
        }
        
        logger.info("✅ 运动项目分布均衡性分析完成")
        return result


if __name__ == "__main__":
    # 测试示例
    evaluator = BalanceEvaluator()
    
    # 城市数据
    cities_data = [
        {"city": "石家庄市", "total_population": 11000000},
        {"city": "保定市", "total_population": 9400000},
        {"city": "唐山市", "total_population": 7700000}
    ]
    
    # 评价设施均衡性
    balance_result = evaluator.evaluate_facility_balance(cities_data)
    
    # 保存结果
    with open('data/processed/balance_evaluation.json', 'w', encoding='utf-8') as f:
        json.dump(balance_result, f, ensure_ascii=False, indent=2)
    
    logger.info("✅ 均衡性评价完成!")
    print(json.dumps(balance_result, ensure_ascii=False, indent=2))
