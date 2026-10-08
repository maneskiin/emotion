# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from openai import OpenAI
import re, json

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Welcome to My Watchlist!'


@app.route('/analysis', methods=["POST"])
def analysis():
    data = request.get_json()
    document = data.get("document")
    systemPrompt = FIXED_SYSTEM_PROMPT

    if document is None:
        return jsonify({'error': 'No document provided'}), 400

    completion = client.chat.completions.create(
        model="/app/Qwen2.5-7B-Instruct/",
        messages=[
            {"role": "system", "content": systemPrompt},
            {"role": "user", "content": document}
        ],
    )
    resultLLM = completion.choices[0].message.content
    print('====\n', document, '\n==original ouput of LLM==\n', resultLLM, '\n====\n')

    # 二次修正
    # 直接对原始大模型输出修正，如果OK就直接用，
    try:
        a = resultLLM.replace("'", '"')
        result = json.loads(a)
        print('++really output++\n', result, '\n++++')
        return result
    except:
        result = ''
    # 如果不OK，再单独分析
    a = re.split('{|}', resultLLM)
    print(1)
    result = ''
    for i in a:
        if "1':" in i:
            result = i
            break
    result = '{' + result + '}'
    result = result.replace("'", '"')
    print('++revised output++\n', result, '\n++++')
    try:
        result = json.loads(result)
        print('++really output++\n', result, '\n++++')
    except:
        result = {}
    return result


@app.route('/completions', methods=["POST"])
def completions():
    data = request.get_json()
    document = data.get("document")
    systemPrompt = data.get("systemPrompt")

    if document is None:
        return jsonify({'error': 'No document provided'}), 400

    completion = client.completions.create(
        model="/app/Qwen2.5-7B-Instruct/",
        prompt=systemPrompt + "." + document,
        temperature=0.8,
        # top_p=0.95
    )
    print(completion)
    resultLLM = completion.choices[0].text
    print('====\n', document, '\n=original ouput of LLM===\n', resultLLM, '\n====\n')

    # 二次修正
    # revise this output
    astr = resultLLM.replace('{', '').replace('}', '')
    a = re.split(",", astr)
    if len(a) % 2 != 0:
        a = a[:-1]  # delete the last non-standard string if the output is not a dict
    result = '{' + ',' + '}'
    return {}


if __name__ == '__main__':
    client = OpenAI(
        api_key='EMPTY',
        base_url="http://0.0.0.0:8001/v1/",
    )

    FIXED_SYSTEM_PROMPT = """你是一个专业的用户情感分析师，请对以下文章内容进行深入的情感分析，并按照以下步骤执行任务：
第一步：理解文章整体情绪
通读全文，识别作者的情绪基调（积极、中性、消极、混合等），并注意文中出现的关键人物、事件、观点或问题。

第二步：提取核心主题词
请从文章中总结出3-5个最能代表其主要内容和情感焦点的核心主题词。
要求：
- 核心主题词应具有代表性，避免过于宽泛，每个核心主题词应聚焦于具体对象或概念
- 按照相关性排序，第一个为主题焦点。

第三步：情感评分
请对提取的每个核心主题词进行情感评分，依据其在文中的情感表达强度和主题观点倾向性，使用以下评分标准：
（4=强烈正面 3=正面 2=中性 1=负面 0=强烈负面）

并严格将核心主题词和情感评分按照以下要求输出：
必须输出纯JSON格式，不包含任何额外内容（如解释、说明、换行等）。
JSON结构：
示例输出{'主题1': '公共安全', '主题1等级': 3, '主题2': '应急管理', '主题2等级': 3, '主题3': '灾害救援', '主题3等级': 3,'主题4': '经济高质
量发展', '主题4等级': 3}

"""
    app.run(host='0.0.0.0', port=8000, debug=True)