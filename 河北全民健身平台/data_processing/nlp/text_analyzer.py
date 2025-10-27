"""
NLP文本分析模块 - 政策文件与文本数据分析
"""
import jieba
import jieba.analyse
from typing import List, Dict, Tuple
from collections import Counter
import re
from loguru import logger
import json


class PolicyTextAnalyzer:
    """政策文本分析器"""
    
    def __init__(self):
        # 加载自定义词典
        self.load_custom_dict()
        logger.info("初始化政策文本分析器")
    
    def load_custom_dict(self):
        """加载体育健身领域自定义词典"""
        custom_words = [
            "全民健身", "公共服务", "体育设施", "健身器材", "体育场馆",
            "健身中心", "运动场", "体育公园", "社区健身", "健身步道",
            "均衡性", "可及性", "覆盖率", "参与率", "人均体育场地面积",
            "经常参加体育锻炼", "国民体质", "健康中国", "体育强国",
            "智慧体育", "数字体育", "体育产业", "群众体育", "竞技体育"
        ]
        
        for word in custom_words:
            jieba.add_word(word)
        
        logger.info(f"加载自定义词典: {len(custom_words)} 个词")
    
    def segment_text(self, text: str) -> List[str]:
        """中文分词"""
        words = jieba.lcut(text)
        # 过滤停用词和标点
        stopwords = {'的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这'}
        words = [w for w in words if w not in stopwords and len(w) > 1]
        return words
    
    def extract_keywords(self, text: str, topK: int = 20) -> List[Tuple[str, float]]:
        """提取关键词 - TF-IDF"""
        keywords = jieba.analyse.extract_tags(text, topK=topK, withWeight=True)
        logger.info(f"提取关键词: {len(keywords)} 个")
        return keywords
    
    def extract_keywords_textrank(self, text: str, topK: int = 20) -> List[Tuple[str, float]]:
        """提取关键词 - TextRank"""
        keywords = jieba.analyse.textrank(text, topK=topK, withWeight=True)
        return keywords
    
    def analyze_policy_document(self, policy_text: str) -> Dict:
        """分析政策文件"""
        logger.info("开始分析政策文件...")
        
        # 分词
        words = self.segment_text(policy_text)
        
        # 词频统计
        word_freq = Counter(words)
        top_words = word_freq.most_common(30)
        
        # 关键词提取
        keywords_tfidf = self.extract_keywords(policy_text, topK=20)
        keywords_textrank = self.extract_keywords_textrank(policy_text, topK=20)
        
        # 提取数值指标
        numbers = self.extract_numeric_indicators(policy_text)
        
        # 情感倾向分析
        sentiment = self.analyze_sentiment(policy_text)
        
        result = {
            "word_count": len(words),
            "unique_words": len(set(words)),
            "top_words": top_words,
            "keywords_tfidf": keywords_tfidf,
            "keywords_textrank": keywords_textrank,
            "numeric_indicators": numbers,
            "sentiment": sentiment
        }
        
        logger.info("✅ 政策文件分析完成")
        return result
    
    def extract_numeric_indicators(self, text: str) -> List[Dict]:
        """提取数值指标"""
        indicators = []
        
        # 提取百分比
        percent_pattern = r'(\d+\.?\d*)%'
        percents = re.findall(percent_pattern, text)
        for p in percents:
            indicators.append({"type": "percentage", "value": float(p)})
        
        # 提取面积指标
        area_pattern = r'(\d+\.?\d*)\s*(?:平方米|㎡|万平方米)'
        areas = re.findall(area_pattern, text)
        for a in areas:
            indicators.append({"type": "area", "value": float(a)})
        
        # 提取人数指标
        people_pattern = r'(\d+\.?\d*)\s*(?:万人|人|亿人)'
        people = re.findall(people_pattern, text)
        for p in people:
            indicators.append({"type": "people", "value": float(p)})
        
        # 提取年份
        year_pattern = r'(20\d{2})年'
        years = re.findall(year_pattern, text)
        for y in years:
            indicators.append({"type": "year", "value": int(y)})
        
        logger.info(f"提取数值指标: {len(indicators)} 个")
        return indicators
    
    def analyze_sentiment(self, text: str) -> Dict:
        """情感分析 - 简化版"""
        positive_words = ['提高', '增加', '改善', '优化', '加强', '推进', '促进', '发展', '完善', '提升']
        negative_words = ['降低', '减少', '不足', '缺乏', '问题', '困难', '挑战']
        
        words = self.segment_text(text)
        
        positive_count = sum(1 for w in words if w in positive_words)
        negative_count = sum(1 for w in words if w in negative_words)
        
        total = positive_count + negative_count
        if total == 0:
            sentiment_score = 0.5
        else:
            sentiment_score = positive_count / total
        
        return {
            "score": sentiment_score,
            "positive_count": positive_count,
            "negative_count": negative_count,
            "label": "积极" if sentiment_score > 0.6 else "中性" if sentiment_score > 0.4 else "消极"
        }
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """实体识别"""
        entities = {
            "locations": [],
            "organizations": [],
            "facilities": [],
            "activities": []
        }
        
        # 地点实体
        location_pattern = r'(石家庄|保定|唐山|秦皇岛|邯郸|邢台|张家口|承德|沧州|廊坊|衡水|河北省|[市县区])'
        entities["locations"] = list(set(re.findall(location_pattern, text)))
        
        # 组织机构
        org_pattern = r'(体育局|统计局|政府|委员会|中心|协会)'
        entities["organizations"] = list(set(re.findall(org_pattern, text)))
        
        # 设施类型
        facility_keywords = ['体育馆', '健身中心', '运动场', '体育公园', '游泳馆', '篮球场', '足球场']
        entities["facilities"] = [f for f in facility_keywords if f in text]
        
        # 运动项目
        activity_keywords = ['跑步', '游泳', '篮球', '足球', '羽毛球', '乒乓球', '健身', '瑜伽', '太极拳', '广场舞']
        entities["activities"] = [a for a in activity_keywords if a in text]
        
        logger.info(f"实体识别完成: {sum(len(v) for v in entities.values())} 个实体")
        return entities


class FitnessTextProcessor:
    """健身文本处理器"""
    
    def __init__(self):
        self.analyzer = PolicyTextAnalyzer()
    
    def process_policy_files(self, policies: List[Dict]) -> List[Dict]:
        """批量处理政策文件"""
        logger.info(f"开始处理 {len(policies)} 个政策文件...")
        
        results = []
        for policy in policies:
            # 合并标题和要点
            full_text = policy.get('title', '') + '\n' + '\n'.join(policy.get('key_points', []))
            
            # 分析文本
            analysis = self.analyzer.analyze_policy_document(full_text)
            
            # 提取实体
            entities = self.analyzer.extract_entities(full_text)
            
            result = {
                **policy,
                "analysis": analysis,
                "entities": entities
            }
            results.append(result)
        
        logger.info("✅ 政策文件处理完成")
        return results
    
    def quantify_policy_indicators(self, policy_text: str) -> Dict:
        """量化政策指标"""
        indicators = {}
        
        # 提取目标参与率
        participation_match = re.search(r'参与率.*?(\d+\.?\d*)%', policy_text)
        if participation_match:
            indicators['target_participation_rate'] = float(participation_match.group(1)) / 100
        
        # 提取人均场地面积目标
        area_match = re.search(r'人均.*?场地.*?(\d+\.?\d*)\s*平方米', policy_text)
        if area_match:
            indicators['target_per_capita_area'] = float(area_match.group(1))
        
        # 提取覆盖率目标
        coverage_match = re.search(r'覆盖率.*?(\d+\.?\d*)%', policy_text)
        if coverage_match:
            indicators['target_coverage_rate'] = float(coverage_match.group(1)) / 100
        
        logger.info(f"量化指标: {indicators}")
        return indicators


if __name__ == "__main__":
    # 测试示例
    processor = FitnessTextProcessor()
    
    # 示例政策文本
    sample_policy = {
        "title": "河北省全民健身实施计划(2021-2025年)",
        "key_points": [
            "到2025年,经常参加体育锻炼人数比例达到38.5%",
            "人均体育场地面积达到2.6平方米",
            "县(市、区)、乡镇(街道)、行政村(社区)三级公共健身设施和社区15分钟健身圈全覆盖"
        ]
    }
    
    # 处理政策
    results = processor.process_policy_files([sample_policy])
    
    # 保存结果
    with open('data/processed/policy_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    logger.info("✅ 文本分析完成!")
