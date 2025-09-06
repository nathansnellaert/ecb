from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("SPF")
    
    if data.num_rows > 0:
        upload_data(data, "professional_forecasters_survey")
        print(f"Uploaded {data.num_rows} rows to professional_forecasters_survey")
        
    save_state("professional_forecasters_survey", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
