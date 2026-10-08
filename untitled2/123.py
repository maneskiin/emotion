import pandas as pd
import json
import os, sys

# 读取 Excel 文件，指定第一行作为列名
file_path = r"D:\情感分析\用户情感分析.xlsx"
df = pd.read_excel(file_path, sheet_name=0, header=0)  # header=0 确保第一行是列名

# 转换数据到 JSON 格式
# 使用列号（0-based index）：A=0, B=1, C=2, D=3, F=5, G=6, H=7, I=8, J=9, K=10, L=11, M=12
data = []
for index, row in df.iterrows():
    output_dict = {}
    # 只添加非 NaN 的标签和等级，并将等级转换为整数
    if pd.notna(row[5]):  # F 列 (标签1)
        output_dict["主题1"] = row[5]
    if pd.notna(row[6]):  # G 列 (标签1等级)
        try:
            output_dict["主题1等级"] = int(float(row[6]))  # 转换为整数
        except (ValueError, TypeError):
            output_dict["主题1等级"] = 0  # 默认值，可根据需求调整
    if pd.notna(row[7]):  # H 列 (主题2)
        output_dict["主题2"] = row[7]
    if pd.notna(row[8]):  # I 列 (主题2等级)
        try:
            output_dict["主题2等级"] = int(float(row[8]))  # 转换为整数
        except (ValueError, TypeError):
            output_dict["主题2等级"] = 0  # 默认值，可根据需求调整
    if pd.notna(row[9]):  # J 列 (主题3)
        output_dict["主题3"] = row[9]
    if pd.notna(row[10]):  # K 列 (主题3等级)
        try:
            output_dict["主题3等级"] = int(float(row[10]))  # 转换为整数
        except (ValueError, TypeError):
            output_dict["主题3等级"] = 0  # 默认值，可根据需求调整
    if pd.notna(row[11]):  # L 列 (主题4)
        output_dict["主题4"] = row[11]
    if pd.notna(row[12]):  # M 列 (主题4等级)
        try:
            output_dict["主题4等级"] = int(float(row[12]))  # 转换为整数
        except (ValueError, TypeError):
            output_dict["主题4等级"] = 0  # 默认值，可根据需求调整

    entry = {
        # -*- coding: utf-8 -*-
        "instruction": "你是一个专业的用户情感分析师，请对以下文章内容进行深入的情感分析，并按照以下步骤执行任务：第一步：理解文章整体情绪通读全文，识别作者的情绪基调（积极、中性、消极、混合等），并注意文中出现的关键人物、事件、观点或问题。第二步：提取核心主题词请从文章中总结出3到5个最能代表其主要内容和情感焦点的主题词。要求：主题词应具有代表性，避免过于宽泛，每个主题词应聚焦于具体对象或概念按照相关性排序，第一个为主题焦点。第三步：情感评分请对每个主题词进行情感评分，依据其在文中的表达强度和倾向性，使用以下评分标准：（4=强烈正面 3=正面 2=中性 1=负面 0=强烈负面）并严格按照以下要求输出：1.必须输出纯JSON格式，不包含任何额外内容（如解释、说明、换行等）。2. JSON结构：包含"主题1"（字符串）、"主题1等级"（数字，0-4）、"主题2"（字符串）、"主题2等级"（数字，0-4）。3. 示例：{"主题1": "示例主题", "主题1等级": 2, "主题2": "示例主题2", "主题2等级": 3}请严格遵循上述规则，确保JSON可直接解析，否则视为无效输出。",
        "input": row[3],  # D 列 (文章内容)
        "output": str(output_dict)
    }
    data.append(entry)

# 将数据保存为 JSON 文件
output_path = r"D:\情感分析\用户情感分析.json"
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f"转换完成，JSON 文件已保存到 {output_path}")