import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from tools.ezr import *
from tools.stats import *
from tools.causal_tools import causalTree, causalTreeLeaf, remove_confounders
import random
import os

# TREATMENTS = ["ezr", "ezr-cf", "cs", "cs-cf"]
TREATMENTS = ["ezr-cf"]


# =============================================================================
# Main experiment
# =============================================================================
def run(file_directory, repeats=1):
    all_data = Data(csv(file_directory))
    if not all_data.cols.y:
        if all_data.cols.klass:
            all_data.cols.y = [all_data.cols.klass]
        else:
            print(f"Error: No objective columns found in {file_directory}")
            return

    # Global baseline stats
    ys      = [disty(all_data, row) for row in all_data.rows]
    b4      = adds(ys)
    win     = lambda v: int(100 * (1 - (v - b4.lo) / (b4.mu - b4.lo)))
    b4_wins = adds([win(k) for k in ys])

    the.Budget  = 50
    the.Impurity= "gini"
    the.acq     = "near"
    the.leaf    = 3

    for trt in TREATMENTS:
        for rand_seed in range(repeats):
            # random.seed(rand_seed)
            # the.seed      = rand_seed
            # shuffled_rows = random.sample(all_data.rows, len(all_data.rows))
            half    = int(0.5 * len(all_data.rows))
            train   = clone(all_data, all_data.rows[:half])
            # holdout = clone(all_data, shuffled_rows[half:])
            # All treatments use the same labeled rows from likely()
            labels  = likely(train)

            train_data = clone(train, labels)
            # if "cf" in trt:
            a = len(train_data.cols.x)
            tmp = remove_confounders(train_data)
            print(f"{(100*(a-len(tmp))//a)} % ,\t{a},\t{a - len(tmp)},\t{file_directory}")
            # print(tmp, len(tmp))
            # input()
            # train_data.cols.x = tmp
            # tree     = Tree(train_data)
            # top_rows = sorted(
            #     [(treeLeaf(tree, row).mu, row) for row in holdout.rows],
            #     key=lambda x: x[0]
            # )[:the.Check]


if __name__ == "__main__":
    # file_directory = sys.argv[1] if len(sys.argv) > 1 else "data/optimize/misc/auto93.csv"
    for file in Path("data/optimize/").rglob("*.csv"):
        run(file, 1)

