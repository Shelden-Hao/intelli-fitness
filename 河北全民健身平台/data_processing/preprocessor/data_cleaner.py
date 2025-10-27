"""
数据清洗与预处理模块
"""
from typing import Dict, List, Optional
from loguru import logger
import json
import re


class DataCleaner:
    """数据清洗器（简化版）"""
    
    def __init__(self):
        logger.info("初始化数据清洗器")
    
    def load_data(self, filepath: str) -> pd.DataFrame:
        """加载数据"""
        logger.info(f"加载数据: {filepath}")
        
        if filepath.endswith('.json'):
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            df = pd.DataFrame(data)
        elif filepath.endswith('.csv'):
            df = pd.DataFrame.read_csv(filepath)
        else:
            raise ValueError(f"不支持的文件格式: {filepath}")
        
        logger.info(f"数据形状: {df.shape}")
        return df
    
    def remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """去除重复数据"""
        before_count = len(df)
        df = df.drop_duplicates()
        after_count = len(df)
        logger.info(f"去重: {before_count} -> {after_count}, 删除 {before_count - after_count} 条")
        return df
    
    def handle_missing_values(self, df: pd.DataFrame, strategy: str = 'mean') -> pd.DataFrame:
        """处理缺失值"""
        missing_count = df.isnull().sum().sum()
        logger.info(f"缺失值总数: {missing_count}")
        
        if missing_count == 0:
            return df
        
        # 数值型列使用均值/中位数填充
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if strategy == 'mean':
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
        elif strategy == 'median':
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
        elif strategy == 'zero':
            df[numeric_cols] = df[numeric_cols].fillna(0)
        
        # 分类型列使用众数填充
        categorical_cols = df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            df[col] = df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else 'Unknown')
        
        logger.info(f"缺失值处理完成,策略: {strategy}")
        return df
    
    def detect_outliers(self, df: pd.DataFrame, columns: List[str], method: str = 'iqr') -> pd.DataFrame:
        """检测异常值"""
        outliers_count = 0
        
        for col in columns:
            if col not in df.columns:
                continue
            
            if method == 'iqr':
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
                outliers_count += len(outliers)
                
                # 替换异常值为边界值
                df.loc[df[col] < lower_bound, col] = lower_bound
                df.loc[df[col] > upper_bound, col] = upper_bound
            
            elif method == 'zscore':
                z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
                outliers = df[z_scores > 3]
                outliers_count += len(outliers)
                
                # 替换异常值为均值
                df.loc[z_scores > 3, col] = df[col].mean()
        
        logger.info(f"检测到 {outliers_count} 个异常值,已处理")
        return df
    
    def normalize_data(self, df: pd.DataFrame, columns: List[str], method: str = 'standard') -> pd.DataFrame:
        """数据标准化"""
        if method == 'standard':
            df[columns] = self.scaler.fit_transform(df[columns])
            logger.info(f"标准化完成(Z-score): {columns}")
        elif method == 'minmax':
            df[columns] = self.minmax_scaler.fit_transform(df[columns])
            logger.info(f"归一化完成(Min-Max): {columns}")
        
        return df
    
    def encode_categorical(self, df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """分类变量编码"""
        for col in columns:
            if col in df.columns:
                # One-Hot编码
                dummies = pd.get_dummies(df[col], prefix=col)
                df = pd.concat([df, dummies], axis=1)
                df = df.drop(col, axis=1)
                logger.info(f"编码完成: {col}")
        
        return df
    
    def save_cleaned_data(self, df: pd.DataFrame, filepath: str):
        """保存清洗后的数据"""
        if filepath.endswith('.csv'):
            df.to_csv(filepath, index=False, encoding='utf-8')
        elif filepath.endswith('.json'):
            df.to_json(filepath, orient='records', force_ascii=False, indent=2)
        
        logger.info(f"清洗后数据已保存: {filepath}")


class FitnessDataPreprocessor:
    """健身数据预处理器"""
    
    def __init__(self):
        self.cleaner = DataCleaner()
    
    def preprocess_facility_data(self, input_file: str, output_file: str):
        """预处理健身设施数据"""
        logger.info("开始预处理健身设施数据...")
        
        # 加载数据
        df = self.cleaner.load_data(input_file)
        
        # 去重
        df = self.cleaner.remove_duplicates(df)
        
        # 处理缺失值
        df = self.cleaner.handle_missing_values(df, strategy='mean')
        
        # 检测异常值
        numeric_cols = ['area', 'capacity', 'investment', 'annual_visitors']
        df = self.cleaner.detect_outliers(df, numeric_cols, method='iqr')
        
        # 添加派生特征
        df['per_capita_area'] = df['area'] / df['capacity']
        df['utilization_rate'] = df['annual_visitors'] / (df['capacity'] * 365)
        
        # 保存
        self.cleaner.save_cleaned_data(df, output_file)
        logger.info("✅ 健身设施数据预处理完成")
        
        return df
    
    def preprocess_population_data(self, input_file: str, output_file: str):
        """预处理人口数据"""
        logger.info("开始预处理人口数据...")
        
        df = self.cleaner.load_data(input_file)
        df = self.cleaner.remove_duplicates(df)
        df = self.cleaner.handle_missing_values(df)
        
        # 计算派生指标
        df['urbanization_rate'] = df['urban_population'] / df['total_population']
        df['aging_rate'] = df['age_65_plus'] / df['total_population']
        df['working_age_rate'] = df['age_15_64'] / df['total_population']
        
        self.cleaner.save_cleaned_data(df, output_file)
        logger.info("✅ 人口数据预处理完成")
        
        return df
    
    def preprocess_participation_data(self, input_file: str, output_file: str):
        """预处理参与数据"""
        logger.info("开始预处理参与数据...")
        
        df = self.cleaner.load_data(input_file)
        df = self.cleaner.remove_duplicates(df)
        df = self.cleaner.handle_missing_values(df)
        
        # 计算健身强度指数
        df['fitness_intensity'] = df['weekly_frequency'] * df['avg_duration'] / 60
        
        # 标准化参与率
        df['participation_rate_normalized'] = self.cleaner.minmax_scaler.fit_transform(
            df[['participation_rate']]
        )
        
        self.cleaner.save_cleaned_data(df, output_file)
        logger.info("✅ 参与数据预处理完成")
        
        return df


if __name__ == "__main__":
    preprocessor = FitnessDataPreprocessor()
    
    # 预处理各类数据
    preprocessor.preprocess_facility_data(
        "data/raw/facilities.json",
        "data/processed/facilities_cleaned.json"
    )
    
    preprocessor.preprocess_population_data(
        "data/raw/population.json",
        "data/processed/population_cleaned.json"
    )
    
    preprocessor.preprocess_participation_data(
        "data/raw/participation.json",
        "data/processed/participation_cleaned.json"
    )
    
    logger.info("🎉 所有数据预处理完成!")
