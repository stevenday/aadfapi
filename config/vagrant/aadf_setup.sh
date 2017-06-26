#!/bin/bash


VENV_NAME=$1

echo "=== Begin AADF Provisioning using 'config/vagrant/aadf_setup.sh'"

workon $VENV_NAME

if [[ -f /vagrant/manage.py ]]; then

  su - vagrant -c "source /home/vagrant/.virtualenvs/$VENV_NAME/bin/activate && cd /vagrant && ./manage.py load_wards"

  su - vagrant -c "source /home/vagrant/.virtualenvs/$VENV_NAME/bin/activate && cd /vagrant && ./manage.py load_aadf_data"

fi

echo "=== End Vagrant Provisioning using 'config/vagrant/aadf_setup.sh'"


