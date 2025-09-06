from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("AGR")
    
    if data.num_rows > 0:
        upload_data(data, "agricultural_statistics")
        print(f"Uploaded {data.num_rows} rows to agricultural_statistics")
        
    save_state("agricultural_statistics", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
