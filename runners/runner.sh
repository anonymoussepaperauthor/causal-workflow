# !/bin/bash
find data/optimize/*/* -name "*.csv" | \
    parallel --jobs 50% --load 80% --progress \
    'echo "Running {/}..." && python experiment/main.py {} > experiment/results/{/}'
