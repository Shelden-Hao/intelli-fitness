"""
数据清洗模块（简化版，无外部依赖）
"""
from typing import Dict, List
from loguru import logger
import re


class DataCleaner:
    """数据清洗器"""
    
    def __init__(self):
        logger.info("初始化数据清洗器")
    
    def clean_text(self, text: str) -> str:
        """清洗文本"""
        if not text:
            return ""
        
        # 去除多余空格
        text = re.sub(r'\s+', ' ', text)
        
        # 去除特殊字符
        text = re.sub(r'[^\w\s\u4e00-\u9fff]', '', text)
        
        # 去除首尾空格
        text = text.strip()
        
        return text
    
    def remove_duplicates(self, data_list: List[Dict]) -> List[Dict]:
        """去除重复数据"""
        seen = set()
        unique_data = []
        
        for item in data_list:
            # 使用标题或名称作为唯一标识
            key = item.get('title') or item.get('name') or str(item)
            if key not in seen:
                seen.add(key)
                unique_data.append(item)
        
        logger.info(f"去重前: {len(data_list)}, 去重后: {len(unique_data)}")
        return unique_data
    
    def validate_data(self, data: Dict) -> bool:
        """验证数据完整性"""
        required_fields = ['title', 'content']
        
        for field in required_fields:
            if field not in data or not data[field]:
                return False
        
        return True
    
    def standardize_date(self, date_str: str) -> str:
        """标准化日期格式"""
        # 简单的日期标准化
        date_str = date_str.strip()
        return date_str
