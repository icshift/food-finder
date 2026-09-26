import os
import urllib.parse
import urllib.request
import re
import html
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# موتور جستجوی ضد بلاک (استخراج ۱۰ الی ۱۵ نتیجه واقعی از بینگ و داک‌داک‌گو)
def fetch_instagram_posts(query):
    results = []
    
    # روش اول: استفاده از موتور بینگ (حساس به سرور ابری نیست و اینستاگرام را عالی ایندکس میکند)
    try:
        encoded_query = urllib.parse.quote(query)
        url = f"https://www.bing.com/search?q={encoded_query}&count=15"
        
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                'Accept-Language': 'fa-IR,fa;q=0.9,en-US;q=0.8,en;q=0.7'
            }
        )
        
        with urllib.request.urlopen(req, timeout=6) as response:
            page_html = response.read().decode('utf-8', errors='ignore')
            
            # استخراج بلاک‌های نتایج
            blocks = re.findall(r'<li class="b_algo".*?</li>', page_html, re.DOTALL)
            for block in blocks:
                # استخراج لینک اینستاگرام
                link_match = re.search(r'href="(https://[a-z0-9\.]*instagram\.com/[^"]+)"', block)
                if not link_match:
                    continue
                post_url = link_match.group(1)
                
                # استخراج تیتر
                title_match = re.search(r'<h2[^>]*><a[^>]*>(.*?)</a></h2>', block, re.DOTALL)
                title = "پست معرفی غذا در اینستاگرام"
                if title_match:
                    raw_title = re.sub(r'<[^>]+>', '', title_match.group(1))
                    title = html.unescape(raw_title).replace("• Instagram photos and videos", "").replace("on Instagram", "").replace("- Instagram", "").strip()
                
                # استخراج کپشن و آدرس
                desc_match = re.search(r'<p[^>]*>(.*?)</p>', block, re.DOTALL)
                desc = "برای مشاهده منو، عکس‌ها و آدرس دقیق روی دکمه مشاهده در اینستاگرام بزنید."
                if desc_match:
                    raw_desc = re.sub(r'<[^>]+>', '', desc_match.group(1))
                    desc = html.unescape(raw_desc).strip()
                
                results.append({
                    "url": post_url,
                    "title": title,
                    "desc": desc
                })
                
                if len(results) >= 15:
                    break
    except Exception as e:
        print("Search error:", e)

    return results

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>فود یاب هوشمند | موتور جستجوی خوراک</title>
    <style>
        :root {
            --primary: #FF5E3A;
            --primary-gradient: linear-gradient(135deg, #FF5E3A 0%, #FF2A54 50%, #C026D3 100%);
            --bg-dark: #0F172A;
            --card-bg: rgba(30, 41, 59, 0.75);
            --card-border: rgba(255, 255, 255, 0.1);
            --text-main: #F8FAFC;
            --text-muted: #94A3B8;
        }

        * { box-sizing: border-box; font-family: system-ui, -apple-system, sans-serif; margin: 0; padding: 0; }
        
        body {
            background-color: var(--bg-dark);
            background-image: 
                radial-gradient(at 0% 0%, rgba(255, 94, 58, 0.15) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(192, 38, 211, 0.15) 0px, transparent 50%);
            background-attachment: fixed;
            color: var(--text-main);
            min-height: 100vh;
            padding: 20px 15px 50px 15px;
            display: flex;
            justify-content: center;
        }

        .container { width: 100%; max-width: 680px; }

        .header { text-align: center; margin-bottom: 25px; }
        .badge {
            display: inline-block;
            background: rgba(255, 94, 58, 0.15);
            color: #FF5E3A;
            border: 1px solid rgba(255, 94, 58, 0.3);
            padding: 5px 14px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        h1 {
            font-size: 32px;
            font-weight: 900;
            background: var(--primary-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
        }
        p.subtitle { color: var(--text-muted); font-size: 14px; }

        .search-panel {
            background: var(--card-bg);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid var(--card-border);
            border-radius: 24px;
            padding: 22px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
            margin-bottom: 30px;
        }

        .section-title {
            font-size: 13px;
            font-weight: 700;
            color: var(--text-muted);
            margin-bottom: 8px;
            display: block;
        }

        .add-box { display: flex; gap: 8px; margin-bottom: 14px; }
        .add-box input {
            flex: 1;
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid var(--card-border);
            border-radius: 12px;
            padding: 12px;
            color: white;
            font-size: 14px;
            outline: none;
        }
        .add-box input:focus { border-color: #FF5E3A; }
        .add-btn {
            background: #10B981;
            color: white;
            border: none;
            padding: 0 16px;
            border-radius: 12px;
            font-weight: bold;
            cursor: pointer;
        }

        .pages-list {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 16px;
            max-height: 120px;
            overflow-y: auto;
        }
        .chip {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--card-border);
            color: var(--text-muted);
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 13px;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 6px;
            transition: 0.2s;
        }
        .chip.active {
            background: var(--primary-gradient);
            color: white;
            border-color: transparent;
            font-weight: bold;
            box-shadow: 0 4px 12px rgba(255, 94, 58, 0.3);
        }
        .chip .del-btn { opacity: 0.6; font-size: 14px; margin-right: 4px; }

        .time-filter {
            display: flex;
            background: rgba(15, 23, 42, 0.6);
            padding: 4px;
            border-radius: 12px;
            margin-bottom: 16px;
            gap: 4px;
        }
        .time-btn {
            flex: 1;
            text-align: center;
            padding: 8px;
            font-size: 13px;
            border-radius: 8px;
            cursor: pointer;
            color: var(--text-muted);
            transition: 0.2s;
        }
        .time-btn.active {
            background: rgba(255, 255, 255, 0.15);
            color: white;
            font-weight: bold;
        }

        .food-input {
            width: 100%;
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid var(--card-border);
            border-radius: 14px;
            padding: 14px;
            color: white;
            font-size: 15px;
            outline: none;
            margin-bottom: 14px;
        }
        .food-input:focus { border-color: #FF5E3A; }

        .search-btn {
            width: 100%;
            background: var(--primary-gradient);
            color: white;
            border: none;
            border-radius: 14px;
            padding: 16px;
            font-size: 16px;
            font-weight: 800;
            cursor: pointer;
            box-shadow: 0 10px 25px rgba(255, 94, 58, 0.35);
        }

        #loading {
            display: none;
            text-align: center;
            margin: 25px 0;
            font-weight: bold;
            color: #FF5E3A;
            font-size: 15px;
        }

        .results-header {
            font-size: 16px;
            font-weight: bold;
            margin: 20px 0 15px 0;
            color: var(--text-main);
        }
        .result-card {
            background: var(--card-bg);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid var(--card-border);
            border-radius: 18px;
            padding: 18px;
            margin-bottom: 14px;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .card-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .card-badge {
            background: rgba(255, 94, 58, 0.15);
            color: #FF5E3A;
            padding: 4px 10px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: bold;
        }
        .post-title {
            font-size: 15px;
            font-weight: 700;
            color: white;
            line-height: 1.5;
        }
        .post-desc {
            font-size: 13px;
            color: var(--text-muted);
            line-height: 1.6;
            background: rgba(0, 0, 0, 0.25);
            padding: 12px;
            border-radius: 10px;
            border-right: 3px solid #FF5E3A;
        }
        .card-action {
            margin-top: 5px;
            display: flex;
            justify-content: flex-end;
        }
        .insta-btn {
            background: var(--primary-gradient);
            color: white;
            text-decoration: none;
            padding: 9px 18px;
            border-radius: 10px;
            font-size: 13px;
            font-weight: bold;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }

        .more-images-box { text-align: center; margin-top: 25px; }
        .more-images-btn {
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid var(--card-border);
            color: white;
            text-decoration: none;
            padding: 14px 20px;
            border-radius: 14px;
            display: inline-block;
            font-size: 14px;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <span class="badge">🔥</span>
            <h1>فود یاب</h1>
            <p class="subtitle">یافتن مستقیم غذا و آدرس رستوران‌ها بدون گم شدن در تبلیغات</p>
        </div>

        <div class="search-panel">
            <span class="section-title">➕ افزودن فودبلاگر جدید:</span>
            <div class="add-box">
                <input type="text" id="newPage" placeholder="مثال: شیراز یامی یا dina_taster">
                <button class="add-btn" onclick="addNewPage()">افزودن</button>
            </div>

            <span class="section-title">🎯 انتخاب فودبلاگرها (چندتایی):</span>
            <div class="pages-list" id="pagesContainer"></div>

            <span class="section-title">📅 بازه زمانی:</span>
            <div class="time-filter">
                <div class="time-btn" id="time-m" onclick="setTime('m')">۱ ماه اخیر</div>
                <div class="time-btn active" id="time-y" onclick="setTime('y')">۱ سال اخیر</div>
                <div class="time-btn" id="time-all" onclick="setTime('all')">همه زمان‌ها</div>
            </div>

            <span class="section-title">🍲 نام غذا یا نوشیدنی:</span>
            <input type="text" class="food-input" id="food" placeholder="مثال: کباب کوبیده، شاورما، پیتزا، پاستا...">

            <button class="search-btn" onclick="startSearch()">🔍 دریافت ۱۰ تا ۱۵ پست برتر</button>

            <div id="loading">✨ در حال استخراج پست‌ها و آدرس‌ها...</div>
        </div>

        <div id="resultsArea"></div>
    </div>

    <script>
        let savedPages = JSON.parse(localStorage.getItem('my_food_pages')) || ['شیراز یامی', 'milad_taster'];
        let selectedPages = new Set(['شیراز یامی']);
        let selectedTime = 'y';

        function renderChips() {
            const container = document.getElementById('pagesContainer');
            container.innerHTML = '';
            savedPages.forEach(page => {
                const isSelected = selectedPages.has(page);
                const chip = document.createElement('div');
                chip.className = `chip ${isSelected ? 'active' : ''}`;
                chip.innerHTML = `
                    <span onclick="toggleSelect('${page}')">${page} ${isSelected ? '✓' : ''}</span>
                    <span class="del-btn" onclick="deletePage(event, '${page}')">×</span>
                `;
                container.appendChild(chip);
            });
            localStorage.setItem('my_food_pages', JSON.stringify(savedPages));
        }

        function toggleSelect(page) {
            if (selectedPages.has(page)) selectedPages.delete(page);
            else selectedPages.add(page);
            renderChips();
        }

        function addNewPage() {
            const input = document.getElementById('newPage');
            const val = input.value.trim().replace('@', '');
            if (val && !savedPages.includes(val)) {
                savedPages.push(val);
                selectedPages.add(val);
                input.value = '';
                renderChips();
            }
        }

        function deletePage(event, page) {
            event.stopPropagation();
            savedPages = savedPages.filter(p => p !== page);
            selectedPages.delete(page);
            renderChips();
        }

        function setTime(timeType) {
            selectedTime = timeType;
            document.querySelectorAll('.time-btn').forEach(btn => btn.classList.remove('active'));
            document.getElementById(`time-${timeType}`).classList.add('active');
        }

        async function startSearch() {
            const food = document.getElementById('food').value.trim();
            const resultsArea = document.getElementById('resultsArea');
            const loading = document.getElementById('loading');

            if (selectedPages.size === 0) {
                alert('لطفاً حداقل یک پیج را انتخاب کنید!');
                return;
            }
            if (!food) {
                alert('لطفاً نام غذا را بنویسید!');
                return;
            }

            resultsArea.innerHTML = '';
            loading.style.display = 'block';

            const pagesArray = Array.from(selectedPages);
            const queryParams = new URLSearchParams({
                pages: pagesArray.join(','),
                food: food,
                time: selectedTime
            });

            try {
                const resp = await fetch(`/api/search?${queryParams}`);
                const data = await resp.json();
                loading.style.display = 'none';

                if (!data.results || data.results.length === 0) {
                    resultsArea.innerHTML = `
                        <div class="result-card" style="text-align:center;">
                            <p style="color:var(--text-muted);">پستی با این مشخصات یافت نشد. می‌توانید آلبوم عکس‌ها را در زیر ببینید:</p>
                        </div>
                    `;
                } else {
                    let html = `
                        <div class="results-header">
                            <span>🎯 نتایج پیدا شده (${data.results.length} پست اختصاصی):</span>
                        </div>
                    `;

                    data.results.forEach((item, index) => {
                        html += `
                            <div class="result-card">
                                <div class="card-top">
                                    <span class="card-badge">📌 پست شماره ${index + 1}</span>
                                </div>
                                <div class="post-title">${item.title}</div>
                                <div class="post-desc">📍 <b>آدرس و جزئیات کپشن:</b><br>${item.desc}</div>
                                <div class="card-action">
                                    <a class="insta-btn" href="${item.url}" target="_blank" rel="noopener noreferrer">
                                        <span>مشاهده پست در اینستاگرام</span> ↗
                                    </a>
                                </div>
                            </div>
                        `;
                    });

                    resultsArea.innerHTML = html;
                }

                resultsArea.innerHTML += `
                    <div class="more-images-box">
                        <a class="more-images-btn" href="${data.images_url}" target="_blank" rel="noopener noreferrer">
                            🖼️ دیدن آلبوم عکس‌های بیشتر در گوگل
                        </a>
                    </div>
                `;

            } catch (err) {
                loading.style.display = 'none';
                alert('خطا در دریافت نتایج.');
            }
        }

        renderChips();
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/search')
def search_api():
    pages_param = request.args.get('pages', '')
    food = request.args.get('food', '')
    time_filter = request.args.get('time', 'y')
    
    pages = [p.strip() for p in pages_param.split(',') if p.strip()]
    if len(pages) == 1:
        pages_query = f'"{pages[0]}"'
    else:
        pages_query = '(' + ' OR '.join([f'"{p}"' for p in pages]) + ')'
        
    query = f'site:instagram.com {pages_query} {food}'
    
    # واکشی ۱۰ الی ۱۵ پست بدون سد بلاک گوگل
    results = fetch_instagram_posts(query)
    
    tbs_param = ""
    if time_filter == 'm':
        tbs_param = "&tbs=qdr:m"
    elif time_filter == 'y':
        tbs_param = "&tbs=qdr:y"
        
    encoded_q = urllib.parse.quote(query)
    images_url = f"https://www.google.com/search?q={encoded_q}&tbm=isch{tbs_param}"

    return jsonify({"results": results, "images_url": images_url})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
