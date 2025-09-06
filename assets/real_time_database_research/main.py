from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("RTD")
    
    if data.num_rows > 0:
        upload_data(data, "real_time_database_research")
        print(f"Uploaded {data.num_rows} rows to real_time_database_research")
        
    save_state("real_time_database_research", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
