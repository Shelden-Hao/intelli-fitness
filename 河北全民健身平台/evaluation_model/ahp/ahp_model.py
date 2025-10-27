"""
AHP层次分析法模块
"""
import numpy as np
from typing import List, Dict, Tuple
from loguru import logger
import json


class AHPModel:
    """AHP层次分析法模型"""
    
    # 随机一致性指标RI
    RI = {
        1: 0, 2: 0, 3: 0.58, 4: 0.90, 5: 1.12,
        6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49
    }
    
    def __init__(self):
        logger.info("初始化AHP模型")
    
    def create_judgment_matrix(self, n: int, comparisons: Dict[Tuple[int, int], float]) -> np.ndarray:
        """
        创建判断矩阵
        n: 矩阵维度
        comparisons: 比较结果字典 {(i, j): value}
        """
        matrix = np.ones((n, n))
        
        for (i, j), value in comparisons.items():
            matrix[i][j] = value
            matrix[j][i] = 1 / value
        
        return matrix
    
    def calculate_weights(self, matrix: np.ndarray) -> np.ndarray:
        """
        计算权重向量 (特征值法)
        """
        n = matrix.shape[0]
        
        # 计算特征值和特征向量
        eigenvalues, eigenvectors = np.linalg.eig(matrix)
        
        # 找到最大特征值的索引
        max_index = np.argmax(eigenvalues.real)
        max_eigenvalue = eigenvalues[max_index].real
        max_eigenvector = eigenvectors[:, max_index].real
        
        # 归一化得到权重
        weights = max_eigenvector / np.sum(max_eigenvector)
        
        # 保存最大特征值用于一致性检验
        self.lambda_max = max_eigenvalue
        
        return weights
    
    def consistency_check(self, matrix: np.ndarray, weights: np.ndarray) -> Dict:
        """
        一致性检验
        """
        n = matrix.shape[0]
        
        # 计算最大特征值
        lambda_max = self.lambda_max
        
        # 一致性指标CI
        CI = (lambda_max - n) / (n - 1) if n > 1 else 0
        
        # 随机一致性指标RI
        RI = self.RI.get(n, 1.49)
        
        # 一致性比率CR
        CR = CI / RI if RI != 0 else 0
        
        # 判断是否通过一致性检验
        is_consistent = CR < 0.1
        
        result = {
            "lambda_max": lambda_max,
            "CI": CI,
            "RI": RI,
            "CR": CR,
            "is_consistent": is_consistent,
            "interpretation": "通过一致性检验" if is_consistent else "未通过一致性检验，需要调整判断矩阵"
        }
        
        logger.info(f"一致性比率CR: {CR:.4f}, {'通过' if is_consistent else '未通过'}")
        return result
    
    def hierarchical_analysis(self, criteria_matrix: np.ndarray,
                             alternatives_matrices: List[np.ndarray]) -> Dict:
        """
        层次分析
        criteria_matrix: 准则层判断矩阵
        alternatives_matrices: 方案层判断矩阵列表
        """
        logger.info("开始层次分析...")
        
        # 计算准则层权重
        criteria_weights = self.calculate_weights(criteria_matrix)
        criteria_consistency = self.consistency_check(criteria_matrix, criteria_weights)
        
        # 计算方案层权重
        alternatives_weights_list = []
        alternatives_consistency_list = []
        
        for i, alt_matrix in enumerate(alternatives_matrices):
            weights = self.calculate_weights(alt_matrix)
            consistency = self.consistency_check(alt_matrix, weights)
            
            alternatives_weights_list.append(weights)
            alternatives_consistency_list.append(consistency)
        
        # 计算综合权重
        alternatives_weights_array = np.array(alternatives_weights_list).T
        comprehensive_weights = alternatives_weights_array @ criteria_weights
        
        result = {
            "criteria_weights": criteria_weights.tolist(),
            "criteria_consistency": criteria_consistency,
            "alternatives_weights": [w.tolist() for w in alternatives_weights_list],
            "alternatives_consistency": alternatives_consistency_list,
            "comprehensive_weights": comprehensive_weights.tolist()
        }
        
        logger.info("✅ 层次分析完成")
        return result


class FitnessServiceAHP:
    """全民健身公共服务AHP评价"""
    
    def __init__(self):
        self.ahp = AHPModel()
        logger.info("初始化全民健身公共服务AHP评价模型")
    
    def build_evaluation_hierarchy(self) -> Dict:
        """
        构建评价层次结构
        
        目标层: 全民健身公共服务水平
        准则层: 均衡性、可及性、服务质量、参与度
        方案层: 各城市
        """
        hierarchy = {
            "goal": "全民健身公共服务水平",
            "criteria": [
                {"name": "均衡性", "sub_criteria": ["设施分布均衡", "资源投入均衡", "服务项目均衡"]},
                {"name": "可及性", "sub_criteria": ["地理可及性", "时间可及性", "经济可及性"]},
                {"name": "服务质量", "sub_criteria": ["设施质量", "服务水平", "管理水平"]},
                {"name": "参与度", "sub_criteria": ["参与率", "活动频次", "满意度"]}
            ],
            "alternatives": ["石家庄市", "保定市", "唐山市"]
        }
        
        return hierarchy
    
    def evaluate_cities(self) -> Dict:
        """评价各城市全民健身公共服务水平"""
        logger.info("开始评价各城市...")
        
        # 准则层判断矩阵 (均衡性、可及性、服务质量、参与度)
        criteria_comparisons = {
            (0, 1): 1.5,   # 均衡性 vs 可及性
            (0, 2): 2,     # 均衡性 vs 服务质量
            (0, 3): 1.2,   # 均衡性 vs 参与度
            (1, 2): 1.5,   # 可及性 vs 服务质量
            (1, 3): 1.3,   # 可及性 vs 参与度
            (2, 3): 0.8    # 服务质量 vs 参与度
        }
        criteria_matrix = self.ahp.create_judgment_matrix(4, criteria_comparisons)
        
        # 方案层判断矩阵 (3个城市在各准则下的比较)
        
        # 均衡性准则下的城市比较
        balance_comparisons = {
            (0, 1): 1.2,   # 石家庄 vs 保定
            (0, 2): 1.1,   # 石家庄 vs 唐山
            (1, 2): 0.9    # 保定 vs 唐山
        }
        balance_matrix = self.ahp.create_judgment_matrix(3, balance_comparisons)
        
        # 可及性准则下的城市比较
        accessibility_comparisons = {
            (0, 1): 1.3,
            (0, 2): 1.2,
            (1, 2): 0.95
        }
        accessibility_matrix = self.ahp.create_judgment_matrix(3, accessibility_comparisons)
        
        # 服务质量准则下的城市比较
        quality_comparisons = {
            (0, 1): 1.4,
            (0, 2): 1.3,
            (1, 2): 0.9
        }
        quality_matrix = self.ahp.create_judgment_matrix(3, quality_comparisons)
        
        # 参与度准则下的城市比较
        participation_comparisons = {
            (0, 1): 1.1,
            (0, 2): 1.05,
            (1, 2): 0.95
        }
        participation_matrix = self.ahp.create_judgment_matrix(3, participation_comparisons)
        
        # 层次分析
        alternatives_matrices = [
            balance_matrix,
            accessibility_matrix,
            quality_matrix,
            participation_matrix
        ]
        
        result = self.ahp.hierarchical_analysis(criteria_matrix, alternatives_matrices)
        
        # 添加解释
        cities = ["石家庄市", "保定市", "唐山市"]
        criteria = ["均衡性", "可及性", "服务质量", "参与度"]
        
        result["hierarchy"] = self.build_evaluation_hierarchy()
        result["ranking"] = self._generate_ranking(cities, result["comprehensive_weights"])
        result["criteria_names"] = criteria
        result["city_names"] = cities
        
        logger.info("✅ 城市评价完成")
        return result
    
    def _generate_ranking(self, cities: List[str], weights: List[float]) -> List[Dict]:
        """生成排名"""
        ranking = []
        for i, city in enumerate(cities):
            ranking.append({
                "rank": i + 1,
                "city": city,
                "score": weights[i],
                "percentage": f"{weights[i] * 100:.2f}%"
            })
        
        # 按分数排序
        ranking.sort(key=lambda x: x["score"], reverse=True)
        
        # 更新排名
        for i, item in enumerate(ranking):
            item["rank"] = i + 1
        
        return ranking


if __name__ == "__main__":
    # 测试AHP模型
    evaluator = FitnessServiceAHP()
    
    # 评价城市
    result = evaluator.evaluate_cities()
    
    # 保存结果
    with open('data/processed/ahp_evaluation.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    logger.info("✅ AHP评价完成!")
    
    # 打印排名
    print("\n城市排名:")
    for item in result["ranking"]:
        print(f"{item['rank']}. {item['city']}: {item['percentage']}")
