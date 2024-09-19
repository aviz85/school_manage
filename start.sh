#!/usr/bin/env bash

gunicorn school_manage.wsgi:application