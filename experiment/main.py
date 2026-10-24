import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from tools.ezr import *
from tools.stats import *
from tools.causal_tools import causalTree, causalTreeLeaf, remove_confounders
import random
import os

TREATMENTS = ["ezr", "ezr-cf", "cs", "cs-cf"]


# =============================================================================
# Main experiment
# =============================================================================
def run(file_directory, repeats=20):
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

    the.Budget  = 200
    the.Impurity= "gini"
    the.acq     = "near"
    the.leaf    = 3
    # =========================================================
    # Performance (RMSE of errors) and Stability (STD of errors) - (20 train/holdout splits per treatment)
    # =========================================================
    performance_error = {}
    error_dist        = {}
    runtime           = {trt : 0 for trt in TREATMENTS}
    suggestions       = {trt : [] for trt in TREATMENTS}
    for trt in TREATMENTS:
        mse    = 0
        errors = []
        for rand_seed in range(repeats):
            random.seed(rand_seed)
            the.seed      = rand_seed
            shuffled_rows = random.sample(all_data.rows, len(all_data.rows))
            half    = int(0.5 * len(all_data.rows))
            train   = clone(all_data, shuffled_rows[:half])
            holdout = clone(all_data, shuffled_rows[half:])

            # All treatments use the same labeled rows from likely()
            labels  = likely(train)

            t0 = time.time()
            if "ezr" in trt:
                train_data = clone(train, labels)
                if "cf" in trt:     remove_confounders(train_data)
                tree     = Tree(train_data)
                top_rows = sorted(
                    [(treeLeaf(tree, row).mu, row) for row in holdout.rows],
                    key=lambda x: x[0]
                )[:the.Check]
            elif "cs" in trt:
                ctree, canon = causalTree(data = clone(train, labels), filter_confounders=True) if "cf" in trt else causalTree(data = clone(train, labels), filter_confounders=False)
                top_rows     = sorted(
                    [(causalTreeLeaf(canon, ctree, row).mu, row)
                     for row in holdout.rows],
                    key=lambda x: x[0]
                )[:the.Check]
            runtime[trt] += time.time() - t0

            # trt_perf = max( 
            #                 win(min([disty(all_data, row) for _, row in top_rows])) ,
            #                 win(min(disty(all_data,row) for row in labels))
            #             )
            
            trt_perf = win(min([disty(all_data, row) for _, row in top_rows]))
            
            # ref_opt  = win(min(disty(all_data, row) for row in holdout.rows + labels))
            ref_opt  = win(min(disty(all_data, row) for row in holdout.rows))

            suggestions[trt].append(trt_perf)

            err      = ref_opt - trt_perf
            errors.append(err)
            mse     += abs(err) ** 2

        error_dist[trt]        = errors
        performance_error[trt] = (mse / repeats) ** 0.5

    # Statistical ranking of performance
    pooled_sd = adds([e for errs in error_dist.values() for e in errs]).sd
    best_performances = top(error_dist, Ks=0.9, Delta="smed", eps=pooled_sd * 0.35)

    stability = { trt: [adds(suggestions[trt]).sd] for trt in TREATMENTS}
    best_stability = top(stability, Ks=0.9, Delta="smed", eps=b4_wins.sd * 0.35)


    # =========================================================
    # Output
    # =========================================================

    print("trt, perf-rmse , stab-std, best_perf, best_stab, runtimes")
    for trt in TREATMENTS:
        print( f"{trt}, {performance_error[trt]:.2f}, {stability[trt][0]:.2f}, {1 if trt in best_performances else 0}, {1 if trt in best_stability else 0}, {runtime[trt]:.2f}" )



if __name__ == "__main__":
    file_directory = sys.argv[1] if len(sys.argv) > 1 else "data/optimize/misc/auto93.csv"
    run(file_directory, 20)
