import requests as req
import base64
import time as tm
import pandas as pd
from io import BytesIO

import endpoints as enp

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
    def is_connected(self):
        enpoint = enp.USER.ME
        response = self.get(enpoint)
        return True if response.status_code == 200 else False
    
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

            

    
    
class UserAPI:
    
    _resources = enp.USER
    
    def __init__(self, auth: object, user_data: dict):
        self.timestamp_ns = tm.time_ns()
        self.auth = auth
        self.data = user_data
        self.email = self.data["email"]
        self.key = self.data["key"]
        
    def __getitem__(self, item):
        return self.data.get(item, None)
        
    def __str__(self):
        return f"{self.key}"
    
    def __repr__(self):
        return f"<RequestUser '{self.email}'>"
    
    @classmethod
    def me(cls, auth):
        end_point = cls._resources.ME
        response = auth.get(end_point)
        if response.status_code == 200:
            return cls(auth, response.json())

    @classmethod
    def get(cls, auth, user_key: str):
        end_point = cls._resources.GET.format(
            **{"user_key": user_key})
        response = auth.get(end_point)
        if response.status_code == 200:
            return cls(auth, response.json())
    
    @staticmethod
    def team(auth):
        return TeamAPI.my(auth)
        

class TeamAPI:
    
    _resources = enp.TEAM
    
    def __init__(self, auth: object, team_data: dict):
        self.timestamp_ns = tm.time_ns()
        self.auth = auth
        self.data = team_data
        self.name = self.data["name"]
        self.key = self.data["key"]
        
    def __getitem__(self, item):
        return self.data.get(item, None)
    
    def __str__(self):
        return f"{self.key}"
    
    def __repr__(self):
        return f"<RequestTeam '{self.name}'>"
    
    @classmethod
    def my(cls, auth):
        end_point = cls._resources.MY
        response = auth.get(end_point)
        if response.status_code == 200:
            keys_to_keep = ("creationDate", "creator", 
                            "name", "key", "members", 
                            "lastSavedTimestamp")
            all_data = response.json()["results"][0]
            data = {k: v for k,v in all_data.items() if k in keys_to_keep}
            return cls(auth, data)



class PipelineAPI:    

    _resources = enp.PIPELINE
    
    def __init__(self, auth: object, pipeline_data: dict):
        self.timestamp_ns = tm.time_ns()
        self.auth = auth
        self.data = pipeline_data
        self.name = self.data["name"]
        self.key = self.data["key"]
        
    def __getitem__(self, item):
        return self.data.get(item, None)
    
    def __str__(self):
        return f"{self.key}"
    
    def __repr__(self):
        return f"<RequestPipeline '{self.name}'>"
    
    
    @classmethod
    def list(cls, auth: object) -> object:
        end_point = cls._resources.LIST
        response = auth.get(end_point)
        if response.status_code == 200:
            for pip in response.json():
                yield cls(auth, pip)

    @classmethod
    def get(cls, auth: object, pipeline_key: str) -> object:
        end_point = cls._resources.GET.format(
            **{"pipeline_key": pipeline_key})
        response = auth.get(end_point)
        if response.status_code == 200:
            pip = response.json()
            return cls(auth, pip)



class BoxAPI:
    
    _resources = enp.BOX
    
    def __init__(self, auth: object, box_data: dict):
        self.timestamp_ns = tm.time_ns()
        self.auth = auth
        self.data = box_data
        self.name = self.data["name"]
        self.key = self.data["boxKey"]

    def __getitem__(self, item):
        return self.data.get(item, None)
    
    def __str__(self):
        return f"{self.key}"
    
    def __repr__(self):
        return f"<RequestBox '{self.name}'>"
    
    
    @classmethod
    def get_by_key(cls, auth: object, box_key: str):
        end_point = cls._resources.GET_BY_KEY.format(box_key = box_key)
        response = auth.get(end_point)
        if response.status_code == 200:
            return cls(auth, response.json())
    
    @classmethod
    def get_by_name(cls, auth, box_name: str, 
                    stage_key: str = None, pipeline_key: str = None):
        end_point = cls._resources._GBN_HEAD
        end_point += "" if pipeline_key is None else cls._resources._GBN_IN_PIP
        end_point += "" if stage_key is None else cls._resources._GBN_AT_STG
        end_point += cls._resources._GBN_TAIL
        
        end_point = end_point.format(box_name = box_name, 
                                     pipeline_key = pipeline_key, 
                                     stage_key = stage_key)
        
        search_response = auth.get(end_point)
        if search_response.status_code == 200:
            boxlist = search_response.json()["results"]["boxes"]
            for box in boxlist:
                box_data = box["boxKey"]
                yield cls.get_by_key(auth, box_data)

    @classmethod
    def list(cls, auth: object, pipeline_key: str, page: int = None, 
             stage_key: str = None, limit: int = 10):
        """
        To limit the response, 'limit' parameter need to be set.
        The 'page' parameter than can be used to move around the response.
        
        If no page is set while limiting, the complete response will be 
        retrieved by the api. Same when 'page' is set but 'limit' is none.
        
        Note:
            no 'hasNextPage' attribute found as mentioned in the api docs.
        """
        
        raw_ep = cls._resources._LIST_HEAD
        raw_ep += "" if page is None else cls._resources._LST_OPT_PAGE
        raw_ep += "" if stage_key is None else cls._resources._LST_OPT_STAGE
        raw_ep += "" if limit is None else cls._resources._LST_OPT_LIMIT
        
        end_point = raw_ep.format(pipeline_key = pipeline_key,
                                  page = page, stage_key = stage_key, 
                                  limit = limit)
        
    
        response = auth.get(end_point)
        if response.status_code == 200:
            boxlist = response.json()
            for box_data in boxlist:
                yield cls(auth, box_data)
    
    @classmethod
    def files(cls, auth: object, box_key: str):
        end_point = cls._resources.FILES
        end_point = end_point.format(box_key = box_key)
        response = auth.get(end_point)
        if response.status_code == 200:
            filelist = response.json()
            for file in filelist:
                yield file
    
    def is_box_key(self, key: str):
        return True if self.get_box(key).status_code == 200 else False
    

class ThreadAPI:
    
    _resource = enp
    
    def list_threads(self, box_key: str):
        end_point = self.ENDP + fr"/v1/boxes/{box_key}/threads"
        response = self.get(end_point)
        return response


    def get_thread(self, thread_key: str):
        end_point = self.ENDP + fr"/v1/threads/{thread_key}"
        response = self.get(end_point)
        return response
        

class FieldAPI:
    
    _resources = enp.FIELD
    
    def __init__(self, auth: object, field_data: dict):
        self.timestamp_ns = tm.time_ns()
        self.auth = auth
        self.data = field_data
        self.name = self.data["name"]
        self.key = self.data["key"]
        
    def __getitem__(self, item):
        return self.data.get(item, None)
    
    def __str__(self):
        return f"{self.key}"
    
    def __repr__(self):
        return f"<RequestField '{self.name}'>"
    
    @classmethod
    def get(cls, auth: object, pipeline_key: str, field_key: str):
        end_point = cls._resources.GET
        end_point = end_point.format(pipeline_key = pipeline_key,
                                     field_key = field_key)
        response = auth.get(end_point)
        if response.status_code == 200:
            field_data = response.json()
            return cls(auth, field_data)
    
    @classmethod
    def update(cls, auth: object, box_key: str, field_key: str, 
               new_value: str):
        end_point = cls._resources.UPDATE
        end_point = end_point.format(box_key = box_key, field_key = field_key)
        response = auth.post(end_point, payload = {"value": new_value})
        if response.status_code == 200:
            return response
    
    @classmethod
    def list(cls, auth: object, pipeline_key: str):
        end_point = cls._resources.LIST
        end_point = end_point.format(pipeline_key = pipeline_key)
        response = auth.get(end_point)
        if response.status_code == 200:
            field_list = response.json()
            for field in field_list:
                yield cls(auth, field)


class FileAPI:
    
    _resources = enp.FILE
    
    def __init__(self, auth: object, file_data: dict):
        self.timestamp_ns = tm.time_ns()
        self.auth = auth
        self.data = file_data
        self.name = self.data["fileName"]
        self.key = self.data["fileKey"]
        
    def __getitem__(self, item):
        return self.data.get(item, None)
    
    def __str__(self):
        return f"{self.key}"
    
    def __repr__(self):
        return f"<RequestFile '{self.name}'>"
    
    def __bytes__(self):
        return self.content(self.auth, self.key)
    
    @classmethod
    def get(cls, auth: object, file_key: str):
        end_point = cls._resources.GET
        end_point = end_point.format(file_key = file_key)
        response = auth.get(end_point)
        if response.status_code == 200:
            file_data = response.json()
            return cls(auth, file_data)
    
    @classmethod
    def list(cls, auth: object, box_key: str):
        # TODO
        # BoxAPI.files return different type of dict of what 
        # returned by FileAPI.list endpoint. Than for the moment,
        # the additional data on BoxAPI.files object is omitted
        for file in BoxAPI.files(auth, box_key):
            yield cls.get(auth, file["fileKey"])
    
    @classmethod
    def content(cls, auth: object, file_key: str) -> bytes:     
        end_point = cls._resources.CONTENT
        end_point = end_point.format(file_key = file_key)
        response = auth.get(end_point)
        if response.status_code == 200:
            filedata = BytesIO(response.content)
            return filedata
    
        

