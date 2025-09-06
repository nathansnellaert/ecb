from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("MMS")
    
    if data.num_rows > 0:
        upload_data(data, "money_market_survey")
        print(f"Uploaded {data.num_rows} rows to money_market_survey")
        
    save_state("money_market_survey", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
