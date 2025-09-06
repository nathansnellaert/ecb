from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("CBD")
    
    if data.num_rows > 0:
        upload_data(data, "consolidated_banking")
        print(f"Uploaded {data.num_rows} rows to consolidated_banking")
        
    save_state("consolidated_banking", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
