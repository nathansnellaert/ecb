from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("PFB")
    
    if data.num_rows > 0:
        upload_data(data, "pension_fund_balance_sheet")
        print(f"Uploaded {data.num_rows} rows to pension_fund_balance_sheet")
        
    save_state("pension_fund_balance_sheet", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
