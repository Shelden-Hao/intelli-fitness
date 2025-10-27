"""
深度学习推荐模型
基于神经网络的协同过滤推荐系统
"""
import numpy as np
from typing import List, Dict, Tuple
import json
from loguru import logger


class NeuralCollaborativeFiltering:
    """神经协同过滤模型"""
    
    def __init__(self, num_users: int, num_items: int, 
                 embedding_dim: int = 32, hidden_layers: List[int] = [64, 32, 16]):
        """
        初始化NCF模型
        
        Args:
            num_users: 用户数量
            num_items: 项目数量
            embedding_dim: 嵌入维度
            hidden_layers: 隐藏层维度列表
        """
        self.num_users = num_users
        self.num_items = num_items
        self.embedding_dim = embedding_dim
        self.hidden_layers = hidden_layers
        
        # 初始化参数
        self._initialize_weights()
        
        logger.info(f"初始化NCF模型: users={num_users}, items={num_items}, emb_dim={embedding_dim}")
    
    def _initialize_weights(self):
        """初始化模型权重"""
        # 用户和项目嵌入
        self.user_embedding = np.random.randn(self.num_users, self.embedding_dim) * 0.01
        self.item_embedding = np.random.randn(self.num_items, self.embedding_dim) * 0.01
        
        # MLP层权重
        self.mlp_weights = []
        self.mlp_biases = []
        
        input_dim = self.embedding_dim * 2
        for hidden_dim in self.hidden_layers:
            weight = np.random.randn(input_dim, hidden_dim) * np.sqrt(2.0 / input_dim)
            bias = np.zeros(hidden_dim)
            self.mlp_weights.append(weight)
            self.mlp_biases.append(bias)
            input_dim = hidden_dim
        
        # 输出层
        self.output_weight = np.random.randn(self.hidden_layers[-1], 1) * 0.01
        self.output_bias = np.zeros(1)
    
    def _relu(self, x: np.ndarray) -> np.ndarray:
        """ReLU激活函数"""
        return np.maximum(0, x)
    
    def _sigmoid(self, x: np.ndarray) -> np.ndarray:
        """Sigmoid激活函数"""
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))
    
    def forward(self, user_id: int, item_id: int) -> float:
        """前向传播"""
        # 获取嵌入
        user_emb = self.user_embedding[user_id]
        item_emb = self.item_embedding[item_id]
        
        # 拼接嵌入
        x = np.concatenate([user_emb, item_emb])
        
        # MLP层
        for i, (weight, bias) in enumerate(zip(self.mlp_weights, self.mlp_biases)):
            x = np.dot(x, weight) + bias
            x = self._relu(x)
        
        # 输出层
        output = np.dot(x, self.output_weight) + self.output_bias
        prediction = self._sigmoid(output[0])
        
        return prediction
    
    def train(self, interactions: List[Tuple[int, int, float]], 
              epochs: int = 10, learning_rate: float = 0.001, batch_size: int = 256):
        """
        训练模型
        
        Args:
            interactions: [(user_id, item_id, rating), ...]
            epochs: 训练轮数
            learning_rate: 学习率
            batch_size: 批次大小
        """
        logger.info(f"开始训练: {len(interactions)}个交互, {epochs}轮")
        
        for epoch in range(epochs):
            np.random.shuffle(interactions)
            total_loss = 0
            
            for i in range(0, len(interactions), batch_size):
                batch = interactions[i:i+batch_size]
                loss = self._train_batch(batch, learning_rate)
                total_loss += loss
            
            avg_loss = total_loss / len(interactions)
            if (epoch + 1) % 2 == 0:
                logger.info(f"Epoch {epoch+1}/{epochs}, Loss: {avg_loss:.4f}")
        
        logger.info("训练完成")
    
    def _train_batch(self, batch: List[Tuple[int, int, float]], learning_rate: float) -> float:
        """训练一个批次（简化版梯度下降）"""
        batch_loss = 0
        
        for user_id, item_id, rating in batch:
            # 前向传播
            prediction = self.forward(user_id, item_id)
            
            # 计算损失（MSE）
            loss = (prediction - rating) ** 2
            batch_loss += loss
            
            # 简化的梯度更新（实际应该用反向传播）
            error = prediction - rating
            
            # 更新嵌入（简化版）
            self.user_embedding[user_id] -= learning_rate * error * 0.01
            self.item_embedding[item_id] -= learning_rate * error * 0.01
        
        return batch_loss
    
    def predict(self, user_id: int, item_ids: List[int]) -> List[Tuple[int, float]]:
        """
        预测用户对多个项目的评分
        
        Args:
            user_id: 用户ID
            item_ids: 项目ID列表
        
        Returns:
            [(item_id, score), ...] 按分数排序
        """
        predictions = []
        for item_id in item_ids:
            score = self.forward(user_id, item_id)
            predictions.append((item_id, float(score)))
        
        predictions.sort(key=lambda x: x[1], reverse=True)
        return predictions
    
    def recommend(self, user_id: int, top_k: int = 10, 
                  exclude_items: List[int] = None) -> List[Tuple[int, float]]:
        """
        为用户推荐项目
        
        Args:
            user_id: 用户ID
            top_k: 推荐数量
            exclude_items: 要排除的项目ID列表
        
        Returns:
            [(item_id, score), ...] 推荐列表
        """
        if exclude_items is None:
            exclude_items = []
        
        # 对所有项目进行预测
        all_items = [i for i in range(self.num_items) if i not in exclude_items]
        predictions = self.predict(user_id, all_items)
        
        return predictions[:top_k]
    
    def save(self, filepath: str):
        """保存模型"""
        model_data = {
            'user_embedding': self.user_embedding.tolist(),
            'item_embedding': self.item_embedding.tolist(),
            'mlp_weights': [w.tolist() for w in self.mlp_weights],
            'mlp_biases': [b.tolist() for b in self.mlp_biases],
            'output_weight': self.output_weight.tolist(),
            'output_bias': self.output_bias.tolist(),
            'config': {
                'num_users': self.num_users,
                'num_items': self.num_items,
                'embedding_dim': self.embedding_dim,
                'hidden_layers': self.hidden_layers
            }
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(model_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"模型已保存到: {filepath}")
    
    def load(self, filepath: str):
        """加载模型"""
        with open(filepath, 'r', encoding='utf-8') as f:
            model_data = json.load(f)
        
        self.user_embedding = np.array(model_data['user_embedding'])
        self.item_embedding = np.array(model_data['item_embedding'])
        self.mlp_weights = [np.array(w) for w in model_data['mlp_weights']]
        self.mlp_biases = [np.array(b) for b in model_data['mlp_biases']]
        self.output_weight = np.array(model_data['output_weight'])
        self.output_bias = np.array(model_data['output_bias'])
        
        config = model_data['config']
        self.num_users = config['num_users']
        self.num_items = config['num_items']
        self.embedding_dim = config['embedding_dim']
        self.hidden_layers = config['hidden_layers']
        
        logger.info(f"模型已从{filepath}加载")


class MatrixFactorization:
    """矩阵分解推荐模型（简化版）"""
    
    def __init__(self, num_users: int, num_items: int, num_factors: int = 20):
        """
        初始化矩阵分解模型
        
        Args:
            num_users: 用户数量
            num_items: 项目数量
            num_factors: 隐因子数量
        """
        self.num_users = num_users
        self.num_items = num_items
        self.num_factors = num_factors
        
        # 初始化用户和项目因子矩阵
        self.user_factors = np.random.randn(num_users, num_factors) * 0.01
        self.item_factors = np.random.randn(num_items, num_factors) * 0.01
        
        logger.info(f"初始化MF模型: users={num_users}, items={num_items}, factors={num_factors}")
    
    def predict(self, user_id: int, item_id: int) -> float:
        """预测评分"""
        return np.dot(self.user_factors[user_id], self.item_factors[item_id])
    
    def train(self, interactions: List[Tuple[int, int, float]], 
              epochs: int = 20, learning_rate: float = 0.01, reg: float = 0.01):
        """
        训练模型（使用SGD）
        
        Args:
            interactions: [(user_id, item_id, rating), ...]
            epochs: 训练轮数
            learning_rate: 学习率
            reg: 正则化系数
        """
        logger.info(f"开始训练MF: {len(interactions)}个交互, {epochs}轮")
        
        for epoch in range(epochs):
            np.random.shuffle(interactions)
            total_loss = 0
            
            for user_id, item_id, rating in interactions:
                # 预测
                prediction = self.predict(user_id, item_id)
                error = rating - prediction
                
                # 更新因子
                user_factor = self.user_factors[user_id].copy()
                item_factor = self.item_factors[item_id].copy()
                
                self.user_factors[user_id] += learning_rate * (
                    error * item_factor - reg * user_factor
                )
                self.item_factors[item_id] += learning_rate * (
                    error * user_factor - reg * item_factor
                )
                
                total_loss += error ** 2
            
            if (epoch + 1) % 5 == 0:
                avg_loss = total_loss / len(interactions)
                logger.info(f"Epoch {epoch+1}/{epochs}, Loss: {avg_loss:.4f}")
        
        logger.info("训练完成")
    
    def recommend(self, user_id: int, top_k: int = 10) -> List[Tuple[int, float]]:
        """推荐项目"""
        scores = []
        for item_id in range(self.num_items):
            score = self.predict(user_id, item_id)
            scores.append((item_id, float(score)))
        
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]


if __name__ == "__main__":
    # 示例：训练推荐模型
    
    # 生成模拟数据
    num_users = 100
    num_items = 50
    
    # 生成交互数据
    interactions = []
    for _ in range(1000):
        user_id = np.random.randint(0, num_users)
        item_id = np.random.randint(0, num_items)
        rating = np.random.uniform(0.5, 1.0)  # 归一化评分
        interactions.append((user_id, item_id, rating))
    
    # 训练NCF模型
    logger.info("=" * 60)
    logger.info("训练神经协同过滤模型")
    logger.info("=" * 60)
    ncf_model = NeuralCollaborativeFiltering(
        num_users=num_users,
        num_items=num_items,
        embedding_dim=32,
        hidden_layers=[64, 32, 16]
    )
    ncf_model.train(interactions, epochs=10, learning_rate=0.001)
    
    # 推荐
    recommendations = ncf_model.recommend(user_id=0, top_k=5)
    print("\nNCF推荐结果 (用户0):")
    for item_id, score in recommendations:
        print(f"  项目{item_id}: {score:.4f}")
    
    # 保存模型
    ncf_model.save('ml_models/saved_models/ncf_model.json')
    
    # 训练MF模型
    logger.info("\n" + "=" * 60)
    logger.info("训练矩阵分解模型")
    logger.info("=" * 60)
    mf_model = MatrixFactorization(num_users=num_users, num_items=num_items, num_factors=20)
    mf_model.train(interactions, epochs=20, learning_rate=0.01, reg=0.01)
    
    # 推荐
    recommendations = mf_model.recommend(user_id=0, top_k=5)
    print("\nMF推荐结果 (用户0):")
    for item_id, score in recommendations:
        print(f"  项目{item_id}: {score:.4f}")
    
    logger.info("\n✅ 推荐模型训练完成!")
