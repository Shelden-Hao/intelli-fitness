#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据集转换脚本 - 将Excel数据集转换为项目所需格式
包含NLP语义分析功能，将文本描述转换为量化指标
"""

import pandas as pd
import json
import re
from datetime import datetime
from loguru import logger
import sys

# 配置日志
log_file = 'logs/dataset_conversion.log'
logger.remove()
logger.add(sys.stderr, level="INFO")
logger.add(log_file, rotation="10 MB", retention="30 days", level="DEBUG", encoding="utf-8")

logger.info("=" * 80)
logger.info("开始数据集转换任务")
logger.info("=" * 80)


class TextToIndicatorConverter:
    """文本描述到指标值的转换器 - NLP语义分析"""
    
    def __init__(self):
        logger.info("初始化文本到指标转换器")
        
    def extract_area_value(self, text: str) -> float:
        """从文本中提取面积数值（平方米）"""
        if pd.isna(text) or not str(text).strip():
            return 0.0
        
        text = str(text)
        # 匹配数字（支持小数和千分位）
        patterns = [
            r'(\d+\.?\d*)\s*(?:平方米|㎡)',
            r'(\d+,\d+\.?\d*)\s*(?:平方米|㎡)',
            r'(\d+\.?\d*)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                value_str = match.group(1).replace(',', '')
                try:
                    value = float(value_str)
                    logger.debug(f"提取面积值: '{text}' -> {value}")
                    return value
                except:
                    continue
        
        logger.warning(f"无法提取面积值: {text}")
        return 0.0
    
    def extract_number_value(self, text: str) -> float:
        """从文本中提取数值"""
        if pd.isna(text) or not str(text).strip():
            return 0.0
        
        text = str(text).replace(',', '')
        # 匹配数字
        match = re.search(r'(\d+\.?\d*)', text)
        if match:
            try:
                value = float(match.group(1))
                logger.debug(f"提取数值: '{text}' -> {value}")
                return value
            except:
                pass
        
        return 0.0
    
    def extract_year(self, text: str) -> int:
        """从文本中提取年份"""
        if pd.isna(text) or not str(text).strip():
            return 0
        
        text = str(text)
        match = re.search(r'(19|20)\d{2}', text)
        if match:
            year = int(match.group(0))
            logger.debug(f"提取年份: '{text}' -> {year}")
            return year
        
        return 0
    
    def parse_location(self, text: str) -> dict:
        """解析地址信息"""
        if pd.isna(text) or not str(text).strip():
            return {"province": "", "city": "", "district": "", "full_address": ""}
        
        text = str(text).strip()
        
        # 提取省市区
        province = ""
        city = ""
        district = ""
        
        # 匹配省份
        if "河北省" in text:
            province = "河北省"
        
        # 匹配城市
        city_pattern = r'(石家庄|保定|唐山|秦皇岛|邯郸|邢台|张家口|承德|沧州|廊坊|衡水)市'
        city_match = re.search(city_pattern, text)
        if city_match:
            city = city_match.group(1) + "市"
        
        # 匹配区县
        district_pattern = r'([^省市]+?(?:区|县|市))'
        district_match = re.search(district_pattern, text)
        if district_match:
            district = district_match.group(1)
        
        logger.debug(f"解析地址: '{text}' -> 省:{province}, 市:{city}, 区:{district}")
        
        return {
            "province": province,
            "city": city,
            "district": district,
            "full_address": text
        }
    
    def parse_facility_type(self, text: str) -> str:
        """解析场馆类型"""
        if pd.isna(text) or not str(text).strip():
            return "未知"
        
        text = str(text).strip()
        
        # 场馆类型映射
        type_mapping = {
            "公共体育场": "体育场",
            "公共体育馆": "体育馆",
            "全民健身中心": "健身中心",
            "体育公园": "体育公园",
            "游泳馆": "游泳馆",
            "综合体育馆": "综合馆"
        }
        
        for key, value in type_mapping.items():
            if key in text:
                logger.debug(f"解析场馆类型: '{text}' -> {value}")
                return value
        
        return text if text else "未知"
    
    def parse_yes_no(self, text: str) -> bool:
        """解析是/否"""
        if pd.isna(text):
            return False
        
        text = str(text).strip()
        result = text in ["是", "有", "yes", "Yes", "YES", "true", "True"]
        logger.debug(f"解析是否: '{text}' -> {result}")
        return result
    
    def extract_sports_types(self, text: str) -> list:
        """提取运动项目"""
        if pd.isna(text) or not str(text).strip():
            return []
        
        text = str(text)
        sports = []
        
        # 常见运动项目
        sport_keywords = [
            "足球", "篮球", "排球", "羽毛球", "乒乓球", "网球",
            "游泳", "跑步", "健身", "瑜伽", "太极拳", "广场舞",
            "滑冰", "滑雪", "攀岩", "武术", "体操"
        ]
        
        for sport in sport_keywords:
            if sport in text:
                sports.append(sport)
        
        if sports:
            logger.debug(f"提取运动项目: '{text}' -> {sports}")
        
        return sports


def convert_dataset():
    """转换数据集主函数"""
    
    logger.info("开始读取Excel数据集...")
    
    try:
        # 读取Excel文件
        df = pd.read_excel('/Users/haoxiugong/Desktop/projects/nlp/数据集.xlsx')
        logger.info(f"✅ 成功读取数据集: {len(df)} 行, {len(df.columns)} 列")
        
        # 初始化转换器
        converter = TextToIndicatorConverter()
        
        # 转换后的数据
        facilities = []
        
        logger.info("开始逐行处理数据...")
        
        for idx, row in df.iterrows():
            try:
                # 提取基本信息 - 根据实际列名
                facility = {
                    "id": idx + 1,
                    "name": str(row['venueName']) if pd.notna(row['venueName']) else "",
                    "location": {},
                    "sports_types": [],
                    "description": "",
                    "facility_type": "",
                    "operator": "",
                    "build_year": 0,
                    "indicators": {
                        "building_area": 0.0,
                        "site_area": 0.0,
                        "land_area": 0.0,
                        "core_area": 0.0,
                        "core_free_area": 0.0,
                        "outdoor_area": 0.0,
                        "outdoor_free_area": 0.0,
                        "seats": 0,
                        "core_courts": 0,
                        "outdoor_courts": 0,
                        "has_outdoor_fitness": False,
                        "daily_visitors": 0
                    },
                    "subsidy_status": "",
                    "image_url": "",
                    "facilities": "",
                    "projects": "",
                    "remarks": ""
                }
                
                # 图片URL
                if pd.notna(row['img src']):
                    facility["image_url"] = str(row['img src'])
                
                # 地址信息
                if pd.notna(row['adress']):
                    location_text = str(row['adress'])
                    facility["location"] = converter.parse_location(location_text)
                
                # 详细地址
                if pd.notna(row['adress.1']):
                    facility["description"] = str(row['adress.1'])
                
                # 场馆类型
                if pd.notna(row['left 2']):
                    facility["facility_type"] = converter.parse_facility_type(str(row['left 2']))
                
                # 运营单位
                if pd.notna(row['left 3']):
                    operator_text = str(row['left 3'])
                    # 去除"运营单位："前缀
                    facility["operator"] = operator_text.replace('运营单位：', '').strip()
                
                # 建成年份
                if pd.notna(row['left 4']):
                    facility["build_year"] = converter.extract_year(str(row['left 4']))
                
                # 建筑面积
                if pd.notna(row['left 5']):
                    facility["indicators"]["building_area"] = converter.extract_area_value(str(row['left 5']))
                
                # 场馆外围免费或低收费开放的场地面积
                if pd.notna(row['left 6']):
                    facility["indicators"]["outdoor_free_area"] = converter.extract_area_value(str(row['left 6']))
                
                # 场地面积
                if pd.notna(row['left 7']):
                    facility["indicators"]["site_area"] = converter.extract_area_value(str(row['left 7']))
                
                # 场馆外围场地面积
                if pd.notna(row['left 8']):
                    facility["indicators"]["outdoor_area"] = converter.extract_area_value(str(row['left 8']))
                
                # 场馆外围免费或低收费开放的场地片数
                if pd.notna(row['left 9']):
                    facility["indicators"]["outdoor_courts"] = int(converter.extract_number_value(str(row['left 9'])))
                
                # 核心区免费或低收费开放的场地面积
                if pd.notna(row['left 10']):
                    facility["indicators"]["core_free_area"] = converter.extract_area_value(str(row['left 10']))
                
                # 是否有户外公共区域及户外健身器材
                if pd.notna(row['left 11']):
                    facility["indicators"]["has_outdoor_fitness"] = converter.parse_yes_no(str(row['left 11']))
                
                # 核心区场地面积
                if pd.notna(row['left 12']):
                    facility["indicators"]["core_area"] = converter.extract_area_value(str(row['left 12']))
                
                # 核心区免费或低收费开放的场地片数
                if pd.notna(row['left 13']):
                    facility["indicators"]["core_courts"] = int(converter.extract_number_value(str(row['left 13'])))
                
                # 用地面积
                if pd.notna(row['left 14']):
                    facility["indicators"]["land_area"] = converter.extract_area_value(str(row['left 14']))
                
                # 固定座位数
                if pd.notna(row['left 15']):
                    facility["indicators"]["seats"] = int(converter.extract_number_value(str(row['left 15'])))
                
                # 上级主管单位
                if pd.notna(row['left 16']):
                    # 可以添加到备注或其他字段
                    pass
                
                # 设施
                if pd.notna(row['设施']):
                    facility["facilities"] = str(row['设施'])
                
                # 项目（运动项目）
                if pd.notna(row['项目']):
                    projects_text = str(row['项目'])
                    facility["projects"] = projects_text
                    facility["sports_types"] = converter.extract_sports_types(projects_text)
                
                # 备注
                if pd.notna(row['备注']):
                    facility["remarks"] = str(row['备注'])
                
                # 补助状态
                if pd.notna(row['venue-text']):
                    facility["subsidy_status"] = str(row['venue-text'])
                
                # 客流量
                if pd.notna(row['img-text']):
                    visitors_text = str(row['img-text'])
                    visitors_match = re.search(r'(\d+)', visitors_text)
                    if visitors_match:
                        facility["indicators"]["daily_visitors"] = int(visitors_match.group(1))
                
                facilities.append(facility)
                
                if (idx + 1) % 100 == 0:
                    logger.info(f"已处理 {idx + 1}/{len(df)} 条数据...")
                
            except Exception as e:
                logger.error(f"处理第 {idx + 1} 行数据时出错: {str(e)}")
                continue
        
        logger.info(f"✅ 数据处理完成，共转换 {len(facilities)} 条记录")
        
        # 保存为JSON格式
        output_data = {
            "metadata": {
                "total_count": len(facilities),
                "conversion_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "source": "数据集.xlsx",
                "description": "河北省全民健身场馆数据 - 通过NLP语义分析转换"
            },
            "facilities": facilities
        }
        
        # 保存到项目根目录
        output_file = 'fitness_facilities_data.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"✅ 数据已保存到: {output_file}")
        
        # 生成统计报告
        generate_statistics(facilities)
        
        return output_data
        
    except Exception as e:
        logger.error(f"❌ 数据转换失败: {str(e)}")
        raise


def generate_statistics(facilities: list):
    """生成统计报告"""
    logger.info("\n" + "=" * 80)
    logger.info("数据统计报告")
    logger.info("=" * 80)
    
    # 按城市统计
    city_count = {}
    facility_type_count = {}
    total_area = 0
    total_visitors = 0
    
    for facility in facilities:
        city = facility["location"].get("city", "未知")
        if city:
            city_count[city] = city_count.get(city, 0) + 1
        
        ftype = facility.get("facility_type", "未知")
        facility_type_count[ftype] = facility_type_count.get(ftype, 0) + 1
        
        total_area += facility["indicators"].get("site_area", 0)
        total_visitors += facility["indicators"].get("daily_visitors", 0)
    
    logger.info(f"\n总场馆数: {len(facilities)}")
    logger.info(f"总场地面积: {total_area:,.2f} 平方米")
    logger.info(f"总日客流量: {total_visitors:,} 人次")
    
    logger.info("\n按城市分布:")
    for city, count in sorted(city_count.items(), key=lambda x: x[1], reverse=True):
        logger.info(f"  {city}: {count} 个场馆")
    
    logger.info("\n按场馆类型分布:")
    for ftype, count in sorted(facility_type_count.items(), key=lambda x: x[1], reverse=True):
        logger.info(f"  {ftype}: {count} 个")
    
    logger.info("=" * 80)


if __name__ == "__main__":
    try:
        convert_dataset()
        logger.info("\n🎉 数据集转换任务完成!")
    except Exception as e:
        logger.error(f"\n❌ 任务失败: {str(e)}")
        sys.exit(1)
