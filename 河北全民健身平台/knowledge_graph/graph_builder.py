"""
时空知识图谱构建模块
"""
from neo4j import GraphDatabase
from typing import List, Dict, Tuple, Optional
from loguru import logger
import json
from datetime import datetime


class Neo4jConnector:
    """Neo4j数据库连接器"""
    
    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        logger.info(f"连接Neo4j数据库: {uri}")
    
    def close(self):
        """关闭连接"""
        self.driver.close()
        logger.info("关闭Neo4j连接")
    
    def execute_query(self, query: str, parameters: Optional[Dict] = None):
        """执行Cypher查询"""
        with self.driver.session() as session:
            result = session.run(query, parameters or {})
            return [record for record in result]


class FitnessKnowledgeGraph:
    """全民健身知识图谱构建器"""
    
    def __init__(self, neo4j_uri: str = "bolt://localhost:7687", 
                 user: str = "neo4j", password: str = "password"):
        self.connector = Neo4jConnector(neo4j_uri, user, password)
        logger.info("初始化全民健身知识图谱构建器")
    
    def create_constraints(self):
        """创建约束和索引"""
        constraints = [
            "CREATE CONSTRAINT IF NOT EXISTS FOR (c:City) REQUIRE c.name IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (f:Facility) REQUIRE f.id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (p:Policy) REQUIRE p.title IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (a:Activity) REQUIRE a.name IS UNIQUE",
            "CREATE INDEX IF NOT EXISTS FOR (f:Facility) ON (f.type)",
            "CREATE INDEX IF NOT EXISTS FOR (c:City) ON (c.province)",
        ]
        
        for constraint in constraints:
            try:
                self.connector.execute_query(constraint)
                logger.info(f"创建约束: {constraint[:50]}...")
            except Exception as e:
                logger.warning(f"约束已存在或创建失败: {e}")
    
    def create_city_nodes(self, cities_data: List[Dict]):
        """创建城市节点"""
        logger.info(f"创建 {len(cities_data)} 个城市节点...")
        
        query = """
        MERGE (c:City {name: $name})
        SET c.province = $province,
            c.total_population = $total_population,
            c.urban_population = $urban_population,
            c.rural_population = $rural_population,
            c.urbanization_rate = $urbanization_rate,
            c.year = $year
        RETURN c
        """
        
        for city in cities_data:
            params = {
                "name": city.get("city", ""),
                "province": "河北省",
                "total_population": city.get("total_population", 0),
                "urban_population": city.get("urban_population", 0),
                "rural_population": city.get("rural_population", 0),
                "urbanization_rate": city.get("urban_population", 0) / city.get("total_population", 1),
                "year": city.get("year", 2024)
            }
            self.connector.execute_query(query, params)
        
        logger.info("✅ 城市节点创建完成")
    
    def create_facility_nodes(self, facilities_data: List[Dict]):
        """创建健身设施节点"""
        logger.info(f"创建 {len(facilities_data)} 个健身设施节点...")
        
        query = """
        MERGE (f:Facility {id: $id})
        SET f.name = $name,
            f.type = $type,
            f.city = $city,
            f.district = $district,
            f.address = $address,
            f.area = $area,
            f.capacity = $capacity,
            f.latitude = $latitude,
            f.longitude = $longitude,
            f.build_year = $build_year,
            f.investment = $investment,
            f.annual_visitors = $annual_visitors,
            f.open_hours = $open_hours
        RETURN f
        """
        
        for facility in facilities_data:
            params = {
                "id": facility.get("id"),
                "name": facility.get("name", ""),
                "type": facility.get("type", ""),
                "city": facility.get("city", ""),
                "district": facility.get("district", ""),
                "address": facility.get("address", ""),
                "area": facility.get("area", 0),
                "capacity": facility.get("capacity", 0),
                "latitude": facility.get("latitude", 0.0),
                "longitude": facility.get("longitude", 0.0),
                "build_year": facility.get("build_year", 2020),
                "investment": facility.get("investment", 0),
                "annual_visitors": facility.get("annual_visitors", 0),
                "open_hours": facility.get("open_hours", "")
            }
            self.connector.execute_query(query, params)
        
        logger.info("✅ 健身设施节点创建完成")
    
    def create_activity_nodes(self, activities: List[str]):
        """创建运动项目节点"""
        logger.info(f"创建 {len(activities)} 个运动项目节点...")
        
        query = """
        MERGE (a:Activity {name: $name})
        SET a.category = $category
        RETURN a
        """
        
        # 运动项目分类
        activity_categories = {
            "跑步": "有氧运动", "健走": "有氧运动", "游泳": "有氧运动",
            "篮球": "球类运动", "足球": "球类运动", "羽毛球": "球类运动", "乒乓球": "球类运动",
            "瑜伽": "柔韧性训练", "太极拳": "传统运动", "广场舞": "群众运动",
            "健身": "力量训练"
        }
        
        for activity in activities:
            params = {
                "name": activity,
                "category": activity_categories.get(activity, "其他运动")
            }
            self.connector.execute_query(query, params)
        
        logger.info("✅ 运动项目节点创建完成")
    
    def create_policy_nodes(self, policies_data: List[Dict]):
        """创建政策节点"""
        logger.info(f"创建 {len(policies_data)} 个政策节点...")
        
        query = """
        MERGE (p:Policy {title: $title})
        SET p.level = $level,
            p.department = $department,
            p.publish_date = $publish_date,
            p.effective_date = $effective_date,
            p.url = $url
        RETURN p
        """
        
        for policy in policies_data:
            params = {
                "title": policy.get("title", ""),
                "level": policy.get("level", ""),
                "department": policy.get("department", ""),
                "publish_date": policy.get("publish_date", ""),
                "effective_date": policy.get("effective_date", ""),
                "url": policy.get("url", "")
            }
            self.connector.execute_query(query, params)
        
        logger.info("✅ 政策节点创建完成")
    
    def create_relationships(self):
        """创建关系"""
        logger.info("创建节点间关系...")
        
        # 设施属于城市
        query1 = """
        MATCH (f:Facility), (c:City)
        WHERE f.city = c.name
        MERGE (f)-[:LOCATED_IN]->(c)
        """
        self.connector.execute_query(query1)
        logger.info("✅ 创建设施-城市关系")
        
        # 设施提供活动
        query2 = """
        MATCH (f:Facility), (a:Activity)
        WHERE a.name IN ['篮球', '羽毛球', '游泳', '健身']
        MERGE (f)-[:PROVIDES]->(a)
        """
        self.connector.execute_query(query2)
        logger.info("✅ 创建设施-活动关系")
        
        # 政策影响城市
        query3 = """
        MATCH (p:Policy), (c:City)
        WHERE p.level = '省级'
        MERGE (p)-[:AFFECTS]->(c)
        """
        self.connector.execute_query(query3)
        logger.info("✅ 创建政策-城市关系")
    
    def query_city_facilities(self, city_name: str) -> List[Dict]:
        """查询城市的健身设施"""
        query = """
        MATCH (c:City {name: $city_name})<-[:LOCATED_IN]-(f:Facility)
        RETURN f.name as name, f.type as type, f.area as area, f.capacity as capacity
        ORDER BY f.area DESC
        """
        
        results = self.connector.execute_query(query, {"city_name": city_name})
        facilities = [dict(record) for record in results]
        logger.info(f"查询到 {len(facilities)} 个设施")
        return facilities
    
    def query_facility_activities(self, facility_name: str) -> List[str]:
        """查询设施提供的运动项目"""
        query = """
        MATCH (f:Facility {name: $facility_name})-[:PROVIDES]->(a:Activity)
        RETURN a.name as activity
        """
        
        results = self.connector.execute_query(query, {"facility_name": facility_name})
        activities = [record["activity"] for record in results]
        return activities
    
    def get_graph_statistics(self) -> Dict:
        """获取图谱统计信息"""
        stats = {}
        
        # 节点统计
        node_query = """
        MATCH (n)
        RETURN labels(n)[0] as label, count(n) as count
        """
        node_results = self.connector.execute_query(node_query)
        stats["nodes"] = {record["label"]: record["count"] for record in node_results}
        
        # 关系统计
        rel_query = """
        MATCH ()-[r]->()
        RETURN type(r) as type, count(r) as count
        """
        rel_results = self.connector.execute_query(rel_query)
        stats["relationships"] = {record["type"]: record["count"] for record in rel_results}
        
        logger.info(f"图谱统计: {stats}")
        return stats
    
    def close(self):
        """关闭连接"""
        self.connector.close()


class KnowledgeGraphBuilder:
    """知识图谱构建流程"""
    
    def __init__(self):
        self.kg = FitnessKnowledgeGraph()
    
    def build_from_data(self, data_dir: str = "data/raw"):
        """从数据文件构建知识图谱"""
        logger.info("开始构建知识图谱...")
        
        # 创建约束
        self.kg.create_constraints()
        
        # 加载数据
        with open(f"{data_dir}/population.json", 'r', encoding='utf-8') as f:
            population_data = json.load(f)
        
        with open(f"{data_dir}/facilities.json", 'r', encoding='utf-8') as f:
            facilities_data = json.load(f)
        
        with open(f"{data_dir}/policies.json", 'r', encoding='utf-8') as f:
            policies_data = json.load(f)
        
        # 创建节点
        self.kg.create_city_nodes(population_data)
        self.kg.create_facility_nodes(facilities_data)
        
        # 提取所有运动项目
        all_activities = set()
        for facility in facilities_data:
            all_activities.update(facility.get("facilities", []))
        self.kg.create_activity_nodes(list(all_activities))
        
        self.kg.create_policy_nodes(policies_data)
        
        # 创建关系
        self.kg.create_relationships()
        
        # 统计信息
        stats = self.kg.get_graph_statistics()
        
        logger.info("🎉 知识图谱构建完成!")
        logger.info(f"节点数: {sum(stats['nodes'].values())}")
        logger.info(f"关系数: {sum(stats['relationships'].values())}")
        
        return stats


if __name__ == "__main__":
    builder = KnowledgeGraphBuilder()
    
    # 构建知识图谱
    stats = builder.build_from_data()
    
    # 测试查询
    facilities = builder.kg.query_city_facilities("石家庄市")
    logger.info(f"石家庄市设施: {facilities}")
    
    # 关闭连接
    builder.kg.close()
