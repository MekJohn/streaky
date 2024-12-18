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
    
    # 'get by name' endpoint parts
    _GBN_HEAD = BASE.ROOT + r"/v1/search?"
    _GBN_TAIL = r"name={box_name}"
    _GBN_IN_PIP = r"pipelineKey={pipeline_key}&"
    _GBN_AT_STG = r"stageKey={stage_key}&"
    GET_BY_NAME_IN_PIPELINE = _GBN_HEAD + _GBN_IN_PIP + _GBN_TAIL
    GET_BY_NAME_AT_STAGE = _GBN_HEAD + _GBN_AT_STG + _GBN_TAIL
    GET_BY_NAME_IN_PIP_AT_STAGE = (_GBN_HEAD + _GBN_IN_PIP + 
                                   _GBN_AT_STG + _GBN_TAIL)
    
    # 'list box' endpoint
    _LIST_IN_PIP = r"/v1/pipelines/{pipeline_key}"
    _LIST_SORT = r"/boxes?sortBy=creationTimestamp"
    _LIST_HEAD = BASE.ROOT + _LIST_IN_PIP + _LIST_SORT
   
    _LST_OPT_PAGE = r"&page={page}"
    _LST_OPT_STAGE = r"&stageKey={stage_key}"
    _LST_OPT_LIMIT = r"&limit={limit}"
    
    
    
    
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
    
