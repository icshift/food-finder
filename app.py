import os
from flask import Flask, render_template_string, send_from_directory

app = Flask(__name__)

# مسیر فراخوانی عکس لوگو از مخزن گیت‌هاب
@app.route('/logo.png')
def serve_logo():
    return send_from_directory('.', 'logo.png')

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta name="theme-color" content="#FF4757">
    <link rel="icon" type="image/png" href="/logo.png">
    <title>فود یاب | موتور هوشمند جستجوی خوراک</title>

    <!-- فونت مدرن وزیرمتن -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">

    <!-- اسکریپت رسمی گوگل اختصاصی شما -->
    <script async src="https://cse.google.com/cse.js?cx=50ace54d7326e4e0d"></script>

    <style>
        :root {
            --primary: #FF4757;
            --primary-soft: rgba(255, 71, 87, 0.1);
            --primary-gradient: linear-gradient(135deg, #FF4757 0%, #FF6B81 55%, #FF8C42 100%);
            --insta-gradient: linear-gradient(135deg, #E1306C 0%, #FD1D1D 50%, #F77737 100%);
            --snapp-color: #FA0050;
            --snapp-gradient: linear-gradient(135deg, #FA0050 0%, #FF2E79 100%);
            --bg-main: #F8FAFC;
            --card-bg: rgba(255, 255, 255, 0.92);
            --border-color: #E2E8F0;
            --text-main: #0F172A;
            --text-secondary: #475569;
            --text-muted: #64748B;
            --radius-xl: 24px;
            --radius-lg: 16px;
            --radius-md: 12px;
        }

        * {
            box-sizing: border-box;
            font-family: 'Vazirmatn', system-ui, -apple-system, sans-serif;
            margin: 0;
            padding: 0;
            -webkit-tap-highlight-color: transparent;
        }

        html, body {
            overflow-x: hidden !important;
            overflow-y: visible !important;
            height: auto !important;
            min-height: 100vh !important;
            touch-action: pan-y !important;
            -webkit-overflow-scrolling: touch !important;
        }

        body {
            background-color: var(--bg-main);
            background-image:
                radial-gradient(at 0% 0%, rgba(255, 71, 87, 0.09) 0px, transparent 50%),
                radial-gradient(at 100% 10%, rgba(255, 165, 2, 0.10) 0px, transparent 45%),
                radial-gradient(at 50% 100%, rgba(250, 0, 80, 0.06) 0px, transparent 50%);
            background-attachment: fixed;
            color: var(--text-main);
            padding: 18px 14px 50px 14px;
            display: flex;
            justify-content: center;
        }

        .container {
            width: 100%;
            max-width: 660px;
        }

        /* Toast Notification */
        .toast {
            position: fixed;
            top: 20px;
            left: 50%;
            transform: translateX(-50%) translateY(-100px);
            background: #1E293B;
            color: #FFFFFF;
            padding: 12px 20px;
            border-radius: 14px;
            font-size: 13px;
            font-weight: 600;
            box-shadow: 0 12px 30px rgba(15, 23, 42, 0.25);
            z-index: 9999;
            opacity: 0;
            transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
            display: flex;
            align-items: center;
            gap: 8px;
            max-width: 90%;
            text-align: center;
        }
        .toast.show {
            transform: translateX(-50%) translateY(0);
            opacity: 1;
        }

        /* هدر */
        .header {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 14px;
            margin-bottom: 18px;
            padding: 4px 0;
        }
        .logo-wrapper {
            position: relative;
            flex-shrink: 0;
        }
        .main-logo {
            width: 68px;
            height: 68px;
            object-fit: cover;
            border-radius: 20px;
            box-shadow: 0 10px 25px rgba(255, 71, 87, 0.16);
            border: 2.5px solid #FFFFFF;
            display: block;
            background: #FFF;
        }
        .header-text {
            text-align: right;
        }
        .brand-row {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 3px;
        }
        .brand-title {
            font-size: 22px;
            font-weight: 900;
            letter-spacing: -0.5px;
            background: var(--primary-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .brand-badge {
            font-size: 10px;
            font-weight: 700;
            background: var(--primary-soft);
            color: var(--primary);
            padding: 3px 8px;
            border-radius: 99px;
        }
        p.subtitle {
            color: var(--text-muted);
            font-size: 13px;
            font-weight: 500;
        }

        /* سوییچ حالت اینستاگرام / اسنپ‌فود */
        .mode-switch {
            display: grid;
            grid-template-columns: 1fr 1fr;
            background: #E2E8F0;
            padding: 5px;
            border-radius: 18px;
            margin-bottom: 16px;
            gap: 6px;
        }
        .mode-btn {
            border: none;
            background: transparent;
            text-align: center;
            padding: 11px 10px;
            font-size: 13.5px;
            font-weight: 700;
            border-radius: 14px;
            cursor: pointer;
            color: var(--text-secondary);
            transition: all 0.25s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }
        .mode-btn svg {
            width: 18px;
            height: 18px;
            flex-shrink: 0;
        }
        .mode-btn.active {
            background: #FFFFFF;
            color: var(--text-main);
            box-shadow: 0 4px 14px rgba(15, 23, 42, 0.08);
        }
        .mode-btn.active.insta { color: #E1306C; }
        .mode-btn.active.snapp { color: var(--snapp-color); }

        /* پنل اصلی جستجو */
        .search-panel {
            background: var(--card-bg);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.9);
            border-radius: var(--radius-xl);
            padding: 20px;
            box-shadow: 0 20px 45px -15px rgba(15, 23, 42, 0.08), 0 0 0 1px rgba(226, 232, 240, 0.6);
            margin-bottom: 22px;
        }

        /* باکس اصلی جستجوی غذا */
        .food-search-box {
            position: relative;
            margin-bottom: 10px;
        }
        .food-input {
            width: 100%;
            background: #F8FAFC;
            border: 2px solid var(--border-color);
            border-radius: var(--radius-lg);
            padding: 14px 44px 14px 40px;
            color: var(--text-main);
            font-size: 15px;
            font-weight: 600;
            outline: none;
            transition: all 0.2s ease;
        }
        .food-input::placeholder {
            color: #94A3B8;
            font-weight: 400;
        }
        .food-input:focus {
            border-color: var(--primary);
            background: #FFFFFF;
            box-shadow: 0 0 0 4px rgba(255, 71, 87, 0.12);
        }
        body.snapp-mode .food-input:focus {
            border-color: var(--snapp-color);
            box-shadow: 0 0 0 4px rgba(250, 0, 80, 0.12);
        }
        .search-icon-right {
            position: absolute;
            right: 14px;
            top: 50%;
            transform: translateY(-50%);
            color: #94A3B8;
            pointer-events: none;
            display: flex;
        }
        .clear-input-btn {
            position: absolute;
            left: 12px;
            top: 50%;
            transform: translateY(-50%);
            width: 24px;
            height: 24px;
            border-radius: 50%;
            border: none;
            background: #E2E8F0;
            color: #475569;
            font-size: 14px;
            cursor: pointer;
            display: none;
            align-items: center;
            justify-content: center;
        }
        .clear-input-btn.visible { display: flex; }

        /* چیپ‌های پیشنهاد سریع غذا */
        .quick-foods {
            display: flex;
            align-items: center;
            gap: 6px;
            overflow-x: auto;
            padding-bottom: 4px;
            margin-bottom: 16px;
            scrollbar-width: none;
        }
        .quick-foods::-webkit-scrollbar { display: none; }
        .quick-food-tag {
            flex-shrink: 0;
            background: #F1F5F9;
            border: 1px solid transparent;
            color: var(--text-secondary);
            padding: 5px 11px;
            border-radius: 99px;
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            transition: 0.2s;
        }
        .quick-food-tag:hover {
            background: var(--primary-soft);
            color: var(--primary);
            border-color: rgba(255, 71, 87, 0.25);
        }

        .divider {
            height: 1px;
            background: #F1F5F9;
            margin: 14px 0 16px 0;
        }

        .section-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
            gap: 8px;
            flex-wrap: wrap;
        }
        .section-title {
            font-size: 13px;
            font-weight: 700;
            color: var(--text-main);
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .count-badge {
            background: var(--primary-soft);
            color: var(--primary);
            font-size: 11px;
            padding: 2px 9px;
            border-radius: 99px;
            font-weight: 700;
        }
        .mini-actions {
            display: flex;
            align-items: center;
            gap: 4px;
        }
        .text-btn {
            background: #F8FAFC;
            border: 1px solid #E2E8F0;
            color: var(--text-secondary);
            font-size: 11.5px;
            font-weight: 600;
            cursor: pointer;
            padding: 4px 9px;
            border-radius: 8px;
            transition: 0.2s;
        }
        .text-btn:hover {
            background: #F1F5F9;
            color: var(--primary);
            border-color: rgba(255, 71, 87, 0.3);
        }

        /* دکمه آکاردئونی لیست بلاگرهای معروف */
        .presets-toggle-bar {
            width: 100%;
            background: #F8FAFC;
            border: 1.5px solid var(--border-color);
            border-radius: 14px;
            padding: 11px 14px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            cursor: pointer;
            transition: all 0.2s ease;
            margin-bottom: 10px;
        }
        .presets-toggle-bar:hover {
            border-color: #CBD5E1;
            background: #F1F5F9;
        }
        .presets-toggle-bar.open {
            border-color: rgba(225, 48, 108, 0.35);
            background: #FFF5F7;
            border-bottom-left-radius: 6px;
            border-bottom-right-radius: 6px;
            margin-bottom: 0;
        }
        .presets-toggle-left {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 13px;
            font-weight: 700;
            color: var(--text-main);
        }
        .presets-toggle-right {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .presets-subcount {
            font-size: 11.5px;
            font-weight: 600;
            color: var(--text-muted);
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            padding: 2px 8px;
            border-radius: 99px;
        }
        .chevron-icon {
            width: 18px;
            height: 18px;
            color: var(--text-muted);
            transition: transform 0.25s ease;
        }
        .presets-toggle-bar.open .chevron-icon {
            transform: rotate(180deg);
            color: #E1306C;
        }

        /* پنل کشویی بلاگرهای معروف (انتخاب درجا بدون جابه‌جایی) */
        .presets-container {
            background: #FFF9FA;
            border: 1.5px solid rgba(225, 48, 108, 0.25);
            border-top: none;
            border-bottom-left-radius: 16px;
            border-bottom-right-radius: 16px;
            padding: 12px;
            margin-bottom: 12px;
            display: none;
            flex-direction: column;
            gap: 10px;
            animation: fadeIn 0.2s ease;
        }
        .presets-container.open {
            display: flex;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-4px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .presets-grid {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }
        .preset-chip {
            background: #FFFFFF;
            border: 1.5px solid #E2E8F0;
            color: var(--text-secondary);
            padding: 7px 12px;
            border-radius: 12px;
            font-size: 12.5px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            user-select: none;
        }
        .preset-chip:hover {
            border-color: #FDA4AF;
            color: var(--text-main);
        }
        .preset-chip .check-dot {
            width: 16px;
            height: 16px;
            border-radius: 50%;
            border: 1.5px solid #CBD5E1;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 10px;
            transition: 0.2s;
            background: #F8FAFC;
            color: transparent;
        }
        .preset-chip.active {
            background: var(--insta-gradient);
            border-color: transparent;
            color: #FFFFFF;
            box-shadow: 0 4px 12px rgba(225, 48, 108, 0.26);
        }
        .preset-chip.active .check-dot {
            background: rgba(255, 255, 255, 0.25);
            border-color: transparent;
            color: #FFFFFF;
        }

        /* افزودن بلاگر دلخواه */
        .add-box {
            display: flex;
            gap: 8px;
            margin-bottom: 12px;
        }
        .add-box input {
            flex: 1;
            min-width: 0;
            background: #F8FAFC;
            border: 1.5px solid var(--border-color);
            border-radius: 13px;
            padding: 10px 14px;
            color: var(--text-main);
            font-size: 13.5px;
            outline: none;
            transition: 0.2s;
        }
        .add-box input:focus {
            border-color: var(--primary);
            background: #FFFFFF;
        }
        .add-btn {
            background: #0F172A;
            color: #FFFFFF;
            border: none;
            padding: 0 16px;
            border-radius: 13px;
            font-size: 13px;
            font-weight: 700;
            cursor: pointer;
            transition: 0.2s;
            white-space: nowrap;
        }
        .add-btn:hover { background: #1E293B; }

        /* بخش آیدی‌های دلخواه کاربر (فقط زمانی دیده می‌شود که آیدی دستی اضافه شود) */
        .custom-pages-wrapper {
            display: none;
            margin-bottom: 16px;
            padding: 10px 12px;
            background: #F8FAFC;
            border: 1px solid #E2E8F0;
            border-radius: 14px;
        }
        .custom-pages-wrapper.visible {
            display: block;
        }
        .custom-pages-label {
            font-size: 11.5px;
            font-weight: 700;
            color: var(--text-muted);
            margin-bottom: 8px;
            display: block;
        }
        .pages-list {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            max-height: 120px;
            overflow-y: auto;
        }
        .chip {
            background: #FFFFFF;
            border: 1.5px solid var(--border-color);
            color: var(--text-secondary);
            padding: 6px 11px;
            border-radius: 12px;
            font-size: 12.5px;
            font-weight: 600;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            transition: all 0.2s ease;
            user-select: none;
        }
        .chip:hover { border-color: #CBD5E1; }
        .chip.active {
            background: var(--insta-gradient);
            color: #FFFFFF;
            border-color: transparent;
            box-shadow: 0 4px 12px rgba(225, 48, 108, 0.25);
        }
        .chip .del-btn {
            width: 18px;
            height: 18px;
            border-radius: 50%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
            line-height: 1;
            opacity: 0.7;
            transition: 0.15s;
        }
        .chip .del-btn:hover {
            background: rgba(0, 0, 0, 0.15);
            opacity: 1;
        }

        /* فیلتر زمانی */
        .time-filter {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            background: #F1F5F9;
            padding: 4px;
            border-radius: 13px;
            margin-bottom: 18px;
            gap: 4px;
        }
        .time-btn {
            text-align: center;
            padding: 8px 6px;
            font-size: 12.5px;
            font-weight: 600;
            border-radius: 10px;
            cursor: pointer;
            color: var(--text-muted);
            transition: 0.2s;
        }
        .time-btn.active {
            background: #FFFFFF;
            color: var(--primary);
            font-weight: 700;
            box-shadow: 0 2px 8px rgba(15, 23, 42, 0.06);
        }

        /* انتخاب شهر در اسنپ‌فود */
        .city-chips {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 12px;
        }
        .city-chip {
            background: #F1F5F9;
            border: 1px solid var(--border-color);
            color: var(--text-secondary);
            padding: 7px 14px;
            border-radius: 12px;
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            transition: 0.2s;
        }
        .city-chip.active {
            background: var(--snapp-color);
            color: #FFFFFF;
            border-color: var(--snapp-color);
            box-shadow: 0 4px 12px rgba(250, 0, 80, 0.25);
        }

        /* دکمه اصلی جستجو */
        .search-btn {
            width: 100%;
            background: var(--primary-gradient);
            color: #FFFFFF;
            border: none;
            border-radius: var(--radius-lg);
            padding: 15px 18px;
            font-size: 15px;
            font-weight: 800;
            cursor: pointer;
            box-shadow: 0 10px 25px -5px rgba(255, 71, 87, 0.45);
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }
        .search-btn:hover { transform: translateY(-1px); filter: brightness(1.03); }
        .search-btn:active { transform: scale(0.985); }
        .search-btn.snapp-btn {
            background: var(--snapp-gradient);
            box-shadow: 0 10px 25px -5px rgba(250, 0, 80, 0.4);
        }

        .spinner {
            width: 18px;
            height: 18px;
            border: 2.5px solid rgba(255, 255, 255, 0.35);
            border-top-color: #FFFFFF;
            border-radius: 50%;
            animation: spin 0.7s linear infinite;
            display: none;
        }
        .search-btn.loading .spinner { display: inline-block; }
        @keyframes spin { to { transform: rotate(360deg); } }

        /* کانتینر نتایج */
        #resultsSection {
            width: 100%;
            margin-top: 22px;
        }
        .results-header-bar {
            display: none;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 12px;
            padding: 0 4px;
        }
        .results-header-bar.visible { display: flex; }
        .results-label {
            font-size: 14px;
            font-weight: 800;
            color: var(--text-main);
        }
        .results-hint {
            font-size: 11.5px;
            color: var(--text-muted);
        }

        .empty-state {
            text-align: center;
            padding: 32px 20px;
            background: rgba(255, 255, 255, 0.65);
            border: 1px dashed #CBD5E1;
            border-radius: var(--radius-xl);
            color: var(--text-muted);
        }
        .empty-state-icon {
            font-size: 34px;
            margin-bottom: 8px;
            display: block;
        }
        .empty-state p {
            font-size: 13px;
            line-height: 1.7;
        }

        /* فوتر */
        .site-footer {
            margin-top: 44px;
            padding: 20px 10px 10px 10px;
            text-align: center;
            border-top: 1px solid #E2E8F0;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 8px;
        }
        .footer-logo {
            width: 40px;
            height: 40px;
            object-fit: cover;
            border-radius: 12px;
            opacity: 0.9;
        }
        .footer-text {
            font-size: 12.5px;
            color: var(--text-muted);
            font-weight: 500;
        }

        /* استایل‌های مدرن نتایج گوگل و مخفی‌سازی اضافات */
        .gsc-search-box, .gsc-tabsArea, .gcse-search-box, .gsc-resultsHeader,
        .gsc-adBlock, .gsc-results-close-btn, .gsc-modal-background-image,
        .gcsc-find-more-on-google, .gcsc-find-more-on-google-root {
            display: none !important;
        }
        .gcsc-branding, .gcsc-branding-text, .gcsc-branding-img,
        .gcsc-branding-clickable, .gsc-branding, .gsc-branding-text, .gsc-branding-img {
            display: none !important; visibility: hidden !important; height: 0 !important; opacity: 0 !important;
        }
        .gsc-results-search-on-google, .gsc-results-search-on-google-box,
        .gsc-results-search-on-google-container, #resultsWrapper a[href*="google.com/search"],
        #resultsWrapper a[href*="client=ms-google-coop"] {
            display: none !important; visibility: hidden !important; height: 0 !important; opacity: 0 !important; pointer-events: none !important;
        }
        .gsc-overflow-hidden { overflow: visible !important; position: static !important; }
        .gsc-results-wrapper-overlay, .gsc-results-wrapper-nooverlay {
            position: static !important; width: 100% !important; height: auto !important;
            max-height: none !important; overflow: visible !important; background: transparent !important;
            border: none !important; box-shadow: none !important; padding: 0 !important;
        }
        .gsc-control-cse, .gsc-control-cse * {
            font-family: 'Vazirmatn', system-ui, sans-serif !important;
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
            padding: 18px !important;
            margin-bottom: 14px !important;
            box-shadow: 0 4px 18px rgba(15, 23, 42, 0.04) !important;
            transition: all 0.2s ease !important;
        }
        .gsc-webResult.gsc-result:hover {
            border-color: var(--primary) !important;
            transform: translateY(-2px);
            box-shadow: 0 12px 26px rgba(15, 23, 42, 0.08) !important;
        }

        .gs-title, .gs-title * {
            color: #E11D48 !important;
            font-size: 16px !important;
            font-weight: 800 !important;
            text-decoration: none !important;
            line-height: 1.6 !important;
        }
        .gs-snippet {
            color: #475569 !important;
            font-size: 13.5px !important;
            line-height: 1.8 !important;
            margin-top: 8px !important;
        }
        .gsc-url-top { padding: 0 !important; }
        .gs-visibleUrl {
            color: #059669 !important;
            font-size: 12px !important;
            font-weight: 700 !important;
            margin-top: 6px !important;
            display: inline-block !important;
            direction: ltr;
        }
        .gs-image-box {
            border-radius: 12px !important;
            overflow: hidden !important;
        }

        .gsc-cursor-box { margin: 28px 0 10px 0 !important; text-align: center !important; }
        .gsc-cursor-page {
            background: #FFFFFF !important;
            border: 1px solid #CBD5E1 !important;
            color: #334155 !important;
            padding: 8px 14px !important;
            border-radius: 12px !important;
            margin: 0 4px !important;
            font-size: 13.5px !important;
            font-weight: 700 !important;
            display: inline-block !important;
            text-decoration: none !important;
        }
        .gsc-cursor-current-page {
            background: var(--primary) !important;
            color: #FFFFFF !important;
            border-color: var(--primary) !important;
        }

        @media (max-width: 480px) {
            .search-panel { padding: 16px; border-radius: 22px; }
            .main-logo { width: 58px; height: 58px; border-radius: 16px; }
            .brand-title { font-size: 20px; }
            .mode-btn { font-size: 12.5px; padding: 10px 8px; }
        }
    </style>
</head>
<body>
    <div id="toast" class="toast"></div>

    <div class="container">
        <!-- هدر -->
        <header class="header">
            <div class="logo-wrapper">
                <img src="/logo.png" alt="فود یاب" class="main-logo" onerror="this.style.display='none'">
            </div>
            <div class="header-text">
                <div class="brand-row">
                    <h1 class="brand-title">فود یاب</h1>
                    <span class="brand-badge">نسخه هوشمند</span>
                </div>
                <p class="subtitle">جستجوی سریع کافه، رستوران و بررسی فودبلاگرها</p>
            </div>
        </header>

        <!-- انتخاب منبع جستجو -->
        <div class="mode-switch">
            <button type="button" class="mode-btn active insta" id="btn-insta" onclick="switchMode('insta')">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line></svg>
                <span>اینستاگرام (فودبلاگرها)</span>
            </button>
            <button type="button" class="mode-btn" id="btn-snapp" onclick="switchMode('snapp')">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1"></circle><circle cx="20" cy="21" r="1"></circle><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path></svg>
                <span>اسنپ‌فود</span>
            </button>
        </div>

        <!-- کارت جستجو -->
        <main class="search-panel">
            <!-- کادر جستجوی غذا -->
            <div class="food-search-box">
                <span class="search-icon-right">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                </span>
                <input type="text" class="food-input" id="food" placeholder="اسم غذا یا کافه چی باشه؟ (مثلاً پیتزا، شاورما، کباب...)" oninput="toggleClearBtn()" onkeypress="handleKeyPress(event)">
                <button type="button" class="clear-input-btn" id="clearFoodBtn" onclick="clearFoodInput()" title="پاک کردن">×</button>
            </div>

            <!-- پیشنهادهای سریع -->
            <div class="quick-foods">
                <span style="font-size: 11.5px; color: var(--text-muted); font-weight: 600; flex-shrink: 0;">سریع:</span>
                <button type="button" class="quick-food-tag" onclick="quickSearchFood('پیتزا')">🍕 پیتزا</button>
                <button type="button" class="quick-food-tag" onclick="quickSearchFood('برگر')">🍔 برگر</button>
                <button type="button" class="quick-food-tag" onclick="quickSearchFood('کباب')">🍢 کباب</button>
                <button type="button" class="quick-food-tag" onclick="quickSearchFood('پاستا')">🍝 پاستا</button>
                <button type="button" class="quick-food-tag" onclick="quickSearchFood('شاورما')">🌯 شاورما</button>
                <button type="button" class="quick-food-tag" onclick="quickSearchFood('کافه')">☕ کافه</button>
                <button type="button" class="quick-food-tag" onclick="quickSearchFood('صبحانه')">🍳 صبحانه</button>
            </div>

            <div class="divider"></div>

            <!-- فیلترهای اینستاگرام -->
            <div id="insta-fields">
                <div class="section-header">
                    <span class="section-title">
                        <span>🎯 فودبلاگرهای جستجو</span>
                        <span class="count-badge" id="selectedCountBadge">۱ فعال</span>
                    </span>
                    <div class="mini-actions">
                        <button type="button" class="text-btn" onclick="selectAllPages()">انتخاب همه</button>
                        <button type="button" class="text-btn" onclick="clearAllPages()">هیچ‌کدام</button>
                    </div>
                </div>

                <!-- دکمه باز و بسته کردن لیست بلاگرهای معروف -->
                <button type="button" class="presets-toggle-bar" id="presetsToggleBtn" onclick="togglePresets()">
                    <span class="presets-toggle-left">
                        <span>🌟 بلاگرهای معروف</span>
                    </span>
                    <span class="presets-toggle-right">
                        <span class="presets-subcount" id="presetsCountLabel">۱ از ۹ انتخاب‌شده</span>
                        <svg class="chevron-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"></polyline></svg>
                    </span>
                </button>

                <!-- پنل کشویی بلاگرهای معروف (انتخاب درجا، بدون جابه‌جایی به پایین) -->
                <div class="presets-container" id="presetsContainer">
                    <div class="presets-grid" id="presetsGrid"></div>
                </div>

                <!-- افزودن آیدی دلخواه -->
                <div class="add-box">
                    <input type="text" id="newPage" placeholder="افزودن آیدی دلخواه (مثلاً: dina_taster)" onkeypress="if(event.key==='Enter') addNewPage()">
                    <button type="button" class="add-btn" onclick="addNewPage()">+ افزودن</button>
                </div>

                <!-- آیدی‌های دلخواهی که خود کاربر اضافه کرده (در صورت وجود نمایش داده می‌شود) -->
                <div class="custom-pages-wrapper" id="customPagesWrapper">
                    <span class="custom-pages-label">📌 آیدی‌های دلخواه شما:</span>
                    <div class="pages-list" id="pagesContainer"></div>
                </div>

                <div class="section-header" style="margin-bottom: 8px;">
                    <span class="section-title">📅 بازه زمانی پست‌ها:</span>
                </div>
                <div class="time-filter">
                    <div class="time-btn" id="time-m" onclick="setTime('m')">۱ ماه اخیر</div>
                    <div class="time-btn active" id="time-y" onclick="setTime('y')">۱ سال اخیر</div>
                    <div class="time-btn" id="time-all" onclick="setTime('all')">همه زمان‌ها</div>
                </div>
            </div>

            <!-- فیلترهای اسنپ‌فود -->
            <div id="snapp-fields" style="display: none;">
                <div class="section-header">
                    <span class="section-title">📍 انتخاب شهر:</span>
                </div>
                <div class="city-chips">
                    <div class="city-chip active" onclick="setCity(this, 'شیراز')">شیراز</div>
                    <div class="city-chip" onclick="setCity(this, 'تهران')">تهران</div>
                    <div class="city-chip" onclick="setCity(this, 'اصفهان')">اصفهان</div>
                    <div class="city-chip" onclick="setCity(this, 'مشهد')">مشهد</div>
                    <div class="city-chip" onclick="setCity(this, 'تبریز')">تبریز</div>
                </div>
                <div class="add-box" style="margin-bottom: 18px;">
                    <input type="text" id="customCity" placeholder="یا نام شهر دیگری را بنویسید..." oninput="onCustomCityInput()" onkeypress="handleKeyPress(event)">
                </div>
            </div>

            <!-- دکمه اصلی -->
            <button type="button" class="search-btn" id="mainSearchBtn" onclick="executeSmartSearch()">
                <span class="spinner"></span>
                <span id="searchBtnText">🔍 جستجو در پست‌های فودبلاگرها</span>
            </button>
        </main>

        <!-- نتایج جستجو -->
        <section id="resultsSection">
            <div class="results-header-bar" id="resultsHeaderBar">
                <span class="results-label">✨ نتایج یافت‌شده</span>
                <span class="results-hint">برای باز شدن در تب جدید روی عنوان بزنید</span>
            </div>

            <div class="empty-state" id="emptyState">
                <span class="empty-state-icon">🍽️</span>
                <p>نام غذای مورد نظرتان را بنویسید تا بهترین بررسی‌های فودبلاگرها یا رستوران‌های اسنپ‌فود برایتان نمایش داده شود.</p>
            </div>

            <div id="resultsWrapper">
                <div class="gcse-searchresults-only" data-gname="foodyab_results" data-linktarget="_blank"></div>
            </div>
        </section>

        <!-- فوتر -->
        <footer class="site-footer">
            <img src="/logo.png" alt="فود یاب" class="footer-logo" onerror="this.style.display='none'">
            <p class="footer-text">فود یاب | دستیار هوشمند کافه‌رستوران‌گردی</p>
        </footer>
    </div>

<script>
    let currentMode = 'insta';
    let selectedCity = 'شیراز';
    let selectedTime = 'y';

    // لیست بلاگرهای معروف (ثابت داخل منوی کشویی؛ آیدی‌های جدید را می‌توانید اینجا اضافه کنید)
    const defaultBloggers = [
        'mr.mrs_shekamoo', 'amin.nilson', 'khas_foood', 'shirazyummy',
        'sadegh.delicious', 'missfoodshiraz', 'ali_food_report', 'mr.foodshz',
        'afshin.lashkari'
    ].map(p => p.trim()).filter(Boolean);

    // بازیابی آیدی‌های دلخواه کاربر (جدا از لیست معروف‌ها)
    let customPages = JSON.parse(localStorage.getItem('my_custom_food_pages') || 'null');
    if (customPages === null) {
        // انتقال از نسخه قبلی در صورت وجود، بدون تکراری شدن معروف‌ها
        const legacyPages = JSON.parse(localStorage.getItem('my_food_pages') || '[]');
        customPages = legacyPages
            .map(p => (p || '').trim())
            .filter(p => p && !defaultBloggers.includes(p));
    } else {
        customPages = customPages.map(p => (p || '').trim()).filter(p => p && !defaultBloggers.includes(p));
    }

    // بازیابی بلاگرهای انتخاب‌شده
    const savedSelectionRaw = localStorage.getItem('my_selected_food_pages');
    let selectedPages = savedSelectionRaw !== null
        ? new Set(JSON.parse(savedSelectionRaw).filter(Boolean))
        : new Set(['mr.mrs_shekamoo']);

    let toastTimer;
    function showToast(msg) {
        const toast = document.getElementById('toast');
        toast.textContent = msg;
        toast.classList.add('show');
        clearTimeout(toastTimer);
        toastTimer = setTimeout(() => {
            toast.classList.remove('show');
        }, 2800);
    }

    function saveState() {
        localStorage.setItem('my_custom_food_pages', JSON.stringify(customPages));
        localStorage.setItem('my_selected_food_pages', JSON.stringify(Array.from(selectedPages)));
    }

    function switchMode(mode) {
        currentMode = mode;
        const btnInsta = document.getElementById('btn-insta');
        const btnSnapp = document.getElementById('btn-snapp');
        const instaFields = document.getElementById('insta-fields');
        const snappFields = document.getElementById('snapp-fields');
        const searchBtn = document.getElementById('mainSearchBtn');
        const searchBtnText = document.getElementById('searchBtnText');

        if (mode === 'insta') {
            document.body.classList.remove('snapp-mode');
            btnInsta.className = 'mode-btn active insta';
            btnSnapp.className = 'mode-btn';
            instaFields.style.display = 'block';
            snappFields.style.display = 'none';
            searchBtn.className = 'search-btn';
            searchBtnText.innerText = '🔍 جستجو در پست‌های فودبلاگرها';
        } else {
            document.body.classList.add('snapp-mode');
            btnInsta.className = 'mode-btn';
            btnSnapp.className = 'mode-btn active snapp';
            instaFields.style.display = 'none';
            snappFields.style.display = 'block';
            searchBtn.className = 'search-btn snapp-btn';
            searchBtnText.innerText = '🛵 جستجو در رستوران‌ها و منوهای اسنپ‌فود';
        }
    }

    function toggleClearBtn() {
        const input = document.getElementById('food');
        const btn = document.getElementById('clearFoodBtn');
        btn.classList.toggle('visible', input.value.length > 0);
    }

    function clearFoodInput() {
        const input = document.getElementById('food');
        input.value = '';
        toggleClearBtn();
        input.focus();
    }

    function quickSearchFood(foodName) {
        const input = document.getElementById('food');
        input.value = foodName;
        toggleClearBtn();
        executeSmartSearch();
    }

    function setCity(el, city) {
        selectedCity = city;
        document.querySelectorAll('.city-chip').forEach(c => c.classList.remove('active'));
        el.classList.add('active');
        document.getElementById('customCity').value = '';
    }

    function onCustomCityInput() {
        const val = document.getElementById('customCity').value.trim();
        if (val) {
            document.querySelectorAll('.city-chip').forEach(c => c.classList.remove('active'));
        }
    }

    function updateCounters() {
        // تعداد کل انتخاب‌ها (معروف + دلخواه)
        const allAvailable = new Set([...defaultBloggers, ...customPages]);
        let totalActive = 0;
        selectedPages.forEach(p => { if (allAvailable.has(p)) totalActive++; });

        document.getElementById('selectedCountBadge').textContent =
            `${totalActive.toLocaleString('fa-IR')} فعال`;

        // تعداد انتخاب‌شده از لیست معروف‌ها
        const presetSelectedCount = defaultBloggers.filter(p => selectedPages.has(p)).length;
        document.getElementById('presetsCountLabel').textContent =
            `${presetSelectedCount.toLocaleString('fa-IR')} از ${defaultBloggers.length.toLocaleString('fa-IR')} انتخاب‌شده`;
    }

    // رندر لیست معروف‌ها داخل همان بخش پنهان (بدون حذف یا انتقال)
    function renderPresets() {
        const grid = document.getElementById('presetsGrid');
        grid.innerHTML = '';

        defaultBloggers.forEach(page => {
            const isSelected = selectedPages.has(page);
            const chip = document.createElement('button');
            chip.type = 'button';
            chip.className = `preset-chip ${isSelected ? 'active' : ''}`;

            const dot = document.createElement('span');
            dot.className = 'check-dot';
            dot.textContent = '✓';

            const label = document.createElement('span');
            label.textContent = page;

            chip.appendChild(dot);
            chip.appendChild(label);
            chip.onclick = () => toggleSelect(page);

            grid.appendChild(chip);
        });
    }

    // رندر آیدی‌های دلخواهی که کاربر خودش اضافه کرده
    function renderCustomPages() {
        const wrapper = document.getElementById('customPagesWrapper');
        const container = document.getElementById('pagesContainer');
        container.innerHTML = '';

        if (customPages.length === 0) {
            wrapper.classList.remove('visible');
            return;
        }

        wrapper.classList.add('visible');
        customPages.forEach(page => {
            const isSelected = selectedPages.has(page);
            const chip = document.createElement('div');
            chip.className = `chip ${isSelected ? 'active' : ''}`;

            const label = document.createElement('span');
            label.textContent = isSelected ? `${page} ✓` : page;
            chip.onclick = () => toggleSelect(page);

            const delBtn = document.createElement('span');
            delBtn.className = 'del-btn';
            delBtn.textContent = '×';
            delBtn.title = 'حذف';
            delBtn.onclick = (e) => deleteCustomPage(e, page);

            chip.appendChild(label);
            chip.appendChild(delBtn);
            container.appendChild(chip);
        });
    }

    function renderAllBloggers() {
        renderPresets();
        renderCustomPages();
        updateCounters();
        saveState();
    }

    function togglePresets() {
        const btn = document.getElementById('presetsToggleBtn');
        const container = document.getElementById('presetsContainer');
        const isOpen = container.classList.toggle('open');
        btn.classList.toggle('open', isOpen);
    }

    function toggleSelect(page) {
        if (selectedPages.has(page)) selectedPages.delete(page);
        else selectedPages.add(page);
        renderAllBloggers();
    }

    function selectAllPages() {
        defaultBloggers.forEach(p => selectedPages.add(p));
        customPages.forEach(p => selectedPages.add(p));
        renderAllBloggers();
    }

    function clearAllPages() {
        selectedPages.clear();
        renderAllBloggers();
    }

    function addNewPage() {
        const input = document.getElementById('newPage');
        const val = input.value.trim().replace(/^@+/, '');
        if (!val) {
            showToast('لطفاً آیدی اینستاگرام بلاگر را وارد کنید.');
            input.focus();
            return;
        }

        // اگر آیدی از قبل در لیست معروف‌ها بود، همان‌جا انتخابش کن و دوباره پایین نساز
        if (defaultBloggers.includes(val)) {
            selectedPages.add(val);
            renderAllBloggers();
            input.value = '';
            showToast(`آیدی ${val} در لیست بلاگرهای معروف انتخاب شد ✓`);
            return;
        }

        if (customPages.includes(val)) {
            selectedPages.add(val);
            renderAllBloggers();
            input.value = '';
            showToast(`آیدی ${val} از قبل اضافه شده بود و انتخاب شد.`);
            return;
        }

        customPages.push(val);
        selectedPages.add(val);
        renderAllBloggers();
        input.value = '';
        showToast(`آیدی ${val} اضافه و انتخاب شد ✓`);
    }

    function deleteCustomPage(event, page) {
        event.stopPropagation();
        customPages = customPages.filter(p => p !== page);
        selectedPages.delete(page);
        renderAllBloggers();
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

            document.querySelectorAll('#resultsWrapper a[href*="google.com/search"], .gsc-results-search-on-google').forEach(el => {
                el.remove();
            });

            if (attempts > 35) clearInterval(interval);
        }, 100);
    }

    function executeSmartSearch() {
        const food = document.getElementById('food').value.trim();
        if (!food) {
            showToast('لطفاً ابتدا نام غذا یا رستوران را بنویسید!');
            document.getElementById('food').focus();
            return;
        }

        let finalQuery = '';

        if (currentMode === 'insta') {
            const validPool = new Set([...defaultBloggers, ...customPages]);
            const pagesArray = Array.from(selectedPages).filter(p => validPool.has(p));

            if (pagesArray.length === 0) {
                showToast('لطفاً حداقل یک فودبلاگر را انتخاب کنید!');
                return;
            }

            const pagesQuery = pagesArray.length === 1
                ? `"${pagesArray[0]}"`
                : '(' + pagesArray.map(p => `"${p}"`).join(' OR ') + ')';

            let dateFilter = '';
            const now = new Date();
            if (selectedTime === 'm') {
                const d = new Date(new Date().setDate(now.getDate() - 30));
                dateFilter = `after:${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
            } else if (selectedTime === 'y') {
                const d = new Date(new Date().setFullYear(now.getFullYear() - 1));
                dateFilter = `after:${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
            }

            finalQuery = `site:instagram.com ${pagesQuery} ${food} ${dateFilter}`.trim();
        } else {
            const customCity = document.getElementById('customCity').value.trim();
            const city = customCity ? customCity : selectedCity;
            finalQuery = `site:snappfood.ir "${city}" ${food}`.trim();
        }

        if (typeof google === 'undefined' || !google.search || !google.search.cse) {
            showToast('موتور جستجو در حال بارگذاری است، یک لحظه صبر کنید...');
            return;
        }

        const element = google.search.cse.element.getElement('foodyab_results');
        if (element) {
            const btn = document.getElementById('mainSearchBtn');
            btn.classList.add('loading');

            document.getElementById('emptyState').style.display = 'none';
            document.getElementById('resultsHeaderBar').classList.add('visible');

            element.execute(finalQuery);
            unlockGoogleScrollTrap();

            setTimeout(() => {
                btn.classList.remove('loading');
                const resultsEl = document.getElementById('resultsSection');
                if (resultsEl) resultsEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }, 650);
        } else {
            showToast('در حال آماده‌سازی جستجو... لطفاً دوباره کلیک کنید.');
        }
    }

    renderAllBloggers();
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
