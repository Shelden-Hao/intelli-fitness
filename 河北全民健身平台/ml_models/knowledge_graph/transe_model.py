"""
TransE知识图谱补全模型
Translation-based Embedding for Knowledge Graph Completion
"""
import numpy as np
from typing import List, Tuple, Dict
import json
from loguru import logger


class TransE:
    """TransE模型实现"""
    
    def __init__(self, entity_dim: int = 50, relation_dim: int = 50, 
                 learning_rate: float = 0.01, margin: float = 1.0):
        """
        初始化TransE模型
        
        Args:
            entity_dim: 实体向量维度
            relation_dim: 关系向量维度
            learning_rate: 学习率
            margin: margin-based ranking loss的margin值
        """
        self.entity_dim = entity_dim
        self.relation_dim = relation_dim
        self.learning_rate = learning_rate
        self.margin = margin
        
        self.entity_embeddings = {}
        self.relation_embeddings = {}
        self.entity2id = {}
        self.relation2id = {}
        self.id2entity = {}
        self.id2relation = {}
        
        logger.info(f"初始化TransE模型: entity_dim={entity_dim}, relation_dim={relation_dim}")
    
    def initialize_embeddings(self, entities: List[str], relations: List[str]):
        """初始化实体和关系的嵌入向量"""
        # 构建实体和关系的ID映射
        for i, entity in enumerate(entities):
            self.entity2id[entity] = i
            self.id2entity[i] = entity
        
        for i, relation in enumerate(relations):
            self.relation2id[relation] = i
            self.id2relation[i] = relation
        
        # 随机初始化嵌入向量
        num_entities = len(entities)
        num_relations = len(relations)
        
        self.entity_embeddings = np.random.uniform(
            -6/np.sqrt(self.entity_dim), 
            6/np.sqrt(self.entity_dim),
            (num_entities, self.entity_dim)
        )
        
        self.relation_embeddings = np.random.uniform(
            -6/np.sqrt(self.relation_dim),
            6/np.sqrt(self.relation_dim),
            (num_relations, self.relation_dim)
        )
        
        # L2归一化
        self.entity_embeddings = self._normalize(self.entity_embeddings)
        self.relation_embeddings = self._normalize(self.relation_embeddings)
        
        logger.info(f"初始化完成: {num_entities}个实体, {num_relations}个关系")
    
    def _normalize(self, vectors: np.ndarray) -> np.ndarray:
        """L2归一化"""
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        return vectors / (norms + 1e-10)
    
    def _distance(self, h: np.ndarray, r: np.ndarray, t: np.ndarray) -> float:
        """计算距离: ||h + r - t||"""
        return np.linalg.norm(h + r - t)
    
    def train(self, triples: List[Tuple[str, str, str]], epochs: int = 100, batch_size: int = 128):
        """
        训练TransE模型
        
        Args:
            triples: 三元组列表 [(head, relation, tail), ...]
            epochs: 训练轮数
            batch_size: 批次大小
        """
        logger.info(f"开始训练: {len(triples)}个三元组, {epochs}轮")
        
        for epoch in range(epochs):
            np.random.shuffle(triples)
            total_loss = 0
            
            for i in range(0, len(triples), batch_size):
                batch = triples[i:i+batch_size]
                loss = self._train_batch(batch)
                total_loss += loss
            
            if (epoch + 1) % 10 == 0:
                avg_loss = total_loss / len(triples)
                logger.info(f"Epoch {epoch+1}/{epochs}, Loss: {avg_loss:.4f}")
        
        logger.info("训练完成")
    
    def _train_batch(self, batch: List[Tuple[str, str, str]]) -> float:
        """训练一个批次"""
        batch_loss = 0
        
        for (h, r, t) in batch:
            # 获取正样本的嵌入
            h_id = self.entity2id[h]
            r_id = self.relation2id[r]
            t_id = self.entity2id[t]
            
            h_emb = self.entity_embeddings[h_id]
            r_emb = self.relation_embeddings[r_id]
            t_emb = self.entity_embeddings[t_id]
            
            # 生成负样本（替换头实体或尾实体）
            if np.random.random() < 0.5:
                # 替换头实体
                neg_h_id = np.random.randint(0, len(self.entity2id))
                neg_h_emb = self.entity_embeddings[neg_h_id]
                neg_t_emb = t_emb
            else:
                # 替换尾实体
                neg_h_emb = h_emb
                neg_t_id = np.random.randint(0, len(self.entity2id))
                neg_t_emb = self.entity_embeddings[neg_t_id]
            
            # 计算距离
            pos_distance = self._distance(h_emb, r_emb, t_emb)
            neg_distance = self._distance(neg_h_emb, r_emb, neg_t_emb)
            
            # Margin-based ranking loss
            loss = max(0, self.margin + pos_distance - neg_distance)
            batch_loss += loss
            
            if loss > 0:
                # 更新梯度
                grad_pos = 2 * (h_emb + r_emb - t_emb)
                grad_neg = 2 * (neg_h_emb + r_emb - neg_t_emb)
                
                # 更新嵌入
                self.entity_embeddings[h_id] -= self.learning_rate * grad_pos
                self.relation_embeddings[r_id] -= self.learning_rate * grad_pos
                self.entity_embeddings[t_id] += self.learning_rate * grad_pos
                
                if np.random.random() < 0.5:
                    self.entity_embeddings[neg_h_id] += self.learning_rate * grad_neg
                else:
                    self.entity_embeddings[neg_t_id] -= self.learning_rate * grad_neg
                
                # 重新归一化
                self.entity_embeddings = self._normalize(self.entity_embeddings)
                self.relation_embeddings = self._normalize(self.relation_embeddings)
        
        return batch_loss
    
    def predict(self, head: str, relation: str, top_k: int = 10) -> List[Tuple[str, float]]:
        """
        预测尾实体
        
        Args:
            head: 头实体
            relation: 关系
            top_k: 返回top-k个候选
        
        Returns:
            [(entity, score), ...] 按分数排序
        """
        h_id = self.entity2id.get(head)
        r_id = self.relation2id.get(relation)
        
        if h_id is None or r_id is None:
            return []
        
        h_emb = self.entity_embeddings[h_id]
        r_emb = self.relation_embeddings[r_id]
        
        # 计算与所有实体的距离
        scores = []
        for t_id, t_name in self.id2entity.items():
            t_emb = self.entity_embeddings[t_id]
            distance = self._distance(h_emb, r_emb, t_emb)
            scores.append((t_name, -distance))  # 负距离作为分数
        
        # 排序并返回top-k
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]
    
    def save(self, filepath: str):
        """保存模型"""
        model_data = {
            'entity_embeddings': self.entity_embeddings.tolist(),
            'relation_embeddings': self.relation_embeddings.tolist(),
            'entity2id': self.entity2id,
            'relation2id': self.relation2id,
            'id2entity': self.id2entity,
            'id2relation': self.id2relation,
            'config': {
                'entity_dim': self.entity_dim,
                'relation_dim': self.relation_dim,
                'learning_rate': self.learning_rate,
                'margin': self.margin
            }
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(model_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"模型已保存到: {filepath}")
    
    def load(self, filepath: str):
        """加载模型"""
        with open(filepath, 'r', encoding='utf-8') as f:
            model_data = json.load(f)
        
        self.entity_embeddings = np.array(model_data['entity_embeddings'])
        self.relation_embeddings = np.array(model_data['relation_embeddings'])
        self.entity2id = model_data['entity2id']
        self.relation2id = model_data['relation2id']
        self.id2entity = {int(k): v for k, v in model_data['id2entity'].items()}
        self.id2relation = {int(k): v for k, v in model_data['id2relation'].items()}
        
        config = model_data['config']
        self.entity_dim = config['entity_dim']
        self.relation_dim = config['relation_dim']
        self.learning_rate = config['learning_rate']
        self.margin = config['margin']
        
        logger.info(f"模型已从{filepath}加载")


if __name__ == "__main__":
    # 示例：训练TransE模型
    
    # 定义实体和关系
    entities = [
        "石家庄市", "保定市", "唐山市",
        "石家庄市体育馆", "保定市健身中心", "唐山市体育公园",
        "篮球", "游泳", "跑步", "健身"
    ]
    
    relations = [
        "HAS_FACILITY",  # 城市拥有设施
        "PROVIDES",      # 设施提供活动
        "LOCATED_IN"     # 设施位于城市
    ]
    
    # 定义三元组
    triples = [
        ("石家庄市", "HAS_FACILITY", "石家庄市体育馆"),
        ("保定市", "HAS_FACILITY", "保定市健身中心"),
        ("唐山市", "HAS_FACILITY", "唐山市体育公园"),
        ("石家庄市体育馆", "PROVIDES", "篮球"),
        ("石家庄市体育馆", "PROVIDES", "游泳"),
        ("保定市健身中心", "PROVIDES", "健身"),
        ("唐山市体育公园", "PROVIDES", "跑步"),
        ("石家庄市体育馆", "LOCATED_IN", "石家庄市"),
        ("保定市健身中心", "LOCATED_IN", "保定市"),
        ("唐山市体育公园", "LOCATED_IN", "唐山市"),
    ]
    
    # 创建并训练模型
    model = TransE(entity_dim=50, relation_dim=50, learning_rate=0.01, margin=1.0)
    model.initialize_embeddings(entities, relations)
    model.train(triples, epochs=100, batch_size=5)
    
    # 预测
    predictions = model.predict("石家庄市", "HAS_FACILITY", top_k=3)
    print("\n预测结果:")
    print("石家庄市 HAS_FACILITY ?")
    for entity, score in predictions:
        print(f"  {entity}: {score:.4f}")
    
    # 保存模型
    model.save('ml_models/saved_models/transe_model.json')
    
    logger.info("✅ TransE模型训练完成!")
