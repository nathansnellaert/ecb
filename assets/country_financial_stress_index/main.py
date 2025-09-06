from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("CLIFS")
    
    if data.num_rows > 0:
        upload_data(data, "country_financial_stress_index")
        print(f"Uploaded {data.num_rows} rows to country_financial_stress_index")
        
    save_state("country_financial_stress_index", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
