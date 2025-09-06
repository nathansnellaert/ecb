from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("BKN")
    
    if data.num_rows > 0:
        upload_data(data, "banknotes_circulation")
        print(f"Uploaded {data.num_rows} rows to banknotes_circulation")
        
    save_state("banknotes_circulation", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
