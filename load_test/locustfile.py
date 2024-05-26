import itertools
import os
import xml.etree.ElementTree as ET
from glob import glob

from dotenv import load_dotenv
from locust import HttpUser, between, task

load_dotenv()
WIKI_CORPUS = os.getenv("WIKI_CORPUS", "./wiki_corpus_2.01")


def load_wiki_corpus(dir_path):
    """load data

    Wikipedia日英京都関連文書対訳コーパス
    https://alaginrc.nict.go.jp/WikiCorpus/index.html
    """
    data_list = []
    target_path = os.path.join(dir_path, "*/*.xml")
    print(target_path)
    path_list = glob(target_path, recursive=True)
    print(f"Find {len(path_list)} data")
    for p in path_list:
        try:
            tree = ET.parse(p)
            texts = [e.text for e in tree.findall(".//j")]

            data_list.append(
                [
                    {"recordId": str(idx), "data": {"text": text}}
                    for idx, text in enumerate(texts)
                ]
            )
        except Exception as e:
            print(f"Error {p}: {e}")
            continue
    return data_list


test_data = load_wiki_corpus(WIKI_CORPUS)


class SpacyFastAPIUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        """get test data"""
        self.test_data = itertools.cycle(test_data)

    @task
    def entities(self):
        data = next(self.test_data)
        data_json = {"values": data}
        self.client.post(
            "/entities",
            headers={"Content-Type": "application/json", "accept": "application/json"},
            json=data_json,
            timeout=10,
        )
