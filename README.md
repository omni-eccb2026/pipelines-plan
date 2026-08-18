# Benchmarking scRNA pipelines (simplified for ECCB 2026 Workshop)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18848104.svg)](https://doi.org/10.5281/zenodo.18848104)

A scRNA-seq pipelines benchmark created using [OmniBenchmark](https://omnibenchmark.org), but trimmed for the purposes of the [ECCB 2026 workshop](https://eccb2026.org/tutorials-workshops#w1-constructing-standardized-benchmarks-using-omnibenchmark).

## Reproducing

OmniBenchmark is required to run this pipeline and can be installed following [this guide](https://docs.omnibenchmark.org/latest/howto/#installation).

```{bash}
git clone https://github.com/scrna-bench/pipelines-plan.git
cd pipelines-plan
git checkout eccb2026
ob run benchmark.yaml -c 10

#ob run benchmark.yaml -- --apptainer-args='--nv'  # not needed for ECCB workshop
```

## Other useful commands (pick one by one, do not cut-paste)

```{bash}
ob validate plan benchmark.yaml 
ob run benchmark.yaml -d                       # dry run (creates Snakefile, not run)
ob run benchmark.yaml -d --unpinned            # if using branch refs (not hashes)
ob run benchmark.yaml -d --unpinned --dirty    # if using local directories
ob run benchmark.yaml -c 16 --unpinned         # specify number of cores
prlimit --rss=64g --cpu=10000 ob run benchmark.yaml -c 8 --unpinned --continue-on-error  # process limits
```


## Citation

If you use this benchmark in your research, please cite it using the information in `CITATION.cff`.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
