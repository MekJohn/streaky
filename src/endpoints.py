from enum import StrEnum


class BASE(StrEnum):
    
    ROOT = r"https://api.streak.com/api"
    V1 = r"https://api.streak.com/api/v1"
    V2 = r"https://api.streak.com/api/v2"    
    
class USER(StrEnum):
    
    ME = BASE.ROOT + r"/v1/users/me"
    GET = BASE.ROOT + r"/v1/users/{user_key}"
    
class TEAM(StrEnum):

    MY = BASE.ROOT + r"/v2/users/me/teams"
    
class PIPELINE(StrEnum):
    
    GET = BASE.ROOT + r"/v1/pipelines/{pipeline_key}"
    LIST = BASE.ROOT + r"/v1/pipelines?sortBy=creationTimestamp%20"
    
class BOX(StrEnum):
    
    GET_BY_KEY = BASE.ROOT + r"/v1/boxes/{box_key}"
    GET_BY_NAME = BASE.ROOT + r"/v1/search?"
    LIST = BASE.ROOT + \
        r"""
        /v1/pipelines/{pipeline_key}/boxes?sortBy=creationTimestamp
        """
    FIELD_NEWVAL = BASE.ROOT + r"/v1/boxes/{box_key}/fields/{field_key}"
    FILE = BASE.ROOT + r"/v1/boxes/{box_key}/files"
    
class THREAD(StrEnum):
    
    GET = BASE.ROOT + r"/v1/threads/{thread_key}"
    LIST = BASE.ROOT + r"/v1/boxes/{box_key}/threads"
    
    
class FIELD(StrEnum):
    
    GET = BASE.ROOT + r"/v1/pipelines/{pipeline_key}/fields/{field_key}"
    UPDATE_NAME = ""
    LIST = BASE.ROOT + r"/v1/pipelines/{pipeline_key}/fields"
    
    
class FILE(StrEnum):
    
    GET = BASE.ROOT + r"/v1/files/{file_key}"
    CONTENT = BASE.ROOT + r"/v1/files/{file_key}/contents"
    
