# Airbud

> There's no rule that says that UAVs can't measure antenna patterns!!

## Pi Setup

This on Raspbian Lite OS on a Raspberry Pi 4 and Python 3.7.

```bash
# Install prereqs
sudo apt install python3-venv python3-pip librtlsdr-dev \
  rtl-sdr libatlas-base-dev libopenjp2-7 libtiff5

# Set up venv
cd ~/airbud
python3 -m venv venv
source venv/bin/activate

# Install reqs
pip3 install -r requirements.txt
```

## Starting it

Root access is required to access the RTL-SDR.

```bash
sudo -E venv/bin/python -m airbud
```

Check the status at `http://localhost:5000/api/status`
