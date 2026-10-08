from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>情感分析AI</title>
    <script src="https://cdn.jsdelivr.net/npm/vue@3/dist/vue.global.js"></script>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background-color: #f5f6fa;
            color: #333;
        }

        /* 导航栏 */
        .navbar {
            background-color: white;
            padding: 15px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            position: sticky;
            top: 0;
            z-index: 1000;
        }

        .nav-container {
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 20px;
        }

        .logo {
            display: flex;
            align-items: center;
            font-weight: bold;
            color: #4A90E2;
            cursor: pointer;
        }

        .nav-links {
            display: flex;
            gap: 30px;
            position: relative;
        }

        .nav-links a {
            text-decoration: none;
            color: #666;
            font-size: 14px;
            cursor: pointer;
            transition: color 0.3s;
        }

        .nav-links a:hover {
            color: #4A90E2;
        }

        /* 下拉菜单样式 */
        .dropdown {
            position: relative;
        }

        .dropdown-menu {
            position: absolute;
            top: 100%;
            left: 0;
            background-color: white;
            min-width: 150px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-radius: 5px;
            padding: 10px 0;
            margin-top: 10px;
            opacity: 0;
            visibility: hidden;
            transform: translateY(-10px);
            transition: all 0.3s ease;
        }

        .dropdown:hover .dropdown-menu {
            opacity: 1;
            visibility: visible;
            transform: translateY(0);
        }

        .dropdown-menu a {
            display: block;
            padding: 10px 20px;
            color: #666;
            transition: background-color 0.3s;
        }

        .dropdown-menu a:hover {
            background-color: #f5f5f5;
            color: #4A90E2;
        }

        .login-btn {
            background-color: #4A90E2;
            color: white;
            border: none;
            padding: 8px 20px;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s;
        }

        .login-btn:hover {
            background-color: #357ABD;
        }

        /* 用户信息区域 */
        .user-info {
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .user-name {
            color: #333;
            font-size: 14px;
        }

        .user-type {
            font-size: 12px;
            color: #666;
            background-color: #f0f0f0;
            padding: 2px 8px;
            border-radius: 10px;
        }

        .logout-btn {
            background-color: transparent;
            color: #666;
            border: 1px solid #ddd;
            padding: 6px 16px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.3s;
        }

        .logout-btn:hover {
            border-color: #4A90E2;
            color: #4A90E2;
        }

        /* 认证页面样式 */
        .auth-container {
            max-width: 400px;
            margin: 80px auto;
            padding: 40px;
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        .auth-header {
            text-align: center;
            margin-bottom: 40px;
        }

        .auth-title {
            font-size: 24px;
            margin-bottom: 10px;
        }

        .auth-subtitle {
            color: #666;
            font-size: 14px;
        }

        .form-group {
            margin-bottom: 20px;
        }

        .form-label {
            display: block;
            margin-bottom: 8px;
            font-size: 14px;
            color: #333;
        }

        .form-input {
            width: 100%;
            padding: 12px 15px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
            transition: border-color 0.3s;
        }

        .form-input:focus {
            outline: none;
            border-color: #4A90E2;
        }

        .form-select {
            width: 100%;
            padding: 12px 15px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
            background-color: white;
            cursor: pointer;
        }

        .auth-btn {
            width: 100%;
            padding: 12px;
            background-color: #4A90E2;
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
            transition: background-color 0.3s;
        }

        .auth-btn:hover {
            background-color: #357ABD;
        }

        .auth-link {
            text-align: center;
            margin-top: 20px;
            font-size: 14px;
            color: #666;
        }

        .auth-link a {
            color: #4A90E2;
            text-decoration: none;
            cursor: pointer;
        }

        .auth-link a:hover {
            text-decoration: underline;
        }

        /* 错误提示 */
        .error-message {
            color: #d32f2f;
            font-size: 12px;
            margin-top: 5px;
        }

        /* 主容器 */
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
        }

        /* 标题部分 */
        .hero-section {
            text-align: center;
            margin-bottom: 60px;
        }

        .hero-section h1 {
            font-size: 36px;
            margin-bottom: 20px;
        }

        .hero-section p {
            color: #666;
            font-size: 16px;
        }

        /* 快速开始 */
        .quick-start {
            margin-bottom: 60px;
        }

        .quick-start h2 {
            text-align: center;
            font-size: 24px;
            margin-bottom: 40px;
        }

        .steps {
            display: flex;
            justify-content: space-around;
            gap: 30px;
        }

        .step {
            flex: 1;
            text-align: center;
            padding: 30px;
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        .step-number {
            width: 50px;
            height: 50px;
            background-color: #4A90E2;
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            font-weight: bold;
            margin: 0 auto 20px;
        }

        .step h3 {
            font-size: 18px;
            margin-bottom: 10px;
        }

        .step p {
            color: #666;
            font-size: 14px;
        }

        /* 功能演示 */
        .demo-section {
            background-color: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 60px;
        }

        .demo-section h2 {
            text-align: center;
            font-size: 24px;
            margin-bottom: 20px;
        }

        .demo-section p {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
        }

        .demo-content {
            display: flex;
            gap: 30px;
            align-items: flex-start;
        }

        .input-section {
            flex: 1;
        }

        .input-section label {
            display: block;
            margin-bottom: 10px;
            font-weight: bold;
        }

        .text-input {
            width: 100%;
            height: 150px;
            padding: 15px;
            border: 1px solid #ddd;
            border-radius: 5px;
            resize: vertical;
            font-size: 14px;
            margin-bottom: 20px;
        }

        .analyze-btn {
            background-color: #4A90E2;
            color: white;
            border: none;
            padding: 12px 40px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            display: block;
            margin: 0 auto;
        }

        .analyze-btn:hover {
            background-color: #357ABD;
        }

        .examples {
            margin-top: 30px;
        }

        .examples h3 {
            margin-bottom: 15px;
        }

        .example-pills {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }

        .example-pill {
            background-color: #f0f0f0;
            padding: 8px 16px;
            border-radius: 20px;
            cursor: pointer;
            font-size: 14px;
            transition: background-color 0.3s;
        }

        .example-pill:hover {
            background-color: #e0e0e0;
        }

        /* 结果展示 */
        .result-section {
            flex: 0 0 350px;
            background-color: #f5f6fa;
            padding: 20px;
            border-radius: 5px;
            min-height: 300px;
        }

        .result-content {
            text-align: center;
            padding: 40px 20px;
        }

        .result-content.has-results {
            text-align: left;
            padding: 20px;
        }

        .result-icon {
            font-size: 48px;
            margin-bottom: 20px;
        }

        .result-title {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 20px;
            text-align: center;
        }

        /* 情感标签列表 */
        .emotion-list {
            list-style: none;
            padding: 0;
        }

        .emotion-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 0;
            border-bottom: 1px solid #eee;
        }

        .emotion-item:last-child {
            border-bottom: none;
        }

        .emotion-label {
            font-size: 16px;
            font-weight: 500;
        }

        .emotion-score {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .score-number {
            font-size: 16px;
            font-weight: bold;
            display: inline-block;
        }

        .score-bar {
            width: 80px;
            height: 8px;
            background-color: #e0e0e0;
            border-radius: 4px;
            overflow: hidden;
        }

        .score-fill {
            height: 100%;
            border-radius: 4px;
            transition: width 0.3s ease;
        }

        /* 评分颜色 */
        .score-0 { color: #d32f2f; }
        .score-1 { color: #f57c00; }
        .score-2 { color: #757575; }
        .score-3 { color: #388e3c; }
        .score-4 { color: #1976d2; }

        .fill-0 { background-color: #d32f2f; }
        .fill-1 { background-color: #f57c00; }
        .fill-2 { background-color: #757575; }
        .fill-3 { background-color: #388e3c; }
        .fill-4 { background-color: #1976d2; }

        /* 使用说明 */
        .instructions {
            margin-top: 60px;
        }

        .instructions h2 {
            text-align: center;
            font-size: 24px;
            margin-bottom: 40px;
        }

        .instruction-cards {
            display: flex;
            gap: 30px;
        }

        .instruction-card {
            flex: 1;
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        .instruction-card h3 {
            font-size: 18px;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .instruction-card ul {
            list-style: none;
            color: #666;
            font-size: 14px;
        }

        .instruction-card li {
            margin-bottom: 10px;
            padding-left: 20px;
            position: relative;
        }

        .instruction-card li:before {
            content: "•";
            position: absolute;
            left: 0;
        }

        .icon {
            font-size: 24px;
        }

        /* 文件上传区域样式 */
        .file-upload-area {
            border: 2px dashed #4A90E2;
            border-radius: 10px;
            padding: 40px;
            text-align: center;
            background-color: #f8f9fa;
            transition: all 0.3s ease;
            cursor: pointer;
            position: relative;
        }

        .file-upload-area:hover {
            background-color: #e8f0fe;
            border-color: #357ABD;
        }

        .file-upload-area.dragover {
            background-color: #e8f0fe;
            border-color: #357ABD;
            transform: scale(1.02);
        }

        .file-input {
            display: none;
        }

        .upload-icon {
            font-size: 48px;
            color: #4A90E2;
            margin-bottom: 20px;
        }

        .upload-text {
            font-size: 16px;
            color: #333;
            margin-bottom: 10px;
        }

        .upload-hint {
            font-size: 14px;
            color: #666;
        }

        .file-info {
            margin-top: 20px;
            padding: 15px;
            background-color: #e8f0fe;
            border-radius: 5px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .file-name {
            font-weight: bold;
            color: #333;
        }

        .remove-file {
            color: #d32f2f;
            cursor: pointer;
            font-size: 14px;
        }

        /* 分析进度条样式 */
        .analysis-progress {
            margin: 30px 0;
            padding: 20px;
            background-color: #f5f6fa;
            border-radius: 10px;
        }

        .progress-text {
            font-size: 16px;
            font-weight: bold;
            margin-bottom: 10px;
            text-align: center;
        }

        .progress-bar {
            width: 100%;
            height: 20px;
            background-color: #e0e0e0;
            border-radius: 10px;
            overflow: hidden;
            margin-bottom: 10px;
        }

        .progress-fill {
            height: 100%;
            background-color: #4A90E2;
            transition: width 0.3s ease;
        }

        .progress-detail {
            font-size: 14px;
            color: #666;
            text-align: center;
        }

        /* 用户画像结果展示样式 */
        .profile-results {
            margin-top: 40px;
        }

        .results-header {
            background-color: #f5f6fa;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
        }

        .results-header h3 {
            font-size: 20px;
            margin-bottom: 10px;
        }

        .results-meta {
            display: flex;
            gap: 30px;
            color: #666;
            font-size: 14px;
        }

        .chart-container {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }

        .chart-title {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 20px;
            text-align: center;
        }

        .chart-wrapper {
            position: relative;
            height: 300px;
        }

        .data-table {
            width: 100%;
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }

        .table-title {
            font-size: 18px;
            font-weight: bold;
            padding: 20px;
            background-color: #f5f6fa;
        }

        .data-table table {
            width: 100%;
            border-collapse: collapse;
            table-layout: fixed; /* 固定表格布局 */
        }

        .data-table th {
            background-color: #f5f6fa;
            padding: 15px;
            text-align: left;
            font-weight: bold;
            color: #333;
            border-bottom: 2px solid #e0e0e0;
            white-space: nowrap; /* 防止表头换行 */
        }
        .data-table th:nth-child(1), /* 日期列 */
        .data-table td:nth-child(1) {
            width: 15%;
            min-width: 100px;
        }
        
        .data-table th:nth-child(2), /* 主题标签列 */
        .data-table td:nth-child(2) {
            width: 25%;
            min-width: 150px;
        }
        
        .data-table th:nth-child(3), /* 平均分列 */
        .data-table td:nth-child(3) {
            width: 15%;
            min-width: 80px;
            text-align: center; /* 居中显示分数 */
            white-space: nowrap; /* 防止换行 */
        }
        
        .data-table th:nth-child(4), /* 内容摘要列 */
        .data-table td:nth-child(4) {
            width: 45%;
            min-width: 200px;
        }
        
        .data-table td {
            padding: 15px;
            border-bottom: 1px solid #e0e0e0;
            vertical-align: top; /* 内容顶部对齐 */
            word-wrap: break-word; /* 长文本换行 */
        }
        .data-table tr:hover {
            background-color: #f8f9fa;
        }

        .tag-list {
            display: flex;
            gap: 5px;
            flex-wrap: wrap;
        }

        .tag {
            background-color: #e8f0fe;
            color: #4A90E2;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            white-space: nowrap; /* 防止标签内文字换行 */
        }
        
        /* 响应式处理 */
        @media (max-width: 1024px) {
            .data-table {
                overflow-x: auto; /* 小屏幕时允许横向滚动 */
            }
            
            .data-table table {
                min-width: 800px; /* 设置最小宽度保证表格完整显示 */
            }
        }
        
        /* 确保表格内容不会溢出 */
        .data-table th,
        .data-table td {
            overflow: hidden;
            text-overflow: ellipsis; /* 超长文本显示省略号 */
        }
    </style>
</head>
<body>
    <div id="app">
        <!-- 导航栏 -->
        <nav class="navbar">
            <div class="nav-container">
                <div class="logo" @click="currentPage = 'home'">
                    <span style="font-size: 24px; margin-right: 10px;">🤖</span>
                    情感分析AI
                </div>
                <div class="nav-links">
                    <div class="dropdown">
                        <a href="#">产品服务</a>
                        <div class="dropdown-menu">
                            <a @click="currentPage = 'home'">情感分析</a>
                            <a @click="currentPage = 'profile'">用户画像</a>
                        </div>
                    </div>
                    <a href="#">技术文档</a>
                    <a href="#">产品定价</a>
                </div>
                <div v-if="!isLoggedIn">
                    <button class="login-btn" @click="currentPage = 'login'">登录</button>
                </div>
                <div v-else class="user-info">
                    <span class="user-name">{{ currentUser.username }}</span>
                    <span class="user-type">{{ currentUser.userType === 'admin' ? '管理员' : '普通用户' }}</span>
                    <button class="logout-btn" @click="logout">退出登录</button>
                </div>
            </div>
        </nav>

        <!-- 页面内容 -->
        <div v-if="currentPage === 'home'">
            <!-- 主容器 -->
            <div class="container">
                <!-- 标题部分 -->
                <section class="hero-section">
                    <h1>情感分析</h1>
                    <p>快速AI情感倾向分析的强大功能，支持多维度情感标签分析，0-4分评级系统</p>
                </section>

                <!-- 快速开始 -->
                <section class="quick-start">
                    <h2>快速开始</h2>
                    <div class="steps">
                        <div class="step">
                            <div class="step-number">1</div>
                            <h3>输入文本</h3>
                            <p>在输入框输入需要分析的中文文本</p>
                        </div>
                        <div class="step">
                            <div class="step-number">2</div>
                            <h3>点击分析</h3>
                            <p>点击"开始分析"按钮运行情感分析</p>
                        </div>
                        <div class="step">
                            <div class="step-number">3</div>
                            <h3>查看结果</h3>
                            <p>获得多个情感标签及其评分结果</p>
                        </div>
                    </div>
                </section>

                <!-- 功能演示 -->
                <section class="demo-section">
                    <h2>功能演示</h2>
                    <p>输入文本并点击"开始分析"查看情感分析结果</p>

                    <div class="demo-content">
                        <div class="input-section">
                            <label>分析输入</label>
                            <textarea
                                v-model="inputText"
                                class="text-input"
                                placeholder="请输入需要分析的文本内容..."
                            ></textarea>
                            <button @click="analyzeText" class="analyze-btn">
                                立即情感分析
                            </button>

                            <div class="examples">
                                <h3>试试这些示例：</h3>
                                <div class="example-pills">
                                    <div @click="setExample('中国2025年可再生能源发电量占比达50%，风光电项目创历史新高。全球环保组织点赞“绿色中国领跑世界”，民众为蓝天白云点赞，称生活质量显著提升。')" class="example-pill">正面评价</div>
                                    <div @click="setExample('中国2025年2月召开全国人大会议，审议2025年度财政预算草案。会议将讨论教育与医疗领域拨款比例，代表们已提交相关提案。')" class="example-pill">中性评价</div>
                                    <div @click="setExample('菲律宾近期遭遇严重洪灾，32人死亡，超37万人受灾。总统马科斯在国情咨文演讲中宣称“经济复苏成果显著”，但现场民众用标语和嘘声回应，指责政府防洪投入低效（仅63%资金用于工程建设），并曝光新建排水系统因设计缺陷失效等问题。')" class="example-pill">负面评价</div>
                                    <div @click="setExample('美国2025年经济增速预计达2.5%，失业率降至3.8%，消费者信心回升。然而，特朗普政府新关税政策推高物价，服装和电子产品价格上涨10%，引发中低收入群体不满。')" class="example-pill">混合评价</div>
                                </div>
                            </div>
                        </div>

                        <div class="result-section">
                            <div v-if="!results.length" class="result-content">
                                <div class="result-icon">📊</div>
                                <p style="color: #999;">输入文本并点击"开始分析"查看情感分析结果</p>
                            </div>
                            <div v-else class="result-content has-results">
                                <div class="result-title">情感分析结果</div>
                                <ul class="emotion-list">
                                    <li v-for="item in results" :key="item.label" class="emotion-item">
                                        <span class="emotion-label">{{ item.label }}</span>
                                        <div class="emotion-score">
                                            <span class="score-number" :class="'score-' + item.score">{{ item.score }}</span>
                                            <div class="score-bar">
                                                <div class="score-fill" :class="'fill-' + item.score" :style="{width: (item.score / 4 * 100) + '%'}"></div>
                                            </div>
                                        </div>
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </section>

                <!-- 使用说明 -->
                <section class="instructions">
                    <h2>使用说明</h2>
                    <div class="instruction-cards">
                        <div class="instruction-card">
                            <h3><span class="icon">📝</span> 支持的文本类型</h3>
                            <ul>
                                <li>产品评价和反馈</li>
                                <li>社交媒体评论</li>
                                <li>新闻评论</li>
                                <li>客户服务对话</li>
                                <li>问卷调查回复</li>
                            </ul>
                        </div>
                        <div class="instruction-card">
                            <h3><span class="icon">📊</span> 评分系统说明</h3>
                            <ul>
                                <li>0分：强烈负面情感</li>
                                <li>1分：一般负面情感</li>
                                <li>2分：中性情感</li>
                                <li>3分：一般正面情感</li>
                                <li>4分：强烈正面情感</li>
                                <li>每次分析返回至多4个情感标签</li>
                            </ul>
                        </div>
                        <div class="instruction-card">
                            <h3><span class="icon">💡</span> 使用建议</h3>
                            <ul>
                                <li>文本长度建议在10-500字之间</li>
                                <li>确保文本内容清晰完整</li>
                                <li>避免输入无意义的符号</li>
                                <li>建议使用标准的中文表达</li>
                                <li>示例文本可免费体验，无需登录</li>
                            </ul>
                        </div>
                    </div>
                </section>
            </div>
        </div>

        <!-- 用户画像页面 -->
        <div v-if="currentPage === 'profile'">
            <div class="container">
                <!-- 标题部分 -->
                <section class="hero-section">
                    <h1>用户画像分析</h1>
                    <p>基于文章阅读行为的用户情感画像</p>
                </section>

                <!-- 快速开始 -->
                <section class="quick-start">
                    <h2>快速开始</h2>
                    <div class="steps">
                        <div class="step">
                            <div class="step-number">1</div>
                            <h3>上传文件</h3>
                            <p>上传包含日期和内容的Excel文件</p>
                        </div>
                        <div class="step">
                            <div class="step-number">2</div>
                            <h3>点击分析</h3>
                            <p>系统自动分析每条内容的情感倾向</p>
                        </div>
                        <div class="step">
                            <div class="step-number">3</div>
                            <h3>查看画像</h3>
                            <p>获得用户情感趋势图和详细分析报告</p>
                        </div>
                    </div>
                </section>

                <!-- 功能演示 -->
                <section class="demo-section">
                    <h2>功能演示</h2>
                    <p>上传Excel文件，系统将自动分析并生成用户画像</p>

                    <!-- 文件上传区域 -->
                    <div class="file-upload-area" 
                         @click="$refs.fileInput.click()"
                         @dragover.prevent="handleDragOver"
                         @dragleave.prevent="handleDragLeave"
                         @drop.prevent="handleDrop"
                         :class="{ dragover: isDragging }">
                        <input type="file" 
                               ref="fileInput" 
                               class="file-input" 
                               accept=".xlsx,.xls"
                               @change="handleFileSelect">
                        <div class="upload-icon">📁</div>
                        <div class="upload-text">拖拽文件到此处上传</div>
                        <div class="upload-hint">或点击选择文件</div>
                        <div class="upload-hint" style="margin-top: 10px;">支持格式：.xlsx, .xls</div>
                    </div>

                    <!-- 已选择文件信息 -->
                    <div v-if="uploadedFile" class="file-info">
                        <span class="file-name">已选择文件：{{ uploadedFile.name }}</span>
                        <span class="remove-file" @click="removeFile">删除</span>
                    </div>

                    <!-- 分析按钮 -->
                    <button v-if="uploadedFile && !isAnalyzing" @click="analyzeUserProfile" class="analyze-btn" style="margin-top: 20px;">
                        开始分析用户画像
                    </button>

                    <!-- 分析进度条 -->
                    <div v-if="isAnalyzing" class="analysis-progress">
                        <div class="progress-text">
                            正在分析数据... {{ Math.round(analysisProgress) }}%
                        </div>
                        <div class="progress-bar">
                            <div class="progress-fill" :style="{width: analysisProgress + '%'}"></div>
                        </div>
                        <div class="progress-detail">
                            正在处理第 {{ currentAnalyzing }} / {{ excelData.length }} 条记录
                        </div>
                    </div>
                </section>

                <!-- 用户画像结果 -->
                <section v-if="showProfileResults" class="profile-results">
                    <div class="results-header">
                        <h3>用户画像分析结果</h3>
                        <div class="results-meta">
                            <span>时间范围：{{ profileResults.dateRange.start }} 至 {{ profileResults.dateRange.end }}</span>
                            <span>分析记录数：{{ profileResults.totalRecords }} 条</span>
                        </div>
                    </div>

                    <!-- 情感趋势图 -->
                    <div class="chart-container">
                        <div class="chart-title">📊 用户情感趋势图</div>
                        <div class="chart-wrapper">
                            <canvas id="trendChart"></canvas>
                        </div>
                    </div>

                    <!-- 情感分布图 -->
                    <div class="chart-container">
                        <div class="chart-title">📈 情感分布统计</div>
                        <div class="chart-wrapper">
                            <canvas id="distributionChart"></canvas>
                        </div>
                    </div>

                    <!-- 详细数据表格 -->
                    <div class="data-table">
                        <div class="table-title">📋 详细数据表格</div>
                        <table>
                            <thead>
                                <tr>
                                    <th>日期</th>
                                    <th>主题标签</th>
                                    <th>平均分</th>
                                    <th>内容摘要</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="row in profileResults.detailTable" :key="row.date">
                                    <td>{{ row.date }}</td>
                                    <td>
                                        <div class="tag-list">
                                            <span v-for="tag in row.tags" :key="tag" class="tag">{{ tag }}</span>
                                        </div>
                                    </td>
                                    <td>
                                        <span class="score-number" :class="'score-' + Math.round(row.avgScore)">
                                            {{ row.avgScore.toFixed(1) }}
                                        </span>
                                    </td>
                                    <td>{{ row.contentSummary }}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </section>
            </div>
        </div>

        <!-- 登录页面 -->
        <div v-if="currentPage === 'login'" class="auth-container">
            <div class="auth-header">
                <h2 class="auth-title">欢迎登录系统</h2>
                <p class="auth-subtitle">登录以使用情感分析功能</p>
            </div>

            <form @submit.prevent="handleLogin">
                <div class="form-group">
                    <label class="form-label">用户名</label>
                    <input
                        v-model="loginForm.username"
                        type="text"
                        class="form-input"
                        placeholder="请输入用户名"
                        required
                    >
                </div>

                <div class="form-group">
                    <label class="form-label">密码</label>
                    <input
                        v-model="loginForm.password"
                        type="password"
                        class="form-input"
                        placeholder="请输入密码"
                        required
                    >
                </div>

                <div class="form-group">
                    <label class="form-label">账户类型</label>
                    <select v-model="loginForm.userType" class="form-select">
                        <option value="user">普通用户</option>
                        <option value="admin">管理员</option>
                    </select>
                </div>

                <div v-if="loginError" class="error-message">{{ loginError }}</div>

                <button type="submit" class="auth-btn">登录</button>
            </form>

            <div class="auth-link">
                还没有账户？ <a @click="currentPage = 'register'">立即注册</a>
            </div>
        </div>

        <!-- 注册页面 -->
        <div v-if="currentPage === 'register'" class="auth-container">
            <div class="auth-header">
                <h2 class="auth-title">创建新账户</h2>
                <p class="auth-subtitle">注册账户以使用所有功能</p>
            </div>

            <form @submit.prevent="handleRegister">
                <div class="form-group">
                    <label class="form-label">用户名</label>
                    <input
                        v-model="registerForm.username"
                        type="text"
                        class="form-input"
                        placeholder="请输入用户名"
                        required
                    >
                </div>

                <div class="form-group">
                    <label class="form-label">邮箱</label>
                    <input
                        v-model="registerForm.email"
                        type="email"
                        class="form-input"
                        placeholder="请输入邮箱地址"
                        required
                    >
                </div>

                <div class="form-group">
                    <label class="form-label">显示名称</label>
                    <input
                        v-model="registerForm.displayName"
                        type="text"
                        class="form-input"
                        placeholder="请输入显示名称（可选）"
                    >
                </div>

                <div class="form-group">
                    <label class="form-label">密码</label>
                    <input
                        v-model="registerForm.password"
                        type="password"
                        class="form-input"
                        placeholder="请输入密码"
                        required
                    >
                </div>

                <div class="form-group">
                    <label class="form-label">确认密码</label>
                    <input
                        v-model="registerForm.confirmPassword"
                        type="password"
                        class="form-input"
                        placeholder="请确认密码"
                        required
                    >
                </div>

                <div v-if="registerError" class="error-message">{{ registerError }}</div>

                <button type="submit" class="auth-btn">注册账户</button>
            </form>

            <div class="auth-link">
                已有账户？ <a @click="currentPage = 'login'">立即登录</a>
            </div>
        </div>
    </div>

    <script>
        const { createApp } = Vue;

        createApp({
            data() {
                return {
                    // 页面控制
                    currentPage: 'home', // home, profile, login, register

                    // 用户状态
                    isLoggedIn: false,
                    currentUser: null,

                    // 登录表单
                    loginForm: {
                        username: '',
                        password: '',
                        userType: 'user'
                    },
                    loginError: '',

                    // 注册表单
                    registerForm: {
                        username: '',
                        email: '',
                        displayName: '',
                        password: '',
                        confirmPassword: ''
                    },
                    registerError: '',

                    // 情感分析
                    inputText: '',
                    results: [],

                    // 用户画像相关
                    uploadedFile: null,
                    excelData: [],
                    isDragging: false,
                    isAnalyzing: false,
                    analysisProgress: 0,
                    currentAnalyzing: 0,
                    showProfileResults: false,
                    profileResults: {
                        dateRange: { start: '', end: '' },
                        totalRecords: 0,
                        emotionTrend: [],
                        emotionDistribution: {},
                        detailTable: []
                    },
                    
                    // 图表实例
                    trendChart: null,
                    distributionChart: null
                };
            },
            methods: {
                // 登录处理
                async handleLogin() {
                    this.loginError = '';

                    // 表单验证
                    if (!this.loginForm.username || !this.loginForm.password) {
                        this.loginError = '请填写所有必填字段';
                        return;
                    }

                    try {
                        // TODO: 调用登录API
                        // const response = await fetch('/api/auth/login', {
                        //     method: 'POST',
                        //     headers: {
                        //         'Content-Type': 'application/json'
                        //     },
                        //     body: JSON.stringify(this.loginForm)
                        // });
                        // const data = await response.json();

                        // 模拟登录成功
                        this.isLoggedIn = true;
                        this.currentUser = {
                            username: this.loginForm.username,
                            userType: this.loginForm.userType,
                            displayName: this.loginForm.username
                        };
                        this.currentPage = 'home';

                        // 清空表单
                        this.loginForm = {
                            username: '',
                            password: '',
                            userType: 'user'
                        };

                        console.log('登录成功');
                    } catch (error) {
                        this.loginError = '登录失败，请检查用户名和密码';
                    }
                },

                // 注册处理
                async handleRegister() {
                    this.registerError = '';

                    // 表单验证
                    if (!this.registerForm.username || !this.registerForm.email ||
                        !this.registerForm.password || !this.registerForm.confirmPassword) {
                        this.registerError = '请填写所有必填字段';
                        return;
                    }

                    if (this.registerForm.password !== this.registerForm.confirmPassword) {
                        this.registerError = '两次输入的密码不一致';
                        return;
                    }

                    if (this.registerForm.password.length < 6) {
                        this.registerError = '密码长度至少为6位';
                        return;
                    }

                    try {
                        // TODO: 调用注册API
                        // const response = await fetch('/api/auth/register', {
                        //     method: 'POST',
                        //     headers: {
                        //         'Content-Type': 'application/json'
                        //     },
                        //     body: JSON.stringify({
                        //         username: this.registerForm.username,
                        //         email: this.registerForm.email,
                        //         password: this.registerForm.password,
                        //         displayName: this.registerForm.displayName || this.registerForm.username
                        //     })
                        // });
                        // const data = await response.json();

                        // 模拟注册成功，跳转到登录页
                        alert('注册成功！请登录');
                        this.currentPage = 'login';

                        // 清空表单
                        this.registerForm = {
                            username: '',
                            email: '',
                            displayName: '',
                            password: '',
                            confirmPassword: ''
                        };

                        console.log('注册成功');
                    } catch (error) {
                        this.registerError = '注册失败，请稍后重试';
                    }
                },

                // 退出登录
                logout() {
                    this.isLoggedIn = false;
                    this.currentUser = null;
                    this.results = [];
                    this.inputText = '';
                    this.currentPage = 'home';
                },

                // 情感分析
                analyzeText() {
                    if (!this.inputText.trim()) {
                        alert('请输入需要分析的文本');
                        return;
                    }

                    // 定义预设示例文本列表
                    const presetExamples = [
                        '中国2025年可再生能源发电量占比达50%，风光电项目创历史新高。全球环保组织点赞“绿色中国领跑世界”，民众为蓝天白云点赞，称生活质量显著提升。',
                        '中国2025年2月召开全国人大会议，审议2025年度财政预算草案。会议将讨论教育与医疗领域拨款比例，代表们已提交相关提案。',
                        '菲律宾近期遭遇严重洪灾，32人死亡，超37万人受灾。总统马科斯在国情咨文演讲中宣称“经济复苏成果显著”，但现场民众用标语和嘘声回应，指责政府防洪投入低效（仅63%资金用于工程建设），并曝光新建排水系统因设计缺陷失效等问题。',
                        '美国2025年经济增速预计达2.5%，失业率降至3.8%，消费者信心回升。然而，特朗普政府新关税政策推高物价，服装和电子产品价格上涨10%，引发中低收入群体不满。'
                    ];

                    // 检查是否是预设示例
                    const isPresetExample = presetExamples.includes(this.inputText.trim());

                    // 如果不是预设示例，需要检查登录状态
                    // if (!isPresetExample && !this.isLoggedIn) {
                    //     alert('请先登录后再使用分析功能');
                    //     this.currentPage = 'login';
                    //     return;
                    // }

                    // 调用分析API
                    const vm = this;
                    const datajson = {
                        "systemPrompt": "你是一个专业的用户情感分析师，请对以下文章内容进行深入的情感分析，并按照以下步骤执行任务：第一步：理解文章整体情绪通读全文，识别作者的情绪基调（积极、中性、消极、混合等），并注意文中出现的关键人物、事件、观点或问题。第二步：提取核心主题词请从文章中总结出3-5个最能代表其主要内容和情感焦点的主题词。要求：主题词应具有代表性，避免过于宽泛，每个主题词应聚焦于具体对象或概念按照相关性排序，第一个为主题焦点。第三步：情感评分请对每个主题词进行情感评分，依据其在文中的表达强度和倾向性，使用以下评分标准：（4=强烈正面 3=正面 2=中性 1=负面 0=强烈负面）并严格按照以下要求输出：必须输出纯JSON格式，不包含任何额外内容（如解释、说明、换行等）。JSON结构：示例輸出{'主题1': '公共安全', '主题1等级': 3, '主题2': '应急管理', '主题2等级': 3, '主题3': '灾害救援', '主题3等级': 3,'主题4': '经济高质量发展', '主题4等级': 3}",
                        "document": this.inputText.trim()
                    };

                    $.ajax({
                        url: "/api/analysis", 
                        method: "post",
                        dataType: "json",
                        contentType: "application/json",
                        
                        data: JSON.stringify(datajson),
                        success: function(data) {
                            console.log(data);

                            const results = [];          
                            const keys = Object.keys(data);
                            const themeNumbers = [];

                            // 找出所有的主题编号
                            keys.forEach(key => {
                                const match = key.match(/^主题(\d+)$/);
                                if (match) {
                                    themeNumbers.push(parseInt(match[1]));
                                }
                            });

                            // 按编号排序
                            themeNumbers.sort((a, b) => a - b);

                            // 根据找到的主题编号提取数据
                            themeNumbers.forEach(num => {
                                const themeKey = `主题${num}`;
                                const scoreKey = `主题${num}等级`;

                                if (data[themeKey] && data[scoreKey] !== undefined) {
                                    results.push({
                                        label: data[themeKey],
                                        score: data[scoreKey]
                                    });
                                }
                            });

                            // 更新Vue组件的results数据
                            vm.results = results;

                            // 如果没有结果，显示提示
                            if (results.length === 0) {
                                alert('分析未返回有效结果，请稍后重试');
                            }
                        },
                        error: function(error) {
                            console.log(error);
                            alert('分析失败，请检查网络连接或稍后重试');
                        }
                    });
                },

                setExample(text) {
                    this.inputText = text;
                },

                // 文件拖拽处理
                handleDragOver(e) {
                    this.isDragging = true;
                },

                handleDragLeave(e) {
                    this.isDragging = false;
                },

                handleDrop(e) {
                    this.isDragging = false;
                    const files = e.dataTransfer.files;
                    if (files.length > 0) {
                        this.processFile(files[0]);
                    }
                },

                // 文件选择处理
                handleFileSelect(e) {
                    const files = e.target.files;
                    if (files.length > 0) {
                        this.processFile(files[0]);
                    }
                },

                // 处理文件
                processFile(file) {
                    // 验证文件类型
                    const validTypes = ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.ms-excel'];
                    if (!validTypes.includes(file.type) && !file.name.match(/\.(xlsx|xls)$/)) {
                        alert('请上传Excel文件（.xlsx或.xls格式）');
                        return;
                    }

                    // 验证文件大小（例如：限制10MB）
                    if (file.size > 10 * 1024 * 1024) {
                        alert('文件大小不能超过10MB');
                        return;
                    }

                    this.uploadedFile = file;
                    this.readExcelFile(file);
                },

                // 读取Excel文件
                readExcelFile(file) {
                    const reader = new FileReader();
                    const vm = this;
                
                    reader.onload = function(e) {
                        try {
                            const data = new Uint8Array(e.target.result);
                            const workbook = XLSX.read(data, { 
                                type: 'array',
                                cellDates: true,  // 重要：启用日期解析
                                dateNF: 'yyyy-mm-dd'  // 指定日期格式
                            });
                            
                            // 获取第一个工作表
                            const firstSheetName = workbook.SheetNames[0];
                            const worksheet = workbook.Sheets[firstSheetName];
                            
                            // 将工作表转换为JSON
                            const jsonData = XLSX.utils.sheet_to_json(worksheet, {
                                raw: false,  // 不使用原始值，使用格式化后的值
                                dateNF: 'yyyy-mm-dd'  // 日期格式
                            });
                            
                            // 验证数据格式
                            if (jsonData.length === 0) {
                                alert('Excel文件中没有数据');
                                vm.removeFile();
                                return;
                            }
                
                            // 检查必要的列
                            const firstRow = jsonData[0];
                            if (!firstRow.hasOwnProperty('日期') || !firstRow.hasOwnProperty('内容')) {
                                alert('Excel文件格式错误，需要包含"日期"和"内容"两列');
                                vm.removeFile();
                                return;
                            }
                
                            // 限制最多5行数据并格式化日期
                            vm.excelData = jsonData.slice(0, 5).map(row => {
                                let formattedDate = row['日期'];
                                
                                // 如果日期是数字（Excel序列号），需要转换
                                if (typeof formattedDate === 'number') {
                                    // Excel的日期序列号转换为JavaScript日期
                                    const excelDate = new Date((formattedDate - 25569) * 86400 * 1000);
                                    formattedDate = excelDate.toISOString().split('T')[0]; // 格式化为 YYYY-MM-DD
                                } else if (formattedDate instanceof Date) {
                                    // 如果已经是Date对象
                                    formattedDate = formattedDate.toISOString().split('T')[0];
                                } else if (typeof formattedDate === 'string') {
                                    // 如果是字符串，尝试解析并格式化
                                    const parsedDate = new Date(formattedDate);
                                    if (!isNaN(parsedDate.getTime())) {
                                        formattedDate = parsedDate.toISOString().split('T')[0];
                                    }
                                }
                
                                return {
                                    date: formattedDate,
                                    content: row['内容']
                                };
                            });
                
                            console.log('Excel数据读取成功:', vm.excelData);
                        } catch (error) {
                            console.error('读取Excel文件失败:', error);
                            alert('读取Excel文件失败，请检查文件格式');
                            vm.removeFile();
                        }
                    };
                
                    reader.readAsArrayBuffer(file);
                },
                // 删除文件
                removeFile() {
                    this.uploadedFile = null;
                    this.excelData = [];
                    this.$refs.fileInput.value = '';
                    this.showProfileResults = false;
                },

                // 用户画像分析
                async analyzeUserProfile() {
                    if (!this.excelData || this.excelData.length === 0) {
                        alert('请先上传Excel文件');
                        return;
                    }

                    // 显示进度
                    this.analysisProgress = 0;
                    this.isAnalyzing = true;
                    this.currentAnalyzing = 0;
                    this.showProfileResults = false;

                    try {
                        // 创建所有分析请求
                        const analysisPromises = this.excelData.map((row, index) => 
                            this.analyzeSingleContent(row, index)
                        );

                        // 使用 Promise.allSettled 以确保即使某些请求失败也能继续
                        const results = await Promise.allSettled(analysisPromises);

                        // 处理成功的结果
                        const successResults = results
                            .filter(r => r.status === 'fulfilled')
                            .map(r => r.value);

                        const failedCount = results.filter(r => r.status === 'rejected').length;
                        
                        if (failedCount > 0) {
                            alert(`${failedCount} 条记录分析失败，将显示成功的结果`);
                        }

                        if (successResults.length === 0) {
                            throw new Error('所有记录分析失败');
                        }

                        // 处理结果
                        this.processProfileResults(successResults);

                    } catch (error) {
                        console.error('分析失败:', error);
                        alert('分析过程中出现错误，请重试');
                    } finally {
                        this.isAnalyzing = false;
                    }
                },

                // 分析单条内容
                async analyzeSingleContent(row, index) {
                    const vm = this;
                    const datajson = {
                        "systemPrompt": "你是一个专业的用户情感分析师，请对以下文章内容进行深入的情感分析，并按照以下步骤执行任务：第一步：理解文章整体情绪通读全文，识别作者的情绪基调（积极、中性、消极、混合等），并注意文中出现的关键人物、事件、观点或问题。第二步：提取核心主题词请从文章中总结出3-5个最能代表其主要内容和情感焦点的主题词。要求：主题词应具有代表性，避免过于宽泛，每个主题词应聚焦于具体对象或概念按照相关性排序，第一个为主题焦点。第三步：情感评分请对每个主题词进行情感评分，依据其在文中的表达强度和倾向性，使用以下评分标准：（4=强烈正面 3=正面 2=中性 1=负面 0=强烈负面）并严格按照以下要求输出：必须输出纯JSON格式，不包含任何额外内容（如解释、说明、换行等）。JSON结构：示例輸出{'主题1': '公共安全', '主题1等级': 3, '主题2': '应急管理', '主题2等级': 3, '主题3': '灾害救援', '主题3等级': 3,'主题4': '经济高质量发展', '主题4等级': 3}",
                        "document": row.content
                    };

                    return new Promise((resolve, reject) => {
                        $.ajax({
                            url: "/api/analysis",
                            method: "post",
                            dataType: "json",
                            contentType: "application/json",
                            data: JSON.stringify(datajson),
                            success: function(data) {
                                // 更新进度
                                vm.currentAnalyzing = index + 1;
                                vm.analysisProgress = ((index + 1) / vm.excelData.length) * 100;

                                // 解析返回的数据
                                const themes = [];
                                const scores = [];
                                const keys = Object.keys(data);
                                const themeNumbers = [];

                                // 找出所有的主题编号
                                keys.forEach(key => {
                                    const match = key.match(/^主题(\d+)$/);
                                    if (match) {
                                        themeNumbers.push(parseInt(match[1]));
                                    }
                                });

                                // 按编号排序
                                themeNumbers.sort((a, b) => a - b);

                                // 提取主题和分数
                                themeNumbers.forEach(num => {
                                    const themeKey = `主题${num}`;
                                    const scoreKey = `主题${num}等级`;

                                    if (data[themeKey] && data[scoreKey] !== undefined) {
                                        themes.push(data[themeKey]);
                                        scores.push(data[scoreKey]);
                                    }
                                });

                                // 返回结果
                                resolve({
                                    date: row.date,
                                    content: row.content,
                                    themes: themes,
                                    scores: scores,
                                    avgScore: scores.length > 0 ? scores.reduce((a, b) => a + b) / scores.length : 0
                                });
                            },
                            error: function(error) {
                                console.error(`分析第${index + 1}条记录失败:`, error);
                                reject(error);
                            }
                        });
                    });
                },

                // 处理分析结果
                processProfileResults(results) {
                    if (!results || results.length === 0) return;
                
                    // 排序结果（按日期）- 改进日期排序
                    results.sort((a, b) => {
                        const dateA = new Date(a.date);
                        const dateB = new Date(b.date);
                        return dateA - dateB;
                    });
                
                    // 计算日期范围 - 格式化显示
                    this.profileResults.dateRange = {
                        start: this.formatDateForDisplay(results[0].date),
                        end: this.formatDateForDisplay(results[results.length - 1].date)
                    };
                    this.profileResults.totalRecords = results.length;
                
                    // 准备趋势数据 - 格式化图表显示的日期
                    this.profileResults.emotionTrend = results.map(r => ({
                        date: this.formatDateForChart(r.date),
                        avgScore: r.avgScore
                    }));

                    // 计算情感分布
                    const distribution = { 0: 0, 1: 0, 2: 0, 3: 0, 4: 0 };
                    results.forEach(r => {
                        r.scores.forEach(score => {
                            distribution[score]++;
                        });
                    });
                    this.profileResults.emotionDistribution = distribution;

                    // 准备详细表格数据
                    this.profileResults.detailTable = results.map(r => ({
                        date: r.date,
                        tags: r.themes,
                        avgScore: r.avgScore,
                        contentSummary: r.content.substring(0, 50) + (r.content.length > 50 ? '...' : '')
                    }));

                    // 显示结果
                    this.showProfileResults = true;

                    // 绘制图表
                    this.$nextTick(() => {
                        this.drawTrendChart();
                        this.drawDistributionChart();
                    });
                },
                
                formatDateForDisplay(dateStr) {
                    const date = new Date(dateStr);
                    if (isNaN(date.getTime())) return dateStr;
                    
                    return date.toLocaleDateString('zh-CN', {
                        year: 'numeric',
                        month: '2-digit',
                        day: '2-digit'
                    });
                },
                formatDateForChart(dateStr) {
                    const date = new Date(dateStr);
                    if (isNaN(date.getTime())) return dateStr;
                    
                    // 根据需要调整格式，比如显示月-日
                    return date.toLocaleDateString('zh-CN', {
                        month: '2-digit',
                        day: '2-digit'
                    });
                },
                
                // 绘制趋势图
                drawTrendChart() {
                    const ctx = document.getElementById('trendChart').getContext('2d');
                    
                    // 销毁已存在的图表
                    if (this.trendChart) {
                        this.trendChart.destroy();
                    }

                    this.trendChart = new Chart(ctx, {
                        type: 'line',
                        data: {
                            labels: this.profileResults.emotionTrend.map(item => item.date),
                            datasets: [{
                                label: '平均情感分数',
                                data: this.profileResults.emotionTrend.map(item => item.avgScore),
                                borderColor: '#4A90E2',
                                backgroundColor: 'rgba(74, 144, 226, 0.1)',
                                tension: 0.1,
                                pointRadius: 5,
                                pointHoverRadius: 7
                            }]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            plugins: {
                                title: {
                                    display: false
                                },
                                legend: {
                                    display: true,
                                    position: 'bottom'
                                }
                            },
                            scales: {
                                y: {
                                    beginAtZero: true,
                                    max: 4,
                                    ticks: {
                                        stepSize: 1,
                                        callback: function(value) {
                                            const labels = ['强烈负面', '负面', '中性', '正面', '强烈正面'];
                                            return labels[value] || value;
                                        }
                                    }
                                },
                                x: {
                                    ticks: {
                                        maxRotation: 45,
                                        minRotation: 45
                                    }
                                }
                            }
                        }
                    });
                },
                
                // 绘制分布图
                drawDistributionChart() {
                    const ctx = document.getElementById('distributionChart').getContext('2d');

                    // 销毁已存在的图表
                    if (this.distributionChart) {
                        this.distributionChart.destroy();
                    }

                    const distribution = this.profileResults.emotionDistribution;
                    const labels = ['强烈负面', '负面', '中性', '正面', '强烈正面'];
                    const data = [
                        distribution[0] || 0,
                        distribution[1] || 0,
                        distribution[2] || 0,
                        distribution[3] || 0,
                        distribution[4] || 0
                    ];

                    this.distributionChart = new Chart(ctx, {
                        type: 'doughnut',
                        data: {
                            labels: labels,
                            datasets: [{
                                data: data,
                                backgroundColor: [
                                    '#d32f2f',
                                    '#f57c00',
                                    '#757575',
                                    '#388e3c',
                                    '#1976d2'
                                ],
                                borderWidth: 2,
                                borderColor: '#fff'
                            }]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            plugins: {
                                legend: {
                                    display: true,
                                    position: 'right'
                                },
                                tooltip: {
                                    callbacks: {
                                        label: function(context) {
                                            const label = context.label || '';
                                            const value = context.parsed || 0;
                                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                            const percentage = total > 0 ? ((value / total) * 100).toFixed(1) : 0;
                                            return `${label}: ${value} (${percentage}%)`;
                                        }
                                    }
                                }
                            }
                        }
                    });
                }
            },
            mounted() {
                // 页面加载完成后的初始化操作
                console.log('应用已加载');
            },
            beforeUnmount() {
                // 清理图表实例
                if (this.trendChart) {
                    this.trendChart.destroy();
                }
                if (this.distributionChart) {
                    this.distributionChart.destroy();
                }
            }
        }).mount('#app');
    </script>
</body>
</html>
    '''


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3527, debug=False)