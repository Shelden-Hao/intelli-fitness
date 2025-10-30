#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
训练数据生成器
基于现有日客流数据生成小时级训练数据
"""

import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict
from loguru import logger
from pathlib import Path


class TrafficDataGenerator:
    """客流数据生成器"""
    
    def __init__(self):
        """初始化"""
        # 不同设施类型的小时分布模式
        self.hourly_patterns = {
            '体育场': {
                6: 0.02, 7: 0.04, 8: 0.06, 9: 0.08, 10: 0.07, 11: 0.06,
                12: 0.05, 13: 0.04, 14: 0.05, 15: 0.06, 16: 0.08, 17: 0.10,
                18: 0.12, 19: 0.10, 20: 0.05, 21: 0.02
            },
            '体育馆': {
                8: 0.03, 9: 0.05, 10: 0.07, 11: 0.06, 12: 0.04, 13: 0.03,
                14: 0.05, 15: 0.07, 16: 0.09, 17: 0.11, 18: 0.14, 19: 0.13,
                20: 0.10, 21: 0.03
            },
            '健身中心': {
                6: 0.03, 7: 0.05, 8: 0.07, 9: 0.08, 10: 0.07, 11: 0.06,
                12: 0.04, 13: 0.03, 14: 0.04, 15: 0.05, 16: 0.07, 17: 0.10,
                18: 0.13, 19: 0.12, 20: 0.05, 21: 0.01
            },
            '游泳馆': {
                9: 0.04, 10: 0.06, 11: 0.07, 12: 0.05, 13: 0.04, 14: 0.06,
                15: 0.08, 16: 0.10, 17: 0.12, 18: 0.15, 19: 0.14, 20: 0.08, 21: 0.01
            }
        }
        
        logger.info("✅ 数据生成器初始化完成")
    
    def generate_hourly_data(self, facilities_data: List[Dict], 
                            start_date: datetime, end_date: datetime,
                            noise_level: float = 0.15) -> pd.DataFrame:
        """生成小时级客流数据
        
        Args:
            facilities_data: 场馆数据列表
            start_date: 开始日期
            end_date: 结束日期
            noise_level: 噪声水平（标准差占比）
            
        Returns:
            包含 facility_id, timestamp, visitors 的DataFrame
        """
        logger.info(f"开始生成数据: {start_date} 到 {end_date}")
        logger.info(f"场馆数量: {len(facilities_data)}")
        
        data = []
        current_date = start_date
        total_days = (end_date - start_date).days + 1
        
        while current_date <= end_date:
            for facility in facilities_data:
                facility_id = f"Facility_{facility['id']}"
                facility_type = facility.get('facility_type', '体育场')
                daily_visitors = facility.get('indicators', {}).get('daily_visitors', 0)
                
                if daily_visitors == 0:
                    continue
                
                # 获取该类型的小时分布模式
                pattern = self.hourly_patterns.get(facility_type, self.hourly_patterns['体育场'])
                
                for hour, ratio in pattern.items():
                    timestamp = current_date.replace(hour=hour, minute=0, second=0)
                    
                    # 基础客流
                    base_visitors = daily_visitors * ratio
                    
                    # 周末调整
                    weekend_factor = 1.3 if timestamp.weekday() >= 5 else 1.0
                    
                    # 季节调整
                    season_factor = self._get_season_factor(timestamp.month)
                    
                    # 节假日调整
                    holiday_factor = 1.5 if self._is_holiday(timestamp) else 1.0
                    
                    # 综合计算
                    expected_visitors = base_visitors * weekend_factor * season_factor * holiday_factor
                    
                    # 添加随机噪声
                    noise = np.random.normal(0, expected_visitors * noise_level)
                    visitors = max(0, int(expected_visitors + noise))
                    
                    data.append({
                        'facility_id': facility_id,
                        'timestamp': timestamp,
                        'visitors': visitors
                    })
            
            current_date += timedelta(days=1)
            
            if (current_date - start_date).days % 30 == 0:
                logger.info(f"已生成 {(current_date - start_date).days}/{total_days} 天数据")
        
        df = pd.DataFrame(data)
        logger.info(f"✅ 数据生成完成: {len(df)} 条记录")
        
        return df
    
    def generate_from_json(self, json_file: str, start_date: str, end_date: str,
                          output_file: str = None) -> pd.DataFrame:
        """从JSON文件生成数据
        
        Args:
            json_file: 场馆数据JSON文件路径
            start_date: 开始日期 (YYYY-MM-DD)
            end_date: 结束日期 (YYYY-MM-DD)
            output_file: 输出CSV文件路径
            
        Returns:
            生成的DataFrame
        """
        # 加载数据
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        facilities = data['facilities']
        
        # 转换日期
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        end_dt = datetime.strptime(end_date, '%Y-%m-%d')
        
        # 生成数据
        df = self.generate_hourly_data(facilities, start_dt, end_dt)
        
        # 保存
        if output_file:
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(output_file, index=False)
            logger.info(f"✅ 数据已保存到: {output_file}")
        
        return df
    
    def _get_season_factor(self, month: int) -> float:
        """获取季节调整因子"""
        if month in [3, 4, 5]:  # 春季
            return 1.1
        elif month in [6, 7, 8]:  # 夏季
            return 1.2
        elif month in [9, 10, 11]:  # 秋季
            return 1.15
        else:  # 冬季
            return 0.9
    
    def _is_holiday(self, timestamp: datetime) -> bool:
        """判断是否为节假日（简化版）"""
        # 春节
        if timestamp.month == 1 and 1 <= timestamp.day <= 7:
            return True
        # 清明
        if timestamp.month == 4 and 4 <= timestamp.day <= 6:
            return True
        # 劳动节
        if timestamp.month == 5 and 1 <= timestamp.day <= 5:
            return True
        # 端午
        if timestamp.month == 6 and timestamp.day in [22, 23, 24]:
            return True
        # 中秋
        if timestamp.month == 9 and timestamp.day in [15, 16, 17]:
            return True
        # 国庆
        if timestamp.month == 10 and 1 <= timestamp.day <= 7:
            return True
        
        return False
    
    def generate_statistics(self, df: pd.DataFrame) -> Dict:
        """生成数据统计信息"""
        stats = {
            'total_records': len(df),
            'facilities_count': df['facility_id'].nunique(),
            'date_range': {
                'start': df['timestamp'].min().strftime('%Y-%m-%d'),
                'end': df['timestamp'].max().strftime('%Y-%m-%d'),
                'days': (df['timestamp'].max() - df['timestamp'].min()).days + 1
            },
            'visitors': {
                'total': int(df['visitors'].sum()),
                'mean': float(df['visitors'].mean()),
                'median': float(df['visitors'].median()),
                'std': float(df['visitors'].std()),
                'min': int(df['visitors'].min()),
                'max': int(df['visitors'].max())
            },
            'by_hour': df.groupby(df['timestamp'].dt.hour)['visitors'].mean().to_dict(),
            'by_weekday': df.groupby(df['timestamp'].dt.dayofweek)['visitors'].mean().to_dict(),
            'by_month': df.groupby(df['timestamp'].dt.month)['visitors'].mean().to_dict()
        }
        
        return stats


def main():
    """主函数 - 生成训练数据"""
    import sys
    
    # 配置日志
    logger.remove()
    logger.add(sys.stderr, level="INFO")
    logger.add("logs/data_generation.log", rotation="10 MB", level="DEBUG")
    
    logger.info("=" * 80)
    logger.info("开始生成训练数据")
    logger.info("=" * 80)
    
    # 创建生成器
    generator = TrafficDataGenerator()
    
    # 生成2023年全年数据
    df = generator.generate_from_json(
        json_file='fitness_facilities_data.json',
        start_date='2023-01-01',
        end_date='2023-12-31',
        output_file='traffic_prediction/data/hourly_traffic_2023.csv'
    )
    
    # 生成统计信息
    stats = generator.generate_statistics(df)
    
    logger.info("\n" + "=" * 80)
    logger.info("数据统计信息")
    logger.info("=" * 80)
    logger.info(f"总记录数: {stats['total_records']:,}")
    logger.info(f"场馆数量: {stats['facilities_count']}")
    logger.info(f"日期范围: {stats['date_range']['start']} 到 {stats['date_range']['end']}")
    logger.info(f"总天数: {stats['date_range']['days']}")
    logger.info(f"\n客流统计:")
    logger.info(f"  总客流: {stats['visitors']['total']:,} 人次")
    logger.info(f"  平均: {stats['visitors']['mean']:.1f} 人次/小时")
    logger.info(f"  中位数: {stats['visitors']['median']:.1f} 人次/小时")
    logger.info(f"  标准差: {stats['visitors']['std']:.1f}")
    logger.info(f"  最小值: {stats['visitors']['min']}")
    logger.info(f"  最大值: {stats['visitors']['max']}")
    
    # 保存统计信息
    stats_file = 'traffic_prediction/data/data_statistics.json'
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    logger.info(f"\n✅ 统计信息已保存到: {stats_file}")
    
    logger.info("\n" + "=" * 80)
    logger.info("🎉 数据生成完成!")
    logger.info("=" * 80)


if __name__ == "__main__":
    main()
