#!/bin/bash
sudo rm -rf ./nohup.out
python3 -m venv ./venvCSIMicroService
./venvCSIMicroService/bin/activate
./venvCSIMicroService/bin/python3 -m pip install -r ./requirements.txt
nohup ./venvCSIMicroService/bin/python3 ./server.py
