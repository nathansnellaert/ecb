from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("CBD2")
    
    if data.num_rows > 0:
        upload_data(data, "consolidated_banking_data")
        print(f"Uploaded {data.num_rows} rows to consolidated_banking_data")
        
    save_state("consolidated_banking_data", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
