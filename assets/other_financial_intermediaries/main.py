from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("OFI")
    
    if data.num_rows > 0:
        upload_data(data, "other_financial_intermediaries")
        print(f"Uploaded {data.num_rows} rows to other_financial_intermediaries")
        
    save_state("other_financial_intermediaries", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
