import pypdf as pp
import os
import io
import re

import client as cl
    

class User:
    
    api = cl.UserAPI

    def __init__(self, data: dict) -> object:
        
        for k, v in data.items():
            setattr(self, k, v)


    def __str__(self):
        return f"{self.userKey}"

    def __repr__(self):
        return f"{self.givenName}"

    @classmethod
    def from_api(cls, user: str = None):
        found_user = dict()
        for u in User.list_users():
            name, key = u["fullName"], u["userKey"]
            if user.lower() in name.lower() or user == key:
                found_user = u
                break
        return cls(found_user)

    @staticmethod
    def list(streak: object):
        response = streak.get_my_team()
        users = response.json()["results"][0]["members"]
        for user in users:
            yield user


class Pipeline:
    
    api = cl.PipelineAPI

    def __init__(self, pipeline_response: object):
        
        self.response = pipeline_response   
        
        self.auth = self.response.auth
        self.key = self.response.key
        self.name = self.response.name
        
        self.stages = self.response.data["stages"]
        self.fields = self.response.data["fields"]
        self.last_update = self.response.data["lastSavedTimestamp"]
        
    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"<Pipeline '{self.name}'>"
    
    def __getitem__(self, item: str):
        return self.response.get(item, None)
    
    def __len__(self):
        return self.response.data["boxCount"]
           
    def __contains__(self, box: str | object):
        pass
    

    @classmethod
    def request(cls, auth: object, name: str = None, key: str = None):
        
        if key is not None:
           pip_response = cls.api.get(auth, key)
           if pip_response is not None:
               return cls(pip_response)
        elif name is not None:
            for pip_response in cls.api.list(auth):
                if pip_response.name.lower() == name.lower():
                    return cls(pip_response)
        else:
            return None
    
    

class Box:
    
    api = cl.BoxAPI

    def __init__(self, box_response: object, pipeline: object = None):
        
        self.response = box_response   
        
        self.auth = self.response.auth
        self.key = self.response.key
        self.name = self.response.name
            
        self.stage = self.response.data["stageKey"]
        self.fields = self.response.data["fields"]
        
        self.notes = self.response.data["notes"]
        self.last_update = self.response.data["lastSavedTimestamp"]


    def __str__(self):
        return f"{self.key}"

    def __repr__(self):
        return f"<Box '{self.name}'>"
    
    
    def __getitem__(self, item):
        return self._data.get(item, None)
    
    def __contains__(self, other: str | object):
        pass
    
    def files(self):
        for file in self.response.files:
            yield file
    
    @classmethod
    def request(cls, pipeline: object, name: str = None, key: str = None):
        
        if key is not None:
           box_rep = cls.api.get(pipeline.auth, key)
           if box_rep is not None:
               return cls(box_rep, pipeline = pipeline)
        elif name is not None:
            for box_rep in cls.api.get_by_name(pipeline.auth, name,
                                               pipeline_key = pipeline.key):
                if box_rep.name.lower() == name.lower():
                    return cls(box_rep, pipeline = pipeline)
        else:
            return None
    

class Field:
    
    api = cl.FieldAPI
    
    def __init__(self, field_response: object, box: object = None):
        pass
        

    def __getitem__(self, item):
        return self._data.get(item, None)
    
    def __str__(self):
        return f"{self.name}"
    
    def __repr__(self):
        return f"<Field '{self.name}'>"



    @classmethod
    def request(cls, pipeline: object, name: str = None, key: str = None):
        
        if key is not None:
           field_rep = cls.api.get(pipeline.auth, key)
           if field_rep is not None:
               return cls(field_rep)
        elif name is not None:
            for field_rep in cls.api.list(pipeline.auth, 
                                          pipeline.key, limit=None):
                if field_rep.name.lower() == name.lower():
                    return cls(field_rep)
        else:
            return None
    



class File:
    
    api = cl.FileAPI
    
    def __init__(self, file: object):

        self._data = file_object
        self.key = file_object.key
        
    
    def __getitem__(self, item):
        return self._data.get(item, None)
    
    def __str__(self):
        return f"{self.name}"
    
    def __repr__(self):
        return f"<File '{self.name}'>"
    
    @property
    def key(self):
        return self["fileKey"]
    
    @property
    def name(self):
        return self["fileName"]
    
    @property
    def stem(self):
        return os.path.splitext(self.name)[0]
    
    @property
    def ext(self):
        return os.path.splitext(self.name)[1]
       
    @property
    def last_update(self):
        return self["lastUpdatedTimestamp"]
    
    @property
    def size(self):
        return self["size"]
    
    @property
    def content(self):
        content = io.BytesIO(self._auth.get_file_content(self.key).content)
        return content
    
        
        


class Automa:
    
    @staticmethod
    def connect(keyfile: str | object) -> object:
        return cl.Auth.connect(keyfile)        
    
    @staticmethod
    def last_price(box: object) -> float:
        
        REGEX = r"Signature\s€\s(?P<deal>.*)Impo"
        
        for file in box.files:
            document = pp.PdfReader(file.content)
            text = document.pages[0].extract_text()
            pattern = re.compile(REGEX, re.DOTALL)
            result = pattern.search(text).groupdict()["deal"]
            if result is not None:
                value = result.groupdict().get("deal", "")
                cleaned = result.replace(".", "_").replace(",", ".")
                value = float(cleaned)
        return value
        

# class InfoParser:
    
#     @staticmethod
#     def search(name: str, pipeline: str = None, box: str, )
    
        


# class Supervisor:
    
#     @staticmethod
#     def update_deal(box: object):
        
#         files = [f for f in box.files if f["fileName"].startswith("MKP-F")]
#         if files != []:
#             sorted_files = sorted(files, key = lambda x: x["lastSavedTimestamp"], reverse = True)[0]
#             filedata = streak.get_file_content(sorted_files["fileKey"]).content
#             filedata = io.BytesIO(filedata)
#             document = pp.PdfReader(filedata)
    
#             text = document.pages[0].extract_text()
    
#             pattern = re.compile(r"Signature\s€\s(?P<deal>.*)Impo", re.DOTALL)
#             found = float(pattern.search(text).groupdict()["deal"].replace(".", "_").replace(",", "."))
#             field = [fd for fd in Pipeline(box.auth, key = box["pipelineKey"]).fields if fd["name"] == "Deal"][0]
#             field_key = field["key"]
#             print(f"Inserting '{found}' in the field '{field['name']}")
#             response = box.auth.update_field_value(box.key, field_key, str(found))
            
#             return response

        



# key64 = Streak.get_key64_fromfile()
# streak = Streak.connect()

# pip = Pipeline(streak, name = "OFFERTE")
# box = Box(streak, pip, name = "0896")

# # aa = Supervisor.update_deal(box)

# ff = File(streak, key ="agxzfm1haWxmb29nYWVyOwsSDE9yZ2FuaXphdGlvbiIYaW5mby5tZWtwaXBpbmdAZ21haWwuY29tDAsSBEZpbGUYgICF6IzD1wsM")












