#!/bin/sh 

venvwrap="virtualenvwrapper.sh"

#python38=`/usr/bin/which python3.8`
#VIRTUALENVWRAPPER_PYTHON=${python38}

export WORKON_HOME=/root/.virtualenvs

if [ $? -eq 0 ]; then
        venvwrap="/usr/local/python3/bin/virtualenvwrapper.sh"
        source $venvwrap
fi

workon hkws_xfj
source activate
uwsgi --ini /root/project/hkws_xfj/uwsgi.ini &
nohup python kill_pid.py>kill_pid.log 2>&1 &
