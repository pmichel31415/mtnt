#!/usr/bin/env python3

from sacrebleu import corpus_bleu
import argparse
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("REF", type=str, metavar="REF", help="Reference file.")
parser.add_argument(
    "HYP_1", type=str, metavar="HYP_1", help="Output from the first model"
)
parser.add_argument(
    "HYP_2", type=str, metavar="HYP_2", help="Output from the second model"
)
parser.add_argument(
    "--sample-percent",
    type=float,
    default=50,
    help="Percentage of the data to resample",
)
parser.add_argument(
    "--num-samples", default=1000, type=int, help="Number of resamples"
)


def get_bleu(ref, hyp, tokenization="intl"):
    """Wrapper for sacreBLEU corpus bleu"""
    BLEU = corpus_bleu(hyp, [ref], tokenize=tokenization)
    return BLEU.score


def loadtxt(filename):
    """Load text file as a numpy array of strings"""
    txt = []
    with open(filename, "r") as f:
        for line in f:
            txt.append(line.strip())
    return np.asarray(txt)


def main(args):
    # Load files
    ref = loadtxt(args.REF)
    hyp_1 = loadtxt(args.HYP_1)
    hyp_2 = loadtxt(args.HYP_2)
    # check file sizes
    assert len(ref) == len(hyp_1) and len(ref) == len(hyp_2), "File sizes don't match"
    N = len(ref)
    size_subsample = int(N * args.sample_percent)
    # Run resampling
    n_1 = n_2 = n_draw = 0
    order = np.arange(N, dtype=int)
    for _ in range(args.num_samples):
        # Shuffle
        np.random.shuffle(order)
        indices = order[:size_subsample]
        # Get bleus
        bleu_1 = get_bleu(ref[indices], hyp_1[indices])
        bleu_2 = get_bleu(ref[indices], hyp_2[indices])
        # Record result
        if bleu_1 > bleu_2:
            n_1 += 1
        elif bleu_1 < bleu_2:
            n_2 += 1
        else:
            n_draw += 1

    # Print conclusion
    print(f"Comparing system 1 {args.HYP_1} vs system 2 {args.HYP_2}")
    print("=" * 20)
    print(f"1 > 2: {n_1*100/args.num_samples:.2f}")
    print(f"1 < 2: {n_2*100/args.num_samples:.2f}")
    print(f"1 = 2: {n_draw*100/args.num_samples:.2f}")


if __name__ == "__main__":
    main(parser.parse_args())
