"""
配置文件
"""
from typing import List


class Settings:
    """应用配置"""
    
    # 基础配置
    PROJECT_NAME: str = "河北全民健身公共服务体系平台"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8001
    
    # CORS配置
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ]
    
    # 数据库配置
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "hebei_fitness"
    POSTGRES_PORT: int = 5432
    
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    # MongoDB配置
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DB: str = "hebei_fitness"
    
    # Neo4j配置
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "password"
    
    # Redis配置
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str = ""
    
    # JWT配置
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7天
    
    # 文件上传配置
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    # HDFS配置
    HDFS_URL: str = "http://localhost:9870"
    HDFS_USER: str = "hadoop"
    
    # Spark配置
    SPARK_MASTER: str = "local[*]"
    SPARK_APP_NAME: str = "HebeFitness"
    
    # 模型配置
    MODEL_DIR: str = "ml_models/saved_models"
    
    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
