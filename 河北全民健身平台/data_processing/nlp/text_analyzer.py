"""
NLP文本分析模块 - 政策文件与文本数据分析
使用NLP技术对文本内容进行语义分析，将对指标的评价转换为具体的指标值，实现量化分析
"""
import jieba
import jieba.analyse
from typing import List, Dict, Tuple, Optional
from collections import Counter
import re
from loguru import logger
import sys
from pathlib import Path


# 配置日志输出
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)
log_file = log_dir / "nlp_analysis.log"

logger.remove()
logger.add(sys.stderr, level="INFO", format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>")
logger.add(log_file, rotation="10 MB", retention="30 days", level="DEBUG", encoding="utf-8", format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}")


class PolicyTextAnalyzer:
    """政策文本分析器 - 使用NLP进行语义分析和指标量化"""
    
    def __init__(self):
        # 加载自定义词典
        self.load_custom_dict()
        logger.info("✅ 初始化政策文本分析器")
    
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
        """提取数值指标 - NLP语义分析"""
        indicators = []
        
        logger.debug(f"开始提取数值指标，文本长度: {len(text)}")
        
        # 提取百分比
        percent_pattern = r'(\d+\.?\d*)%'
        percents = re.findall(percent_pattern, text)
        for p in percents:
            indicators.append({"type": "percentage", "value": float(p), "unit": "%"})
            logger.debug(f"提取百分比: {p}%")
        
        # 提取面积指标（支持多种单位）
        area_pattern = r'(\d+\.?\d*)\s*(?:平方米|㎡|万平方米)'
        areas = re.findall(area_pattern, text)
        for a in areas:
            indicators.append({"type": "area", "value": float(a), "unit": "平方米"})
            logger.debug(f"提取面积: {a} 平方米")
        
        # 提取人数指标
        people_pattern = r'(\d+\.?\d*)\s*(?:万人|人|亿人)'
        people = re.findall(people_pattern, text)
        for p in people:
            indicators.append({"type": "people", "value": float(p), "unit": "人"})
            logger.debug(f"提取人数: {p} 人")
        
        # 提取年份
        year_pattern = r'(20\d{2})年'
        years = re.findall(year_pattern, text)
        for y in years:
            indicators.append({"type": "year", "value": int(y), "unit": "年"})
            logger.debug(f"提取年份: {y}")
        
        logger.info(f"✅ 提取数值指标完成: {len(indicators)} 个")
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
    
    def quantify_policy_indicators(self, policy_text: str) -> Dict:
        """量化政策指标 - 核心NLP语义分析功能
        
        将文本描述中的定性评价转换为定量指标值
        例如: "参与率达到38.5%" -> {"target_participation_rate": 0.385}
        """
        logger.info("开始量化政策指标...")
        indicators = {}
        
        # 提取目标参与率
        participation_match = re.search(r'参与率.*?(\d+\.?\d*)%', policy_text)
        if participation_match:
            value = float(participation_match.group(1)) / 100
            indicators['target_participation_rate'] = value
            logger.info(f"✅ 提取参与率目标: {value:.2%}")
        
        # 提取人均场地面积目标
        area_match = re.search(r'人均.*?场地.*?(\d+\.?\d*)\s*平方米', policy_text)
        if area_match:
            value = float(area_match.group(1))
            indicators['target_per_capita_area'] = value
            logger.info(f"✅ 提取人均场地面积目标: {value} 平方米")
        
        # 提取覆盖率目标
        coverage_match = re.search(r'覆盖率.*?(\d+\.?\d*)%', policy_text)
        if coverage_match:
            value = float(coverage_match.group(1)) / 100
            indicators['target_coverage_rate'] = value
            logger.info(f"✅ 提取覆盖率目标: {value:.2%}")
        
        # 提取设施数量目标
        facility_match = re.search(r'(\d+)\s*(?:个|座).*?(?:体育场馆|健身中心|体育设施)', policy_text)
        if facility_match:
            value = int(facility_match.group(1))
            indicators['target_facility_count'] = value
            logger.info(f"✅ 提取设施数量目标: {value} 个")
        
        # 提取投资金额
        investment_match = re.search(r'(\d+\.?\d*)\s*(?:亿元|万元)', policy_text)
        if investment_match:
            value = float(investment_match.group(1))
            unit = "亿元" if "亿元" in policy_text else "万元"
            indicators['target_investment'] = {"value": value, "unit": unit}
            logger.info(f"✅ 提取投资目标: {value} {unit}")
        
        logger.info(f"✅ 量化指标完成，共提取 {len(indicators)} 个指标")
        return indicators
    
    def semantic_analysis_to_score(self, text: str, indicator_type: str) -> Optional[float]:
        """语义分析转评分 - 将文本评价转换为0-100的量化分数
        
        Args:
            text: 待分析的文本
            indicator_type: 指标类型 (accessibility, balance, quality等)
        
        Returns:
            量化分数 (0-100)
        """
        logger.info(f"开始语义分析转评分，指标类型: {indicator_type}")
        
        # 定义评价词及其对应分数
        positive_high = ['优秀', '很好', '非常好', '卓越', '杰出', '显著', '大幅', '充分', '完善']
        positive_medium = ['良好', '较好', '不错', '改善', '提升', '增加', '加强']
        positive_low = ['一般', '尚可', '基本', '初步', '逐步']
        negative_low = ['不足', '欠缺', '有待', '需要', '应当']
        negative_high = ['较差', '很差', '严重不足', '缺乏', '落后']
        
        score = 50.0  # 默认中等分数
        
        words = self.segment_text(text)
        
        # 计算各类词的出现次数
        pos_high_count = sum(1 for w in words if w in positive_high)
        pos_med_count = sum(1 for w in words if w in positive_medium)
        pos_low_count = sum(1 for w in words if w in positive_low)
        neg_low_count = sum(1 for w in words if w in negative_low)
        neg_high_count = sum(1 for w in words if w in negative_high)
        
        # 计算加权分数
        score += pos_high_count * 15
        score += pos_med_count * 10
        score += pos_low_count * 5
        score -= neg_low_count * 10
        score -= neg_high_count * 20
        
        # 限制在0-100范围内
        score = max(0, min(100, score))
        
        logger.info(f"✅ 语义分析完成，评分: {score:.2f}")
        logger.debug(f"正面词(高): {pos_high_count}, 正面词(中): {pos_med_count}, 正面词(低): {pos_low_count}")
        logger.debug(f"负面词(低): {neg_low_count}, 负面词(高): {neg_high_count}")
        
        return score


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


if __name__ == "__main__":
    # 模块可以直接导入使用，无需测试代码
    pass
