from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("EST")
    
    if data.num_rows > 0:
        upload_data(data, "euro_short_term_rate")
        print(f"Uploaded {data.num_rows} rows to euro_short_term_rate")
        
    save_state("euro_short_term_rate", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
