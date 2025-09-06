from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("AME")
    
    if data.num_rows > 0:
        upload_data(data, "ameco_macroeconomic")
        print(f"Uploaded {data.num_rows} rows to ameco_macroeconomic")
        
    save_state("ameco_macroeconomic", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
