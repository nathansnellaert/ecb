from utils import save_state, upload_data
from datetime import datetime
from general import fetch_data

def main():
    data = fetch_data("BSP")
    
    if data.num_rows > 0:
        upload_data(data, "blue_book_balance_sheet")
        print(f"Uploaded {data.num_rows} rows to blue_book_balance_sheet")
        
    save_state("blue_book_balance_sheet", {
        "last_updated": datetime.now().isoformat(),
        "row_count": data.num_rows
    })
    
    return data
