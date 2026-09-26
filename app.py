import os
from flask import Flask, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>فود یاب | کافه و رستوران </title>
    
    <!-- اسکریپت رسمی گوگل اختصاصی شما -->
    <script async src="https://cse.google.com/cse.js?cx=50ace54d7326e4e0d"></script>

    <style>
        :root {
            --primary: #FF4757;
            --primary-gradient: linear-gradient(135deg, #FF4757 0%, #FF6B81 50%, #FFA502 100%);
            --snapp-color: #FA0050;
            --bg-light: #F8F9FA;
            --card-bg: rgba(255, 255, 255, 0.9);
            --card-border: rgba(0, 0, 0, 0.08);
            --text-main: #1E293B;
            --text-muted: #64748B;
        }

        * { box-sizing: border-box; font-family: system-ui, -apple-system, sans-serif; margin: 0; padding: 0; }
        
        html, body {
            overflow-x: hidden !important;
            overflow-y: visible !important;
            height: auto !important;
            min-height: 100vh !important;
            touch-action: pan-y !important;
            -webkit-overflow-scrolling: touch !important;
        }

        body {
            background-color: #F8FAF8;
            background-image: 
                radial-gradient(circle at 10% 10%, rgba(255, 71, 87, 0.08) 0%, transparent 40%),
                radial-gradient(circle at 90% 20%, rgba(255, 165, 2, 0.12) 0%, transparent 45%),
                radial-gradient(circle at 50% 90%, rgba(250, 0, 80, 0.06) 0%, transparent 50%),
                linear-gradient(180deg, #FFFFFF 0%, #F1F5F9 100%);
            background-attachment: fixed;
            color: var(--text-main);
            padding: 25px 15px 120px 15px;
            display: flex;
            justify-content: center;
        }

        .container { width: 100%; max-width: 680px; }

        .header { text-align: center; margin-bottom: 25px; }
        .badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: #FFE8EC;
            color: var(--primary);
            border: 1px solid rgba(255, 71, 87, 0.2);
            padding: 6px 16px;
            border-radius: 30px;
            font-size: 13px;
            font-weight: 700;
            margin-bottom: 10px;
        }
        h1 {
            font-size: 34px;
            font-weight: 900;
            background: var(--primary-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 6px;
        }
        p.subtitle { color: var(--text-muted); font-size: 14px; }

        .mode-switch {
            display: flex;
            background: #E2E8F0;
            padding: 5px;
            border-radius: 20px;
            margin-bottom: 20px;
            gap: 6px;
        }
        .mode-btn {
            flex: 1;
            text-align: center;
            padding: 12px 10px;
            font-size: 14px;
            font-weight: bold;
            border-radius: 16px;
            cursor: pointer;
            color: var(--text-muted);
            transition: 0.25s;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }
        .mode-btn.active {
            background: white;
            color: var(--text-main);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        }
        .mode-btn.active.snapp {
            color: var(--snapp-color);
        }

        .search-panel {
            background: var(--card-bg);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--card-border);
            border-radius: 28px;
            padding: 24px;
            box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.06);
            margin-bottom: 25px;
        }

        .section-title {
            font-size: 13px;
            font-weight: 700;
            color: var(--text-main);
            margin-bottom: 8px;
            display: block;
        }

        .add-box { display: flex; gap: 8px; margin-bottom: 14px; }
        .add-box input {
            flex: 1;
            background: #F8FAFC;
            border: 1.5px solid #E2E8F0;
            border-radius: 14px;
            padding: 12px 14px;
            color: var(--text-main);
            font-size: 14px;
            outline: none;
            transition: 0.2s;
        }
        .add-box input:focus { border-color: var(--primary); background: white; }
        .add-btn {
            background: #10B981;
            color: white;
            border: none;
            padding: 0 18px;
            border-radius: 14px;
            font-weight: bold;
            cursor: pointer;
        }

        .pages-list {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 18px;
            max-height: 120px;
            overflow-y: auto;
        }
        .chip {
            background: #F1F5F9;
            border: 1px solid #E2E8F0;
            color: var(--text-main);
            padding: 7px 14px;
            border-radius: 20px;
            font-size: 13px;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .chip.active {
            background: var(--primary-gradient);
            color: white;
            border-color: transparent;
            font-weight: bold;
            box-shadow: 0 4px 12px rgba(255, 71, 87, 0.3);
        }
        .chip .del-btn { opacity: 0.6; font-size: 14px; margin-right: 4px; }

        .time-filter {
            display: flex;
            background: #F1F5F9;
            padding: 4px;
            border-radius: 14px;
            margin-bottom: 18px;
            gap: 4px;
        }
        .time-btn {
            flex: 1;
            text-align: center;
            padding: 8px 6px;
            font-size: 13px;
            border-radius: 10px;
            cursor: pointer;
            color: var(--text-muted);
        }
        .time-btn.active {
            background: white;
            color: var(--primary);
            font-weight: bold;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
        }

        .city-chips {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 16px;
        }
        .city-chip {
            background: #F1F5F9;
            border: 1px solid #E2E8F0;
            padding: 6px 14px;
            border-radius: 12px;
            font-size: 13px;
            cursor: pointer;
            font-weight: 500;
        }
        .city-chip.active {
            background: var(--snapp-color);
            color: white;
            border-color: var(--snapp-color);
            font-weight: bold;
        }

        .food-input {
            width: 100%;
            background: #F8FAFC;
            border: 1.5px solid #E2E8F0;
            border-radius: 16px;
            padding: 15px 16px;
            color: var(--text-main);
            font-size: 15px;
            outline: none;
            margin-bottom: 16px;
            transition: 0.2s;
        }
        .food-input:focus {
            border-color: var(--primary);
            background: white;
            box-shadow: 0 0 15px rgba(255, 71, 87, 0.15);
        }

        .search-btn {
            width: 100%;
            background: var(--primary-gradient);
            color: white;
            border: none;
            border-radius: 16px;
            padding: 16px;
            font-size: 16px;
            font-weight: 800;
            cursor: pointer;
            box-shadow: 0 10px 25px rgba(255, 71, 87, 0.3);
            transition: 0.2s;
        }
        .search-btn.snapp-btn {
            background: linear-gradient(135deg, #FA0050 0%, #FF3366 100%);
            box-shadow: 0 10px 25px rgba(250, 0, 80, 0.3);
        }
        .search-btn:active { transform: scale(0.98); }

        #resultsWrapper {
            width: 100%;
            margin-top: 25px;
        }

        /* ======================================================== */
        /* حذف قطعی گزینه‌های مزاحم و لینک Search on Google */
        /* ======================================================== */
        
        .gsc-search-box, 
        .gsc-tabsArea, 
        .gcse-search-box,
        .gsc-resultsHeader,
        .gsc-adBlock,
        .gsc-results-close-btn,
        .gsc-modal-background-image {
            display: none !important;
        }

        /* حذف واترمارک و متن برند گوگل */
        .gcsc-branding,
        .gcsc-branding-text,
        .gcsc-branding-img,
        .gcsc-branding-clickable,
        .gsc-branding,
        .gsc-branding-text,
        .gsc-branding-img {
            display: none !important;
            visibility: hidden !important;
            height: 0 !important;
            opacity: 0 !important;
        }

        /* حذف ۱۰۰٪ گزینه Search on Google که در عکس فرستادید */
        .gsc-results-search-on-google,
        .gsc-results-search-on-google-box,
        .gsc-results-search-on-google-container,
        #resultsWrapper a[href*="google.com/search"],
        #resultsWrapper a[href*="client=ms-google-coop"] {
            display: none !important;
            visibility: hidden !important;
            height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
            opacity: 0 !important;
            pointer-events: none !important;
        }

        .gsc-overflow-hidden {
            overflow: visible !important;
            position: static !important;
        }

        .gsc-results-wrapper-overlay, 
        .gsc-results-wrapper-nooverlay {
            position: static !important;
            width: 100% !important;
            height: auto !important;
            max-height: none !important;
            overflow: visible !important;
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            padding: 0 !important;
        }

        .gsc-control-cse {
            background: transparent !important;
            border: none !important;
            padding: 0 !important;
        }

        .gsc-webResult.gsc-result {
            background: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            border-radius: 20px !important;
            padding: 20px !important;
            margin-bottom: 16px !important;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04) !important;
            transition: 0.2s !important;
        }
        .gsc-webResult.gsc-result:hover {
            border-color: var(--primary) !important;
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08) !important;
        }

        .gs-title, .gs-title * {
            color: #E11D48 !important;
            font-size: 17px !important;
            font-weight: 800 !important;
            text-decoration: none !important;
            line-height: 1.5 !important;
        }
        .gs-snippet {
            color: #475569 !important;
            font-size: 14px !important;
            line-height: 1.7 !important;
            margin-top: 10px !important;
        }
        .gsc-url-top { padding: 0 !important; }
        .gs-visibleUrl {
            color: #059669 !important;
            font-size: 12px !important;
            font-weight: bold !important;
            margin-top: 6px !important;
            display: inline-block !important;
        }

        .gsc-cursor-box { margin: 35px 0 15px 0 !important; text-align: center !important; }
        .gsc-cursor-page {
            background: white !important;
            border: 1px solid #CBD5E1 !important;
            color: #334155 !important;
            padding: 10px 16px !important;
            border-radius: 12px !important;
            margin: 0 5px !important;
            font-size: 14px !important;
            font-weight: bold !important;
            display: inline-block !important;
        }
        .gsc-cursor-current-page {
            background: var(--primary) !important;
            color: white !important;
            border-color: var(--primary) !important;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <span class="badge">🍽️ فود یاب | خوراک</span>
            <h1>کافه و رستوران </h1>
            <p class="subtitle">یافتن سریع غذاها، منوها و آدرس رستوران‌ها</p>
        </div>

        <div class="mode-switch">
            <div class="mode-btn active" id="btn-insta" onclick="switchMode('insta')">
                <span>📸 اینستاگرام (فودبلاگرها)</span>
            </div>
            <div class="mode-btn" id="btn-snapp" onclick="switchMode('snapp')">
                <span>🛵 اسنپ‌فود (سفارش و منو)</span>
            </div>
        </div>

        <div class="search-panel">
            <div id="insta-fields">
                <span class="section-title">➕ افزودن فودبلاگر جدید:</span>
                <div class="add-box">
                    <input type="text" id="newPage" placeholder="مثال: شیراز یامی یا dina_taster">
                    <button class="add-btn" onclick="addNewPage()">افزودن</button>
                </div>

                <span class="section-title">🎯 انتخاب فودبلاگرها (همزمان):</span>
                <div class="pages-list" id="pagesContainer"></div>

                <span class="section-title">📅 بازه زمانی انتشار:</span>
                <div class="time-filter">
                    <div class="time-btn" id="time-m" onclick="setTime('m')">۱ ماه اخیر</div>
                    <div class="time-btn active" id="time-y" onclick="setTime('y')">۱ سال اخیر</div>
                    <div class="time-btn" id="time-all" onclick="setTime('all')">همه زمان‌ها</div>
                </div>
            </div>

            <div id="snapp-fields" style="display: none;">
                <span class="section-title">📍 انتخاب شهر شما:</span>
                <div class="city-chips">
                    <div class="city-chip active" onclick="setCity(this, 'شیراز')">شیراز</div>
                    <div class="city-chip" onclick="setCity(this, 'تهران')">تهران</div>
                    <div class="city-chip" onclick="setCity(this, 'اصفهان')">اصفهان</div>
                    <div class="city-chip" onclick="setCity(this, 'مشهد')">مشهد</div>
                    <div class="city-chip" onclick="setCity(this, 'تبریز')">تبریز</div>
                </div>
                <div class="add-box" style="margin-bottom: 18px;">
                    <input type="text" id="customCity" placeholder="یا نام شهر دیگر را تایپ کنید...">
                </div>
            </div>

            <span class="section-title">🍲 نام غذا یا دسر مورد نظر:</span>
            <input type="text" class="food-input" id="food" placeholder="مثال: شاورما، پیتزا، کباب کوبیده، پاستا..." onkeypress="handleKeyPress(event)">

            <button class="search-btn" id="mainSearchBtn" onclick="executeSmartSearch()">🔍 جستجوی هوشمند در پست‌های اینستاگرام</button>
        </div>

        <div id="resultsWrapper">
            <div class="gcse-searchresults-only" data-gname="foodyab_results" data-linktarget="_blank"></div>
        </div>
    </div>

    <script>
        let currentMode = 'insta';
        let selectedCity = 'شیراز';
        let savedPages = JSON.parse(localStorage.getItem('my_food_pages')) || ['شیراز یامی', 'milad_taster'];
        let selectedPages = new Set(['شیراز یامی']);
        let selectedTime = 'y';

        function switchMode(mode) {
            currentMode = mode;
            const btnInsta = document.getElementById('btn-insta');
            const btnSnapp = document.getElementById('btn-snapp');
            const instaFields = document.getElementById('insta-fields');
            const snappFields = document.getElementById('snapp-fields');
            const searchBtn = document.getElementById('mainSearchBtn');

            if (mode === 'insta') {
                btnInsta.className = 'mode-btn active';
                btnSnapp.className = 'mode-btn';
                instaFields.style.display = 'block';
                snappFields.style.display = 'none';
                searchBtn.className = 'search-btn';
                searchBtn.innerText = '🔍 جستجوی هوشمند در پست‌های اینستاگرام';
            } else {
                btnInsta.className = 'mode-btn';
                btnSnapp.className = 'mode-btn active snapp';
                instaFields.style.display = 'none';
                snappFields.style.display = 'block';
                searchBtn.className = 'search-btn snapp-btn';
                searchBtn.innerText = '🛵 جستجو در رستوران‌ها و منوهای اسنپ‌فود';
            }
        }

        function setCity(el, city) {
            selectedCity = city;
            document.querySelectorAll('.city-chip').forEach(c => c.classList.remove('active'));
            el.classList.add('active');
            document.getElementById('customCity').value = '';
        }

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
            if (e.key === 'Enter') executeSmartSearch();
        }

        function unlockGoogleScrollTrap() {
            let attempts = 0;
            const interval = setInterval(() => {
                attempts++;
                document.documentElement.style.setProperty('overflow', 'visible', 'important');
                document.body.style.setProperty('overflow', 'visible', 'important');
                document.body.classList.remove('gsc-overflow-hidden');

                const modal = document.querySelector('.gsc-modal-background-image');
                if (modal) modal.remove();

                const overlay = document.querySelector('.gsc-results-wrapper-overlay');
                if (overlay) {
                    overlay.style.setProperty('position', 'static', 'important');
                    overlay.style.setProperty('height', 'auto', 'important');
                    overlay.style.setProperty('overflow', 'visible', 'important');
                }

                // حذف فیزیکی لینک Search on Google
                document.querySelectorAll('#resultsWrapper a[href*="google.com/search"], .gsc-results-search-on-google').forEach(el => {
                    el.remove();
                });

                if (attempts > 30) clearInterval(interval);
            }, 100);
        }

        function executeSmartSearch() {
            const food = document.getElementById('food').value.trim();
            if (!food) {
                alert('لطفاً نام غذا را بنویسید!');
                return;
            }

            let finalQuery = '';

            if (currentMode === 'insta') {
                if (selectedPages.size === 0) {
                    alert('لطفاً حداقل یک پیج فودبلاگر را انتخاب کنید!');
                    return;
                }
                const pagesArray = Array.from(selectedPages);
                const pagesQuery = pagesArray.length === 1 ? `"${pagesArray[0]}"` : '(' + pagesArray.map(p => `"${p}"`).join(' OR ') + ')';

                let dateFilter = '';
                const now = new Date();
                if (selectedTime === 'm') {
                    const d = new Date(new Date().setDate(now.getDate() - 30));
                    dateFilter = `after:${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;
                } else if (selectedTime === 'y') {
                    const d = new Date(new Date().setFullYear(now.getFullYear() - 1));
                    dateFilter = `after:${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;
                }

                finalQuery = `site:instagram.com ${pagesQuery} ${food} ${dateFilter}`.trim();
            } else {
                const customCity = document.getElementById('customCity').value.trim();
                const city = customCity ? customCity : selectedCity;
                finalQuery = `site:snappfood.ir "${city}" ${food}`.trim();
            }

            const element = google.search.cse.element.getElement('foodyab_results');
            if (element) {
                element.execute(finalQuery);
                unlockGoogleScrollTrap();

                setTimeout(() => {
                    const resultsEl = document.getElementById('resultsWrapper');
                    if (resultsEl) resultsEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }, 600);
            } else {
                alert('در حال بارگذاری موتور جستجو... لطفاً دوباره دکمه را بزنید.');
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
