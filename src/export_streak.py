import requests as rq
import base64 as b64
from dataclasses import dataclass, field
import os
from json import dumps
import re


class Endpoint:

    def __init__(self, pipeline):
        # lambda o t-string
        self.pip = PipelineEP(pipeline)
        self.box = BoxEP(pipeline)
        self.file = FileEP(box)


class BoxEP:

    def __init__(self, box):
        self._box = box

    @property
    def list(self):
        return f"https://api.streak.com/api/v1/pipelines/{self._box.pipeline.key}/boxes?sortBy=creationTimestamp"

    @property
    def batch(self):
        return f"https://api.streak.com/api/v1/pipelines/{self._box.pipeline.key}/boxes/batch/"



class PipelineEP:

    def __init__(self, pipeline):
        self._pipeline = pipeline

    @property
    def get(self):
        return f"https://api.streak.com/api/v1/pipelines/{self._pipeline.key}"

    @classmethod
    def list(cls):
        return "https://api.streak.com/api/v1/pipelines"

class FileEP:

    def __init__(self, box):
        self.box = box

    @property
    def list(self):
        return f"https://api.streak.com/api/v1/boxes/{self.box.key}/files"

    @property
    def content(self):
        return f"https://api.streak.com/api/v1/files/{self.box.key}/contents"


@dataclass
class FileData:

    name: str
    key: str = field(repr = None)
    json: dict = field(repr = None)

    @property
    def content(self):
        endpoint = f"https://api.streak.com/api/v1/files/{self.key}/contents"
        content = rq.get(url = endpoint, headers = Streak.GETHEADER()).content
        return content

    def save(self, target: str = None):
        target = self.name if target is None else target
        if not os.path.exists(target):
            with open(target, "wb") as f:
                f.write(self.content)
        return target


@dataclass
class BoxData:

    name: str
    key: str = field(repr = None)
    json: dict = field(repr = None)


    @property
    def files(self):
        return File(self)

    @property
    def list(self):
        boxes = rq.get(
            url = self.endpoints.box.list, headers = Streak.GETHEADER()).json()
        return boxes

    @property
    def fields(self):
        endpoint = f"https://api.streak.com/api/v1/boxes/{self.key}/fields"
        response = rq.get(url = endpoint, headers = Streak.GETHEADER()).json()
        for p in streak.pipelines.list:
            if p.key == self.json["pipelineKey"]:
                pip_fields = {f.key: f for f in p.fields}
                break
        for f in response:
            key = f["key"]
            field_value = f.get("value", None)
            pip_fields[key].json.update({"value": field_value})
        return pip_fields

    @property
    def tasks(self):
        endpoint = f"https://api.streak.com/api/v2/boxes/{self.key}/tasks"
        response = rq.get(url = endpoint, headers = Streak.GETHEADER()).json()
        tasks = []
        for t in response.get("results", []):
            task = StreakData(name = t["text"], key = t["key"], json = t)
            tasks.append(task)
        return tasks

    @property
    def threads(self):
        endpoint = f"https://api.streak.com/api/v1/boxes/{self.key}/threads"
        response = rq.get(url = endpoint, headers = Streak.GETHEADER()).json()
        threads = []
        for t in response:
            thread = StreakData(name = t["subject"], key = t["key"], json = t)
            threads.append(thread)
        return threads

    @property
    def comments(self):
        endpoint = f"https://api.streak.com/api/v2/boxes/{self.key}/comments"
        response = rq.get(url = endpoint, headers = Streak.GETHEADER()).json()
        comments = []
        for c in response.get("results", []):
            comment = StreakData(name = c["timestamp"], key = c["key"], json = c)
            comments.append(comment)
        if response.get("hasNextPage"):
           raise ValueError("ci sono altri commenti")
            # TODO
        return comments

    @property
    def history(self):
        endpoint = f"https://api.streak.com/api/v1/boxes/{self.key}/newsfeed?detailLevel=ALL"
        response = rq.get(url = endpoint, headers = Streak.GETHEADER()).json()
        history = []
        for h in response:
            crono = StreakData(name = h["timestamp"], key = h["key"], json = h)
            history.append(crono)
        return history



class File:

    def __init__(self, box):
        self.box = box

    @property
    def endpoints(self):
        return FileEP(self.box)

    @property
    def list(self):
        response = rq.get(
            url = self.endpoints.list, headers = Streak.GETHEADER()
            ).json()
        files = [FileData(
            name = f["fileName"], key = f["fileKey"], json=f)
            for f in response]
        return files


class Box:

    def __init__(self, pipeline):
        self.pipeline = pipeline

    @property
    def endpoints(self):
        return BoxEP(self)

    @property
    def list(self):
        boxes_dict = rq.get(
            url = self.endpoints.list, headers = Streak.GETHEADER()
            ).json()
        boxes = [BoxData(name = b["name"], key = b["boxKey"], json=b)
                         for b in boxes_dict]
        return boxes

    def batch(self, *keys: str):
        boxes = rq.post(
            url = self.endpoints.batch, json = keys, headers = Streak.GETHEADER()
            ).json()
        return boxes



@dataclass
class StreakData:

    name: str
    key: str = field(repr = None)
    json: dict = field(repr = None)

    @property
    def endpoints(self):
        return Endpoint(self)


class PipelineData(StreakData):

    name: str
    key: str = field(repr = None)
    json: dict = field(repr = None)

    @property
    def boxes(self):
        return Box(self)

    @property
    def stages(self):
        endpoint = f"https://api.streak.com/api/v1/pipelines/{self.key}/stages"
        response = rq.get(url = endpoint, headers = Streak.GETHEADER()).json()
        stages = []
        for k, v in response.items():
            stage = StreakData(name = v["name"], key = v["key"], json = v)
            stages.append(stage)
        return stages

    @property
    def history(self):
        endpoint = f"https://api.streak.com/api/v1/pipelines/{self.key}/newsfeed?detailLevel=ALL"
        response = rq.get(url = endpoint, headers = Streak.GETHEADER()).json()
        history = []
        for h in response:
            crono = StreakData(name = h["timestamp"], key = h["key"], json = h)
            history.append(crono)
        return history

    @property
    def fields(self):
        endpoint = f"https://api.streak.com/api/v1/pipelines/{self.key}/fields"
        response = rq.get(url = endpoint, headers = Streak.GETHEADER()).json()
        fields = []
        for fd in response:
            field = StreakData(name = fd["name"], key = fd["key"], json = fd)
            fields.append(field)
        return fields


class Pipeline:

    def __init__(self, streak):
        self.streak = streak

    @property
    def _ep_list(self):
        return PipelineEP.list()

    @property
    def _header(self):
        return Streak.GETHEADER()

    @property
    def boxes(self):
        return Box(self)

    @property
    def list(self):
        response = rq.get(url = self._ep_list, headers = self._header).json()
        pipelines = []
        for p in response:
            pip = PipelineData(name = p["name"], key = p["key"], json = p)
            pipelines.append(pip)
        return pipelines


class Streak:

    def __init__(self):
        self.key = self.streak_key_b64()

    @property
    def endpoints(self):
        return Endpoint(self)

    @property
    def pipelines(self):
        return Pipeline(self)

    @property
    def req_header(self):
        return self.GETHEADER()

    def walk(self):
        for pip in self.pipelines.list:
            for box in pip.boxes.list:
                for file in box.files.list:
                    yield pip, box, file

    @staticmethod
    def _clean_filename(name: str):
        name = str(name).upper().strip()
        forbidden_chars = r'[<>:"/\\|?*\x00-\x1f]'
        clean_name = re.sub(forbidden_chars, '-', name)
        clean_name = re.sub(r'\s+', ' ', clean_name).strip()
        filename = clean_name.rstrip('.')
        return filename

    @classmethod
    def _dump(cls, data: object):
        filename = cls._clean_filename(data.name)[:150] + ".txt"
        content = dumps(data.json)
        return filename, content

    @classmethod
    def _save(cls, directory, type_name, data):
        filename, content = cls._dump(data)
        path = os.path.join(directory, f"{type_name.upper()} - " + filename)
        with open(path, "w") as file:
            file.write(content)
            print(f"{type_name.upper()} '{data.name}' wrote.")


    def backup(self, target: str = None, files: bool = True):

        target = "streak-bk"
        if not os.path.exists(target):
            os.makedirs(target)

        pip_paths = set()
        for p in self.pipelines.list:
            pip_name = self._clean_filename(p.name)
            pip_path = os.path.join(target, pip_name)
            pip_paths.update(pip_path)
            if not os.path.exists(pip_path): os.makedirs(pip_path)
            for f in p.fields:
                self._save(pip_path, "field", f)

            box_paths = set()
            for b in p.boxes.list:
                box_name = self._clean_filename(b.name)
                box_path = os.path.join(pip_path, box_name)
                box_paths.update(box_path)
                if not os.path.exists(box_path): os.makedirs(box_path)
                for c in b.comments:
                    self._save(box_path, "comment", c)
                for t in b.threads:
                    self._save(box_path, "thread", t)
                for h in b.history:
                    self._save(box_path, "history", h)
                for t in b.tasks:
                    self._save(box_path, "task", t)

                if files:
                    for f in b.files.list:
                        file_path = os.path.join(box_path, f.name)
                        if not os.path.exists(file_path):
                            with open(file_path, "wb") as file:
                                file.write(f.content)
                                print(f"FILE '{f.name}' wrote.")

                print(f"BOX '{b.name}' wrote.")
            print(f"PIPELINE '{p.name}' wrote.")
        print(f"BACKUP '{target}' wrote.")


    def extract(self, ext: str = None):
        from hashlib import sha256

        datas = dict()
        for p, b, f in self.walk():
            if not ext or f.name.endswith(ext):
                content = f.content
                hashcode = sha256(content)
                data = {hashcode: (f.name, len(content))}
                if hashcode not in datas:
                    datas.update(data)
                    print(f.name)
                else:
                    if f.name != datas[hashcode][0]:
                        datas.update(data)
                        print(f.name)
        return datas


    @staticmethod
    def streak_key_b64(key_path: str = None):
        key_path = "key.txt" if key_path is None else key_path
        with open(key_path, "r") as f:
            streak_key = f.read().encode()
        return b64.urlsafe_b64encode(streak_key).decode()

    @classmethod
    def GETHEADER(cls):
        streak_key = cls.streak_key_b64()
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "authorization": f"Basic {streak_key}"
        }
        return headers


if __name__ == "__main__":
    streak = Streak()
    pipeline = streak.pipelines.list[0]
    box = pipeline.boxes.list[45]
    file = box.files.list[0]
    content = file.content
    print("test ok.")
