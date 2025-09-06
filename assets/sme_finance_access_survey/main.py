from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("SAFE")
    
    if data.num_rows > 0:
        upload_data(data, "sme_finance_access_survey")
        print(f"Uploaded {data.num_rows} rows to sme_finance_access_survey")
        
    save_state("sme_finance_access_survey", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
