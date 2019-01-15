# MT experiments

This folder contains the XNMT recipes to run the MT experiments from the [MTNT paper](http://www.cs.cmu.edu/~pmichel1/hosting/mtnt-emnlp.pdf).

## Requirements


[XNMT](https://github.com/neulab/xnmt) is a neural machine translation toolkit based on [Dynet](https://github.com/clab/dynet). On a UNIX system, you can install XNMT by first [installing Dynet](https://dynet.readthedocs.io/en/latest/python.html) and then running

```bash
# Clone
git clone https://github.com/neulab/xnmt.git
# The experiments were run with this specific version
git reset --hard feb3951
# Install xnmt
cd xnmt
pip install -r requirements.txt
python setup.py install
```

For the `en-ja` experiments you will also need [Kytea](http://www.phontron.com/kytea/) to segment the detokenized japanese text to compute BLEU scores. You can find instructions to install Kytea [here](http://www.phontron.com/kytea/#download). The following will assume that Kytea is located at `~/kytea` (if it isn't change the path in `../bleu_ja.sh`). 

## Running the Experiments

Assuming you have prepared the data according to the provided scripts, you can run the experiments with the following commands (here for `en-fr`)

```bash
# Training (this will take a while)
OVERWRITE_LOG=1 python -m xnmt.xnmt_run_experiments --dynet-gpu config.en-fr.yaml
# Run on test sets
OVERWRITE_LOG=1 python -m xnmt.xnmt_run_experiments --dynet-gpu config.en-fr.eval.yaml
# Fine-tuning on MTNT
OVERWRITE_LOG=1 python -m xnmt.xnmt_run_experiments --dynet-gpu config.en-fr.tune.yaml
```

Note that XNMT will produce detokenized outputs. For comparison with the paper you should compute the BLEU scores with [sacreBLEU](https://github.com/mjpost/sacreBLEU). Additionally, for en-ja, you will need to run the Kytea segmenter to tokenize the data before calling sacrebleu (this is encapsulated in the `../scripts/bleu_ja.sh` file).

Here are all the commands you need to run after the experiments are over:

```bash
## en-fr
# newstest2014
cat hyp/base-en-fr-eval.newstest2014.hyp.fr | sacrebleu --tokenize=intl ../fr/newstest2014.fr
# newsdiscusstest2015
cat hyp/base-en-fr-eval.newsdiscusstest2015.fr | sacrebleu --tokenize=intl ../fr/newsdiscusstest2015.fr
# MTNT (base)
cat hyp/base-en-fr-eval.hyp.fr | sacrebleu --tokenize=intl ../MTNT/test/test.en-fr.fr
# MTNT (tuned)
cat hyp/tune-en-fr.tuned.fr | sacrebleu --tokenize=intl ../MTNT/test/test.en-fr.fr

## fr-en
# newstest2014
cat hyp/base-fr-en-eval.newstest2014.hyp.en | sacrebleu --tokenize=intl ../fr/newstest2014.en
# newsdiscusstest2015
cat hyp/base-fr-en-eval.newsdiscusstest2015.en | sacrebleu --tokenize=intl ../fr/newsdiscusstest2015.en
# MTNT (base)
cat hyp/base-fr-en-eval.hyp.en | sacrebleu --tokenize=intl ../MTNT/test/test.fr-en.en
# MTNT (tuned)
cat hyp/tune-fr-en.tuned.en | sacrebleu --tokenize=intl ../MTNT/test/test.fr-en.en

## en-ja
# TED
bash ../scripts/bleu_ja.sh hyp/base-en-ja-eval.ted.ja ../ja/test.ted.ja
# KFTT
bash ../scripts/bleu_ja.sh hyp/base-en-ja-eval.kftt.ja ../ja/test.kftt.ja
# JESC
bash ../scripts/bleu_ja.sh hyp/base-en-ja-eval.jesc.ja ../ja/test.jesc.ja
# MTNT (base)
bash ../scripts/bleu_ja.sh hyp/base-en-ja-eval.noisy.ja ../MTNT/test/test.en-ja.ja
# MTNT (tuned)
bash ../scripts/bleu_ja.sh hyp/tune-en-ja.tuned.ja ../MTNT/test/test.en-ja.ja

## ja-en
# TED
cat hyp/base-ja-en-eval.ted.en | sacrebleu --tokenize intl ../ja/test.ted.en
# KFTT
cat hyp/base-ja-en-eval.kftt.en | sacrebleu --tokenize intl ../ja/test.kftt.en
# JESC
cat hyp/base-ja-en-eval.jesc.en | sacrebleu --tokenize intl ../ja/test.jesc.en
# MTNT (base)
cat hyp/base-ja-en-eval.hyp.en | sacrebleu --tokenize=intl ../MTNT/test/test.ja-en.en
# MTNT (tuned)
cat hyp/tune-ja-en.tuned.en | sacrebleu --tokenize=intl ../MTNT/test/test.ja-en.en
```


