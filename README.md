# HiganHana-prototype

## Libraries Used
1. py-cord (beta 2.0.#)
2. flask
3. unittest
4. zw-util-lib
5. honkaidex

# Prereq
1. use `pip install -r requirements.txt -U` to update and install all required pacakges
2. make sure the following folders exist in the root directory
```
appdata
cache
```
3. make sure a valid json file `config.json` in `appdata` directory
4. following fields must present and is valid in `config.json`
```
token           - discord bot token
allowed_servers - a list[int] server ids
ltuid           - hoyolab login cookie
ltoken          - hoyolab login token
```

# Exec Instructions
1. use `runbot.sh`
2. use vscode launch.json to start

> note: if the bot is started with --test, it will first attempt to retrieve [test_] prefixed items in the config
