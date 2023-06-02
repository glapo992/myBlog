# defines an image to start from, if not present will pull it first
FROM alpine 

LABEL editor="glapo"

# defines a working directory in the docker image
WORKDIR /usr/src/app

#execute the copy form the local folder to the root folder of the workdir
COPY . ..

# run a command to install dependencies
ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools
RUN pip install --no-cache-dir -r req.txt
# expose a port, in this case 5000 because is def port of flask
EXPOSE 5000

# the command that will run the application
CMD ["flask run"]
