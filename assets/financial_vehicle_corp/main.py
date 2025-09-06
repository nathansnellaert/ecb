from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("FVC")
    
    if data.num_rows > 0:
        upload_data(data, "financial_vehicle_corp")
        print(f"Uploaded {data.num_rows} rows to financial_vehicle_corp")
        
    save_state("financial_vehicle_corp", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
