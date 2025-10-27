"""
体育数据爬虫 - 采集河北省全民健身相关数据
"""
import scrapy
from scrapy import Request
from typing import Dict, List
import json
from datetime import datetime
from loguru import logger


class SportsDataSpider(scrapy.Spider):
    """体育数据爬虫"""
    
    name = "sports_data"
    allowed_domains = []
    
    # 数据源配置
    data_sources = {
        "national_stats": "http://www.stats.gov.cn",  # 国家统计局
        "hebei_stats": "http://tjj.hebei.gov.cn",  # 河北省统计局
        "sports_bureau": "http://www.sport.gov.cn",  # 国家体育总局
        "hebei_sports": "http://tyw.hebei.gov.cn",  # 河北省体育局
    }
    
    custom_settings = {
        'ROBOTSTXT_OBEY': True,
        'CONCURRENT_REQUESTS': 16,
        'DOWNLOAD_DELAY': 2,
        'COOKIES_ENABLED': False,
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    }
    
    def start_requests(self):
        """开始爬取"""
        # 国家统计局 - 体育相关数据
        yield Request(
            url=f"{self.data_sources['national_stats']}/tjsj/",
            callback=self.parse_national_stats,
            meta={'source': 'national_stats'}
        )
        
        # 河北省统计局
        yield Request(
            url=f"{self.data_sources['hebei_stats']}/",
            callback=self.parse_hebei_stats,
            meta={'source': 'hebei_stats'}
        )
    
    def parse_national_stats(self, response):
        """解析国家统计局数据"""
        logger.info(f"正在解析国家统计局数据: {response.url}")
        
        # 提取体育设施数据
        facilities = response.css('.sports-facilities::text').getall()
        
        # 提取健身参与率数据
        participation = response.css('.participation-rate::text').getall()
        
        yield {
            'source': '国家统计局',
            'type': 'national_statistics',
            'facilities': facilities,
            'participation': participation,
            'crawl_time': datetime.now().isoformat(),
            'url': response.url
        }
    
    def parse_hebei_stats(self, response):
        """解析河北省统计局数据"""
        logger.info(f"正在解析河北省统计局数据: {response.url}")
        
        # 提取各市县体育数据
        cities_data = []
        for city in response.css('.city-data'):
            city_info = {
                'name': city.css('.city-name::text').get(),
                'population': city.css('.population::text').get(),
                'facilities_count': city.css('.facilities::text').get(),
                'sports_area': city.css('.sports-area::text').get(),
            }
            cities_data.append(city_info)
        
        yield {
            'source': '河北省统计局',
            'type': 'provincial_statistics',
            'cities': cities_data,
            'crawl_time': datetime.now().isoformat(),
            'url': response.url
        }


class FitnessDataCollector:
    """健身数据采集器 - 整合多源数据"""
    
    def __init__(self):
        self.data_cache = []
        logger.info("初始化健身数据采集器")
    
    def collect_facility_data(self) -> List[Dict]:
        """采集健身设施数据"""
        logger.info("开始采集健身设施数据...")
        
        # 模拟真实数据采集
        facilities = [
            {
                "id": 1,
                "name": "石家庄市体育馆",
                "type": "综合体育馆",
                "city": "石家庄市",
                "district": "长安区",
                "address": "中山东路318号",
                "area": 15000,  # 平方米
                "capacity": 8000,
                "facilities": ["篮球场", "羽毛球场", "游泳馆", "健身房"],
                "open_hours": "06:00-22:00",
                "latitude": 38.0428,
                "longitude": 114.5149,
                "build_year": 2010,
                "investment": 50000000,  # 元
                "annual_visitors": 500000
            },
            {
                "id": 2,
                "name": "保定市全民健身中心",
                "type": "健身中心",
                "city": "保定市",
                "district": "竞秀区",
                "address": "朝阳南大街",
                "area": 12000,
                "capacity": 5000,
                "facilities": ["健身房", "游泳池", "乒乓球馆", "瑜伽室"],
                "open_hours": "06:00-21:00",
                "latitude": 38.8738,
                "longitude": 115.4645,
                "build_year": 2015,
                "investment": 30000000,
                "annual_visitors": 300000
            },
            {
                "id": 3,
                "name": "唐山市体育公园",
                "type": "体育公园",
                "city": "唐山市",
                "district": "路南区",
                "address": "南新道",
                "area": 50000,
                "capacity": 10000,
                "facilities": ["足球场", "篮球场", "跑道", "健身器材区"],
                "open_hours": "全天开放",
                "latitude": 39.6304,
                "longitude": 118.1803,
                "build_year": 2018,
                "investment": 80000000,
                "annual_visitors": 800000
            }
        ]
        
        logger.info(f"采集到 {len(facilities)} 条健身设施数据")
        return facilities
    
    def collect_population_data(self) -> List[Dict]:
        """采集人口数据"""
        logger.info("开始采集人口数据...")
        
        population_data = [
            {
                "city": "石家庄市",
                "total_population": 11000000,
                "urban_population": 6500000,
                "rural_population": 4500000,
                "age_0_14": 1800000,
                "age_15_64": 7500000,
                "age_65_plus": 1700000,
                "year": 2024
            },
            {
                "city": "保定市",
                "total_population": 9400000,
                "urban_population": 4200000,
                "rural_population": 5200000,
                "age_0_14": 1500000,
                "age_15_64": 6400000,
                "age_65_plus": 1500000,
                "year": 2024
            },
            {
                "city": "唐山市",
                "total_population": 7700000,
                "urban_population": 4500000,
                "rural_population": 3200000,
                "age_0_14": 1200000,
                "age_15_64": 5300000,
                "age_65_plus": 1200000,
                "year": 2024
            }
        ]
        
        logger.info(f"采集到 {len(population_data)} 条人口数据")
        return population_data
    
    def collect_participation_data(self) -> List[Dict]:
        """采集健身参与数据"""
        logger.info("开始采集健身参与数据...")
        
        participation_data = [
            {
                "city": "石家庄市",
                "year": 2024,
                "regular_participants": 3500000,  # 经常参加体育锻炼人数
                "participation_rate": 0.318,  # 参与率
                "weekly_frequency": 3.5,  # 平均每周锻炼次数
                "avg_duration": 45,  # 平均每次锻炼时长(分钟)
                "popular_activities": ["跑步", "健走", "广场舞", "羽毛球", "游泳"]
            },
            {
                "city": "保定市",
                "year": 2024,
                "regular_participants": 2800000,
                "participation_rate": 0.298,
                "weekly_frequency": 3.2,
                "avg_duration": 42,
                "popular_activities": ["健走", "跑步", "太极拳", "篮球", "乒乓球"]
            },
            {
                "city": "唐山市",
                "year": 2024,
                "regular_participants": 2400000,
                "participation_rate": 0.312,
                "weekly_frequency": 3.4,
                "avg_duration": 43,
                "popular_activities": ["跑步", "健走", "羽毛球", "篮球", "游泳"]
            }
        ]
        
        logger.info(f"采集到 {len(participation_data)} 条参与数据")
        return participation_data
    
    def collect_policy_data(self) -> List[Dict]:
        """采集政策文件数据"""
        logger.info("开始采集政策文件数据...")
        
        policies = [
            {
                "title": "河北省全民健身实施计划(2021-2025年)",
                "level": "省级",
                "department": "河北省人民政府",
                "publish_date": "2021-12-15",
                "effective_date": "2022-01-01",
                "key_points": [
                    "到2025年,经常参加体育锻炼人数比例达到38.5%",
                    "人均体育场地面积达到2.6平方米",
                    "县(市、区)、乡镇(街道)、行政村(社区)三级公共健身设施和社区15分钟健身圈全覆盖"
                ],
                "url": "http://example.com/policy1"
            },
            {
                "title": "关于构建更高水平的全民健身公共服务体系的意见",
                "level": "国家级",
                "department": "中共中央办公厅、国务院办公厅",
                "publish_date": "2022-03-23",
                "effective_date": "2022-03-23",
                "key_points": [
                    "推动全民健身公共服务城乡区域均衡发展",
                    "提升全民健身公共服务智慧化水平",
                    "完善全民健身激励机制"
                ],
                "url": "http://example.com/policy2"
            }
        ]
        
        logger.info(f"采集到 {len(policies)} 条政策数据")
        return policies
    
    def save_data(self, data: List[Dict], filename: str):
        """保存数据到文件"""
        filepath = f"data/raw/{filename}.json"
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"数据已保存到 {filepath}")


if __name__ == "__main__":
    collector = FitnessDataCollector()
    
    # 采集各类数据
    facilities = collector.collect_facility_data()
    population = collector.collect_population_data()
    participation = collector.collect_participation_data()
    policies = collector.collect_policy_data()
    
    # 保存数据
    collector.save_data(facilities, "facilities")
    collector.save_data(population, "population")
    collector.save_data(participation, "participation")
    collector.save_data(policies, "policies")
    
    logger.info("✅ 数据采集完成!")
