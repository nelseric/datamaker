FROM phusion/passenger-full:0.9.11
ENV HOME /root
CMD ["/sbin/my_init"]

# Put all apt stuff here
RUN apt-get update


# # Install H2O, Borrowed from mikecomstock/h2o-docker
RUN apt-get install -y unzip openjdk-7-jre
RUN curl 'http://s3.amazonaws.com/h2o-release/h2o/rel-kolmogorov/3/h2o-2.4.4.3.zip' > /tmp/h2o.zip
RUN unzip /tmp/h2o.zip -d /root
RUN mkdir /etc/service/h2o
ADD docker-data/h2o.sh /etc/service/h2o/run
EXPOSE 54321

RUN apt-get install -y python-pip python-dev
RUN apt-get install -y h5utils libhdf5-dev libblas-dev liblapack-dev gfortran

ADD docker-data/id_rsa.pub /tmp/id_rsa.pub
RUN cat /tmp/id_rsa.pub >> /root/.ssh/authorized_keys && rm -f /tmp/id_rsa.pub
EXPOSE 22

# RUN pip install virtualenvwrapper
# RUN ln -s /usr/local/bin/virtualenvwrapper.sh /etc/profile.d/virtualenvwrapper.sh

# RUN /bin/bash -lc "mkvirtualenv -a /root/datamaker datamaker"
RUN pip install pip -U

RUN pip install numpy==1.8.2 Cython==0.20.2 numexpr==2.4
ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# Now the meat
RUN mkdir /root/datamaker
ADD . /root/datamaker

# Everybody do your share
# RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
