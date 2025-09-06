from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("CISS")
    
    if data.num_rows > 0:
        upload_data(data, "systemic_stress_composite")
        print(f"Uploaded {data.num_rows} rows to systemic_stress_composite")
        
    save_state("systemic_stress_composite", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
