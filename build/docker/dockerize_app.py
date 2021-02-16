# dockerize_model.py - Package complete app in docker image to run on target server.

import os

FLASK_PORT=5555
DOMAIN='DRIVEN'
DIR = 'images/'
IMAGE_NAME=DOMAIN  # directory where Docker image will be saved in.
FILE_NAME = DIR + IMAGE_NAME + '_latest.tar'

DOCKER_USER = 'ubuntu'
DOCKER_HOST = '18.222.98.146'  # Server Dockerized loaninfo app will be deployed to.

AWS_KEY = '' # os[env] or "~/.AWS/byjove1.pem"


build_cmd = "docker build -f build/predict/Dockerfile --build-arg FLASK_RUN_PORT={flask_port} -t {image_name} .".format(
    flask_port=FLASK_PORT,
    image_name=IMAGE_NAME,
    )
save_cmd = "docker save {image_name}:latest > {file_name}".format(
    image_name=IMAGE_NAME,
    file_name=FILE_NAME,
    )

#os.system(build_cmd)
#   os.system(save_cmd)


if __name__ == '__main__':
    KEY=AWS_KEY
    # For testing only. We use ansible or airflow to move our dockerized model.
    #os.system("scp -i ~/.AWS/byjove1.pem {filename} ubuntu@3.12.163.71:~/".format(filename=FILE_NAME))
    input("load?")
    """
    os.system("ssh -i {key} {docker_user}@{docker_host} docker load -i {filename}".format(
        key=KEY,
        docker_user=DOCKER_USER,
        docker_host=DOCKER_HOST,
        filename=FILE_NAME,
        )
    )
    """
    input("run?")
    # Run model.
    RUN_CMD = "ssh -i {key} {docker_user}@{docker_host} docker run --expose {port} -p {port}:{port} {image_name}".format(
        key=KEY,
        docker_user=DOCKER_USER,
        docker_host=DOCKER_HOST,
        filename=FILE_NAME,
        port=FLASK_PORT,
        image_name=IMAGE_NAME,
        )
    os.system(RUN_CMD)
