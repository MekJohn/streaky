import requests as rq
import base64 as ba


def get_apikey():

    with open(r"key.txt", "r") as f:
        key = f.read()
        key_en = key.encode()
    encrypted = ba.b64encode(key_en)
    return encrypted


def get_pipelines(auth: str):
    url = "https://api.streak.com/api/v1/pipelines"
    
    headers = {"authorization": f"Basic {auth.decode()}",
               "accept": "application/json",
               "Content-Type": "application/json"
               }

    response = rq.get(url, headers=headers)
    pipeline_keys = {pipeline["name"]: pipeline["key"] for pipeline in response.json()}
    
    return pipeline_keys

def _search_boxes(auth: str, pipelinekey: str, box_number: str):
    """
    Search for all boxes in pipeline with that box number.
    Return a simplified box list with minimal data.
    """   
        
    url = rf"https://api.streak.com/api/v1/search?pipelineKey={pipelinekey}&name={box_number}"
    
    headers = {"authorization": f"Basic {auth.decode()}",
               "accept": "application/json",
               "Content-Type": "application/json"
               }

    response = rq.get(url, headers = headers)
    response = response.json()
    
    # boxes with keys
    found_boxes = response["results"]["boxes"]
    return found_boxes


def get_boxes(auth: str, pipelinekey: str, box_number: str):
    """
    Get all boxes in pipeline with that box number.
    Return a complete box list with extended data.
    """  
    
    boxlist = _search_boxes(auth, pipelinekey, box_number)
    
    boxes = list()
    # complete boxes
    for box in boxlist:
        boxkey = box["boxKey"]
        url = f"https://api.streak.com/api/v1/boxes/{boxkey}"
        headers = {"accept": "application/json",
                   "Content-Type": "application/json",
                   "authorization": f"Basic {auth.decode()}"
                   }        
        response = rq.get(url, headers=headers)        
        boxes.append(response.json())
    
    return boxes


def get_fields(auth: str, pipelinekey: str):
    
    url = f"https://api.streak.com/api/v1/pipelines/{pipelinekey}/fields"
    
    headers = {"accept": "application/json",
               "Content-Type": "application/json",
               "authorization": f"Basic {auth.decode()}"
               }
    
    response = rq.get(url, headers=headers)
    return response.json()


def get_explicit_fields(auth, box, fields):
    
    company = {"name": "Company"}
    company["key"] = [f["key"] for f in fields if f["name"] == company["name"]][0]
    company["dict"] = [f["dropdownSettings"]["items"] for f in fields if f["name"] == company["name"]][0] 
    
    year = {"name": "Year"}
    year["key"] = [f["key"] for f in fields if f["name"] == year["name"]][0]
    year["dict"] = [f["dropdownSettings"]["items"] for f in fields if f["name"] == year["name"]][0] 
    
    return company, year


def list_refs(auth: str, pipelinekey: str, box_number: str):
    
        
    boxes = get_boxes(auth, pipelinekey, box_number)
    
    reference = list()
    for box in boxes:
        
        fields = get_fields(auth, pipelinekey)
    
        # complete box with fields
        company_map, year_map = get_explicit_fields(auth, box, fields)
        
        company_id = boxes[0]["fields"][company_map["key"]]
        company_value = [opt["name"] for opt in company_map["dict"] if opt["key"] == company_id][0]
        
        year_id = boxes[0]["fields"][year_map["key"]]
        year_value = [opt["name"] for opt in year_map["dict"] if opt["key"] == year_id][0]
        
        data = {"key": box["boxKey"], "company": company_value, "year": year_value[2:], "number": box["name"]}
        reference.append(data)
    
    return reference


def match_box(codes: str, pipeline_name: str) -> str:
    
    # waited string type like "(MKP,25,0250)"
    codes = codes[1:-1].split(",")
    
    # search info
    auth = get_apikey()
    pipelines = get_pipelines(auth)    
    references = list_refs(auth, pipelines[pipeline_name], codes[2])
    box_key = references[0]["key"]
    return {"key": box_key}


  