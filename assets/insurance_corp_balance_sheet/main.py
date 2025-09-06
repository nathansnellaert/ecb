from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("ICB")
    
    if data.num_rows > 0:
        upload_data(data, "insurance_corp_balance_sheet")
        print(f"Uploaded {data.num_rows} rows to insurance_corp_balance_sheet")
        
    save_state("insurance_corp_balance_sheet", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
