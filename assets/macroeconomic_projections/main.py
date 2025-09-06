from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("MPD")
    
    if data.num_rows > 0:
        upload_data(data, "macroeconomic_projections")
        print(f"Uploaded {data.num_rows} rows to macroeconomic_projections")
        
    save_state("macroeconomic_projections", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
