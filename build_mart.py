import sqlite3
import json
from datetime import datetime

DB_PATH = 'shop_data.db'

def build_mart():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Quét bảng orders để lấy doanh thu Gross và gán vào fact_sales_daily
    # Lưu ý: channel_id tạm thời gán cứng là 'tiktok' cho các order hiện có, shop_id='all'
    cursor.execute("SELECT create_time, status, total_amount, line_items, platform, shop_id FROM orders")
    orders = cursor.fetchall()

    daily_sales = {} # (date, channel, shop, sku) -> {qty, orders, gross_revenue, name, brand}
    
    for order in orders:
        status = order[1]
        # Bỏ qua đơn huỷ/chưa thanh toán để lấy GROSS REVENUE
        if status in ["CANCEL", "CANCELLED", "UNPAID", "ĐÃ HỦY"]:
            continue
            
        create_time = order[0]
        date_str = datetime.fromtimestamp(create_time).strftime("%Y-%m-%d")
        
        channel = order[4] if order[4] else 'tiktok'
        shop = order[5] if order[5] else 'all'
        
        line_items_str = order[3]
        if not line_items_str:
            continue
            
        try:
            line_items = json.loads(line_items_str)
            for item in line_items:
                product_name_raw = item.get("product_name", "").strip()
                sku_name = item.get("sku_name", "").strip()
                
                # Ưu tiên lấy tên gốc (product_name) thay vì tên phân loại (sku_name)
                display_name = product_name_raw if product_name_raw else (sku_name if sku_name else "Khác")
                
                # Brand logic (tạm thời)
                lower_name = display_name.lower()
                if any(kw in lower_name for kw in ["glanzen", "sáp", "gôm", "wax", "booster", "kevin murphy"]):
                    brand = "Glanzen"
                elif any(kw in lower_name for kw in ["dr.forskin", "dr. forskin", "tràm trà", "serum", "than hoạt", "sữa rửa mặt"]):
                    brand = "Dr.FORSKIN"
                else:
                    brand = "Khác"
                
                sku_code = item.get("seller_sku", "").strip()
                if not sku_code:
                    sku_code = display_name # Dùng tên làm sku_code tạm thời nếu seller_sku rỗng
                    
                # Combine SKU and Name
                if sku_code != display_name and sku_code not in display_name:
                    display_name = f"[{sku_code}] {display_name}"
                    
                price = float(item.get("sale_price", 0))
                quantity = int(item.get("quantity", 1))
                revenue = price * quantity
                
                key = (date_str, channel, shop, sku_code)
                if key not in daily_sales:
                    daily_sales[key] = {
                        "name": display_name,
                        "brand": brand,
                        "qty": 0,
                        "orders": 0,
                        "gross_revenue": 0
                    }
                daily_sales[key]["qty"] += quantity
                daily_sales[key]["orders"] += 1 # Đếm số lượt xuất hiện trong đơn (gần đúng số đơn chứa SKU)
                daily_sales[key]["gross_revenue"] += revenue
        except json.JSONDecodeError:
            continue

    # 1.5. Đọc thêm dữ liệu từ Lark (daily_metrics) cho các sàn chưa có data API chi tiết
    cursor.execute("SELECT date, source, seller, revenue, orders FROM daily_metrics")
    metrics = cursor.fetchall()
    
    for metric in metrics:
        date_str, source, seller, rev, ord_count = metric
        if not source or not date_str:
            continue
            
        source_lower = source.lower()
        if 'tiktok' in source_lower or 'shopee' in source_lower or 'lazada' in source_lower:
            continue # Đã có data chi tiết từ bảng orders

        channel = 'facebook' if 'facebook' in source_lower else 'webapp'
        shop = seller
        sku = 'UNALLOCATED'
        
        key = (date_str, channel, shop, sku)
        if key not in daily_sales:
            daily_sales[key] = {
                "name": f"Chưa phân bổ ({source})",
                "brand": "N/A",
                "qty": ord_count,
                "orders": ord_count,
                "gross_revenue": 0
            }
        daily_sales[key]["gross_revenue"] += float(rev)
        daily_sales[key]["orders"] += int(ord_count)

    # Nạp vào fact_sales_daily
    cursor.execute("DELETE FROM fact_sales_daily")
    for (date_str, channel, shop, sku), data in daily_sales.items():
        cursor.execute('''
            INSERT INTO fact_sales_daily (date, channel_id, shop_id, sku_code, gross_revenue, qty, orders, net_revenue, return_value)
            VALUES (?, ?, ?, ?, ?, ?, ?, 0, 0)
        ''', (date_str, channel, shop, sku, data['gross_revenue'], data['qty'], data['orders']))
        
        # Insert tạm vào dim_sku nếu chưa có
        cursor.execute("INSERT OR IGNORE INTO dim_sku (sku_code, name, category) VALUES (?, ?, ?)", (sku, data['name'], data['brand']))

    # 2. Xử lý Chi phí (fact_cost_daily)
    # Lấy Ads Spend từ ads_spend table
    cursor.execute("SELECT date, platform, SUM(spend) FROM ads_spend GROUP BY date, platform")
    ads_data = cursor.fetchall()
    
    daily_ads = {}
    for row in ads_data:
        date_str, platform, spend = row
        channel = 'tiktok' if 'tiktok' in platform.lower() else ('facebook' if 'facebook' in platform.lower() else platform.lower())
        daily_ads[(date_str, channel)] = spend

    # Phân bổ Ads xuống SKU
    cursor.execute("DELETE FROM fact_cost_daily")
    
    # Tính tổng doanh thu theo ngày + kênh để chia tỷ trọng
    daily_channel_rev = {}
    for (date_str, channel, shop, sku), data in daily_sales.items():
        k = (date_str, channel)
        daily_channel_rev[k] = daily_channel_rev.get(k, 0) + data['gross_revenue']

    for (date_str, channel, shop, sku), data in daily_sales.items():
        k = (date_str, channel)
        total_rev = daily_channel_rev.get(k, 1) # tránh chia 0
        ratio = data['gross_revenue'] / total_rev if total_rev > 0 else 0
        
        total_ads = daily_ads.get(k, 0)
        allocated_ads = total_ads * ratio
        
        # Các chi phí khác
        cogs = data['gross_revenue'] * 0.265
        promo_cost = 0
        
        # Tạm tính phí sàn theo yêu cầu: tiktok 28%, shopee 32%, lazada 35%
        platform_fee = 0
        if channel == 'tiktok':
            platform_fee = data['gross_revenue'] * 0.28
        elif channel == 'shopee':
            platform_fee = data['gross_revenue'] * 0.32
        elif channel == 'lazada':
            platform_fee = data['gross_revenue'] * 0.35
        
        cursor.execute('''
            INSERT INTO fact_cost_daily (date, channel_id, shop_id, sku_code, cogs, platform_fee, promo_cost, ads_spend, booking_cost)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0)
        ''', (date_str, channel, shop, sku, cogs, platform_fee, promo_cost, allocated_ads))

    conn.commit()
    
    # 3. Xuất Data JSON cho UI (mart_pnl_data)
    cursor.execute('''
        SELECT s.date, s.channel_id, s.sku_code, d.name, d.category as brand, 
               s.gross_revenue, s.qty, s.orders,
               c.cogs, c.platform_fee, c.promo_cost, c.ads_spend
        FROM fact_sales_daily s
        JOIN dim_sku d ON s.sku_code = d.sku_code
        LEFT JOIN fact_cost_daily c ON s.date = c.date AND s.channel_id = c.channel_id AND s.shop_id = c.shop_id AND s.sku_code = c.sku_code
    ''')
    
    pnl_rows = cursor.fetchall()
    
    pnl_data = []
    for row in pnl_rows:
        gross = row[5] or 0
        cogs = row[8] or 0
        platform_fee = row[9] or 0
        promo_cost = row[10] or 0
        ads_spend = row[11] or 0
        pnl = gross - cogs - platform_fee - promo_cost - ads_spend
        
        pnl_data.append({
            "date": row[0],
            "channel": row[1],
            "sku": row[2],
            "name": row[3],
            "brand": row[4],
            "gross_revenue": gross,
            "qty": row[6],
            "orders": row[7],
            "cogs": cogs,
            "platform_fee": platform_fee,
            "promo_cost": promo_cost,
            "ads_spend": ads_spend,
            "pnl": pnl
        })
    # 4. Xuất Data JSON cho Marketing (marketing_data)
    cursor.execute('''
        SELECT date, platform, campaign, spend, gmv_max_orders, gmv_max_revenue, clicks, impressions
        FROM ads_spend
    ''')
    
    marketing_rows = cursor.fetchall()
    marketing_data = []
    for row in marketing_rows:
        marketing_data.append({
            "date": row[0],
            "platform": row[1],
            "campaign": row[2],
            "spend": row[3] or 0,
            "orders": row[4] or 0,
            "revenue": row[5] or 0,
            "clicks": row[6] or 0,
            "impressions": row[7] or 0
        })
        
    out_data = {
        "pnl_data": pnl_data,
        "marketing_data": marketing_data,
        "last_updated": datetime.now().strftime("%d/%m/%Y %H:%M")
    }
    
    with open('/home/pham-phi-long-109/Downloads/tiktok-dashboard/data_v2.json', 'w', encoding='utf-8') as f:
        json.dump(out_data, f, ensure_ascii=False)
        
    print("Build mart và xuất data_v2.json thành công!")
    conn.close()

if __name__ == '__main__':
    build_mart()
