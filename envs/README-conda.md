# Building conda environments

This guide covers using (in theory) cross-platform conda environments for running Omnibenchmarks

---

## What is conda?

**[conda](https://anaconda.org/)** is a general-purpose package manager that in principle will build an environment on Mac, Linux and Windows. We use it here to pin environments for running our benchmark modules.

---

## How we use it

### 1. specify requirements in a conda YAML file (e.g., r_osta.yml)

### 2. test the env with `create` command: e.g., conda env create -f r_osta.yml

### 3. Omnibenchmark will build and then active such environments from `ob run my-benchmark.yaml`

