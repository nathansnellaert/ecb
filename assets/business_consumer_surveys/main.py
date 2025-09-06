from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("SUR")
    
    if data.num_rows > 0:
        upload_data(data, "business_consumer_surveys")
        print(f"Uploaded {data.num_rows} rows to business_consumer_surveys")
        
    save_state("business_consumer_surveys", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
