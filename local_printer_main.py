import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# We can import the printer functions from the new common location
from typing import Optional
from common.local_printer_functions import print_local_barcode_label, get_all_printers

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

app = FastAPI(title="ScanStock Silent Printer API")

# Enable CORS so the browser (running on Django's port 8000) can make
# cross-origin requests to this standalone FastAPI app running on port 54321
app.add_middleware(
    CORSMiddleware,
    # Adjust this in production to specific origins if needed
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PrintRequest(BaseModel):
    barcode: str
    printer_name: Optional[str] = None
    code_type: Optional[str] = "auto"
    custom_subtitle: Optional[str] = None

@app.get("/health")
def health_check():
    """
    Health check endpoint for the frontend to verify if the silent 
    printer service is actively running on this machine.
    """
    return {"status": "ok"}

@app.get("/printers")
def get_printers():
    """
    Returns a list of all currently connected physical printers on the local workstation.
    """
    try:
        printers = get_all_printers()
        return {"printers": printers}
    except Exception as e:
        logging.error(f"Error fetching local printers: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch local printers.")

@app.post("/print-label/")
def print_label(request: PrintRequest):
    """
    Trigger a local print job for the provided barcode using win32print,
    entirely bypassing any browser popups.
    """
    try:
        logging.info(f"Received silent print request for barcode: {request.barcode}")
        print_local_barcode_label(
            request.barcode,
            printer_name=request.printer_name,
            code_type=request.code_type,
            custom_subtitle=request.custom_subtitle,
        )
        return {"status": "success", "message": "Print job sent successfully"}
    except Exception as e:
        logging.error(f"Error printing label: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Start the server on port 54321, easily reachable from localhost
    uvicorn.run(app, host="127.0.0.1", port=54321)
