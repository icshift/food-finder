import os
from flask import Flask, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>فود یاب  |  جستجوی خوراک</title>
    
    <!-- اسکریپت رسمی گوگل اختصاصی شما -->
    <script async src="https://cse.google.com/cse.js?cx=50ace54d7326e4e0d"></script>

    <style>
        :root {
            --primary: #FF5E3A;
            --primary-gradient: linear-gradient(135deg, #FF6B4A 0%, #FF2A54 50%, #C026D3 100%);
            --accent-warm: #F59E0B;
            --bg-base: #0B0F19;
            --card-glass: rgba(22, 29, 47, 0.85);
            --card-border: rgba(255, 255, 255, 0.12);
            --text-main: #F8FAFC;
            --text-muted: #94A3B8;
        }

        * { box-sizing: border-box; font-family: system-ui, -apple-system, sans-serif; margin: 0; padding: 0; }
        
        /* باز کردن کامل و اجباری اسکرول در سطح کل صفحه */
        html, body {
            overflow-x: hidden !important;
            overflow-y: visible !important;
            height: auto !important;
            min-height: 100vh !important;
            position: static !important;
            touch-action: pan-y !important;
            -webkit-overflow-scrolling: touch !important;
        }

        body {
            background-color: var(--bg-base);
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(245, 158, 11, 0.18) 0%, transparent 40%),
                radial-gradient(circle at 90% 10%, rgba(255, 94, 58, 0.22) 0%, transparent 45%),
                radial-gradient(circle at 50% 80%, rgba(192, 38, 211, 0.15) 0%, transparent 50%),
                linear-gradient(180deg, #0B0F19 0%, #111827 100%);
            background-attachment: fixed;
            color: var(--text-main);
            padding: 25px 15px 120px 15px;
            display: flex;
            justify-content: center;
        }

        .container { width: 100%; max-width: 680px; position: static !important; }

        .header { text-align: center; margin-bottom: 25px; }
        .badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(245, 158, 11, 0.15);
            color: #FBBF24;
            border: 1px solid rgba(245, 158, 11, 0.3);
            padding: 6px 16px;
            border-radius: 30px;
            font-size: 13px;
            font-weight: 700;
            margin-bottom: 12px;
        }
        h1 {
            font-size: 34px;
            font-weight: 900;
            background: linear-gradient(135deg, #FFF 20%, #FBBF24 50%, #FF5E3A 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
        }
        p.subtitle { color: var(--text-muted); font-size: 14px; }

        .search-panel {
            background: var(--card-glass);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--card-border);
            border-radius: 28px;
            padding: 24px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            margin-bottom: 25px;
            position: relative;
            z-index: 10;
        }

        .section-title {
            font-size: 13px;
            font-weight: 700;
            color: #CBD5E1;
            margin-bottom: 8px;
            display: block;
        }

        .add-box { display: flex; gap: 8px; margin-bottom: 14px; }
        .add-box input {
            flex: 1;
            background: rgba(11, 15, 25, 0.7);
            border: 1px solid var(--card-border);
            border-radius: 14px;
            padding: 12px 14px;
            color: white;
            font-size: 14px;
            outline: none;
        }
        .add-box input:focus { border-color: var(--accent-warm); }
        .add-btn {
            background: linear-gradient(135deg, #10B981 0%, #059669 100%);
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
            background: rgba(255, 255, 255, 0.06);
            border: 1px solid var(--card-border);
            color: #CBD5E1;
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
            box-shadow: 0 4px 14px rgba(255, 94, 58, 0.35);
        }
        .chip .del-btn { opacity: 0.6; font-size: 14px; margin-right: 4px; }

        .time-filter {
            display: flex;
            background: rgba(11, 15, 25, 0.7);
            padding: 5px;
            border-radius: 16px;
            margin-bottom: 18px;
            gap: 5px;
            border: 1px solid var(--card-border);
        }
        .time-btn {
            flex: 1;
            text-align: center;
            padding: 9px 6px;
            font-size: 13px;
            border-radius: 12px;
            cursor: pointer;
            color: var(--text-muted);
        }
        .time-btn.active {
            background: rgba(255, 255, 255, 0.15);
            color: #FFF;
            font-weight: bold;
        }

        .food-input {
            width: 100%;
            background: rgba(11, 15, 25, 0.7);
            border: 1px solid var(--card-border);
            border-radius: 16px;
            padding: 15px 16px;
            color: white;
            font-size: 15px;
            outline: none;
            margin-bottom: 16px;
        }
        .food-input:focus { border-color: #FF5E3A; }

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
            box-shadow: 0 12px 28px rgba(255, 94, 58, 0.4);
        }

        /* ظرف اصلی نتایج */
        #resultsWrapper {
            width: 100%;
            margin-top: 25px;
            position: relative;
            z-index: 5;
        }

        /* ======================================================== */
        /* استایل‌های اجباری برای شکستن قفل اسکرول گوگل */
        /* ======================================================== */
        
        .gsc-search-box, 
        .gsc-tabsArea, 
        .gcse-search-box,
        .gsc-resultsHeader,
        .gsc-adBlock,
        .gsc-results-close-btn {
            display: none !important;
        }

        /* حذف پرده سیاه مزاحم */
        .gsc-modal-background-image {
            display: none !important;
            visibility: hidden !important;
            pointer-events: none !important;
            height: 0 !important;
            width: 0 !important;
        }

        /* باز کردن قفل اسکرول ریشه */
        .gsc-overflow-hidden {
            overflow: visible !important;
            position: static !important;
            height: auto !important;
        }

        /* کارت‌ها به صورت کامل در صفحه جریان پیدا کنند */
        .gsc-results-wrapper-overlay, 
        .gsc-results-wrapper-nooverlay {
            position: static !important;
            top: auto !important;
            left: auto !important;
            right: auto !important;
            bottom: auto !important;
            width: 100% !important;
            height: auto !important;
            max-height: none !important;
            overflow: visible !important;
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            padding: 0 !important;
            margin: 0 !important;
            z-index: 1 !important;
        }

        .gsc-control-cse {
            background: transparent !important;
            border: none !important;
            padding: 0 !important;
            width: 100% !important;
        }

        /* کارت‌های زیبای غذا */
        .gsc-webResult.gsc-result {
            background: var(--card-glass) !important;
            backdrop-filter: blur(16px) !important;
            -webkit-backdrop-filter: blur(16px) !important;
            border: 1px solid var(--card-border) !important;
            border-radius: 20px !important;
            padding: 20px !important;
            margin-bottom: 16px !important;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3) !important;
        }

        .gs-title, .gs-title * {
            color: #FF7A59 !important;
            font-size: 17px !important;
            font-weight: 800 !important;
            text-decoration: none !important;
            line-height: 1.5 !important;
        }
        .gs-snippet {
            color: #94A3B8 !important;
            font-size: 14px !important;
            line-height: 1.7 !important;
            margin-top: 10px !important;
        }
        .gsc-url-top { padding: 0 !important; }
        .gs-visibleUrl {
            color: #10B981 !important;
            font-size: 12px !important;
            font-weight: bold !important;
            margin-top: 6px !important;
            display: inline-block !important;
        }

        /* دکمه‌های صفحه بعد */
        .gsc-cursor-box {
            margin: 35px 0 !important;
            text-align: center !important;
        }
        .gsc-cursor-page {
            background: rgba(255, 255, 255, 0.1) !important;
            border: 1px solid var(--card-border) !important;
            color: white !important;
            padding: 10px 16px !important;
            border-radius: 12px !important;
            margin: 0 5px !important;
            font-size: 14px !important;
            font-weight: bold !important;
            display: inline-block !important;
        }
        .gsc-cursor-current-page {
            background: var(--primary-gradient) !important;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <span class="badge">🍽️ فود یاب اینستاگرام</span>
            <h1>کافه و رستوران یاب</h1>
            <p class="subtitle">یافتن مستقیم غذاها، منوها و آدرس رستوران‌ها </p>
        </div>

        <div class="search-panel">
            <span class="section-title">➕ افزودن فودبلاگر جدید:</span>
            <div class="add-box">
                <input type="text" id="newPage" placeholder="مثال: شیراز یامی یا dina_taster">
                <button class="add-btn" onclick="addNewPage()">افزودن</button>
            </div>

            <span class="section-title">🎯 انتخاب فودبلاگرها (جستجوی همزمان):</span>
            <div class="pages-list" id="pagesContainer"></div>

            <span class="section-title">📅 بازه زمانی:</span>
            <div class="time-filter">
                <div class="time-btn" id="time-m" onclick="setTime('m')">۱ ماه اخیر</div>
                <div class="time-btn active" id="time-y" onclick="setTime('y')">۱ سال اخیر</div>
                <div class="time-btn" id="time-all" onclick="setTime('all')">همه زمان‌ها</div>
            </div>

            <span class="section-title">🍲 نام غذا یا نوشیدنی:</span>
            <input type="text" class="food-input" id="food" placeholder="مثال: شاورما، کباب، پیتزا..." onkeypress="handleKeyPress(event)">

            <button class="search-btn" onclick="executeGoogleSearch()">🔍 جستجوی هوشمند در پست‌ها</button>
        </div>

        <!-- کادر نتایج با اسکرول نامحدود -->
        <div id="resultsWrapper">
            <div class="gcse-searchresults-only" data-gname="foodyab_results" data-linktarget="_blank"></div>
        </div>
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

        function handleKeyPress(e) {
            if (e.key === 'Enter') {
                executeGoogleSearch();
            }
        }

        // تابع شکستن قطعی قفل اسکرول گوگل
        function unlockGoogleScrollTrap() {
            let attempts = 0;
            const interval = setInterval(() => {
                attempts++;
                
                // ۱. باز کردن اجباری اسکرول در تمام ریشه‌ها
                document.documentElement.style.setProperty('overflow', 'visible', 'important');
                document.documentElement.style.setProperty('position', 'static', 'important');
                document.body.style.setProperty('overflow', 'visible', 'important');
                document.body.style.setProperty('position', 'static', 'important');
                document.body.classList.remove('gsc-overflow-hidden');

                // ۲. حذف فیزیکی پرده مزاحم گوگل
                const modal = document.querySelector('.gsc-modal-background-image');
                if (modal) {
                    modal.style.display = 'none';
                    modal.remove();
                }

                // ۳. آزاد کردن کانتینر نتایج
                const overlay = document.querySelector('.gsc-results-wrapper-overlay');
                if (overlay) {
                    overlay.style.setProperty('position', 'static', 'important');
                    overlay.style.setProperty('height', 'auto', 'important');
                    overlay.style.setProperty('overflow', 'visible', 'important');
                }

                if (attempts > 30) {
                    clearInterval(interval);
                }
            }, 100);
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

            const pagesArray = Array.from(selectedPages);
            let pagesQuery = '';
            if (pagesArray.length === 1) {
                pagesQuery = `"${pagesArray[0]}"`;
            } else {
                pagesQuery = '(' + pagesArray.map(p => `"${p}"`).join(' OR ') + ')';
            }

            let dateFilter = '';
            const now = new Date();
            if (selectedTime === 'm') {
                const d = new Date(new Date().setDate(now.getDate() - 30));
                const yyyy = d.getFullYear();
                const mm = String(d.getMonth() + 1).padStart(2, '0');
                const dd = String(d.getDate()).padStart(2, '0');
                dateFilter = `after:${yyyy}-${mm}-${dd}`;
            } else if (selectedTime === 'y') {
                const d = new Date(new Date().setFullYear(now.getFullYear() - 1));
                const yyyy = d.getFullYear();
                const mm = String(d.getMonth() + 1).padStart(2, '0');
                const dd = String(d.getDate()).padStart(2, '0');
                dateFilter = `after:${yyyy}-${mm}-${dd}`;
            }

            const finalQuery = `${pagesQuery} ${food} ${dateFilter}`.trim();

            const element = google.search.cse.element.getElement('foodyab_results');
            if (element) {
                element.execute(finalQuery);
                
                // شکستن قفل اسکرول بلافاصله پس از سرچ
                unlockGoogleScrollTrap();

                // هدایت نرم صفحه به سمت نتایج
                setTimeout(() => {
                    const resultsEl = document.getElementById('resultsWrapper');
                    if (resultsEl) {
                        resultsEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    }
                }, 600);
            } else {
                alert('موتور جستجو در حال آماده‌سازی است، لطفاً دوباره امتحان کنید.');
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
