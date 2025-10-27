"""
协同过滤推荐系统
"""
import numpy as np
import pandas as pd
from typing import List, Dict, Tuple
from loguru import logger
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix
import json


class CollaborativeFilteringRecommender:
    """协同过滤推荐器"""
    
    def __init__(self):
        self.user_item_matrix = None
        self.user_similarity = None
        self.item_similarity = None
        logger.info("初始化协同过滤推荐器")
    
    def build_user_item_matrix(self, interactions: List[Dict]) -> pd.DataFrame:
        """
        构建用户-项目评分矩阵
        interactions: [{"user_id": 1, "item_id": 1, "rating": 5}, ...]
        """
        df = pd.DataFrame(interactions)
        matrix = df.pivot_table(
            index='user_id',
            columns='item_id',
            values='rating',
            fill_value=0
        )
        
        self.user_item_matrix = matrix
        logger.info(f"用户-项目矩阵: {matrix.shape}")
        return matrix
    
    def calculate_user_similarity(self, method: str = 'cosine') -> np.ndarray:
        """计算用户相似度"""
        if self.user_item_matrix is None:
            raise ValueError("请先构建用户-项目矩阵")
        
        if method == 'cosine':
            similarity = cosine_similarity(self.user_item_matrix)
        elif method == 'pearson':
            similarity = np.corrcoef(self.user_item_matrix)
        else:
            raise ValueError(f"未知的相似度计算方法: {method}")
        
        self.user_similarity = similarity
        logger.info(f"用户相似度矩阵: {similarity.shape}")
        return similarity
    
    def calculate_item_similarity(self, method: str = 'cosine') -> np.ndarray:
        """计算项目相似度"""
        if self.user_item_matrix is None:
            raise ValueError("请先构建用户-项目矩阵")
        
        if method == 'cosine':
            similarity = cosine_similarity(self.user_item_matrix.T)
        elif method == 'pearson':
            similarity = np.corrcoef(self.user_item_matrix.T)
        else:
            raise ValueError(f"未知的相似度计算方法: {method}")
        
        self.item_similarity = similarity
        logger.info(f"项目相似度矩阵: {similarity.shape}")
        return similarity
    
    def user_based_recommend(self, user_id: int, top_n: int = 10) -> List[Tuple[int, float]]:
        """基于用户的协同过滤推荐"""
        if self.user_similarity is None:
            self.calculate_user_similarity()
        
        # 获取用户索引
        user_idx = self.user_item_matrix.index.get_loc(user_id)
        
        # 获取相似用户
        similar_users = self.user_similarity[user_idx]
        
        # 获取用户未评分的项目
        user_ratings = self.user_item_matrix.iloc[user_idx]
        unrated_items = user_ratings[user_ratings == 0].index
        
        # 预测评分
        predictions = []
        for item_id in unrated_items:
            item_idx = self.user_item_matrix.columns.get_loc(item_id)
            
            # 加权平均
            numerator = 0
            denominator = 0
            
            for other_user_idx, similarity in enumerate(similar_users):
                if other_user_idx != user_idx and similarity > 0:
                    other_rating = self.user_item_matrix.iloc[other_user_idx, item_idx]
                    if other_rating > 0:
                        numerator += similarity * other_rating
                        denominator += abs(similarity)
            
            if denominator > 0:
                predicted_rating = numerator / denominator
                predictions.append((item_id, predicted_rating))
        
        # 排序并返回Top-N
        predictions.sort(key=lambda x: x[1], reverse=True)
        
        logger.info(f"为用户 {user_id} 生成 {len(predictions[:top_n])} 个推荐")
        return predictions[:top_n]
    
    def item_based_recommend(self, user_id: int, top_n: int = 10) -> List[Tuple[int, float]]:
        """基于项目的协同过滤推荐"""
        if self.item_similarity is None:
            self.calculate_item_similarity()
        
        # 获取用户索引
        user_idx = self.user_item_matrix.index.get_loc(user_id)
        
        # 获取用户已评分的项目
        user_ratings = self.user_item_matrix.iloc[user_idx]
        rated_items = user_ratings[user_ratings > 0]
        
        # 获取未评分的项目
        unrated_items = user_ratings[user_ratings == 0].index
        
        # 预测评分
        predictions = []
        for item_id in unrated_items:
            item_idx = self.user_item_matrix.columns.get_loc(item_id)
            
            # 基于相似项目计算预测评分
            numerator = 0
            denominator = 0
            
            for rated_item_id, rating in rated_items.items():
                rated_item_idx = self.user_item_matrix.columns.get_loc(rated_item_id)
                similarity = self.item_similarity[item_idx, rated_item_idx]
                
                if similarity > 0:
                    numerator += similarity * rating
                    denominator += abs(similarity)
            
            if denominator > 0:
                predicted_rating = numerator / denominator
                predictions.append((item_id, predicted_rating))
        
        # 排序并返回Top-N
        predictions.sort(key=lambda x: x[1], reverse=True)
        
        logger.info(f"为用户 {user_id} 生成 {len(predictions[:top_n])} 个推荐")
        return predictions[:top_n]


class FitnessActivityRecommender:
    """健身活动推荐系统"""
    
    def __init__(self):
        self.cf_recommender = CollaborativeFilteringRecommender()
        self.activities = self._load_activities()
        logger.info("初始化健身活动推荐系统")
    
    def _load_activities(self) -> Dict[int, Dict]:
        """加载健身活动数据"""
        activities = {
            1: {"name": "跑步", "category": "有氧运动", "intensity": "中等", "duration": 30},
            2: {"name": "游泳", "category": "有氧运动", "intensity": "中等", "duration": 45},
            3: {"name": "篮球", "category": "球类运动", "intensity": "高", "duration": 60},
            4: {"name": "瑜伽", "category": "柔韧性训练", "intensity": "低", "duration": 60},
            5: {"name": "健身房", "category": "力量训练", "intensity": "高", "duration": 60},
            6: {"name": "羽毛球", "category": "球类运动", "intensity": "中等", "duration": 45},
            7: {"name": "太极拳", "category": "传统运动", "intensity": "低", "duration": 30},
            8: {"name": "广场舞", "category": "群众运动", "intensity": "低", "duration": 45},
            9: {"name": "乒乓球", "category": "球类运动", "intensity": "中等", "duration": 45},
            10: {"name": "健走", "category": "有氧运动", "intensity": "低", "duration": 30}
        }
        return activities
    
    def generate_sample_interactions(self, num_users: int = 50, 
                                    num_interactions: int = 200) -> List[Dict]:
        """生成示例交互数据"""
        interactions = []
        
        for _ in range(num_interactions):
            user_id = np.random.randint(1, num_users + 1)
            activity_id = np.random.randint(1, len(self.activities) + 1)
            rating = np.random.randint(1, 6)  # 1-5分
            
            interactions.append({
                "user_id": user_id,
                "item_id": activity_id,
                "rating": rating
            })
        
        logger.info(f"生成 {len(interactions)} 条交互数据")
        return interactions
    
    def recommend_activities(self, user_id: int, method: str = 'item_based', 
                           top_n: int = 5) -> List[Dict]:
        """推荐健身活动"""
        logger.info(f"为用户 {user_id} 推荐活动 (方法: {method})...")
        
        # 获取推荐
        if method == 'user_based':
            recommendations = self.cf_recommender.user_based_recommend(user_id, top_n)
        elif method == 'item_based':
            recommendations = self.cf_recommender.item_based_recommend(user_id, top_n)
        else:
            raise ValueError(f"未知的推荐方法: {method}")
        
        # 添加活动详情
        detailed_recommendations = []
        for activity_id, score in recommendations:
            activity = self.activities.get(activity_id, {})
            detailed_recommendations.append({
                "activity_id": activity_id,
                "activity_name": activity.get("name", "未知"),
                "category": activity.get("category", ""),
                "intensity": activity.get("intensity", ""),
                "duration": activity.get("duration", 0),
                "recommendation_score": score,
                "reason": self._generate_reason(activity, score)
            })
        
        logger.info(f"✅ 生成 {len(detailed_recommendations)} 个推荐")
        return detailed_recommendations
    
    def _generate_reason(self, activity: Dict, score: float) -> str:
        """生成推荐理由"""
        reasons = [
            f"根据您的运动偏好,推荐{activity.get('name')}",
            f"与您喜欢的活动相似,{activity.get('name')}也很适合您",
            f"许多和您相似的用户都喜欢{activity.get('name')}",
            f"{activity.get('name')}是{activity.get('category')},符合您的运动需求"
        ]
        
        return np.random.choice(reasons)
    
    def recommend_by_user_profile(self, user_profile: Dict) -> List[Dict]:
        """基于用户画像推荐"""
        age = user_profile.get('age', 30)
        fitness_level = user_profile.get('fitness_level', 'medium')  # low, medium, high
        preferences = user_profile.get('preferences', [])
        
        recommendations = []
        
        # 根据年龄推荐
        if age < 30:
            intensity_preference = ['高', '中等']
        elif age < 50:
            intensity_preference = ['中等', '低']
        else:
            intensity_preference = ['低', '中等']
        
        # 筛选活动
        for activity_id, activity in self.activities.items():
            score = 0
            
            # 强度匹配
            if activity['intensity'] in intensity_preference:
                score += 30
            
            # 类别偏好
            if activity['category'] in preferences:
                score += 40
            
            # 健身水平匹配
            if fitness_level == 'high' and activity['intensity'] == '高':
                score += 20
            elif fitness_level == 'medium' and activity['intensity'] == '中等':
                score += 20
            elif fitness_level == 'low' and activity['intensity'] == '低':
                score += 20
            
            if score > 0:
                recommendations.append({
                    **activity,
                    "activity_id": activity_id,
                    "activity_name": activity['name'],
                    "score": score
                })
        
        # 排序
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        
        logger.info(f"基于用户画像生成 {len(recommendations)} 个推荐")
        return recommendations[:5]


if __name__ == "__main__":
    # 测试推荐系统
    recommender = FitnessActivityRecommender()
    
    # 生成示例数据
    interactions = recommender.generate_sample_interactions()
    
    # 构建矩阵
    recommender.cf_recommender.build_user_item_matrix(interactions)
    
    # 计算相似度
    recommender.cf_recommender.calculate_item_similarity()
    
    # 推荐活动
    recommendations = recommender.recommend_activities(user_id=1, method='item_based', top_n=5)
    
    # 保存结果
    with open('data/processed/recommendations.json', 'w', encoding='utf-8') as f:
        json.dump(recommendations, f, ensure_ascii=False, indent=2)
    
    logger.info("✅ 推荐系统测试完成!")
    print("\n推荐结果:")
    for rec in recommendations:
        print(f"- {rec['activity_name']} ({rec['category']}) - 评分: {rec['recommendation_score']:.2f}")
