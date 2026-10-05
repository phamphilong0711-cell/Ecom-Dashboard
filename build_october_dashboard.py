import json

with open('/Users/longnd/tiktok-dashboard/october_campaigns.json', 'r', encoding='utf-8') as f:
    shopee_camps = json.load(f)

# Add TikTok GMV Max campaigns
tiktok_camps = [
    {
        "shop": "TikTok Shop (GMV Max)",
        "name": "TikTok GMV Max - Sáp Glanzen & Combo Dưỡng Tóc (Video Shopping Ads)",
        "type": "Video Ads",
        "bidding": "GMV Max Auto",
        "imp": 36500,
        "clicks": 680,
        "ctr": 1.86,
        "cpc": 4550.0,
        "orders": 64,
        "sold": 68,
        "spend": 3094000.0,
        "gmv": 18920000.0,
        "aov": 295625.0,
        "cpa": 48344.0,
        "roas": 6.11,
        "cir": 16.35,
        "status": "safe"
    },
    {
        "shop": "TikTok Shop (GMV Max)",
        "name": "TikTok Product Card (PSA / Shop Tab) - Hero SKU Glanzen & Dr.FORSKIN",
        "type": "Product Card",
        "bidding": "GMV Max Product Card",
        "imp": 15500,
        "clicks": 300,
        "ctr": 1.94,
        "cpc": 4773.0,
        "orders": 35,
        "sold": 37,
        "spend": 1432000.0,
        "gmv": 8511924.0,
        "aov": 243198.0,
        "cpa": 40914.0,
        "roas": 5.94,
        "cir": 16.82,
        "status": "safe"
    }
]

all_campaigns = shopee_camps + tiktok_camps
json_str = json.dumps(all_campaigns, ensure_ascii=False)

html_content = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Báo Cáo Toàn Diện Hiệu Suất Quảng Cáo Đa Kênh (01/10 - 04/10/2026) | Shopee & TikTok Shop</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --bg-base: #080c14;
            --bg-card: rgba(17, 24, 39, 0.75);
            --bg-card-hover: rgba(30, 41, 59, 0.85);
            --border-color: rgba(255, 255, 255, 0.08);
            --border-highlight: rgba(56, 189, 248, 0.3);
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --text-sub: #64748b;
            --shopee: #ee4d2d;
            --tiktok: #00f2fe;
            --success: #10b981;
            --warn: #f59e0b;
            --danger: #ef4444;
            --purple: #a855f7;
            --blue: #3b82f6;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }

        body {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: var(--bg-base);
            background-image: 
                radial-gradient(at 0% 0%, rgba(59, 130, 246, 0.12) 0px, transparent 50%),
                radial-gradient(at 100% 0%, rgba(238, 77, 45, 0.1) 0px, transparent 50%),
                radial-gradient(at 50% 100%, rgba(0, 242, 254, 0.08) 0px, transparent 50%);
            background-attachment: fixed;
            color: var(--text-main);
            min-height: 100vh;
            padding: 24px;
            line-height: 1.5;
        }

        .container { max-width: 1560px; margin: 0 auto; }
        .num-font { font-family: 'JetBrains Mono', monospace; }

        /* HEADER */
        .header {
            background: var(--bg-card);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid var(--border-color);
            border-radius: 20px;
            padding: 28px 32px;
            margin-bottom: 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 20px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
        }

        .header-left h1 {
            font-size: 26px;
            font-weight: 800;
            background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 6px;
            letter-spacing: -0.5px;
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .header-left p {
            color: var(--text-muted);
            font-size: 14px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .badge-live {
            background: rgba(16, 185, 129, 0.15);
            color: #34d399;
            border: 1px solid rgba(16, 185, 129, 0.3);
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }

        .badge-live::before {
            content: '';
            width: 8px;
            height: 8px;
            background-color: #10b981;
            border-radius: 50%;
            display: inline-block;
            box-shadow: 0 0 10px #10b981;
        }

        .scope-switcher {
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid var(--border-color);
            padding: 4px;
            border-radius: 14px;
            display: inline-flex;
            gap: 4px;
            flex-wrap: wrap;
        }

        .switch-btn {
            background: transparent;
            border: none;
            color: var(--text-muted);
            padding: 8px 14px;
            border-radius: 10px;
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .switch-btn.active {
            background: rgba(255, 255, 255, 0.12);
            color: #ffffff;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
        }

        .switch-btn[data-scope="Shopee"].active {
            background: linear-gradient(135deg, rgba(238, 77, 45, 0.3), rgba(238, 77, 45, 0.15));
            color: #ff7b5a;
            border: 1px solid rgba(238, 77, 45, 0.3);
        }
        .switch-btn[data-scope="TikTok Shop (GMV Max)"].active {
            background: linear-gradient(135deg, rgba(0, 242, 254, 0.3), rgba(0, 242, 254, 0.15));
            color: #00f2fe;
            border: 1px solid rgba(0, 242, 254, 0.3);
        }

        /* STRATEGIC ALERT BANNER */
        .alert-banner {
            background: linear-gradient(135deg, rgba(56, 189, 248, 0.1) 0%, rgba(37, 99, 235, 0.15) 100%);
            border: 1px solid rgba(56, 189, 248, 0.3);
            border-radius: 16px;
            padding: 18px 24px;
            margin-bottom: 24px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
            flex-wrap: wrap;
        }

        /* KPI GRID - 11 FUNNEL METRICS */
        .kpi-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }

        .kpi-card {
            background: var(--bg-card);
            backdrop-filter: blur(12px);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 20px;
            position: relative;
            overflow: hidden;
            transition: all 0.3s ease;
        }

        .kpi-card:hover {
            transform: translateY(-2px);
            border-color: var(--border-highlight);
            background: var(--bg-card-hover);
        }

        .kpi-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 3px;
            background: linear-gradient(90deg, transparent, var(--card-accent, #38bdf8), transparent);
        }

        .kpi-title {
            font-size: 13px;
            color: var(--text-muted);
            font-weight: 600;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .kpi-val {
            font-size: 24px;
            font-weight: 800;
            color: #fff;
            margin-bottom: 6px;
            letter-spacing: -0.5px;
        }

        .kpi-sub {
            font-size: 12px;
            color: var(--text-sub);
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .badge-safe { background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); padding: 2px 8px; border-radius: 8px; font-size: 11px; font-weight: 700; }
        .badge-warn { background: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); padding: 2px 8px; border-radius: 8px; font-size: 11px; font-weight: 700; }
        .badge-danger { background: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); padding: 2px 8px; border-radius: 8px; font-size: 11px; font-weight: 700; }

        /* TABS SECTION */
        .tab-nav {
            display: flex;
            gap: 8px;
            border-bottom: 1px solid var(--border-color);
            margin-bottom: 20px;
            padding-bottom: 8px;
            flex-wrap: wrap;
        }

        .tab-btn {
            background: transparent;
            border: none;
            color: var(--text-muted);
            font-size: 14px;
            font-weight: 600;
            padding: 10px 20px;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .tab-btn.active {
            background: rgba(255, 255, 255, 0.1);
            color: #fff;
            border: 1px solid var(--border-color);
        }

        .tab-pane { display: none; }
        .tab-pane.active { display: block; animation: fadeIn 0.3s ease; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: translateY(0); } }

        /* CHARTS GRID */
        .chart-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(480px, 1fr));
            gap: 20px;
            margin-bottom: 24px;
        }

        .chart-card {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 18px;
            padding: 24px;
        }

        .chart-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 18px;
        }

        .chart-title {
            font-size: 15px;
            font-weight: 700;
            color: #fff;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        /* TABLE */
        .table-container {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 18px;
            padding: 24px;
            margin-bottom: 24px;
        }

        .table-responsive {
            overflow-x: auto;
            border-radius: 12px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
            text-align: left;
        }

        th {
            background: rgba(0, 0, 0, 0.4);
            color: var(--text-muted);
            padding: 14px 16px;
            font-weight: 700;
            border-bottom: 1px solid var(--border-color);
            white-space: nowrap;
        }

        td {
            padding: 14px 16px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.04);
            color: var(--text-main);
            vertical-align: middle;
        }

        tr:hover td {
            background: rgba(255, 255, 255, 0.03);
        }

        .campaign-name {
            font-weight: 600;
            color: #fff;
            max-width: 320px;
            line-height: 1.4;
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- HEADER -->
        <div class="header">
            <div class="header-left">
                <h1><i class="fa-solid fa-chart-line" style="color: #ee4d2d;"></i> Báo Cáo Hiệu Suất Quảng Cáo Đa Kênh (01/10 - 04/10/2026)</h1>
                <p>
                    <span class="badge-live">Dữ liệu thực tế 4 ngày đầu tháng 10</span>
                    <span>• Hợp nhất 15 chiến dịch (Shopee 3 Shop + TikTok Shop GMV Max)</span>
                </p>
            </div>
            <div class="scope-switcher">
                <button class="switch-btn active" data-scope="all" onclick="filterScope('all', this)"><i class="fa-solid fa-globe"></i> Toàn Sàn (Shopee + TikTok)</button>
                <button class="switch-btn" data-scope="Shopee" onclick="filterScope('Shopee', this)"><i class="fa-solid fa-bag-shopping" style="color: #ee4d2d;"></i> Shopee (3 Shop)</button>
                <button class="switch-btn" data-scope="TikTok Shop (GMV Max)" onclick="filterScope('TikTok Shop (GMV Max)', this)"><i class="fa-brands fa-tiktok" style="color: #00f2fe;"></i> TikTok Shop</button>
                <button class="switch-btn" data-scope="30Shine Store" onclick="filterScope('30Shine Store', this)">30Shine</button>
                <button class="switch-btn" data-scope="Dr.FORSKIN" onclick="filterScope('Dr.FORSKIN', this)">Dr.FORSKIN</button>
                <button class="switch-btn" data-scope="Glanzen Vietnam" onclick="filterScope('Glanzen Vietnam', this)">Glanzen</button>
            </div>
        </div>

        <!-- STRATEGIC ALERT BANNER -->
        <div class="alert-banner">
            <div>
                <strong style="color: #38bdf8; font-size: 15px;"><i class="fa-solid fa-bullseye"></i> Kế Hoạch Đánh Đổi Lợi Nhuận Tuyệt Đối (Tháng 10):</strong>
                <span style="color: var(--text-muted); font-size: 13px; margin-left: 8px;">
                    Mục tiêu Gross GMV: <strong>966.3M đ</strong> | Ngân sách Ads: <strong>116.3M đ</strong> (CIR ≤ 12.04%).
                    Đến ngày <strong>15/10</strong>, nếu luỹ kế GMV &lt; 385M đ (&lt; 80% tiến độ), kích hoạt Plan B: bung ngân sách Ads lên <strong>15% - 16% CIR</strong> để bảo vệ Doanh thu tuyệt đối và <strong>EBITDA ròng ≥ 164M - 184M đ</strong>.
                </span>
            </div>
            <a href="https://github.com/phamphilong0711-cell/Ecom-Dashboard" target="_blank" class="badge-safe" style="text-decoration: none; padding: 6px 14px;">
                <i class="fa-brands fa-github"></i> GitHub Live Repo
            </a>
        </div>

        <!-- 11 FUNNEL KPI CARDS -->
        <div class="kpi-grid">
            <!-- 1. GMV -->
            <div class="kpi-card" style="--card-accent: #10b981;">
                <div class="kpi-title"><span>Tổng Doanh Thu (GMV)</span><i class="fa-solid fa-sack-dollar" style="color: #10b981;"></i></div>
                <div class="kpi-val num-font" id="kpi-gmv" style="color: #34d399;">77,381,884 đ</div>
                <div class="kpi-sub">Bình quân: <strong class="num-font" style="color: #fff;" id="kpi-gmv-day">19,345,471 đ/ngày</strong></div>
            </div>

            <!-- 2. Spend -->
            <div class="kpi-card" style="--card-accent: #ef4444;">
                <div class="kpi-title"><span>Chi Phí Quảng Cáo (Spend)</span><i class="fa-solid fa-credit-card" style="color: #ef4444;"></i></div>
                <div class="kpi-val num-font" id="kpi-spend" style="color: #f87171;">12,830,305 đ</div>
                <div class="kpi-sub">Bình quân: <strong class="num-font" style="color: #fff;" id="kpi-spend-day">3,207,576 đ/ngày</strong></div>
            </div>

            <!-- 3. ROAS & CIR -->
            <div class="kpi-card" style="--card-accent: #38bdf8;">
                <div class="kpi-title"><span>Hiệu Suất ROAS & CIR</span><i class="fa-solid fa-gauge-high" style="color: #38bdf8;"></i></div>
                <div class="kpi-val num-font" id="kpi-roas" style="color: #38bdf8;">6.03x <span style="font-size: 16px; color: #fbbf24;">(16.58%)</span></div>
                <div class="kpi-sub"><span class="badge-safe">🟢 An toàn trước Mega 10.10</span></div>
            </div>

            <!-- 4. Orders & AOV -->
            <div class="kpi-card" style="--card-accent: #a855f7;">
                <div class="kpi-title"><span>Đơn Hàng & AOV</span><i class="fa-solid fa-bag-shopping" style="color: #a855f7;"></i></div>
                <div class="kpi-val num-font" id="kpi-orders" style="color: #c084fc;">252 đơn <span style="font-size: 14px; color: var(--text-muted);">/ 264 sp</span></div>
                <div class="kpi-sub">AOV: <strong class="num-font" style="color: #fff;" id="kpi-aov">307,071 đ</strong> (Chuẩn 305k)</div>
            </div>

            <!-- 5. Impressions -->
            <div class="kpi-card" style="--card-accent: #3b82f6;">
                <div class="kpi-title"><span>Lượt Hiển Thị (Imp)</span><i class="fa-solid fa-eye" style="color: #3b82f6;"></i></div>
                <div class="kpi-val num-font" id="kpi-imp">107,867</div>
                <div class="kpi-sub">Bình quân: <strong class="num-font" style="color: #fff;">26,967 Imp/ngày</strong></div>
            </div>

            <!-- 6. Clicks & CTR -->
            <div class="kpi-card" style="--card-accent: #f59e0b;">
                <div class="kpi-title"><span>Lượt Clicks & CTR</span><i class="fa-solid fa-arrow-pointer" style="color: #f59e0b;"></i></div>
                <div class="kpi-val num-font" id="kpi-clicks" style="color: #fbbf24;">2,173 <span style="font-size: 15px; color: #34d399;">(2.01%)</span></div>
                <div class="kpi-sub">CTR Đạt chuẩn mục tiêu <strong class="num-font">&gt; 2.0%</strong></div>
            </div>

            <!-- 7. CPC -->
            <div class="kpi-card" style="--card-accent: #64748b;">
                <div class="kpi-title"><span>Giá Mỗi Click (CPC)</span><i class="fa-solid fa-tag" style="color: #94a3b8;"></i></div>
                <div class="kpi-val num-font" id="kpi-cpc">5,904 đ</div>
                <div class="kpi-sub">Ngưỡng kiểm soát an toàn &lt; 7.0k đ</div>
            </div>

            <!-- 8. Conversion Rates -->
            <div class="kpi-card" style="--card-accent: #10b981;">
                <div class="kpi-title"><span>Tỷ Lệ Chuyển Đổi (CR)</span><i class="fa-solid fa-filter" style="color: #10b981;"></i></div>
                <div class="kpi-val num-font" id="kpi-cr" style="color: #34d399;">11.60% <span style="font-size: 13px; color: var(--text-muted);">Click CR</span></div>
                <div class="kpi-sub">Imp-to-Order CR: <strong class="num-font" style="color: #fff;" id="kpi-imp-cr">0.234%</strong> (Chuẩn 0.20%)</div>
            </div>

            <!-- 9. CPA -->
            <div class="kpi-card" style="--card-accent: #ec4899;">
                <div class="kpi-title"><span>Chi Phí Mỗi Đơn (CPA)</span><i class="fa-solid fa-receipt" style="color: #ec4899;"></i></div>
                <div class="kpi-val num-font" id="kpi-cpa" style="color: #f472b6;">50,914 đ</div>
                <div class="kpi-sub"><span class="badge-safe">🟢 Dưới trần tối đa 60,300 đ</span></div>
            </div>

            <!-- 10. Mega 10.10 Target Tracker -->
            <div class="kpi-card" style="--card-accent: #eab308;">
                <div class="kpi-title"><span>Mục Tiêu Mega 10.10</span><i class="fa-solid fa-flag-checkered" style="color: #eab308;"></i></div>
                <div class="kpi-val num-font" style="color: #facc15;">75,000,000 đ</div>
                <div class="kpi-sub">Mục tiêu 250 đơn (AOV 300k, CIR ≤ 11.4%)</div>
            </div>

            <!-- 11. 15/10 Pacing Status -->
            <div class="kpi-card" style="--card-accent: #06b6d4;">
                <div class="kpi-title"><span>Tiến Độ Mốc 15/10</span><i class="fa-solid fa-stopwatch" style="color: #06b6d4;"></i></div>
                <div class="kpi-val num-font" style="color: #22d3ee;">77.38M / 483M</div>
                <div class="kpi-sub">Đạt 16.0% mục tiêu nửa tháng sau 4 ngày</div>
            </div>
        </div>

        <!-- TAB NAVIGATION -->
        <div class="tab-nav">
            <button class="tab-btn active" onclick="switchTab('tab-channels', this)"><i class="fa-solid fa-diagram-project"></i> Phân Bổ Sàn (Shopee vs TikTok)</button>
            <button class="tab-btn" onclick="switchTab('tab-campaigns', this)"><i class="fa-solid fa-list-check"></i> Chi Tiết Toàn Bộ 15 Chiến Dịch</button>
            <button class="tab-btn" onclick="switchTab('tab-actions', this)"><i class="fa-solid fa-lightbulb"></i> Cảnh Báo & Hành Động Tối Ưu</button>
        </div>

        <!-- TAB 1: CHANNEL COMPARISON -->
        <div id="tab-channels" class="tab-pane active">
            <div class="chart-grid">
                <div class="chart-card">
                    <div class="chart-header">
                        <div class="chart-title"><i class="fa-solid fa-chart-pie" style="color: #ee4d2d;"></i> Tỷ Trọng Doanh Thu & Chi Phí Theo Kênh</div>
                    </div>
                    <canvas id="chartChannelGmv" height="240"></canvas>
                </div>
                <div class="chart-card">
                    <div class="chart-header">
                        <div class="chart-title"><i class="fa-solid fa-chart-bar" style="color: #38bdf8;"></i> Hiệu Suất ROAS & CIR Theo Kênh</div>
                    </div>
                    <canvas id="chartChannelRoas" height="240"></canvas>
                </div>
            </div>

            <!-- CHANNEL SUMMARY TABLE -->
            <div class="table-container">
                <div class="chart-title" style="margin-bottom: 16px;"><i class="fa-solid fa-table-list" style="color: #38bdf8;"></i> Bảng So Sánh Hiệu Suất Theo Kênh & Gian Hàng (01 - 04/10/2026)</div>
                <div class="table-responsive">
                    <table>
                        <thead>
                            <tr>
                                <th>Kênh / Gian Hàng</th>
                                <th>Chi Phí (Spend)</th>
                                <th>Doanh Thu (GMV)</th>
                                <th>Số Đơn</th>
                                <th>Lượt Xem</th>
                                <th>Lượt Click</th>
                                <th>CTR</th>
                                <th>CPC</th>
                                <th>CR</th>
                                <th>AOV</th>
                                <th>CPA</th>
                                <th>ROAS</th>
                                <th>CIR (%)</th>
                                <th>Trạng Thái</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><strong style="color: #ff7b5a;"><i class="fa-solid fa-bag-shopping"></i> Shopee 30Shine Store</strong></td>
                                <td class="num-font">4,828,077 đ</td>
                                <td class="num-font" style="font-weight: 700; color: #fff;">31,542,960 đ</td>
                                <td class="num-font">95</td>
                                <td class="num-font">33,454</td>
                                <td class="num-font">734</td>
                                <td class="num-font">2.19%</td>
                                <td class="num-font">6,578 đ</td>
                                <td class="num-font" style="color: #34d399;">12.94%</td>
                                <td class="num-font">332,031 đ</td>
                                <td class="num-font" style="color: #34d399;">50,822 đ</td>
                                <td class="num-font" style="color: #34d399; font-weight: 700;">6.53x</td>
                                <td class="num-font" style="color: #34d399; font-weight: 700;">15.31%</td>
                                <td><span class="badge-safe">🟢 Ổn định (Auto ROAS 9.18x)</span></td>
                            </tr>
                            <tr>
                                <td><strong style="color: #60a5fa;"><i class="fa-solid fa-bag-shopping"></i> Shopee Dr.FORSKIN Store</strong></td>
                                <td class="num-font">2,046,891 đ</td>
                                <td class="num-font" style="font-weight: 700; color: #fff;">12,213,000 đ</td>
                                <td class="num-font">37</td>
                                <td class="num-font">13,365</td>
                                <td class="num-font">248</td>
                                <td class="num-font">1.86%</td>
                                <td class="num-font">8,254 đ</td>
                                <td class="num-font" style="color: #34d399;">14.92%</td>
                                <td class="num-font">330,081 đ</td>
                                <td class="num-font">55,321 đ</td>
                                <td class="num-font" style="color: #38bdf8;">5.97x</td>
                                <td class="num-font" style="color: #fbbf24;">16.76%</td>
                                <td><span class="badge-warn">🟡 Cận biên (Serum 7IN1 ROAS 7.58x)</span></td>
                            </tr>
                            <tr>
                                <td><strong style="color: #c084fc;"><i class="fa-solid fa-bag-shopping"></i> Shopee Glanzen Vietnam</strong></td>
                                <td class="num-font">1,429,337 đ</td>
                                <td class="num-font" style="font-weight: 700; color: #fff;">6,194,000 đ</td>
                                <td class="num-font">21</td>
                                <td class="num-font">9,048</td>
                                <td class="num-font">211</td>
                                <td class="num-font">2.33%</td>
                                <td class="num-font">6,774 đ</td>
                                <td class="num-font" style="color: #f87171;">9.95%</td>
                                <td class="num-font">294,952 đ</td>
                                <td class="num-font" style="color: #f87171;">68,064 đ</td>
                                <td class="num-font" style="color: #f87171;">4.33x</td>
                                <td class="num-font" style="color: #f87171;">23.08%</td>
                                <td><span class="badge-danger">🔴 Vượt trần (Cần tối ưu Gôm xịt)</span></td>
                            </tr>
                            <tr style="background: rgba(238, 77, 45, 0.08); font-weight: 700;">
                                <td><strong style="color: #ff7b5a;">TỔNG SHOPEE ADS (3 SHOP)</strong></td>
                                <td class="num-font" style="color: #f87171;">8,304,305 đ</td>
                                <td class="num-font" style="color: #ff7b5a;">49,949,960 đ</td>
                                <td class="num-font">153</td>
                                <td class="num-font">55,867</td>
                                <td class="num-font">1,193</td>
                                <td class="num-font">2.14%</td>
                                <td class="num-font">6,961 đ</td>
                                <td class="num-font" style="color: #34d399;">12.82%</td>
                                <td class="num-font">326,470 đ</td>
                                <td class="num-font" style="color: #34d399;">54,277 đ</td>
                                <td class="num-font" style="color: #34d399;">6.01x</td>
                                <td class="num-font" style="color: #34d399;">16.63%</td>
                                <td><span class="badge-safe">🟢 SHOPEE AN TOÀN</span></td>
                            </tr>
                            <tr style="background: rgba(0, 242, 254, 0.08); font-weight: 700;">
                                <td><strong style="color: #00f2fe;"><i class="fa-brands fa-tiktok"></i> TIKTOK SHOP (GMV MAX)</strong></td>
                                <td class="num-font" style="color: #f87171;">4,526,000 đ</td>
                                <td class="num-font" style="color: #00f2fe;">27,431,924 đ</td>
                                <td class="num-font">99</td>
                                <td class="num-font">52,000</td>
                                <td class="num-font">980</td>
                                <td class="num-font">1.88%</td>
                                <td class="num-font">4,618 đ</td>
                                <td class="num-font" style="color: #34d399;">10.10%</td>
                                <td class="num-font">277,090 đ</td>
                                <td class="num-font" style="color: #34d399;">45,717 đ</td>
                                <td class="num-font" style="color: #34d399;">6.06x</td>
                                <td class="num-font" style="color: #34d399;">16.50%</td>
                                <td><span class="badge-safe">🟢 TIKTOK AN TOÀN</span></td>
                            </tr>
                            <tr style="background: rgba(255, 255, 255, 0.06); font-weight: 800; font-size: 14px;">
                                <td><strong>TỔNG TOÀN SÀN OMNICHANNEL</strong></td>
                                <td class="num-font" style="color: #f87171;">12,830,305 đ</td>
                                <td class="num-font" style="color: #34d399;">77,381,884 đ</td>
                                <td class="num-font">252</td>
                                <td class="num-font">107,867</td>
                                <td class="num-font">2,173</td>
                                <td class="num-font">2.01%</td>
                                <td class="num-font">5,904 đ</td>
                                <td class="num-font" style="color: #34d399;">11.60%</td>
                                <td class="num-font">307,071 đ</td>
                                <td class="num-font" style="color: #34d399;">50,914 đ</td>
                                <td class="num-font" style="color: #34d399;">6.03x</td>
                                <td class="num-font" style="color: #34d399;">16.58%</td>
                                <td><span class="badge-safe">🟢 TOÀN SÀN AN TOÀN</span></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- TAB 2: CAMPAIGNS DRILL-DOWN -->
        <div id="tab-campaigns" class="tab-pane">
            <div class="table-container">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; flex-wrap: wrap; gap: 12px;">
                    <div class="chart-title"><i class="fa-solid fa-list" style="color: #38bdf8;"></i> Bảng Chi Tiết Toàn Bộ 15 Chiến Dịch Quảng Cáo</div>
                    <input type="text" id="searchCamp" placeholder="🔍 Tìm kiếm chiến dịch, shop, SKU..." oninput="renderTable()" 
                           style="background: rgba(0,0,0,0.3); border: 1px solid var(--border-color); color: #fff; padding: 8px 14px; border-radius: 10px; font-size: 13px; outline: none; width: 280px;">
                </div>
                <div class="table-responsive">
                    <table>
                        <thead>
                            <tr>
                                <th>Kênh / Shop</th>
                                <th>Tên Chiến Dịch Quảng Cáo</th>
                                <th>Đấu Thầu</th>
                                <th>Chi Phí (Spend)</th>
                                <th>Doanh Số (GMV)</th>
                                <th>Đơn</th>
                                <th>Xem (Imp)</th>
                                <th>Click</th>
                                <th>CTR</th>
                                <th>CPC</th>
                                <th>CR</th>
                                <th>AOV</th>
                                <th>CPA</th>
                                <th>ROAS</th>
                                <th>CIR (%)</th>
                                <th>Trạng Thái</th>
                            </tr>
                        </thead>
                        <tbody id="campaignTableBody">
                            <!-- Injected by JS -->
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- TAB 3: STRATEGIC ACTIONS -->
        <div id="tab-actions" class="tab-pane">
            <div class="chart-grid">
                <div class="chart-card">
                    <div class="chart-title" style="margin-bottom: 16px; color: #34d399;"><i class="fa-solid fa-circle-check"></i> 4 Điểm Sáng Nổi Bật (01 - 04/10)</div>
                    <ul style="color: var(--text-muted); font-size: 14px; line-height: 1.8; padding-left: 20px;">
                        <li><strong>Shopee Auto Bidding (30Shine):</strong> Đạt ROAS <strong style="color: #34d399;">9.18x</strong>, CIR chỉ <strong style="color: #34d399;">10.90%</strong> với 17 đơn hàng. Cỗ máy kéo doanh thu có biên lãi tốt nhất.</li>
                        <li><strong>TikTok Shop GMV Max:</strong> Đóng góp <strong style="color: #00f2fe;">27.43M GMV</strong> (99 đơn) với ROAS <strong style="color: #34d399;">6.06x</strong>, CIR <strong style="color: #34d399;">16.50%</strong>.</li>
                        <li><strong>TikTok Product Card (PSA):</strong> Chi phí CPC chỉ <strong style="color: #34d399;">4,773 đ</strong>, CPA chỉ <strong style="color: #34d399;">40,914 đ</strong> (rẻ hơn 25% so với Video ads).</li>
                        <li><strong>Shopee Serum 7IN1 Dr.FORSKIN:</strong> Đạt ROAS <strong style="color: #34d399;">7.58x</strong>, AOV cao nhất sàn <strong style="color: #fff;">657,167 đ</strong>.</li>
                    </ul>
                </div>

                <div class="chart-card">
                    <div class="chart-title" style="margin-bottom: 16px; color: #f87171;"><i class="fa-solid fa-triangle-exclamation"></i> 3 Hành Động Cần Tối Ưu Ngay Trước Thềm Mega 10.10</div>
                    <ul style="color: var(--text-muted); font-size: 14px; line-height: 1.8; padding-left: 20px;">
                        <li><strong>Gôm xịt Glanzen (Glanzen Vietnam):</strong> CIR bị vọt lên <strong style="color: #f87171;">29.33%</strong> (ROAS 3.41x, CPA 72.9k đ). <em>Hành động:</em> Tăng Target ROAS từ 4.0x lên <strong>≥ 5.5x</strong> để hạ giá thầu click.</li>
                        <li><strong>Mở rộng Product Card TikTok (PSA / Shop Tab):</strong> Nâng tỷ trọng hiển thị của Product Card từ 30% lên <strong>≥ 40%</strong> trên TikTok để tận dụng CPA rẻ 40k đ kéo CIR toàn sàn về mức 12-14%.</li>
                        <li><strong>Chuẩn bị cổng Mega 10.10 (Mục tiêu 75M đ):</strong> Điều chỉnh tăng 30% ngân sách cho 2 Hero SKU (Sáp 60g & Serum 7IN1) bắt đầu từ 08/10.</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>

    <script>
        const campaignsData = """ + json_str + """;
        let currentScope = 'all';

        function filterScope(scope, btn) {
            currentScope = scope;
            document.querySelectorAll('.scope-switcher .switch-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            updateKPIs();
            renderTable();
        }

        function switchTab(tabId, btn) {
            document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.getElementById(tabId).classList.add('active');
            btn.classList.add('active');
        }

        function updateKPIs() {
            let filtered = campaignsData;
            if (currentScope === 'Shopee') {
                filtered = campaignsData.filter(c => c.shop !== 'TikTok Shop (GMV Max)');
            } else if (currentScope !== 'all') {
                filtered = campaignsData.filter(c => c.shop === currentScope);
            }
            
            let totalSpend = filtered.reduce((sum, c) => sum + c.spend, 0);
            let totalGmv = filtered.reduce((sum, c) => sum + c.gmv, 0);
            let totalOrders = filtered.reduce((sum, c) => sum + c.orders, 0);
            let totalItems = filtered.reduce((sum, c) => sum + c.sold, 0);
            let totalImp = filtered.reduce((sum, c) => sum + c.imp, 0);
            let totalClicks = filtered.reduce((sum, c) => sum + c.clicks, 0);
            
            let ctr = totalImp > 0 ? (totalClicks / totalImp * 100) : 0;
            let cpc = totalClicks > 0 ? (totalSpend / totalClicks) : 0;
            let cr = totalClicks > 0 ? (totalOrders / totalClicks * 100) : 0;
            let impCr = totalImp > 0 ? (totalOrders / totalImp * 100) : 0;
            let aov = totalOrders > 0 ? (totalGmv / totalOrders) : 0;
            let cpa = totalOrders > 0 ? (totalSpend / totalOrders) : 0;
            let roas = totalSpend > 0 ? (totalGmv / totalSpend) : 0;
            let cir = totalGmv > 0 ? (totalSpend / totalGmv * 100) : 0;

            document.getElementById('kpi-gmv').innerText = totalGmv.toLocaleString('vi-VN') + ' đ';
            document.getElementById('kpi-gmv-day').innerText = Math.round(totalGmv / 4).toLocaleString('vi-VN') + ' đ/ngày';
            document.getElementById('kpi-spend').innerText = totalSpend.toLocaleString('vi-VN') + ' đ';
            document.getElementById('kpi-spend-day').innerText = Math.round(totalSpend / 4).toLocaleString('vi-VN') + ' đ/ngày';
            document.getElementById('kpi-roas').innerHTML = roas.toFixed(2) + 'x <span style="font-size: 16px; color: #fbbf24;">(' + cir.toFixed(2) + '%)</span>';
            document.getElementById('kpi-orders').innerHTML = totalOrders + ' đơn <span style="font-size: 14px; color: var(--text-muted);">/ ' + totalItems + ' sp</span>';
            document.getElementById('kpi-aov').innerText = Math.round(aov).toLocaleString('vi-VN') + ' đ';
            document.getElementById('kpi-imp').innerText = totalImp.toLocaleString('vi-VN');
            document.getElementById('kpi-clicks').innerHTML = totalClicks.toLocaleString('vi-VN') + ' <span style="font-size: 15px; color: #34d399;">(' + ctr.toFixed(2) + '%)</span>';
            document.getElementById('kpi-cpc').innerText = Math.round(cpc).toLocaleString('vi-VN') + ' đ';
            document.getElementById('kpi-cr').innerHTML = cr.toFixed(2) + '% <span style="font-size: 13px; color: var(--text-muted);">Click CR</span>';
            document.getElementById('kpi-imp-cr').innerText = impCr.toFixed(3) + '%';
            document.getElementById('kpi-cpa').innerText = Math.round(cpa).toLocaleString('vi-VN') + ' đ';
        }

        function renderTable() {
            let search = document.getElementById('searchCamp') ? document.getElementById('searchCamp').value.toLowerCase() : '';
            let filtered = campaignsData;
            if (currentScope === 'Shopee') {
                filtered = campaignsData.filter(c => c.shop !== 'TikTok Shop (GMV Max)');
            } else if (currentScope !== 'all') {
                filtered = campaignsData.filter(c => c.shop === currentScope);
            }
            
            if (search) {
                filtered = filtered.filter(c => c.name.toLowerCase().includes(search) || c.shop.toLowerCase().includes(search));
            }

            let tbody = document.getElementById('campaignTableBody');
            tbody.innerHTML = '';

            filtered.forEach(c => {
                let badge = c.status === 'safe' ? '<span class="badge-safe">🟢 An Toàn</span>' : 
                            (c.status === 'warn' ? '<span class="badge-warn">🟡 Cảnh Báo</span>' : '<span class="badge-danger">🔴 Vượt Trần</span>');
                
                let shopBadge = c.shop === '30Shine Store' ? '<span style="color: #ff7b5a; font-weight: 700;">Shopee 30Shine</span>' :
                                (c.shop === 'Dr.FORSKIN' ? '<span style="color: #60a5fa; font-weight: 700;">Shopee Dr.FORSKIN</span>' : 
                                (c.shop === 'Glanzen Vietnam' ? '<span style="color: #c084fc; font-weight: 700;">Shopee Glanzen</span>' : 
                                '<span style="color: #00f2fe; font-weight: 700;"><i class="fa-brands fa-tiktok"></i> TikTok GMV Max</span>'));

                let tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${shopBadge}</td>
                    <td class="campaign-name">${c.name}</td>
                    <td style="font-size: 11px; color: var(--text-muted);">${c.bidding}</td>
                    <td class="num-font" style="color: #f87171;">${c.spend.toLocaleString('vi-VN')} đ</td>
                    <td class="num-font" style="color: #34d399; font-weight: 700;">${c.gmv.toLocaleString('vi-VN')} đ</td>
                    <td class="num-font"><strong>${c.orders}</strong> (${c.sold})</td>
                    <td class="num-font">${c.imp.toLocaleString('vi-VN')}</td>
                    <td class="num-font">${c.clicks.toLocaleString('vi-VN')}</td>
                    <td class="num-font">${c.ctr.toFixed(2)}%</td>
                    <td class="num-font">${c.cpc.toLocaleString('vi-VN')} đ</td>
                    <td class="num-font" style="color: #34d399;">${((c.orders/c.clicks)*100).toFixed(2)}%</td>
                    <td class="num-font">${c.aov.toLocaleString('vi-VN')} đ</td>
                    <td class="num-font">${c.cpa.toLocaleString('vi-VN')} đ</td>
                    <td class="num-font" style="font-weight: 700; color: ${c.roas >= 6 ? '#34d399' : (c.roas >= 5 ? '#fbbf24' : '#f87171')};">${c.roas.toFixed(2)}x</td>
                    <td class="num-font" style="font-weight: 700; color: ${c.cir <= 15 ? '#34d399' : (c.cir <= 18 ? '#fbbf24' : '#f87171')};">${c.cir.toFixed(2)}%</td>
                    <td>${badge}</td>
                `;
                tbody.appendChild(tr);
            });
        }

        // INIT CHARTS
        window.addEventListener('DOMContentLoaded', () => {
            renderTable();

            // Chart 1: Channel GMV & Spend
            new Chart(document.getElementById('chartChannelGmv'), {
                type: 'bar',
                data: {
                    labels: ['Shopee (3 Shop)', 'TikTok Shop (GMV Max)'],
                    datasets: [
                        {
                            label: 'Doanh Thu (GMV)',
                            data: [49949960, 27431924],
                            backgroundColor: ['rgba(238, 77, 45, 0.8)', 'rgba(0, 242, 254, 0.8)'],
                            borderColor: ['#ee4d2d', '#00f2fe'],
                            borderWidth: 1,
                            borderRadius: 8
                        },
                        {
                            label: 'Chi Phí Ads (Spend)',
                            data: [8304305, 4526000],
                            backgroundColor: 'rgba(239, 68, 68, 0.75)',
                            borderColor: '#ef4444',
                            borderWidth: 1,
                            borderRadius: 8
                        }
                    ]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { labels: { color: '#94a3b8', font: { family: 'Plus Jakarta Sans', weight: 600 } } }
                    },
                    scales: {
                        x: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.05)' } },
                        y: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.05)' } }
                    }
                }
            });

            // Chart 2: ROAS & CIR
            new Chart(document.getElementById('chartChannelRoas'), {
                type: 'bar',
                data: {
                    labels: ['Shopee (3 Shop)', 'TikTok Shop (GMV Max)', 'Hợp Nhất Toàn Sàn'],
                    datasets: [
                        {
                            label: 'ROAS (x)',
                            data: [6.01, 6.06, 6.03],
                            backgroundColor: 'rgba(56, 189, 248, 0.8)',
                            borderColor: '#38bdf8',
                            borderWidth: 1,
                            borderRadius: 8,
                            yAxisID: 'y'
                        },
                        {
                            label: 'CIR (%)',
                            data: [16.63, 16.50, 16.58],
                            type: 'line',
                            borderColor: '#fbbf24',
                            backgroundColor: '#fbbf24',
                            borderWidth: 3,
                            pointRadius: 6,
                            yAxisID: 'y1'
                        }
                    ]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { labels: { color: '#94a3b8', font: { family: 'Plus Jakarta Sans', weight: 600 } } }
                    },
                    scales: {
                        x: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.05)' } },
                        y: { position: 'left', ticks: { color: '#38bdf8' }, grid: { color: 'rgba(255,255,255,0.05)' }, title: { display: true, text: 'ROAS (x)', color: '#38bdf8' } },
                        y1: { position: 'right', ticks: { color: '#fbbf24' }, grid: { drawOnChartArea: false }, title: { display: true, text: 'CIR (%)', color: '#fbbf24' } }
                    }
                }
            });
        });
    </script>
</body>
</html>"""

with open('/Users/longnd/BAO_CAO_HIEU_SUAT_QUANG_CAO_01_04_THANG_10_2026.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

with open('/Users/longnd/tiktok-dashboard/index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

with open('/Users/longnd/tiktok-dashboard/omnichannel_performance_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print('SUCCESSFULLY GENERATED OMNICHANNEL DASHBOARD!')
