from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("CAR")
    
    if data.num_rows > 0:
        upload_data(data, "capital_adequacy_ratios")
        print(f"Uploaded {data.num_rows} rows to capital_adequacy_ratios")
        
    save_state("capital_adequacy_ratios", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
