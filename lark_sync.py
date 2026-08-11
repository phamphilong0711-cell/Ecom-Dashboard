import os
import requests
import datetime
from dotenv import load_dotenv
import database

# Load môi trường
load_dotenv("config.env")

def excel_date_to_datetime(excel_date):
    """Chuyển đổi số serial của Excel/Lark thành YYYY-MM-DD"""
    try:
        dt = datetime.datetime(1899, 12, 30) + datetime.timedelta(days=float(excel_date))
        return dt.strftime('%Y-%m-%d')
    except:
        return None

def sync_lark_revenue():
    app_id = os.getenv("LARK_APP_ID")
    app_secret = os.getenv("LARK_APP_SECRET")
    spreadsheet_token = os.getenv("LARK_SPREADSHEET_TOKEN")
    
    # Mặc định lấy sheet cấu hình, hoặc list các sheet T7, T8
    sheet_ids = ["XFj6B7", "YYekBK"] # T7, T8
    
    if not all([app_id, app_secret, spreadsheet_token]):
        print("Lỗi: Thiếu cấu hình Lark API trong config.env")
        return False
        
    print("Đang kết nối Lark API lấy Token...")
    # 1. Lấy Token
    url = "https://open.larksuite.com/open-apis/auth/v3/tenant_access_token/internal"
    payload = {
        "app_id": app_id,
        "app_secret": app_secret
    }
    response = requests.post(url, json=payload)
    data = response.json()
    if data.get("code") != 0:
        print("Lỗi lấy Lark Token:", data)
        return False
        
    token = data["tenant_access_token"]
    
    all_metrics = []
    all_costs = []

    # 2. Lặp qua các Sheet
    for sheet_id in sheet_ids:
        print(f"Đang tải dữ liệu Báo Cáo Hàng Ngày từ Sheet ID: {sheet_id}...")
        sheet_url = f"https://open.larksuite.com/open-apis/sheets/v2/spreadsheets/{spreadsheet_token}/values/{sheet_id}!A10:AZ500"
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        resp = requests.get(sheet_url, headers=headers)
        sheet_data = resp.json()
        if sheet_data.get("code") != 0:
            print(f"Lỗi lấy dữ liệu Lark từ {sheet_id}:", sheet_data)
            continue
            
        values = sheet_data.get("data", {}).get("valueRange", {}).get("values", [])
        
        for row in values:
            if not row or not row[0]:
                continue
                
            date_val = excel_date_to_datetime(row[0])
            if not date_val:
                continue
                
            def safe_float(idx):
                if len(row) > idx and row[idx]:
                    val = str(row[idx]).replace(',', '').replace(' ', '')
                    try: 
                        if '+' in val:
                            return sum(float(x) for x in val.split('+') if x)
                        return float(val)
                    except: 
                        return 0.0
                return 0.0
                
            def safe_int(idx):
                if len(row) > idx and row[idx]:
                    try: return int(float(row[idx]))
                    except: return 0
                return 0

            # Cấu hình map cột (Index: Tên Seller, Tên Source)
            mapping = [
                {"rev_idx": 2, "ord_idx": 11, "seller": "Shopee Dr", "source": "Shopee"},
                {"rev_idx": 3, "ord_idx": 12, "seller": "Shopee 30Shine", "source": "Shopee"},
                {"rev_idx": 4, "ord_idx": 13, "seller": "Shopee GL", "source": "Shopee"},
                {"rev_idx": 6, "ord_idx": 15, "seller": "Lazada", "source": "Lazada"},
                {"rev_idx": 7, "ord_idx": 16, "seller": "Facebook", "source": "Facebook"},
                {"rev_idx": 8, "ord_idx": 17, "seller": "Web/App", "source": "Web/App"},
            ]
            
            for m in mapping:
                rev = safe_float(m["rev_idx"])
                orders = safe_int(m["ord_idx"])
                
                if rev > 0 or orders > 0:
                    aov = rev / orders if orders > 0 else 0
                    
                    all_metrics.append({
                        'date': date_val,
                        'source': m["source"],
                        'seller': m["seller"],
                        'revenue': rev,
                        'orders': orders,
                        'aov': aov,
                        'upsell': 0,
                        'final_revenue': rev
                    })
                    
            # Xử lý Chi phí (Ads Spend)
            shopee_cost = safe_float(27) + safe_float(28) + safe_float(29)
            tiktok_cost = safe_float(30)
            lazada_cost = safe_float(31)
            facebook_cost = safe_float(32)
            
            if shopee_cost > 0:
                all_costs.append({"date": date_val, "platform": "Shopee", "campaign": "Shopee (Lark)", "spend": shopee_cost})
            if tiktok_cost > 0:
                all_costs.append({"date": date_val, "platform": "TikTok Ads", "campaign": "TikTok (Lark)", "spend": tiktok_cost})
            if lazada_cost > 0:
                all_costs.append({"date": date_val, "platform": "Lazada", "campaign": "Lazada (Lark)", "spend": lazada_cost})
            if facebook_cost > 0:
                all_costs.append({"date": date_val, "platform": "Facebook Ads", "campaign": "Facebook (Lark)", "spend": facebook_cost})
                
            # Xử lý Chi phí khác
            ttlk_shopee = safe_float(33)
            ttlk_tiktok = safe_float(34)
            booking = safe_float(35)
            media_mkt = safe_float(36)
            
            if ttlk_shopee > 0:
                all_costs.append({"date": date_val, "platform": "Khác - TTLK Shopee", "campaign": "TTLK Shopee", "spend": ttlk_shopee})
            if ttlk_tiktok > 0:
                all_costs.append({"date": date_val, "platform": "Khác - TTLK Tiktok", "campaign": "TTLK Tiktok", "spend": ttlk_tiktok})
            if booking > 0:
                all_costs.append({"date": date_val, "platform": "Khác - Booking", "campaign": "Booking", "spend": booking})
            if media_mkt > 0:
                all_costs.append({"date": date_val, "platform": "Khác - Media MKT", "campaign": "Media MKT", "spend": media_mkt})
                
    if all_metrics:
        database.save_daily_metrics(all_metrics)
        print(f"Đã lưu thành công {len(all_metrics)} bản ghi Doanh thu từ Lark API!")
        
    if all_costs:
        database.save_ads_spend(all_costs)
        print(f"Đã lưu thành công {len(all_costs)} bản ghi Chi phí từ Lark API!")
        
    if all_metrics or all_costs:
        return True
    else:
        print("Không tìm thấy dữ liệu hợp lệ trong file Lark.")
        return False

if __name__ == "__main__":
    sync_lark_revenue()
