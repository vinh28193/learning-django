#!/bin/sh

# Local Window venv
# from project root
D:/workspaces/py-venvs/django/Scripts/python -m pip install -U pip
D:/workspaces/py-venvs/django/Scripts/python -m pip install -U pip
D:/workspaces/py-venvs/django/Scripts/python -m pip install -r requirements.txt
D:/workspaces/py-venvs/django/Scripts/python manage.py runserver 127.0.0.1:8100
D:/workspaces/py-venvs/django/Scripts/celery -A ecommerce.celery worker -l info --concurrency=2
D:/workspaces/py-venvs/django/Scripts/celery -A ecommerce.celery beat -l info

# Jenkin
dev_branch="dev"
master_branch="master"
git_branch_local=$(echo $GIT_BRANCH   | sed -e "s|origin/||g")

#cp /data/syncode_proroxy_rsa ~/.ssh/syncode_rsa
#chmod 600 ~/.ssh/syncode_rsa
#chmod 775 .

# Check branch deploy
if [ $git_branch_local = $dev_branch ]
then
    cp /data/syncode_proroxy_rsa .
    echo "Deploy branch dev to ENV Dev"
    rsync -avz -e 'ssh  -i ~/.ssh/syncode_rsa -o StrictHostKeyChecking=no' . syncode@10.148.15.196:/data/projects/ecommerce-backend
    ssh -i ~/.ssh/syncode_rsa syncode@127:0.0.1 '/data/venvs/ecommerce/bin/pip install -U pip'
    ssh -i ~/.ssh/syncode_rsa syncode@127:0.0.1 '/data/venvs/ecommerce/bin/pip install -U setuptools'
    ssh -i ~/.ssh/syncode_rsa syncode@127:0.0.1 'cd /data/code/ecommerce && /data/venvs/ecommerce/bin/pip install -r requirements.txt'
    ssh -i ~/.ssh/syncode_rsa syncode@127:0.0.1 'sudo supervisorctl restart ecommerce'
    ssh -i ~/.ssh/syncode_rsa syncode@127:0.0.1 'sudo supervisorctl restart ecommerce_celery_worker'
    ssh -i ~/.ssh/syncode_rsa syncode@127:0.0.1 'sudo supervisorctl restart ecommerce_celery_beat'
elif [ $git_branch_local = $master_branch ]
then
    echo "Deploy branch master to ENV Prod"
    echo "Branch" $git_branch_local " not have config deploy"
else
    echo "Branch" $git_branch_local " not have config deploy"
fi