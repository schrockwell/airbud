# Airbud

> There's no rule that says that UAVs can't measure antenna patterns!

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

## Turning Pi into an Access Point

You want to be able to connect to the Pi wirelessly in the field. You should have the Pi plugged into ethernet to configure this (duh).

https://www.raspberrypi.org/documentation/configuration/wireless/access-point-routed.md

## Starting it

```bash
./bin/airbud
```

Check it out at `http://localhost:5000/`.

There's also an example systemd `airbud.service` file provided if you want it to run as a service.

```bash
sudo cp airbud.service /etc/systemd/system/airbud.service
sudo systemctl enable airbud
sudo systemctl start airbud
```

## Running tests

Tests are set up using [`Pytest`](https://docs.pytest.org/en/stable/). Inside of the virtual environment, with requirements installed, you can run the tests with

```bash
pytest
```
