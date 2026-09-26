import os
from flask import Flask, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>فود یاب  | جستجوی خوراک و رستوران و کافه </title>
    
    <!-- اسکریپت رسمی موتور اختصاصی شما -->
    <script async src="https://cse.google.com/cse.js?cx=50ace54d7326e4e0d"></script>

    <style>
        :root {
            --primary: #FF5E3A;
            --primary-gradient: linear-gradient(135deg, #FF5E3A 0%, #FF2A54 50%, #C026D3 100%);
            --bg-dark: #0F172A;
            --card-bg: rgba(30, 41, 59, 0.85);
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
            padding: 20px 15px 60px 15px;
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
            margin-bottom: 25px;
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

        /* کلیدهای انتخاب زمان */
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

        /* شکستن پاپ‌آپ سفید گوگل و تبدیل به کارت‌های درون‌صفحه‌ای شیک */
        .gsc-modal-background-image {
            display: none !important; /* حذف پرده سیاه/سفید پشت پاپ‌آپ */
        }
        .gsc-results-wrapper-overlay {
            position: relative !important;
            top: auto !important;
            left: auto !important;
            width: 100% !important;
            max-width: 100% !important;
            height: auto !important;
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            padding: 0 !important;
            margin-top: 20px !important;
            z-index: 1 !important;
        }
        .gsc-results-close-btn {
            display: none !important; /* حذف ضربدر بستن پاپ‌آپ */
        }
        .gsc-overflow-hidden {
            overflow: visible !important; /* رفع قفل شدن اسکرول صفحه */
        }
        .gsc-control-cse {
            background: transparent !important;
            border: none !important;
            padding: 0 !important;
        }
        .gsc-webResult.gsc-result {
            background: var(--card-bg) !important;
            backdrop-filter: blur(12px) !important;
            border: 1px solid var(--card-border) !important;
            border-radius: 18px !important;
            padding: 16px !important;
            margin-bottom: 14px !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2) !important;
        }
        .gsc-webResult.gsc-result:hover {
            border-color: rgba(255, 94, 58, 0.4) !important;
            transform: translateY(-2px);
        }
        .gs-title, .gs-title * {
            color: #FF5E3A !important;
            font-size: 16px !important;
            font-weight: bold !important;
            text-decoration: none !important;
        }
        .gs-snippet {
            color: var(--text-muted) !important;
            font-size: 13px !important;
            line-height: 1.6 !important;
            margin-top: 8px !important;
        }
        .gsc-url-top { padding: 0 !important; }
        .gs-visibleUrl { color: #10B981 !important; font-size: 12px !important; }
        .gsc-cursor-box { margin-top: 20px !important; text-align: center !important; }
        .gsc-cursor-page {
            background: rgba(255, 255, 255, 0.1) !important;
            color: white !important;
            padding: 6px 12px !important;
            border-radius: 8px !important;
            margin: 0 4px !important;
        }
        .gsc-cursor-current-page { background: #FF5E3A !important; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <span class="badge">🔥</span>
            <h1>فود یاب</h1>
            <p class="subtitle">یافتن مستقیم غذا و آدرس رستوران‌ها در اینستاگرام</p>
        </div>

        <div class="search-panel">
            <span class="section-title">➕ افزودن فودبلاگر جدید:</span>
            <div class="add-box">
                <input type="text" id="newPage" placeholder="مثال: شیراز یامی یا dina_taster">
                <button class="add-btn" onclick="addNewPage()">افزودن</button>
            </div>

            <span class="section-title">🎯 انتخاب فودبلاگرها (چندتایی):</span>
            <div class="pages-list" id="pagesContainer"></div>

            <span class="section-title">📅 بازه زمانی انتشار:</span>
            <div class="time-filter">
                <div class="time-btn" id="time-m" onclick="setTime('m')">۱ ماه اخیر</div>
                <div class="time-btn active" id="time-y" onclick="setTime('y')">۱ سال اخیر</div>
                <div class="time-btn" id="time-all" onclick="setTime('all')">همه زمان‌ها</div>
            </div>

            <span class="section-title">🍲 نام غذا یا نوشیدنی:</span>
            <input type="text" class="food-input" id="food" placeholder="مثال: کباب کوبیده، شاورما، پیتزا، پاستا..." onkeypress="handleKeyPress(event)">

            <button class="search-btn" onclick="executeGoogleSearch()">🔍 جستجوی پست‌های جدید</button>
        </div>

        <!-- محل چیده شدن کارت‌ها دقیقا زیر پنل (بدون پاپ‌آپ) -->
        <div id="resultsWrapper">
            <div class="gcse-searchresults-only" data-gname="foodyab_results" data-linktarget="_blank"></div>
        </div>
    </div>

    <script>
        let savedPages = JSON.parse(localStorage.getItem('my_food_pages')) || ['شیراز یامی', 'milad_taster'];
        let selectedPages = new Set(['شیراز یامی']);
        let selectedTime = 'y'; // پیش‌فرض: یک سال اخیر

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

        function handleKeyPress(e) {
            if (e.key === 'Enter') {
                executeGoogleSearch();
            }
        }

        function executeGoogleSearch() {
            const food = document.getElementById('food').value.trim();

            if (selectedPages.size === 0) {
                alert('لطفاً حداقل یک پیج را انتخاب کنید!');
                return;
            }
            if (!food) {
                alert('لطفاً نام غذا را بنویسید!');
                return;
            }

            // ترکیب پیج‌ها
            const pagesArray = Array.from(selectedPages);
            let pagesQuery = '';
            if (pagesArray.length === 1) {
                pagesQuery = `"${pagesArray[0]}"`;
            } else {
                pagesQuery = '(' + pagesArray.map(p => `"${p}"`).join(' OR ') + ')';
            }

            // محاسبه فیلتر تاریخ (حذف قطعی پست‌های قدیمی با بعد از فلان تاریخ)
            let dateFilter = '';
            const now = new Date();
            if (selectedTime === 'm') {
                // 30 روز گذشته
                const d = new Date(new Date().setDate(now.getDate() - 30));
                const yyyy = d.getFullYear();
                const mm = String(d.getMonth() + 1).padStart(2, '0');
                const dd = String(d.getDate()).padStart(2, '0');
                dateFilter = `after:${yyyy}-${mm}-${dd}`;
            } else if (selectedTime === 'y') {
                // 365 روز گذشته (1 سال اخیر)
                const d = new Date(new Date().setFullYear(now.getFullYear() - 1));
                const yyyy = d.getFullYear();
                const mm = String(d.getMonth() + 1).padStart(2, '0');
                const dd = String(d.getDate()).padStart(2, '0');
                dateFilter = `after:${yyyy}-${mm}-${dd}`;
            }

            // کوئری نهایی با کنترل دقیق تاریخ
            const finalQuery = `${pagesQuery} ${food} ${dateFilter}`.trim();

            const element = google.search.cse.element.getElement('foodyab_results');
            if (element) {
                element.execute(finalQuery);
            } else {
                alert('موتور جستجو در حال بارگذاری است، لطفاً مجدداً کلیک کنید.');
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

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
