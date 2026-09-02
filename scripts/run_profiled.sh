#!/usr/bin/env bash
# Exercise 17: same job, sampled. Registered as the `profiled` entrypoint next
# to `default` and `pinned`, so the plan selects it without the module changing
# again.
#
# The job runs inside this module's conda env, and the `prof` env holding denet
# is NOT active there -- so denet is taken from $DENET by absolute path. With
# $DENET unset this is exactly the default entrypoint, which is what you want
# on a normal run.
set -euo pipefail

if [ -z "${DENET:-}" ]; then
  exec ./run.R "$@"
fi

# --output_dir is where every other artefact of this job lands; put the trace
# beside them so it is keyed by the same parameter hash as the run it describes.
out=.
for i in $(seq 1 $#); do
  [ "${!i}" = "--output_dir" ] || [ "${!i}" = "-o" ] || continue
  j=$((i + 1)); out=${!j}
done

exec "$DENET" -i 200 -m 200 -q --out "$out/denet.jsonl" run -- ./run.R "$@"
