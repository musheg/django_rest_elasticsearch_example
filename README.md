
##Development setup

####Install required system packages:

    sudo apt-get install python3-pip
    sudo apt-get install python3-dev python3-setuptools
    sudo apt-get install libpq-dev

####Create www directory where project sites and environment dir

    mkdir /var/www && mkdir /var/envs && mkdir /var/envs/bin

#####Install virtualenvwrapper

    sudo pip3 install virtualenvwrapper
    sudo pip3 install --upgrade virtualenv

####Add these to your bashrc virutualenvwrapper work

    export WORKON_HOME=/var/envs
    export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
    export PROJECT_HOME=/var/www
    export VIRTUALENVWRAPPER_HOOK_DIR=/var/envs/bin
    source /usr/local/bin/virtualenvwrapper.sh

#####Create virtualenv

    cd /var/envs && mkvirtualenv --python=python3 drf_elastic_example

####Install requirements for a project.

    cd /var/www/drf_elastic_example && pip install -r requirements/base.txt
    
    
####Install ElasticSearch
    Please see the attached link
    https://www.elastic.co/guide/en/elasticsearch/reference/current/install-elasticsearch.html