from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("STP")
    
    if data.num_rows > 0:
        upload_data(data, "step_securities_settlement")
        print(f"Uploaded {data.num_rows} rows to step_securities_settlement")
        
    save_state("step_securities_settlement", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
