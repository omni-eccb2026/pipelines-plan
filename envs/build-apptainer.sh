#!/bin/bash

apptainer build r-bioc-320.sif r-bioc-320.def
apptainer build --build-arg RAPIDS_SINGLECELL_VERSION=0.14.1 py-rsc-0.14.1.sif py.def
apptainer build --build-arg RAPIDS_SINGLECELL_VERSION=0.13.5 py-rsc-0.13.5.sif py.def
