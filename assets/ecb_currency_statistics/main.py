from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("ECS")
    
    if data.num_rows > 0:
        upload_data(data, "ecb_currency_statistics")
        print(f"Uploaded {data.num_rows} rows to ecb_currency_statistics")
        
    save_state("ecb_currency_statistics", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
