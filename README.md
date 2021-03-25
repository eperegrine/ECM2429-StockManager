# ECM2429-StockManager
System Design and Programming Exercise for Systems Development 2 module

## Install

Create virtual env
```shell
/usr/bin/python3 -m venv ./venv
```

Activate Virtual env
```shell
source venv/bin/activate
```

Update pip
```shell
pip install --upgrade pip setuptools virtualenv
```

Install Libraries
```shell
pip install -r requirements.txt
```
or
```shell
pip install kivy[base] kivy_examples
```

# Develop

To run the app call
```shell
python main.py
```

To run the tests run this command:
```shell
python -m unittest discover -s Tests/
```