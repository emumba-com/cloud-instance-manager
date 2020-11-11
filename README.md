
# AWS Bootcloud

**AWS Bootcloud** is web based managed solution that allows admins to provision and manage Amazon EC2 Instances quite easily and efficiently. In other words, it is a wrapper on AWS for managing EC2 instances.

It provides an easy to use interface through which admins can create users, assigns & un-assign instances to users and upload ssh keys. Users can start and stop assigned instances on demand and view usage bill.

Following are the features of AWS Bootcloud:

- Separate Interfaces for Admin and User
- Users management
- Stop / Start Capability
- SSH key for VM access
- View Bills
- Simple deployment

# Steps to run AWS Bootcloud

For deployment, **AWS BootCloud** can be setup in two different ways.
The file explorer is accessible using the button in left corner of the navigation bar. You can create a new file by clicking the **New file** button in the file explorer. You can also create folders by clicking the **New folder** button.


============
## 2. Dockerized Version of AWS BootCloud
============
### 1. Dependencies:

To be able to run **AWS BooCloud** you have to meet following dependencies:

-   [Install Docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
-   [Install docker-compose](https://docs.docker.com/compose/install/)

### 2. Configurations:

-   Move `.env-sample` to `.env` in `$ /PROJECT_ROOT/aws-bootcloud/`
-   Paste value against each environment variable in `.env` file.
```
- AWS_ACCESS_KEY_ID=<aws_access_key_id>
- AWS_SECRET_ACCESS_KEY=<aws_secret_key_id>
- REGION_NAME=<default_region>
- SECRET_KEY=my_secret_key
- POSTGRES_USER=<pg_username>
- POSTGRES_PASSWORD=<pg_pass>
- POSTGRES_DB=<pg_db_name>
- DATABASE_URL=postgres://<pg_username>:<pg_pass>@database:5432/<db_db_name>
```
### 3. Steps to Spin Up Deployment:

-   Make sure to clone this repository first.
-   Switch to project root directory.
-   RUN `sudo docker-compose build`
-   RUN `sudo docker-compose up -d`
=======

## 1. Installation on local machine:
============
### I. Dependencies:
To be able to run **AWS BooCloud** on your local environment you have to meet the following dependencies:  
#### (i). Install Python3 and relevant dependencies
```
sudo apt update
sudo apt-get install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install python3.8 -y
sudo apt-get install python3-pip
sudo apt install -y python3-venv
```
#### (ii). Install Postgres
```
sudo apt update
sudo apt install postgresql postgresql-contrib
```
#### (iii). Create User and Database
```
sudo su - postgres  
postgres=# create database <db_name>;  
postgres=# create user <pg_username> with encrypted password <'pg_pass'>;  
postgres=# grant all privileges on database <db_name> to <pg_username>;
```
### II. Configurations:
* Make sure to clone this repository first.
* Switch to project root directory.
* Create virtual environment
	```
	python3 -m venv venv
	source venv/bin/activate
	```
* Install pip dependency requirements
   `pip3 install -r requirement.txt`
* Rename `.env-sample` to `.env` in `$ /PROJECT_ROOT/aws-bootcloud/`
* Paste value against each environment variable in `.env` file.
```
AWS_ACCESS_KEY_ID=<aws_access_key_id>
AWS_SECRET_ACCESS_KEY=<aws_secret_key_id>
REGION_NAME=<default_region>
SECRET_KEY=my_secret_key
POSTGRES_USER=<pg_username>
POSTGRES_PASSWORD=<pg_pass>
POSTGRES_DB=<db_name>
DATABASE_URL=postgres://<pg_username>:<pg_pass>@localhost:5432/<db_name>
```
* Run database migrations
`python3 manage.py db upgrade`

### III. Running application locally
* RUN `export FLASK_APP=app.py`
* RUN `export FLASK_ENV=development`
* RUN  `flask run`


AWS Bootcloud server should now up on `localhost:5000`

============

## 2. Dockerized Version of AWS BootCloud
============
### I. Dependencies:
To be able to run **AWS BooCloud** you have to meet following dependencies:  

-  [Install Docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
-  [Install docker-compose](https://docs.docker.com/compose/install/)

### II. Configurations:
- Make sure to clone this repository first.
- Switch to project root directory.
- Rename `.env-sample` to `.env` in `$ /PROJECT_ROOT/aws-bootcloud/`
- Paste value against each environment variable in `.env` file.
```
AWS_ACCESS_KEY_ID=<aws_access_key_id>
AWS_SECRET_ACCESS_KEY=<aws_secret_key_id>
REGION_NAME=<default_region>
SECRET_KEY=my_secret_key
POSTGRES_USER=<pg_username>
POSTGRES_PASSWORD=<pg_pass>
POSTGRES_DB=<pg_db_name>
DATABASE_URL=postgres://<pg_username>:<pg_pass>@database:5432/<db_db_name>
```

### III. Steps to Spin Up Deployment:
- RUN `sudo docker-compose build`
- RUN `sudo docker-compose up -d`

AWS Bootcloud server should now up on `<server-IP>:5000`

=============