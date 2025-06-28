import random
import json
from typing import List, Dict, Tuple

class NewsDatasetGenerator:
    """新闻数据集生成器"""
    
    def __init__(self):
        # 定义真假新闻的关键词和模板
        self.true_keywords = [
            "研究发现", "科学家证实", "官方发布", "数据显示", "调查报告", 
            "实验证明", "专家表示", "权威机构确认", "根据统计", "最新消息"
        ]
        
        self.fake_keywords = [
            "惊人真相", "内幕曝光", "绝对独家", "紧急提醒", "重大发现", 
            "惊人秘密", "惊天阴谋", "权威揭秘", "内部消息", "可靠来源"
        ]
        
        # 定义不同情感倾向的词汇
        self.positive_words = [
            "成功", "进步", "突破", "改善", "增长", "创新", "积极", "优秀", "领先", "发展"
        ]
        
        self.negative_words = [
            "失败", "下降", "危机", "衰退", "损失", "问题", "灾难", "冲突", "伤害", "丑闻"
        ]
        
        self.neutral_words = [
            "宣布", "讨论", "计划", "会议", "研究", "调查", "报告", "数据", "分析", "信息"
        ]
        
        # 定义新闻主题
        self.topics = [
            "科技", "健康", "环境", "经济", "政治", "教育", "娱乐", "体育", "文化", "交通"
        ]
    
    def generate_news(self, num_samples: int, seed: int = 42) -> List[Dict]:
        """生成新闻数据集
        
        Args:
            num_samples: 生成的新闻样本数量
            seed: 随机数种子，用于结果可复现
        """
        random.seed(seed)
        news_data = []
        
        # 平衡生成真假新闻
        num_true = num_samples // 2
        num_fake = num_samples - num_true
        
        # 生成真新闻
        for _ in range(num_true):
            news = self._generate_true_news()
            news_data.append(news)
        
        # 生成假新闻
        for _ in range(num_fake):
            news = self._generate_fake_news()
            news_data.append(news)
        
        # 随机打乱顺序
        random.shuffle(news_data)
        return news_data
    
    def _generate_true_news(self) -> Dict:
        """生成一条真新闻"""
        keyword = random.choice(self.true_keywords)
        topic = random.choice(self.topics)
        sentiment = random.choices(
            ["positive", "negative", "neutral"], 
            weights=[0.3, 0.3, 0.4]
        )[0]
        
        # 根据情感选择词汇
        if sentiment == "positive":
            content_word = random.choice(self.positive_words)
        elif sentiment == "negative":
            content_word = random.choice(self.negative_words)
        else:
            content_word = random.choice(self.neutral_words)
        
        # 构建新闻内容
        content = f"{keyword}，{topic}领域近日有了新的{content_word}进展。据相关人士透露，这一变化可能会对未来产生重要影响。"
        
        return {
            "label": 1,  # 1表示真新闻
            "text": content,
            "sentiment": sentiment
        }
    
    def _generate_fake_news(self) -> Dict:
        """生成一条假新闻"""
        keyword = random.choice(self.fake_keywords)
        topic = random.choice(self.topics)
        sentiment = random.choices(
            ["positive", "negative", "neutral"], 
            weights=[0.4, 0.5, 0.1]  # 假新闻更倾向于正负极端情感
        )[0]
        
        # 根据情感选择词汇
        if sentiment == "positive":
            content_word = random.choice(self.positive_words)
        elif sentiment == "negative":
            content_word = random.choice(self.negative_words)
        else:
            content_word = random.choice(self.neutral_words)
        
        # 添加一些夸张词汇
        exaggeration = random.choice([
            "绝对", "惊人", "前所未有", "超级", "令人震惊", "难以置信", "重大", "历史性"
        ])
        
        # 构建新闻内容
        content = f"{keyword}！{exaggeration}{topic}领域出现{content_word}事件，专家称这将彻底改变现状。"
        
        return {
            "label": 0,  # 0表示假新闻
            "text": content,
            "sentiment": sentiment
        }
    
    def save_to_file(self, news_data: List[Dict], file_path: str = "news_data.txt") -> None:
        """保存新闻数据到文件
        
        Args:
            news_data: 新闻数据列表
            file_path: 保存路径
        """
        with open(file_path, 'w', encoding='utf-8') as f:
            for news in news_data:
                # 保存格式: 标签\t文本
                f.write(f"{news['label']}\t{news['text']}\n")
        
        print(f"已保存 {len(news_data)} 条新闻到 {file_path}")
    
    def save_to_json(self, news_data: List[Dict], file_path: str = "news_data.json") -> None:
        """保存新闻数据到JSON文件（包含情感信息）
        
        Args:
            news_data: 新闻数据列表
            file_path: 保存路径
        """
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(news_data, f, ensure_ascii=False, indent=2)
        
        print(f"已保存 {len(news_data)} 条新闻到 {file_path}")

# 生成并保存数据集
if __name__ == "__main__":
    generator = NewsDatasetGenerator()
    
    # 生成100条新闻
    news_data = generator.generate_news(num_samples=100)
    
    # 保存为文本格式（用于模型输入）
    generator.save_to_file(news_data, "news_data.txt")
    
    # 保存为JSON格式（包含情感信息，用于分析）
    generator.save_to_json(news_data, "news_data_with_sentiment.json")
    
    # 打印样本
    print("\n数据样本:")
    for i in range(3):
        print(f"标签: {news_data[i]['label']}")
        print(f"情感: {news_data[i]['sentiment']}")
        print(f"内容: {news_data[i]['text']}")
        print("-" * 50)