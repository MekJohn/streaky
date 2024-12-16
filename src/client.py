import requests as req
import base64
import time as tm
import pandas as pd


import endpoints as endp
from endpoints import jformat

# Insert your api key here.

class Auth:
    

    DOCS = r"https://streak.readme.io/reference/get-current-user"
    ENDP = r"https://api.streak.com/api"

    def __init__(self, auth64: bytes) -> object:
        self._auth64: bytes = auth64     
        self._log = [(tm.time_ns(), "START", "", None)]
        
    
    def __str__(self):
        return f"{self.key}"
    
    def __repr__(self):
        return f"<Auth '{self.key}'>"
    
    def __getitem__(self, item):
        return self._log[item] if item < len(self._log) else None
    
    @property
    def is_authorized(self):
        enpoint = jformat([endp.BASE, endp.USER.ME])
        response = self.get(enpoint)
        if response.status_code == 200:
            return True
        else:
            raise ConnectionError(
                f"Authorization failed. Status code: {response.status_code}")     
    
    @property
    def log(self):
        log_columns = "Time", "Type", "Url", "Response"
        table = pd.DataFrame(data=self._log,columns=log_columns)
        return table
        
    @property
    def key(self):
        return self._auth64
    
        
    @classmethod
    def connect(cls, key_filepath: str = ""):
        key64 = cls._from_file(key_filepath)
        return cls(key64)


    def _logger(self, *data):
        self._log.append(data)
        

    def get(self, url: str) -> req.models.Response:        
        query = {"authorization": f"Basic {self.key.decode()}",
                 "accept": "application/json",
                 "Content-Type": "application/json"}
        response = req.get(url, headers = query)
        self._logger(tm.time_ns(), "GET", url, response)
        return response
    
    def post(self, url, payload: dict = None):
        query = {"authorization": f"Basic {self.key.decode()}",
                 "accept": "application/json",
                 "Content-Type": "application/json"}
        response = req.post(url, headers = query, json = payload)
        self._logger(tm.time_ns(), "POST", url, response)
        return response

    @staticmethod
    def _from_file(key_filepath: str = "") -> bytes:
        with open(key_filepath, "r") as file:
            key = file.read()
        encrypted_key = base64.b64encode(key.encode())
        return encrypted_key

            

    
    
class RequestUser:
    # TODO come pipeline
    
    
    def me(self) -> object:
        RESOURCE = r"/v1/users/me"
        end_point = self.ENDP + RESOURCE
        response = self.get(end_point)
        return response

    def get_user(self, user_key: str) -> object:
        RESOURCE = fr"/v1/users/{user_key}"
        end_point = self.ENDP + RESOURCE
        response = self.get(end_point)
        return response

    def get_my_team(self) -> object:
        RESOURCE = r"/v2/users/me/teams"
        end_point = self.ENDP + RESOURCE
        response = self.get(end_point)
        return response





class RequestPipeline:    

    _base = endp.BASE.ROOT
    _connect = Auth.connect
    _resources = endp.PIPELINE
    
    def __init__(self, auth: object, pipeline_data: dict):
        self.timestamp_ns = tm.time_ns()
        self.auth = auth
        self.data = pipeline_data
        self.name = self.data["name"]
        self.key = self.data["key"]
        
    
    def __str__(self):
        return f"{self.key}"
    
    def __repr__(self):
        return f"<RequestPipeline '{self.name}'>"
    
    
    @classmethod
    def list(cls, auth: object) -> object:
        blocks = [cls._base, cls._resources.LIST]   
        end_point = jformat(blocks)
        response = auth.get(end_point)
        if response.status_code == 200:
            for pip in response.json():
                yield cls(auth, pip)

    @classmethod
    def from_key(cls, auth: object, pipeline_key: str) -> object:
        blocks = [cls._base, cls._resources.GET]
        kargs = {"pipeline_key": pipeline_key}
        end_point = jformat(blocks, **kargs)
        response = auth.get(end_point)
        if response.status_code == 200:
            pip = response.json()
            return cls(auth, pip)

    
    def is_pipeline_key(self, key: str):
        return True if self.get_pipeline(key).status_code == 200 else False



class RequestBox:
    
    # TODO come pipeline
    
    LIST_BOXES = r"/v1/pipelines/{pipeline_key}/boxes?sortBy=creationTimestamp"
    GET_BOX = r"/v1/boxes/{box_key}"
    
    
    def get_box(self, auth: object, box_key: str):
        RESOURCE = fr"/v1/boxes/{box_key}"
        end_point = auth.ENDP + RESOURCE
        response = auth.get(end_point)
        return response
    
    def get_box_by_name(self, box_name: str, stage_key: str = None, pipeline_key: str = None):
        RESOURCE = r"/v1/search?"
        
        end_point = self.ENDP + RESOURCE
        end_point += "" if pipeline_key is None else fr"pipelineKey={pipeline_key}&"
        end_point += "" if stage_key is None else fr"stageKey={stage_key}&"
        end_point = end_point + fr"name={box_name}"
        
        response = self.get(end_point)
        return response


    def list_boxes(self, pipeline_key: str, page: int = None, 
                   stage_key: str = None, limit: int = None):
        RESOURCE = fr"/v1/pipelines/{pipeline_key}/boxes?sortBy=creationTimestamp"
        
        end_point = self.ENDP + RESOURCE
        end_point += fr"&page={page}" if page is not None else ""
        end_point += fr"&stageKey={stage_key}" if stage_key is not None else ""
        end_point += fr"&limit={limit}" if limit is not None else ""
        
        response = self.get(end_point)
        return response
    
    def get_box_files(self, box_key: str):
        RESOURCE = fr"/v1/boxes/{box_key}/files"
        end_point = self.ENDP + RESOURCE
        response = self.get(end_point)
        return response
    
    def is_box_key(self, key: str):
        return True if self.get_box(key).status_code == 200 else False
    

class RequestThread:
    
    # TODO come pipeline
    
    def list_threads(self, box_key: str):
        end_point = self.ENDP + fr"/v1/boxes/{box_key}/threads"
        response = self.get(end_point)
        return response


    def get_thread(self, thread_key: str):
        end_point = self.ENDP + fr"/v1/threads/{thread_key}"
        response = self.get(end_point)
        return response
        

class RequestField:
    
    # TODO come pipeline
    
    auth = Auth
    resources = endp.FIELD
    
    def __init__(self, auth: object, key: str):
        pass
    
            
    def get_field(self, pipeline_key: str, field_key: str):
        RESOURCE = fr"/v1/pipelines/{pipeline_key}/fields/{field_key}"
        end_point = self.ENDP + RESOURCE
        response = self.get(end_point)
        return response
    
    def update_field_value(self, box_key: str, field_key: str, new_value: str):
        RESOURCE = fr"/v1/boxes/{box_key}/fields/{field_key}"
        end_point = self.ENDP + RESOURCE
        response = self.post(end_point, payload = {"value": new_value})
        return response
    
    def list_fields(self, pipeline_key: str):
        end_point = self.ENDP + fr"/v1/pipelines/{pipeline_key}/fields"
        response = self.get(end_point)
        return response

    def is_field_key(self, key: str):
        return True if self.get_box(key).status_code == 200 else False



class RequestFile:
    
    # TODO come pipeline
    
    connect = Auth.connect
    resources = endp.FILE
    base = endp.BASE.ROOT
    
    def __init__(self, auth: object, file_key: str):
        self.auth = auth
        self.key = file_key
        self.data = self.request(self.auth, self.key).json()
    
    @classmethod
    def request(cls, auth: object, file_key: str):
        blocks = [cls.base, cls.resources.GET]
        input_keys = {"file_key": file_key}
        
        end_point = jformat(blocks, **input_keys)
        response = auth.get(end_point)
        return response
    
    @classmethod
    def content(cls, auth: object, file_key: str):        
        blocks = [cls.base, cls.resources.CONTENT]
        input_keys = {"file_key": file_key}
        
        end_point = jformat(blocks, **input_keys)
        response = auth.get(end_point)
        return response
    
        
        
        
            
        












