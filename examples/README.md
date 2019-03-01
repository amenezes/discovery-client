# Discovery-Client Examples

## Using docker and docker-compose

From inside the `example` folder.

````bash
docker-compose up -d
````

## On bare metal

From inside the `example` folder.

### setup


````yml
# uncomment the following lines and change MY_IP value to your local IP.
# lines 8-10
extra_hosts:
  - "aio-client:MY_IP"
  - "standard-client:MY_IP"
````

### run

````bash
# first install virtualenv
pip install virtualenv

# create and activate venv
virtualenv venv
source venv/bin/activate

# install dependencies
pip install -r requirements-example.txt

# start consul container
docker-compose up -d discovery

# start aio-client
python test_aio.py

# OR

# start standard-client
FLASK_APP=test_client.py flask run -h 0.0.0.0
````
