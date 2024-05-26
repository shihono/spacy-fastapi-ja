# load_test


load test for spacy-fastapi-ja 

## usage

- Download [Wikipedia日英京都関連文書対訳コーパス](https://alaginrc.nict.go.jp/WikiCorpus/index.html)
- Set corpus directory as an environment variable named `WIKI_CORPUS`

```bash
# run spacy_fastapi
docker-compose up
# optional: output memory usage
docker stats --no-stream --format "{{ json . }}"
# run locust
poetry run locust -f locustfile.py
```

more details (in Japanese): https://eieito.hatenablog.com/entry/2024/02/26/090000