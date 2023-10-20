# E6156 - Merry Men Trading App Securities Microservice

## A combination of the first microservice project and example Docker project from the professor for sprint 1

## Local Project Execution

### Setup

# python-docker

A simple Python app for [Docker's Python Language Guide](https://docs.docker.com/language/python).

# DFF Copied Over

- I copied over some of the scripts from the website to make easier to cut and paste.

## Run a simple test.

```
# This is not necessary becaise I am in the directory
# cd /path/to/python-docker

# Create a virtual environment. https://docs.python.org/3/library/venv.html
python3 -m venv .venv

# Activate the virtual environment.
source .venv/bin/activate

# Install dependencies. This is an example of one of the 12 Factor Rules --> Declare dependencies.
(.venv) $ python3 -m pip install -r requirements.txt

# Run the application and access from a browser
(.venv) $ python3 main.py

# CNTL-C to end application

# Exit virtual environment.
deactivate
```

## Docker

- The command example is in beta and I am not using that version of Docker.


- So, I went old school and wrote the files following a different example.  https://medium.com/geekculture/how-to-dockerize-your-flask-application-2d0487ecefb8

- Commands:
  - ```docker build -t raoberman/securities-microservice-1 .```
  - For multiple builds since I built on arm: ```docker buildx build . --platform linux/amd64,linux/arm64 --push -t raoberman/securities-microservice-1``` Based on https://blog.jaimyn.dev/how-to-build-multi-architecture-docker-images-on-an-m1-mac/
  - ```docker images``` (I have a lot of images)
  - ```docker run -p 8015:8015 raoberman/securities-microservice-1```
  - ```docker push raoberman/securities-microservice-1``` (This step pushed an image for your architecture)

- I committed and pushed the project. 

## EC2

- I used an Amazon Linux instance.


- I followed this example: https://medium.com/appgambit/part-1-running-docker-on-aws-ec2-cbcf0ec7c3f8
  - ```sudo yum update -y```
  - ```sudo service docker start```
  - ```sudo usermod -a -G docker ec2-user```
  - I also installed Git.


- I cloned the project instead of pulling the container because my Mac is ARM.
  - docker build  . -f cool


- There is a way to "build" on ARM for an Intel chipset. I am lazy.


- I built the Dockerfile and then used ```curl localhost:8015```


- I now need to modify the service group to get to port 8015. Go through the instance to security group and add a rule.


- Go into the console and get the EC2 instances public IP address. You can now access the app on 8015.


- Pull the Docker container ```docker pull raoberman/securities-microservice-1```


- I used an Amazon Linux instance.
- 

## Some Helpful Commands

- Kill a process on a port (MacOS): ```lsof -i tcp:3000```



