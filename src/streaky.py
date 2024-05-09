import requests as rqs
import base64

# Insert your api key here.
KEYPATH = r"../key.txt"

def get_key(key_filepath: str):
    with open(key_filepath, "r") as file:
        key = file.read()
    return key

class Streak:

    REF = r"https://streak.readme.io/reference/get-current-user"
    ENDP = r"https://api.streak.com/api"

    def __init__(self, auth_key: str) -> object:
        self.auth = base64.b64encode(auth_key.encode()).decode()

    @staticmethod
    def get(url: str) -> dict:
        encrypted_key = base64.b64encode(Streak.KEY.encode()).decode()
        query = {"authorization": f"Basic {encrypted_key}"}
        response = rqs.get(url, headers=query)
        return response

    @staticmethod
    def get_me() -> rqs.models.Response:
        """
        Get current user details.
        (https://streak.readme.io/reference/get-current-user)
        """
        end_point = Streak.ENDP + r"/v1/users/me"
        response = Streak.get(end_point)
        return response

    @staticmethod
    def get_user(user_key: str) -> rqs.models.Response:
        """
        Get user details.
        (https://streak.readme.io/reference/get-user)
        """
        end_point = Streak.ENDP + fr"/v1/users/{user_key}"
        response = Streak.get(end_point)
        return response

    @staticmethod
    def get_my_team() -> rqs.models.Response:
        end_point = Streak.ENDP + r"/v2/users/me/teams"
        response = Streak.get(end_point)
        return response

    @staticmethod
    def list_pipelines():
        end_point = Streak.ENDP + r"/v1/pipelines?sortBy=creationTimestamp%20"
        response = Streak.get(end_point)
        return response

    @staticmethod
    def get_pipeline(pipeline_key: str):
        end_point = Streak.ENDP + fr"/v1/pipelines/{pipeline_key}"
        response = Streak.get(end_point)
        return response


    @staticmethod
    def get_box(box_key: str):
        end_point = Streak.ENDP + fr"/v1/boxes/{box_key}"
        response = Streak.get(end_point)
        return response

    @staticmethod
    def list_boxes(pipeline_key: str, page: int = None, stage_key: str = None, limit: int = None):
        end_point = Streak.ENDP + fr"/v1/pipelines/{pipeline_key}/boxes?sortBy=creationTimestamp"
        end_point = end_point if page is None else end_point + "&page={pages}"
        end_point = end_point if stage_key is None else end_point + fr"&stageKey={stage_key}"
        end_point = end_point if limit is None else end_point + fr"&limit={limit}"
        response = Streak.get(end_point)
        return response

    @staticmethod
    def list_threads(box_key: str):
        end_point = Streak.ENDP + fr"/v1/boxes/{box_key}/threads"
        response = Streak.get(end_point)
        return response

    @staticmethod
    def get_thread(thread_key: str):
        end_point = Streak.ENDP + fr"/v1/threads/{thread_key}"
        response = Streak.get(end_point)
        return response



class User:

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
    def list_users():
        response = Streak.get_my_team()
        users = response.json()["results"][0]["members"]
        for user in users:
            yield user


class Pipeline:

    def __init__(self, data: dict) -> object:
        for k, v in data.items():
            setattr(self, k, v)


    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}"


    @classmethod
    def from_api(cls, name: str):
        pipelines = Streak.list_pipelines().json()
        pipeline = None
        for p in pipelines:
            if name.upper() in p["name"]:
                pipeline = p
                break
        return cls(pipeline)


class Box:

    def __init__(self, box_infos: dict) -> object:
        for k, v in box_infos.items():
            setattr(self, k, v)


    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}"


    @classmethod
    def from_api(cls, pipeline: str, name: str):
        boxes = Box.list_boxes(pipeline)
        box = None
        for b in boxes:
            if name == b["name"]:
                box = b
                break
        return cls(box)

    @staticmethod
    def list_boxes(pipeline: str):
        pipeline_key = Pipeline.from_api(pipeline).key
        boxes = Streak.list_boxes(pipeline_key).json()
        for box in boxes:
            yield box


class Thread:
    pass
















