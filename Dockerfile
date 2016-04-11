FROM ubuntu:14.04
MAINTAINER Steven Skoczen <steven@buddyup.org>
CMD ["gulp", "app"]

# Set up the directory for the codebase link.
RUN mkdir -p /code
RUN mkdir -p /code/app
VOLUME /code/app
EXPOSE 5000

# Update the OS
RUN apt-get update  # March 4 2016

# Install the base languages & tools
RUN rm -rf /usr/lib/node_modules/npm
RUN apt-get install -y curl git nginx python3 npm python3-setuptools libpq-dev python3-dev libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk libmemcached-dev nodejs libncurses5-dev libffi-dev nano  # March 4 2016

## Carrying on
RUN npm install -g n
RUN n 4.3.1
RUN n use 4.3.1

# Install node globals, pip
RUN easy_install3 pip
RUN pip3 install --upgrade pip

# Skipping for now.
# RUN pip3 install virtualenv virtualenvwrapper
# RUN mkvirtualenv buddyup
# RUN workon buddyup
 
# Prep the app for updating.
WORKDIR /code

# Set up reqs
COPY requirements.txt /code/requirements.txt
RUN pip3 install -r requirements.txt

WORKDIR /code/app

# Set up nginx
COPY docker/nginx.conf /etc/nginx/nginx.conf
RUN nginx -g "daemon on;"
RUN if ! cat /etc/hosts | grep "bu app.bu" > /dev/null ; then echo '127.0.0.1 bu app.bu api.bu marketing.bu gc.bu groundcontrol.bu m.bu dashboard.bu' >> /etc/hosts; fi
RUN if ! cat /etc/hosts | grep "dev.firebase.bu" > /dev/null ; then echo '127.0.0.1 dev.firebase.bu test.firebase.bu' >> /etc/hosts; fi
