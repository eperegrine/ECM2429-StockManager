# ECM2429-StockManager

System Design and Programming Exercise for Systems Development 2 module

## Develop

To run the app call, but only after installing dependencies

```shell
python main.py
```

The app depends on the webay api to be running at `http://localhost:8080`
to run the app run 

```shell
python webay.py
```


### Install Dependencies

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
pip install kivy[base] kivy_examples peeweee pycodestyle 
```

### Testing

Tests are run with the python unittest module. 

There is a github action that runs these automatically, but to run it localy call: 

```shell
python -m unittest discover -s Tests
```

### Linting

Linting is done using PEP8 via `pycodestyle`. 
This is run on a github action but can also be done locally

To run the lint call 
```shell
pycodestyle --max-line-length=120 . 
```

For a more detailed view you can run
```shell
pycodestyle --show-source --show-pep8 --max-line-length=120 .
```