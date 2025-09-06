from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("SESFOD")
    
    if data.num_rows > 0:
        upload_data(data, "securities_financing_otc_derivatives_survey")
        print(f"Uploaded {data.num_rows} rows to securities_financing_otc_derivatives_survey")
        
    save_state("securities_financing_otc_derivatives_survey", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
