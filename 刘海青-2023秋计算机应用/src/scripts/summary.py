from transformers import pipeline
# summarizer = pipeline("summarization")
from pathlib import Path
model_name_or_path = "bert-base-chinese"
summarizer = pipeline(task="summarization", model=Path(f'{model_name_or_path}'), framework="pt")
ARTICLE = ARTICLE = """行政处罚决定书文号
鄂州金监罚决字〔2023〕3号
被处罚当事人
一、泰康人寿保险有限责任公司湖北鄂州中心支公司
二、王能文（时任泰康人寿保险有限责任公司湖北鄂州中心支公司营销部经理）
三、吕凯君（时任泰康人寿保险有限责任公司湖北鄂州中心支公司营销一区经理）
四、胡新荣（时任泰康人寿保险有限责任公司湖北鄂州中心支公司保险代理人）
主要违法违规事实
财务业务数据不真实；代理行为超出经营区域
行政处罚依据
《中华人民共和国保险法》第八十六条、第一百七十条、第一百七十一条，《保险公司中介业务违法行为处罚办法》第八条、第十九条，《保险代理人监管规定》第四十三条、第一百零九条
行政处罚决定
一、对泰康人寿保险有限责任公司湖北鄂州中心支公司罚款14万元
二、对王能文警告并处罚款1万元
三、对吕凯君警告并处罚款0.5万元
四、对胡新荣警告并处罚款0.5万元
作出处罚决定的
机关名称
国家金融监督管理总局
鄂州监管分局
作出处罚决定的日期
2023年12月7日"""
result = summarizer(ARTICLE, max_length=130, min_length=30, do_sample=False)
print(result)

