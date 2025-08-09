from fastapi import FastAPI
import re
import streak_api as stk



  
app = FastAPI()

@app.get("/")
def root() -> str:
    return {"Welcome.": None}
        
@app.get("/offerte/{offer_tuple}")
def reference(offer_tuple: str) -> dict:   
    # pattern = re.compile(r"(?P<company>M\w\w)-R(?P<year>\d\d)-(?P<number>\d\d\d\d)")
    return stk.match_box(offer_tuple)



if __name__ == "__main__":
    start_command = "uvicorn thisfile:app --reload"
    
    print(f"Start the App:\n >> {start_command}")