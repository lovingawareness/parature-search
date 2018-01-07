#!/bin/bash -x
source .secrets && export $(cut -d= -f1 .secrets)
