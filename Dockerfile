From ubuntu:14.04

COPY requirements.txt requirements.txt 

RUN /bin/bash -c 'apt-get install -y python-setuptools && \
                  mkdir -p $HOME/.pip && \
                  easy_install pip virtualenv && \
                  virtualenv /env && \
                  source /env/bin/activate && \
                  pip install -r requirements.txt'

CMD ["/env/bin/python", "setup.py", "test"]
