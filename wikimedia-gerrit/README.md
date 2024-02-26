## Running scripts

Create a container with python runtime and dependencies (packages), e.g.
```commandline
docker built -t python-with-deps .
```

Run the script in the container, e.g.
```commandline
docker run -it --rm -v "$PWD":/usr/src/app -w /usr/src/app python-with-deps python download_gerrit_api_data.py --repository="mediawiki/extensions/Wikibase" --since=2020-01-01 -o wikibase.json
```
