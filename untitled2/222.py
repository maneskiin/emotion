# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from openai import OpenAI
import re, json

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Welcome to My Watchlist!'


@app.route('/completions', methods=["POST"])
def analysis():
    data = request.get_json()
    document = data.get("document")
    systemPrompt = data.get("systemPrompt")

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
    a = re.split('{|}', resultLLM)
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
    except:
        result = {}
    return result


@app.route('/analysis', methods=["POST"])
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
    resultLLM = completion.choices[0].text
    print('====\n', document, '\n=original ouput of LLM===\n', resultLLM, '\n====\n')
    # revise this output
    astr = resultLLM.replace('{', '').replace('}', '')
    a = re.split(",", astr)
    if len(a) % 2 != 0:
        a = a[:-1]  # delete the last non-standard string if the output is not a dict
    result = '{' + ','+'}'
    return {}


if __name__ == '__main__':
    client = OpenAI(
        api_key='EMPTY',
        base_url="http://0.0.0.0:8000/v1/",
    )
    app.run(host='0.0.0.0', port=8001, debug=True)