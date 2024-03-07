# #!/bin/bash
# from time import sleep
#
# import celery
#
# set -o errexit
# set -o nounset
#
# # wait for redis server to start
# sleep 10
#
# celery -A root --broker="${CELERY_BROKER}" flower