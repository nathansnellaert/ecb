from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("DCM")
    
    if data.num_rows > 0:
        upload_data(data, "dealogic_debt_capital_markets")
        print(f"Uploaded {data.num_rows} rows to dealogic_debt_capital_markets")
        
    save_state("dealogic_debt_capital_markets", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
