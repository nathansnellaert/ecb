from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("LIG")
    
    if data.num_rows > 0:
        upload_data(data, "large_insurance_groups")
        print(f"Uploaded {data.num_rows} rows to large_insurance_groups")
        
    save_state("large_insurance_groups", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
