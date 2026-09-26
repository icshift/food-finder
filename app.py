import os
from flask import Flask, request, jsonify, render_template_string
from googlesearch import search
import urllib.parse
import urllib.request
import re

app = Flask(__name__)

def get_instagram_preview(url):
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)'}
        )
        with urllib.request.urlopen(req, timeout=3) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            img_match = re.search(r'<meta property="og:image" content="([^"]+)"', html)
            desc_match = re.search(r'<meta property="og:description" content="([^"]+)"', html)
            
            img_url = img_match.group(1) if img_match else None
            description = desc_match.group(1) if desc_match else "مشاهده جزئیات و آدرس در اینستاگرام..."
            
            if description and "likes, " in description:
                parts = description.split(":", 1)
                if len(parts) > 1:
                    description = parts[1].strip().strip('"')
                    
            return img_url, description
    except:
        return None, "برای دیدن آدرس و جزئیات روی دکمه مشاهده بزنید."

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>فود یاب هوشمند</title>
    <style>
        * { box-sizing: border-box; font-family: system-ui, -apple-system, sans-serif; }
        body { background: #f0f2f5; margin: 0; padding: 15px; display: flex; justify-content: center; }
        .container { background: white; width: 100%; max-width: 480px; padding: 20px; border-radius: 24px; box-shadow: 0 10px 30px rgba(0,0,0,0.06); }
        h2 { text-align: center; color: #d62976; margin: 5px 0 15px 0; }
        .label-title { font-weight: bold; font-size: 13px; color: #4a5568; margin-bottom: 8px; display: block; }
        .add-box { display: flex; gap: 8px; margin-bottom: 12px; }
        .add-box input { flex: 1; padding: 10px 12px; border: 2px solid #e2e8f0; border-radius: 12px; font-size: 14px; outline: none; }
        .add-btn { background: #38a169; color: white; border: none; padding: 10px 16px; border-radius: 12px; font-weight: bold; cursor: pointer; }
        .pages-list { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 15px; max-height: 120px; overflow-y: auto; padding: 2px; }
        .chip { background: #edf2f7; border: 2px solid #cbd5e0; padding: 6px 12px; border-radius: 20px; font-size: 13px; cursor: pointer; display: flex; align-items: center; gap: 6px; user-select: none; }
        .chip.active { background: #d62976; color: white; border-color: #d62976; font-weight: bold; }
        .chip .del-btn { color: #888; font-weight: bold; margin-right: 4px; }
        .chip.active .del-btn { color: #ffe4e6; }
        .time-filter { display: flex; background: #edf2f7; padding: 4px; border-radius: 12px; margin-bottom: 15px; gap: 4px; }
        .time-btn { flex: 1; text-align: center; padding: 8px 4px; font-size: 13px; border-radius: 8px; cursor: pointer; color: #4a5568; font-weight: 500; transition: 0.2s; }
        .time-btn.active { background: white; color: #d62976; font-weight: bold; box-shadow: 0 2px 5px rgba(0,0,0,0.08); }
        .food-input { width: 100%; padding: 12px; border: 2px solid #e2e8f0; border-radius: 12px; font-size: 15px; outline: none; margin-bottom: 12px; }
        .food-input:focus { border-color: #d62976; }
        .search-btn { width: 100%; padding: 14px; background: linear-gradient(45deg, #f09433, #dc2743, #bc1888); color: white; border: none; border-radius: 12px; font-size: 16px; font-weight: bold; cursor: pointer; }
        #loading { display: none; text-align: center; margin: 15px 0; color: #d62976; font-weight: bold; }
        .results { margin-top: 20px; }
        .food-card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; overflow: hidden; margin-bottom: 16px; box-shadow: 0 4px 15px rgba(0,0,0,0.04); }
        .food-card img { width: 100%; height: 210px; object-fit: cover; background: #e2e8f0; display: block; }
        .card-body { padding: 14px; }
        .card-desc { font-size: 13px; color: #4a5568; line-height: 1.6; margin-bottom: 12px; max-height: 80px; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; }
        .card-footer { display: flex; justify-content: space-between; align-items: center; }
        .card-footer a { background: #d62976; color: white; text-decoration: none; padding: 8px 14px; border-radius: 8px; font-size: 13px; font-weight: bold; }
        .source-tag { font-size: 12px; color: #718096; background: #edf2f7; padding: 4px 8px; border-radius: 6px; }
        .images-btn { display: block; text-align: center; background: #4285f4; color: white; text-decoration: none; padding: 12px; border-radius: 12px; font-weight: bold; margin-top: 15px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>🍔 فود یاب هوشمند</h2>

        <span class="label-title">➕ افزودن پیج فودبلاگر:</span>
        <div class="add-box">
            <input type="text" id="newPage" placeholder="مثلاً: شیراز یامی یا milad_taster">
            <button class="add-btn" onclick="addNewPage()">افزودن</button>
        </div>

        <span class="label-title">🎯 انتخاب پیج‌ها:</span>
        <div class="pages-list" id="pagesContainer"></div>

        <span class="label-title">📅 بازه زمانی انتشار پست:</span>
        <div class="time-filter">
            <div class="time-btn" id="time-m" onclick="setTime('m')">۱ ماه اخیر</div>
            <div class="time-btn active" id="time-y" onclick="setTime('y')">۱ سال اخیر</div>
            <div class="time-btn" id="time-all" onclick="setTime('all')">همه زمان‌ها</div>
        </div>

        <span class="label-title">🍲 نام غذا:</span>
        <input type="text" class="food-input" id="food" placeholder="مثلاً: کباب کوبیده، شاورما، پیتزا">

        <button class="search-btn" onclick="startSearch()">🔍 جستجوی پیشرفته</button>

        <div id="loading">⏳ در حال آماده‌سازی اطلاعات و تصاویر...</div>
        <div class="results" id="results"></div>
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
            const resultsDiv = document.getElementById('results');
            const loading = document.getElementById('loading');

            if (selectedPages.size === 0) {
                alert('لطفاً حداقل یک پیج را انتخاب کنید!');
                return;
            }
            if (!food) {
                alert('نام غذا را بنویسید!');
                return;
            }

            resultsDiv.innerHTML = '';
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

                if (data.cards && data.cards.length > 0) {
                    data.cards.forEach((card, index) => {
                        const imgHtml = card.image ? `<img src="${card.image}" onerror="this.style.display='none'">` : '';
                        resultsDiv.innerHTML += `
                            <div class="food-card">
                                ${imgHtml}
                                <div class="card-body">
                                    <div class="card-desc">${card.desc}</div>
                                    <div class="card-footer">
                                        <span class="source-tag">📌 پست ${index + 1}</span>
                                        <a href="${card.url}" target="_blank">مشاهده در اینستاگرام</a>
                                    </div>
                                </div>
                            </div>
                        `;
                    });
                } else {
                    resultsDiv.innerHTML = '<p style="text-align:center; color:#718096;">برای دیدن نتایج مستقیم روی دکمه زیر بزنید:</p>';
                }

                resultsDiv.innerHTML += `
                    <a class="images-btn" href="${data.images_url}" target="_blank">
                        🖼️ مشاهده آلبوم تصاویر و پست‌ها
                    </a>
                `;

            } catch (err) {
                loading.style.display = 'none';
                alert('خطا در اتصال به سرور.');
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
    
    tbs_param = ""
    if time_filter == 'm':
        tbs_param = "&tbs=qdr:m"
    elif time_filter == 'y':
        tbs_param = "&tbs=qdr:y"
        
    cards = []
    try:
        links = list(search(query, num_results=6))
        for link in links:
            if "/p/" in link or "/reel/" in link:
                img_url, description = get_instagram_preview(link)
                cards.append({
                    "url": link,
                    "image": img_url,
                    "desc": description
                })
                if len(cards) >= 4:
                    break
    except Exception as e:
        print("Search error:", e)

    encoded_q = urllib.parse.quote(query)
    images_url = f"https://www.google.com/search?q={encoded_q}&tbm=isch{tbs_param}"

    return jsonify({"cards": cards, "images_url": images_url})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
