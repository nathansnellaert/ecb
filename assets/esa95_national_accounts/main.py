from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("ESA")
    
    if data.num_rows > 0:
        upload_data(data, "esa95_national_accounts")
        print(f"Uploaded {data.num_rows} rows to esa95_national_accounts")
        
    save_state("esa95_national_accounts", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
