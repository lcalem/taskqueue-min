#!/bin/bash

mrq-worker --greenlets $WORKER_GREENLETS $(echo $WORKER_QUEUES | sed 's/,/ /g')
