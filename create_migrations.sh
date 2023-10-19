#!/bin/bash

cd $PWD'/scripts/alembic/' || exit
alembic revision --autogenerate -m 'xpymxpymbot'