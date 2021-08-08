#!/bin/sh


gunicorn --worker-class eventlet -w 1 apps:app -b 0.0.0.0:$SERVER_PORT