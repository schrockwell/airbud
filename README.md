# Airbud

> There's no rule that says that UAVs can't measure antenna patterns!!

## Pi Setup

This on Raspbian Lite OS on a Raspberry Pi 4 and Python 3.7.

```bash
sudo apt install python3-venv python3-pip librtlsdr-dev rtl-sdr libatlas-base-dev libopenjp2-7 libtiff5

cd ~/airbud
python3 -m venv venv
source venv/bin/activate
pip3 install

# For reference
# pip3 install pyrtlsdr matplotlib
# pip3 freeze > requirements.txt
```
