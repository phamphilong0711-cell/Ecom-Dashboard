import requests
import datetime
import os
import shutil
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# 1. Authenticate with Lark Open Platform API
from dotenv import load_dotenv
load_dotenv('/Users/longnd/tiktok-dashboard/config.env')
app_id = os.getenv('LARK_APP_ID')
app_secret = os.getenv('LARK_APP_SECRET')
resp = requests.post(
    'https://open.larksuite.com/open-apis/auth/v3/tenant_access_token/internal',
    json={'app_id': app_id, 'app_secret': app_secret}
)
token = resp.json().get('tenant_access_token')
if not token:
    raise RuntimeError(f"Failed to get Lark token: {resp.text}")

headers = {'Authorization': f'Bearer {token}'}
ss_token = 'VchysWW5dh7uvLtxlcSl4scRgLh'

# 2. Function to fetch all rows for a sheet
def fetch_lark_sheet_data(sheet_id):
    url = f'https://open.larksuite.com/open-apis/sheets/v2/spreadsheets/{ss_token}/values/{sheet_id}!A1:N120'
    r = requests.get(url, headers=headers)
    data = r.json().get('data', {}).get('valueRange', {}).get('values', [])
    # Filter out completely empty trailing rows
    filtered = []
    for row in data:
        if any(row):
            filtered.append(row)
    return filtered

wrjoa_rows = fetch_lark_sheet_data('WRJzoA')  # Tháng 11.2026
nf1beo_rows = fetch_lark_sheet_data('NF1Beo')  # Tháng 10.2026

print(f"Fetched WRJzoA (Tháng 11): {len(wrjoa_rows)} rows")
print(f"Fetched NF1Beo (Tháng 10): {len(nf1beo_rows)} rows")

# 3. Styling constants matching 'Đăng ký ca livestream  (1).xlsx' concept
FONT_CALIBRI_10_BOLD = Font(name='Calibri', size=10, bold=True, color='000000')
FONT_CALIBRI_10 = Font(name='Calibri', size=10, bold=False, color='000000')
FONT_CALIBRI_11_BOLD = Font(name='Calibri', size=11, bold=True, color='000000')

FILL_BLUE_HEADER = PatternFill(start_color='FFBACEFD', end_color='FFBACEFD', fill_type='solid')   # Pastel Blue
FILL_YELLOW_HEADER = PatternFill(start_color='FFFAF1D1', end_color='FFFAF1D1', fill_type='solid') # Pastel Yellow
FILL_CA6 = PatternFill(start_color='FFEEF6C6', end_color='FFEEF6C6', fill_type='solid')           # Light Pastel Yellow-Green
FILL_TOTAL = PatternFill(start_color='FFF2F4F7', end_color='FFF2F4F7', fill_type='solid')         # Soft Gray

BORDER_GRAY = 'D0D5DD'
THIN_SIDE = Side(border_style='thin', color=BORDER_GRAY)
DOUBLE_SIDE = Side(border_style='double', color='000000')

CELL_BORDER = Border(left=THIN_SIDE, right=THIN_SIDE, top=THIN_SIDE, bottom=THIN_SIDE)
TOTAL_BORDER = Border(left=THIN_SIDE, right=THIN_SIDE, top=THIN_SIDE, bottom=DOUBLE_SIDE)

ALIGN_CENTER = Alignment(horizontal='center', vertical='center', wrap_text=True)
ALIGN_LEFT = Alignment(horizontal='left', vertical='center', wrap_text=True)
ALIGN_RIGHT = Alignment(horizontal='right', vertical='center', wrap_text=False)

COLUMN_WIDTHS = {
    'A': 13.0,  # Ngày
    'B': 17.5,  # Ca
    'C': 12.0,  # Host (Đăng ký)
    'D': 12.0,  # Host (Thực tế)
    'E': 13.0,  # Giờ bắt đầu
    'F': 13.0,  # Giờ kết thúc
    'G': 10.0,  # Số giờ
    'H': 17.0,  # Doanh thu
    'I': 18.0,  # Doanh thu thực tế
    'J': 32.0,  # Mã đơn trong live
    'K': 15.0,  # Chi phí ads
    'L': 28.0,  # Chi phí thuê phòng ngoài giờ (Cột L)
    'M': 16.0,  # Địa điểm live (Cột M)
    'N': 25.0,  # Tổng giá trị hàng hóa của buổi LIVE (₫)
}

def parse_cell_value(val):
    if val is None or val == '':
        return None
    if isinstance(val, (int, float)):
        return val
    s = str(val).strip()
    if s == '' or s == '-':
        return s
    # Check if integer
    try:
        if s.isdigit() or (s.startswith('-') and s[1:].isdigit()):
            return int(s)
    except:
        pass
    # Check if float
    try:
        return float(s)
    except:
        pass
    return s

def build_concept_sheet(ws, raw_rows, is_nov=True):
    # Setup sheet view properties
    ws.views.sheetView[0].showGridLines = True
    
    # 1. Apply column widths
    for col_letter, width in COLUMN_WIDTHS.items():
        ws.column_dimensions[col_letter].width = width
        
    # 2. Header Row 1 & 2
    ws.row_dimensions[1].height = 41.05
    ws.row_dimensions[2].height = 41.05
    
    # Pre-fill all header cells with border & empty default
    for r in [1, 2]:
        for c in range(1, 15):
            cell = ws.cell(row=r, column=c)
            cell.border = CELL_BORDER
            cell.font = FONT_CALIBRI_10_BOLD
            cell.alignment = ALIGN_CENTER
            # Blue for cols A, B, C; Yellow for D to N
            if c <= 3:
                cell.fill = FILL_BLUE_HEADER
            else:
                cell.fill = FILL_YELLOW_HEADER
                
    # Specific Header Text matching concept
    ws.cell(row=1, column=1, value='Ngày')
    ws.cell(row=2, column=1, value='Ngày')
    ws.merge_cells('A1:A2')
    
    ws.cell(row=1, column=2, value='Đăng ký')
    ws.cell(row=1, column=3, value=None)
    ws.merge_cells('B1:C1')
    ws.cell(row=2, column=2, value='Ca')
    ws.cell(row=2, column=3, value='Host')
    
    ws.cell(row=1, column=4, value='Thực tế')
    ws.merge_cells('D1:H1')
    ws.cell(row=2, column=4, value='Host')
    ws.cell(row=2, column=5, value='Giờ bắt đầu')
    ws.cell(row=2, column=6, value='Giờ kết thúc')
    ws.cell(row=2, column=7, value='Số giờ ')
    ws.cell(row=2, column=8, value='Doanh thu')
    
    ws.cell(row=1, column=9, value='DT SAU HUỶ')
    ws.cell(row=2, column=9, value='Doanh thu thực tế')
    
    ws.cell(row=1, column=10, value='Mã đơn trong live')
    ws.cell(row=2, column=10, value=None)
    ws.merge_cells('J1:J2')
    
    ws.cell(row=1, column=11, value='Chi phí ads')
    ws.cell(row=2, column=11, value=None)
    ws.merge_cells('K1:K2')
    
    ws.cell(row=1, column=12, value='Chi phí thuê phòng ngoài giờ')
    ws.cell(row=2, column=12, value=None)
    ws.merge_cells('L1:L2')
    
    ws.cell(row=1, column=13, value='Địa điểm live')
    ws.cell(row=2, column=13, value=None)
    ws.merge_cells('M1:M2')
    
    ws.cell(row=1, column=14, value='Tổng giá trị hàng hóa của buổi LIVE (₫)')
    ws.cell(row=2, column=14, value=None)
    ws.merge_cells('N1:N2')
    
    # 3. Data rows (starting from row index 2 in raw_rows)
    data_start_row = 3
    current_row = data_start_row
    
    base_excel_date = datetime.date(1899, 12, 30)
    
    for r_idx in range(2, len(raw_rows)):
        row_data = raw_rows[r_idx]
        if not any(row_data):
            continue
            
        ws.row_dimensions[current_row].height = 36.0
        
        # Col A: Ngày
        raw_ngay = row_data[0] if len(row_data) > 0 else None
        cell_a = ws.cell(row=current_row, column=1)
        if isinstance(raw_ngay, (int, float)) and raw_ngay > 40000:
            calc_date = base_excel_date + datetime.timedelta(days=int(raw_ngay))
            cell_a.value = calc_date
            cell_a.number_format = 'dd/mm/yyyy'
        elif isinstance(raw_ngay, str) and raw_ngay.strip():
            cell_a.value = raw_ngay.strip()
        else:
            cell_a.value = raw_ngay
        cell_a.font = FONT_CALIBRI_10
        cell_a.alignment = ALIGN_CENTER
        cell_a.border = CELL_BORDER
        
        # Col B: Ca
        raw_ca = str(row_data[1]).strip() if len(row_data) > 1 and row_data[1] is not None else ''
        cell_b = ws.cell(row=current_row, column=2, value=raw_ca)
        cell_b.font = FONT_CALIBRI_10
        cell_b.alignment = ALIGN_LEFT
        cell_b.border = CELL_BORDER
        if 'Ca 6' in raw_ca or '21h' in raw_ca:
            cell_b.fill = FILL_CA6  # Concept highlight for Ca 6
            
        # Col C: Host (ĐK)
        raw_host_dk = row_data[2] if len(row_data) > 2 else None
        cell_c = ws.cell(row=current_row, column=3, value=parse_cell_value(raw_host_dk))
        cell_c.font = FONT_CALIBRI_10
        cell_c.alignment = ALIGN_CENTER
        cell_c.border = CELL_BORDER
        
        # Col D: Host (TT)
        raw_host_tt = row_data[3] if len(row_data) > 3 else None
        cell_d = ws.cell(row=current_row, column=4, value=parse_cell_value(raw_host_tt))
        cell_d.font = FONT_CALIBRI_10
        cell_d.alignment = ALIGN_CENTER
        cell_d.border = CELL_BORDER
        
        # Col E: Giờ bắt đầu
        raw_gbd = row_data[4] if len(row_data) > 4 else None
        cell_e = ws.cell(row=current_row, column=5, value=parse_cell_value(raw_gbd))
        cell_e.font = FONT_CALIBRI_10
        cell_e.alignment = ALIGN_CENTER
        cell_e.border = CELL_BORDER
        
        # Col F: Giờ kết thúc
        raw_gkt = row_data[5] if len(row_data) > 5 else None
        cell_f = ws.cell(row=current_row, column=6, value=parse_cell_value(raw_gkt))
        cell_f.font = FONT_CALIBRI_10
        cell_f.alignment = ALIGN_CENTER
        cell_f.border = CELL_BORDER
        
        # Col G: Số giờ
        raw_gio = row_data[6] if len(row_data) > 6 else None
        cell_g = ws.cell(row=current_row, column=7, value=parse_cell_value(raw_gio))
        cell_g.font = FONT_CALIBRI_10
        cell_g.alignment = ALIGN_CENTER
        cell_g.border = CELL_BORDER
        if isinstance(cell_g.value, (int, float)):
            cell_g.number_format = '0.0' if isinstance(cell_g.value, float) and cell_g.value % 1 != 0 else '0'
            
        # Col H: Doanh thu
        raw_dt = row_data[7] if len(row_data) > 7 else None
        cell_h = ws.cell(row=current_row, column=8, value=parse_cell_value(raw_dt))
        cell_h.font = FONT_CALIBRI_10
        cell_h.alignment = ALIGN_RIGHT
        cell_h.border = CELL_BORDER
        if isinstance(cell_h.value, (int, float)):
            cell_h.number_format = '#,##0'
            
        # Col I: Doanh thu thực tế
        raw_dttt = row_data[8] if len(row_data) > 8 else None
        cell_i = ws.cell(row=current_row, column=9, value=parse_cell_value(raw_dttt))
        cell_i.font = FONT_CALIBRI_10
        cell_i.alignment = ALIGN_RIGHT
        cell_i.border = CELL_BORDER
        if isinstance(cell_i.value, (int, float)):
            cell_i.number_format = '#,##0'
            
        # Col J: Mã đơn trong live
        raw_md = row_data[9] if len(row_data) > 9 else None
        cell_j = ws.cell(row=current_row, column=10, value=raw_md)
        cell_j.font = FONT_CALIBRI_10
        cell_j.alignment = ALIGN_LEFT
        cell_j.border = CELL_BORDER
        
        # Col K: Chi phí ads
        raw_ads = row_data[10] if len(row_data) > 10 else None
        cell_k = ws.cell(row=current_row, column=11, value=parse_cell_value(raw_ads))
        cell_k.font = FONT_CALIBRI_10
        cell_k.alignment = ALIGN_RIGHT
        cell_k.border = CELL_BORDER
        if isinstance(cell_k.value, (int, float)):
            cell_k.number_format = '#,##0'
            
        # Col M: Địa điểm live (Cột M)
        raw_dd = row_data[12] if len(row_data) > 12 else None
        dd_clean = str(raw_dd).strip() if raw_dd is not None and str(raw_dd).strip() != '' else None
        cell_m = ws.cell(row=current_row, column=13, value=dd_clean)
        cell_m.font = FONT_CALIBRI_10
        cell_m.alignment = ALIGN_CENTER
        cell_m.border = CELL_BORDER
        
        # Col L: Chi phí thuê phòng ngoài giờ (Cột L)
        # Dynamic formula based on Column M (Địa điểm) and Column B / E (Ca / Giờ Bắt Đầu)
        cell_l = ws.cell(row=current_row, column=12)
        cell_l.value = f'=IF(AND(OR(ISNUMBER(SEARCH("văn phòng", M{current_row})), ISNUMBER(SEARCH("vp", M{current_row}))), OR(ISNUMBER(SEARCH("Ca 6", B{current_row})), ISNUMBER(SEARCH("21h", E{current_row})))), 200000, 0)'
        cell_l.font = FONT_CALIBRI_10
        cell_l.alignment = ALIGN_CENTER
        cell_l.border = CELL_BORDER
        cell_l.number_format = '#,##0'
        
        # Col N: Tổng giá trị hàng hóa của buổi LIVE (₫)
        raw_tgth = row_data[13] if len(row_data) > 13 else None
        cell_n = ws.cell(row=current_row, column=14, value=parse_cell_value(raw_tgth))
        cell_n.font = FONT_CALIBRI_10
        cell_n.alignment = ALIGN_RIGHT
        cell_n.border = CELL_BORDER
        if isinstance(cell_n.value, (int, float)):
            cell_n.number_format = '#,##0'
            
        current_row += 1
        
    last_data_row = current_row - 1
    
    # 4. Total Row
    total_row = current_row
    ws.row_dimensions[total_row].height = 35.0
    
    for c in range(1, 15):
        cell = ws.cell(row=total_row, column=c)
        cell.font = FONT_CALIBRI_10_BOLD
        cell.fill = FILL_TOTAL
        cell.border = TOTAL_BORDER
        cell.alignment = ALIGN_CENTER
        
    ws.cell(row=total_row, column=1, value='Tổng cộng')
    
    # Sum formulas
    ws.cell(row=total_row, column=7, value=f'=SUM(G{data_start_row}:G{last_data_row})')
    ws.cell(row=total_row, column=7).number_format = '0.0'
    
    ws.cell(row=total_row, column=8, value=f'=SUM(H{data_start_row}:H{last_data_row})')
    ws.cell(row=total_row, column=8).number_format = '#,##0'
    ws.cell(row=total_row, column=8).alignment = ALIGN_RIGHT
    
    ws.cell(row=total_row, column=9, value=f'=SUM(I{data_start_row}:I{last_data_row})')
    ws.cell(row=total_row, column=9).number_format = '#,##0'
    ws.cell(row=total_row, column=9).alignment = ALIGN_RIGHT
    
    ws.cell(row=total_row, column=11, value=f'=SUM(K{data_start_row}:K{last_data_row})')
    ws.cell(row=total_row, column=11).number_format = '#,##0'
    ws.cell(row=total_row, column=11).alignment = ALIGN_RIGHT
    
    ws.cell(row=total_row, column=12, value=f'=SUM(L{data_start_row}:L{last_data_row})')
    ws.cell(row=total_row, column=12).number_format = '#,##0'
    ws.cell(row=total_row, column=12).alignment = ALIGN_CENTER
    
    ws.cell(row=total_row, column=14, value=f'=SUM(N{data_start_row}:N{last_data_row})')
    ws.cell(row=total_row, column=14).number_format = '#,##0'
    ws.cell(row=total_row, column=14).alignment = ALIGN_RIGHT
    
    # Freeze header rows
    ws.freeze_panes = 'A3'
    print(f"Sheet built successfully. Rows: {data_start_row} to {last_data_row}. Total row: {total_row}")

# 4. Create Standalone Workbook: 'Đăng ký ca livestream Tháng 11.xlsx'
wb_standalone = openpyxl.Workbook()
# Default sheet
ws_nov = wb_standalone.active
ws_nov.title = 'Ca tháng 11.2026'
build_concept_sheet(ws_nov, wrjoa_rows, is_nov=True)

# Add October sheet as reference
ws_oct = wb_standalone.create_sheet('Ca tháng 10.2026')
build_concept_sheet(ws_oct, nf1beo_rows, is_nov=False)

standalone_path = '/Users/longnd/Downloads/Đăng ký ca livestream Tháng 11.xlsx'
wb_standalone.save(standalone_path)
print(f"Saved standalone workbook to: {standalone_path}")

# 5. Backup and Update Master Template File: 'Đăng ký ca livestream  (1).xlsx'
template_path = '/Users/longnd/Downloads/Đăng ký ca livestream  (1).xlsx'
backup_path = '/Users/longnd/Downloads/Đăng ký ca livestream  (1)_backup.xlsx'

if not os.path.exists(backup_path):
    shutil.copy2(template_path, backup_path)
    print(f"Created backup of master file at: {backup_path}")

# Load master workbook and add new sheets
wb_master = openpyxl.load_workbook(template_path)

# If sheets already exist in master, remove and recreate them cleanly
for title in ['Ca tháng 10.2026', 'Ca tháng 11.2026']:
    if title in wb_master.sheetnames:
        del wb_master[title]

ws_master_oct = wb_master.create_sheet('Ca tháng 10.2026')
build_concept_sheet(ws_master_oct, nf1beo_rows, is_nov=False)

ws_master_nov = wb_master.create_sheet('Ca tháng 11.2026')
build_concept_sheet(ws_master_nov, wrjoa_rows, is_nov=True)

wb_master.save(template_path)
print(f"Updated master workbook at: {template_path}")

# Also copy standalone file to tiktok-dashboard for git tracking
repo_file_path = '/Users/longnd/tiktok-dashboard/Dang_ky_ca_livestream_Thang_11.xlsx'
shutil.copy2(standalone_path, repo_file_path)
print(f"Copied to repo: {repo_file_path}")
