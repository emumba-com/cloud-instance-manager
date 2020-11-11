# AWS Bootcloud
**AWS Bootcloud** is web based managed solution that allows admins to provision and manage Amazon EC2 Instances quite easily and efficiently. In other words, it is a wrapper on AWS for managing EC2 instances.
It provides an easy to use interface through which admins can create users, assigns & un-assign instances to users and upload ssh keys. Users can start and stop assigned instances on demand and view usage bill.

Following are the features of AWS Bootcloud:

-   Separate Interfaces for Admin and User
-   Users management
-   Stop / Start Capability
-   SSH key for VM access
-   View Bills
-   Simple deployment

# Steps to run AWS Bootcloud

For deployment, **AWS BootCloud** can be setup in two different ways.
## 1. Installation on local machine:
============
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

AWS Bootcloud server should now up on `<server-IP>:5000`

=============