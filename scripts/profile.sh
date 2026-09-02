#!/usr/bin/env bash
# Exercise 17: sample the process tree with denet, once for a single module and
# once for the whole DAG, then print denet's own summary for each.
#
#   scripts/profile.sh [OUT_DIR]     # default: out_prof
#
# Writes benchmark outputs to OUT_DIR (whole DAG) and OUT_DIR_m (single
# module), and the denet traces to OUT_DIR.prof/. Nothing is shared between the
# two runs, so both traces are of real work.
#
# Assumes `denet` and `ob` are already on PATH:
#   conda create -n prof -c https://repo.prefix.dev/almost-conductor -c conda-forge denet
#   conda activate prof
set -euo pipefail
cd "$(dirname "$0")/.."

command -v denet >/dev/null || { echo "denet not on PATH — see exercise 17"; exit 1; }
command -v ob    >/dev/null || { echo "ob not on PATH"; exit 1; }

OUT=${1:-${OUT_DIR:-out_prof}}
PROF=${PROF_DIR:-$OUT.prof}
MODULE=${MODULE:-osta-r}
mkdir -p "$PROF"

# Point CONDA_PREFIX_DIR at an out-dir you have already built and snakemake
# reuses those envs instead of resolving ~5 GB again, e.g.
#   CONDA_PREFIX_DIR=$PWD/out/.snakemake/conda scripts/profile.sh
SNAKE_ARGS=()
[ -n "${CONDA_PREFIX_DIR:-}" ] && SNAKE_ARGS=(-- --conda-prefix "$CONDA_PREFIX_DIR")

# -i == -m pins the sampling interval; denet otherwise backs off towards
# --max-interval and you get too few points to plot.
sample() {
  local tag=$1; shift
  echo "==> $tag: $*"
  denet -i 200 -m 200 -q --out "$PROF/$tag.jsonl" run -- "$@" || true
  denet stats "$PROF/$tag.jsonl"
}

# One module, dev mode: prunes everything after its stage, first param
# expansion only. The cheap view.
sample "$MODULE" ob run benchmark.yaml --out-dir "${OUT}_m" -m "$MODULE" -c 1 "${SNAKE_ARGS[@]}"

# The whole DAG, in its OWN out-dir: same sampler, now with snakemake, env
# activation and job overlap all inside the tree. This is the view the single
# module cannot give. Sharing an out-dir with the run above would leave this
# one nothing to do and the trace would be meaningless.
sample full ob run benchmark.yaml --out-dir "$OUT" -c 2 "${SNAKE_ARGS[@]}"

echo
echo "traces in $PROF/. Plot them with:"
echo "  python3 scripts/aggregate.py $PROF/*.jsonl"
