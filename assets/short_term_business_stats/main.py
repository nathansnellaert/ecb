from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("ECB_STBS1")
    
    if data.num_rows > 0:
        upload_data(data, "short_term_business_stats")
        print(f"Uploaded {data.num_rows} rows to short_term_business_stats")
        
    save_state("short_term_business_stats", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
