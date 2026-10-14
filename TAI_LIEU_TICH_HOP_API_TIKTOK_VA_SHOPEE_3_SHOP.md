# TÀI LIỆU HƯỚNG DẪN TÍCH HỢP & TRÍCH XUẤT DỮ LIỆU TỪ API
## HỆ THỐNG SHOPEE (3 SHOP) VÀ TIKTOK (MARKETING ADS & TIKTOK SHOP)
*(Phiên bản cập nhật đầy đủ Credentials, Live Tokens & Sửa lỗi ngày 14/10/2026)*

> **Mục đích tài liệu:** Cung cấp đầy đủ thông số xác thực (Credentials, Active Access Tokens, Refresh Tokens), cơ chế ký số (HMAC-SHA256), danh mục Endpoints chuẩn xác và code mẫu Python sẵn sàng chạy để trích xuất dữ liệu vận hành (Chi phí Ads, Doanh thu, Đơn hàng, Hiệu suất GMV Max) từ **3 Shop Shopee chính** và **Hệ sinh thái TikTok**.

---

## PHẦN I: DANH SÁCH TÀI KHOẢN & THÔNG SỐ XÁC THỰC (CREDENTIALS & LIVE TOKENS)

### 1. Hệ thống Shopee Open Platform

* **API Base Host:** `https://partner.shopeemobile.com`
* **Partner ID:** `2037201`
* **Partner Key:** `shpk6f6c74594e5462544541724b4568426f657741416e516855424551437274`
* **Thời hạn ủy quyền App:** Đã ủy quyền hợp lệ đến **08/2027**.

#### Bảng thông số chi tiết & Cặp Token hoạt động (Active Tokens):

| STT | Tên Gian Hàng | Shop ID | Vai Trò & Ghi Chú | Live Access Token (Sống 4h) | Refresh Token (Sống 30 ngày) |
| :---: | :--- | :---: | :--- | :--- | :--- |
| 1 | **Shopee 30Shine Official** | `21080428` | **Hero Store** (HCM/Toàn quốc) | `eyJhbGciOiJIUzI1NiJ9.CNGrfBABGOzShgogASjnq7zWBjC2uIrDDDgBQAFIAw.-dN5qT8WdHCcG78XVXX-iTJWIrDg_oW1m6CBEdFOMhg` | `eyJhbGciOiJIUzI1NiJ9.CNGrfBABGOzShgogAijnq7zWBjDE-sY9OAFAAUgD.L3jcZ-WFkRySQxQ3oACKKWLooQUSl2-V1RU9d-J_5Gc` |
| 2 | **Shopee Dr.FORSKIN Store** | `278080971` | Gian Dược mỹ phẩm (Hà Nội) | `eyJhbGciOiJIUzI1NiJ9.CNGrfBABGMvbzIQBIAEo56u81gYwrtrp6AI4AUABSAM.J_yO01grv3ouCDZnQKB7SiEPayrXHKEdFr9Yu5bWmPU` | `eyJhbGciOiJIUzI1NiJ9.CNGrfBABGMvbzIQBIAIo56u81gYw5YK_vQE4AUABSAM.ZUN1S1fWAauMI9xr56LZ53rH83fTpW0zZTa7-5Lp89Y` |
| 3 | **Shopee Glanzen Official** | `945974027` | Gian hàng Mall Glanzen | `eyJhbGciOiJIUzI1NiJ9.CNGrfBABGIvWicMDIAEo56u81gYw5q33iAM4AUABSAM.ibF31njlpHPU8l3T9U4qJQ5EAplquotE4xSg-NzOjgw` | `eyJhbGciOiJIUzI1NiJ9.CNGrfBABGIvWicMDIAIo56u81gYwj_nRhQw4AUABSAM.dFVz32mxBoa_wuBlyonmKBaNXanRpoVV8VT9lMRC3kA` |
| *Ref* | *Shopee Laborie Derma* | `1339675825` | *Shop thứ 4 (Ủy quyền dự phòng)* | *Ngân sách Ads T10 = 0đ (Không chạy Ads)* | **KHÔNG CẦN KÉO DỮ LIỆU SHOP NÀY** |

> **⚠️ Giải đáp về Shop thứ 4 (`1339675825`):**
> Trong Console Shopee Partner có liên kết thêm shop `1339675825` (Laborie Derma). Tuy nhiên theo **Kế hoạch Ecom Tháng 10/2026** (dòng 31): *"Ngân sách Shopee theo gian: 30Shine 41M · Dr.Forskin 13.3M · Glanzen 6M · Laborie 0đ"*. Gian hàng này tháng 10 không phân bổ ngân sách chạy ads và không có KPI vận hành chính. Kỹ thuật **KHÔNG CẦN kéo dữ liệu** của shop này, chỉ tập trung vào **3 shop chính (30Shine, Dr.FORSKIN, Glanzen)**.

> **Cơ chế Token Shopee:**
> * `access_token` có hiệu lực trong **4 giờ (14.400 giây)**.
> * `refresh_token` có hiệu lực trong **30 ngày**.
> * Khi gọi API gặp lỗi `error_auth`, chỉ cần gọi API refresh token (mục III.1.4) bằng `refresh_token` tương ứng để nhận cặp mã mới.

---

### 2. Hệ thống TikTok
TikTok được chia thành **2 hệ thống API độc lập**:

#### A. TikTok Marketing API (Báo cáo Ads & GMV Max)
* **API Base Host:** `https://business-api.tiktok.com`
* **Advertiser ID (Tài khoản QC):** `7444857279880609808`
* **Access Token:** `d1acc31a7ccb6a32d77666a87d3ef4345c03d7f7`
* **Authentication Header:** Truyền trực tiếp qua header:  
  `Access-Token: d1acc31a7ccb6a32d77666a87d3ef4345c03d7f7`

#### B. TikTok Shop Open API (Đơn hàng, Doanh số, Kho, Sản phẩm)
* **API Base Host:** `https://open-api.tiktokglobalshop.com`
* **App Key:** `6jh02dvuq2oe9`
* **App Secret:** `066a3871e77d2ee4a1a526d70d5071795b59510a`
* **Shop ID:** `7494588084948339259`
* **Shop Cipher (Đã lấy sẵn):** `ROW_-F3j2wAAAAARt1ww1BaHT_fyFUQCRc62`
* **Active Access Token mới (Đã refresh):**  
  `ROW_bndNqgAAAAA0oMGsQ949Ax2uVMspFFpzfKGK39NnCfJLkr6SEIDz98sFpl35L57omMUtZcgLBSbrwIRcNtkC8mHptk_vvnZtFSj6FEXuNYepNozp8SGvOhDssnetz3YVhR7Triyf0WUaaO81MkfNFhexPBYwjUSr3XmzTQ9pCWZ58tI8CReVug`
* **Active Refresh Token:**  
  `ROW_yyA5zQAAAABbts_ERy1ZrX0s0eG3Bn6FPlJlmUfwksdqO8t9VcKo0OVr_rm2Yq-0gk5CYhZBqEk`
* **Authentication Header:** `x-tts-access-token: <SHOP_ACCESS_TOKEN>`

---

## PHẦN II: CƠ CHẾ KÝ CHỮ KÝ SỐ (SIGNATURE GENERATION)

### 1. Thuật toán tạo chữ ký Shopee (HMAC-SHA256)
* **Đối với API làm mới Token (`/api/v2/auth/access_token/get`):**  
  $$\text{base\_string} = \text{partner\_id} + \text{path} + \text{timestamp}$$
* **Đối với các API dữ liệu Shop (Đơn hàng, Ads, Sản phẩm):**  
  $$\text{base\_string} = \text{partner\_id} + \text{path} + \text{timestamp} + \text{access\_token} + \text{shop\_id}$$
* **Công thức ký:**  
  $$\text{sign} = \text{HMAC-SHA256}(\text{key}=\text{partner\_key}, \text{msg}=\text{base\_string}).\text{hexdigest}()$$

### 2. Thuật toán tạo chữ ký TikTok Shop (HMAC-SHA256)
* Sắp xếp toàn bộ query parameters (ngoại trừ param `sign` và `access_token`) theo thứ tự bảng chữ cái (`key`).
* Ghép chuỗi theo quy tắc:  
  $$\text{message} = \text{app\_secret} + \text{api\_path} + \text{param1value1param2value2...} + \text{body\_json\_string} + \text{app\_secret}$$
  *(Lưu ý: Nếu request dạng `GET` hoặc không có body, `body_json_string` là chuỗi rỗng `""`)*.
* Ký HMAC-SHA256:  
  $$\text{sign} = \text{HMAC-SHA256}(\text{key}=\text{app\_secret}, \text{msg}=\text{message}).\text{hexdigest}()$$

---

## PHẦN III: DANH MỤC CÁC ENDPOINT CHI TIẾT CẦN TÍCH HỢP

### 1. Nhóm Shopee Open API

#### 1.1. Lấy báo cáo hiệu suất Shopee Ads hàng ngày (Khuyên dùng)
* **Endpoint:** `GET /api/v2/ads/get_all_cpc_ads_daily_performance`
* **Query Params:**
  * `partner_id`: `2037201`
  * `timestamp`: Unix timestamp (giây)
  * `access_token`: Access token của shop tương ứng
  * `shop_id`: Shop ID cần lấy (`21080428`, `278080971`, `945974027`)
  * `sign`: Chữ ký HMAC-SHA256
  * `start_date`: Định dạng **`DD-MM-YYYY`** (ví dụ: `01-10-2026`)
  * `end_date`: Định dạng **`DD-MM-YYYY`** (ví dụ: `13-10-2026`)
* **Lưu ý:** Shopee giới hạn khoảng cách giữa `start_date` và `end_date` tối đa **14 ngày/lần gọi**.

#### 1.2. Làm mới Access Token Shopee
* **Endpoint:** `POST /api/v2/auth/access_token/get`
* **Sign formula:** `partner_id + path + timestamp`
* **Body (JSON):**
  ```json
  {
    "partner_id": 2037201,
    "shop_id": 21080428,
    "refresh_token": "eyJhbGciOiJIUzI1NiJ9..."
  }
  ```

#### 1.3. Lấy danh sách đơn hàng Shopee
* **Endpoint:** `GET /api/v2/order/get_order_list`
* **Query Params:**
  * `time_range_field`: `"create_time"`
  * `time_from`: Timestamp bắt đầu (giây)
  * `time_to`: Timestamp kết thúc (giây, tối đa 14 ngày)
  * `page_size`: `100`

---

### 2. Nhóm TikTok API

#### 2.1. Lấy báo cáo chi phí & GMV Max (TikTok Marketing API)
* **Endpoint:** `GET https://business-api.tiktok.com/open_api/v1.3/gmv_max/report/get/`
* **Headers:**
  * `Access-Token`: `d1acc31a7ccb6a32d77666a87d3ef4345c03d7f7`
* **Query Params:**
  * `advertiser_id`: `"7444857279880609808"`
  * `store_ids`: `json.dumps(["7494588084948339259"])`
  * `dimensions`: `json.dumps(["campaign_id", "stat_time_day"])` (hoặc `["advertiser_id", "stat_time_day"]`)
  * `metrics`: `json.dumps(["cost", "orders", "gross_revenue", "roi"])`
  * `start_date`: `"2026-10-01"` (YYYY-MM-DD)
  * `end_date`: `"2026-10-13"` (YYYY-MM-DD)
  * `page_size`: `1000`

#### 2.2. Làm mới Access Token TikTok Shop (Khi hết hạn)
* **Endpoint:** `GET https://auth.tiktok-shops.com/api/v2/token/refresh`
* **Query Params:**
  * `app_key`: `6jh02dvuq2oe9`
  * `app_secret`: `066a3871e77d2ee4a1a526d70d5071795b59510a`
  * `refresh_token`: `ROW_yyA5zQAAAABbts_ERy1ZrX0s0eG3Bn6FPlJlmUfwksdqO8t9VcKo0OVr_rm2Yq-0gk5CYhZBqEk`
  * `grant_type`: `"refresh_token"`

#### 2.3. Lấy Shop Cipher (TikTok Shop API)
* **Endpoint:** `GET https://open-api.tiktokglobalshop.com/authorization/202309/shops`
* **Headers:** `x-tts-access-token: ROW_bndNqg...`
* **Cipher trả về:** `ROW_-F3j2wAAAAARt1ww1BaHT_fyFUQCRc62` (đã lưu sẵn).

#### 2.4. Tìm kiếm đơn hàng TikTok Shop (ĐÃ SỬA CHUẨN TIMESTAMP NĂM 2026)
* **Endpoint:** `POST https://open-api.tiktokglobalshop.com/order/202309/orders/search`
* **Headers:**
  * `x-tts-access-token`: `ROW_bndNqgAAAAA0oMGsQ949Ax2uVMspFFpzfKGK39NnCfJLkr6SEIDz98sFpl35L57omMUtZcgLBSbrwIRcNtkC8mHptk_vvnZtFSj6FEXuNYepNozp8SGvOhDssnetz3YVhR7Triyf0WUaaO81MkfNFhexPBYwjUSr3XmzTQ9pCWZ58tI8CReVug`
  * `Content-Type`: `application/json`
* **Query Params:** `app_key`, `timestamp`, `shop_cipher`, `sign`
* **Body (JSON) — Thời gian Tháng 10/2026 chuẩn:**
  ```json
  {
    "page_size": 100,
    "create_time_ge": 1790787600,
    "create_time_lt": 1791910800
  }
  ```
  *(1790787600 = 01/10/2026 00:00:00 GMT+7; 1791910800 = 14/10/2026 00:00:00 GMT+7)*.

---

## PHẦN IV: CODE MẪU PYTHON HOÀN CHỈNH (CHẠY NGAY ĐƯỢC)

### 1. Code mẫu: Kéo Ads 3 Shop Shopee (Kèm Tự Động Refresh Token)
```python
import time
import hmac
import hashlib
import requests

HOST = "https://partner.shopeemobile.com"
PARTNER_ID = 2037201
PARTNER_KEY = "shpk6f6c74594e5462544541724b4568426f657741416e516855424551437274"

# Danh sách 3 shop chính kèm token đang hoạt động
SHOPS = [
    {
        "shop_id": 21080428,
        "shop_name": "Shopee 30Shine Official",
        "access_token": "eyJhbGciOiJIUzI1NiJ9.CNGrfBABGOzShgogASjnq7zWBjC2uIrDDDgBQAFIAw.-dN5qT8WdHCcG78XVXX-iTJWIrDg_oW1m6CBEdFOMhg",
        "refresh_token": "eyJhbGciOiJIUzI1NiJ9.CNGrfBABGOzShgogAijnq7zWBjDE-sY9OAFAAUgD.L3jcZ-WFkRySQxQ3oACKKWLooQUSl2-V1RU9d-J_5Gc"
    },
    {
        "shop_id": 278080971,
        "shop_name": "Shopee Dr.FORSKIN Store",
        "access_token": "eyJhbGciOiJIUzI1NiJ9.CNGrfBABGMvbzIQBIAEo56u81gYwrtrp6AI4AUABSAM.J_yO01grv3ouCDZnQKB7SiEPayrXHKEdFr9Yu5bWmPU",
        "refresh_token": "eyJhbGciOiJIUzI1NiJ9.CNGrfBABGMvbzIQBIAIo56u81gYw5YK_vQE4AUABSAM.ZUN1S1fWAauMI9xr56LZ53rH83fTpW0zZTa7-5Lp89Y"
    },
    {
        "shop_id": 945974027,
        "shop_name": "Shopee Glanzen Official",
        "access_token": "eyJhbGciOiJIUzI1NiJ9.CNGrfBABGIvWicMDIAEo56u81gYw5q33iAM4AUABSAM.ibF31njlpHPU8l3T9U4qJQ5EAplquotE4xSg-NzOjgw",
        "refresh_token": "eyJhbGciOiJIUzI1NiJ9.CNGrfBABGIvWicMDIAIo56u81gYwj_nRhQw4AUABSAM.dFVz32mxBoa_wuBlyonmKBaNXanRpoVV8VT9lMRC3kA"
    }
]

def generate_shopee_sign(partner_key, base_string):
    return hmac.new(partner_key.encode('utf-8'), base_string.encode('utf-8'), hashlib.sha256).hexdigest()

def refresh_shopee_token(shop_id, refresh_token):
    path = "/api/v2/auth/access_token/get"
    ts = int(time.time())
    base_str = f"{PARTNER_ID}{path}{ts}"
    sign = generate_shopee_sign(PARTNER_KEY, base_str)
    
    url = f"{HOST}{path}?partner_id={PARTNER_ID}&timestamp={ts}&sign={sign}"
    body = {"partner_id": PARTNER_ID, "shop_id": int(shop_id), "refresh_token": refresh_token}
    res = requests.post(url, json=body, timeout=15).json()
    return res

def get_shopee_ads(shop):
    path = "/api/v2/ads/get_all_cpc_ads_daily_performance"
    ts = int(time.time())
    base_str = f"{PARTNER_ID}{path}{ts}{shop['access_token']}{shop['shop_id']}"
    sign = generate_shopee_sign(PARTNER_KEY, base_str)
    
    url = f"{HOST}{path}"
    params = {
        "partner_id": PARTNER_ID,
        "timestamp": ts,
        "access_token": shop["access_token"],
        "shop_id": shop["shop_id"],
        "sign": sign,
        "start_date": "10-10-2026",
        "end_date": "10-10-2026"
    }
    
    res = requests.get(url, params=params, timeout=15).json()
    # Nếu token hết hạn thì tự động làm mới
    if res.get("error") in ["error_auth", "token_invalid"]:
        print(f"Token shop {shop['shop_name']} hết hạn, đang tự động làm mới...")
        new_token = refresh_shopee_token(shop["shop_id"], shop["refresh_token"])
        if "access_token" in new_token:
            shop["access_token"] = new_token["access_token"]
            shop["refresh_token"] = new_token["refresh_token"]
            return get_shopee_ads(shop)
    return res

if __name__ == "__main__":
    for shop in SHOPS:
        res = get_shopee_ads(shop)
        print(f"Shop: {shop['shop_name']} -> Số bản ghi: {len(res.get('response', []))}")
```

---

### 2. Code mẫu: Kéo Đơn Hàng TikTok Shop (Chuẩn Ký & Timestamp 2026)
```python
import time
import hashlib
import hmac
import json
import requests
from datetime import datetime, timezone, timedelta

APP_KEY = "6jh02dvuq2oe9"
APP_SECRET = "066a3871e77d2ee4a1a526d70d5071795b59510a"
ACCESS_TOKEN = "ROW_bndNqgAAAAA0oMGsQ949Ax2uVMspFFpzfKGK39NnCfJLkr6SEIDz98sFpl35L57omMUtZcgLBSbrwIRcNtkC8mHptk_vvnZtFSj6FEXuNYepNozp8SGvOhDssnetz3YVhR7Triyf0WUaaO81MkfNFhexPBYwjUSr3XmzTQ9pCWZ58tI8CReVug"
SHOP_CIPHER = "ROW_-F3j2wAAAAARt1ww1BaHT_fyFUQCRc62"

def generate_tiktok_shop_sign(secret, path, params, body=""):
    sorted_keys = sorted(params.keys())
    param_string = "".join([f"{k}{params[k]}" for k in sorted_keys])
    msg = f"{secret}{path}{param_string}{body}{secret}"
    return hmac.new(secret.encode("utf-8"), msg.encode("utf-8"), hashlib.sha256).hexdigest()

def search_tiktok_orders(start_dt, end_dt):
    path = "/order/202309/orders/search"
    ts = str(int(time.time()))
    
    params = {
        "app_key": APP_KEY,
        "timestamp": ts,
        "shop_cipher": SHOP_CIPHER,
        "page_size": "50"
    }
    
    # Tính timestamp GMT+7 chuẩn năm 2026
    start_ts = int(start_dt.timestamp())
    end_ts = int(end_dt.timestamp())
    
    body = json.dumps({
        "create_time_ge": start_ts,
        "create_time_lt": end_ts
    })
    
    # Tạo chữ ký HMAC-SHA256
    sign = generate_tiktok_shop_sign(APP_SECRET, path, params, body)
    params["sign"] = sign
    
    headers = {
        "x-tts-access-token": ACCESS_TOKEN,
        "Content-Type": "application/json"
    }
    
    url = f"https://open-api.tiktokglobalshop.com{path}"
    res = requests.post(url, headers=headers, params=params, data=body, timeout=20)
    return res.json()

if __name__ == "__main__":
    tz_vn = timezone(timedelta(hours=7))
    start_date = datetime(2026, 10, 1, 0, 0, 0, tzinfo=tz_vn)
    end_date = datetime(2026, 10, 14, 0, 0, 0, tzinfo=tz_vn)
    
    data = search_tiktok_orders(start_date, end_date)
    print("Mã phản hồi:", data.get("code"), data.get("message"))
    orders = data.get("data", {}).get("orders", [])
    print(f"Số lượng đơn kéo được: {len(orders)}")
    if orders:
        print("Mẫu đơn hàng đầu tiên:", orders[0].get("id"), "Trạng thái:", orders[0].get("status"))
```

---

## PHẦN V: TỔNG KẾT CÁC LƯU Ý KỸ THUẬT (ACTIONABLE CHECKLIST)

1. **Shopee (3 Shop chính):**
   * Sử dụng trực tiếp danh sách `SHOPS` với `access_token` và `refresh_token` đã cung cấp ở Phần I.
   * Khi `access_token` hết hạn (sau 4h), hệ thống sẽ tự dùng `refresh_token` lấy cặp mã mới mà không cần đăng nhập lại trình duyệt.
   * **Bỏ qua shop `1339675825`** (Laborie) do không chạy Ads tháng 10.
2. **TikTok Shop:**
   * Sử dụng ngay `ACCESS_TOKEN` mới (tiền tố `ROW_bndNqg...`) và `SHOP_CIPHER` (`ROW_-F3j2w...`).
   * Luôn sử dụng timestamp tính theo năm **2026** (ví dụ `1790787600` đến `1791910800`).
3. **TikTok GMV Max Ads:**
   * Tiếp tục duy trì endpoint `https://business-api.tiktok.com/open_api/v1.3/gmv_max/report/get/` với các chỉ số `cost, orders, gross_revenue, roi` như bạn đã chạy thành công.
