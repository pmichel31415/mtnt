<div align="center">
  <a href="http://www.cs.cmu.edu/~pmichel1/mtnt"><img alt="MTNT" width=100 src="http://www.cs.cmu.edu/~pmichel1/assets/img/mtnt-icon.gif"></a><br><br>
</div>


# MTNT: A Testbed for Machine Translation of Noisy Text

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/960a15f688d94a88922d45a907d1f0bc)](https://www.codacy.com/app/pmichel31415/mtnt?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=pmichel31415/mtnt&amp;utm_campaign=Badge_Grade)

This repo contains the code for the EMNLP 2018 paper [MTNT: A Testbed for Machine Translation of Noisy Text](http://www.cs.cmu.edu/~pmichel1/hosting/mtnt-emnlp.pdf). It will allow you to reproduce the collection process as well as the MT experiments. You can access the data [here](http://www.cs.cmu.edu/~pmichel1/mtnt).

## Prerequisites

For preprocessing, you will need [Moses](https://github.com/moses-smt/mosesdecoder) (for tokenization, clean-up, etc...), [sentencepiece](https://github.com/google/sentencepiece) (for subwords) and [KenLM](https://kheafield.com/code/kenlm/) (for n-gram language modeling). If you want to work with japanese data you should also install [Kytea](http://www.phontron.com/kytea/) (for word segmentation)

To run the collection code, you will need the following python modules:

```
kenlm
langid
numpy
pickle
praw
sentencepiece>=0.1.6
yaml
```

Finally, for the MT experiments, refer to the README in the `recipes` folder

## Downloading and Preparing the Data

From this folder, run

```bash
# Monolingual en data from WMT17
bash scripts/download_en.sh config/data.en.config
bash scripts/prepare_model config/data.en.config

# Monolingual fr data from WMT15
bash scripts/download_fr.sh config/data.fr.config
bash scripts/prepare_model config/data.fr.config

# Prepare en<->fr parallel data
bash scripts/prepare-en-fr.sh config/data.fr.config path/to/moses/scripts

# Download and prepare the en<->ja monolingual and parallel data
bash scripts/download_ja.sh config/data.ja.config path/to/moses/scripts

# Download and extract MTNT
wget http://www.cs.cmu.edu/~pmichel1/hosting/MTNT.1.0.tar.gz && tar xvzf MTNT.1.0.tar.gz && rm MTNT.1.0.tar.gz
# Split the tsv files
bash MTNT/split_tsv.sh
```

You can edit the `config/data.{en,fr,ja}.config` files to change filenames, subword parameters, etc...

## Running the Scraper

Edit the `config/{en,fr,ja}_reddit.yaml` to include the appropriate credentials for your bot. You can also change some of the parameters (like subreddits, etc...).

Then run 

```bash
bash scripts/start_scraper.sh [config_file]`
```

When running the scraper, be mindful of the [Reddit API terms](https://www.reddit.com/wiki/api).

## Analysing the Data

You can analyse the collected data using the various scripts in the `analysis` folder, for example:

```bash
# Count the number of profanities (should return 38)
cat MTNT/test/test.en-fr.en | python3 analysis/count_keywords.py resources/profanities.en
# Count the number of emojis (should return 46)
cat MTNT/test/test.en-fr.en | python3 analysis/count_emojis.py
# Check the ration US/UK spelling (for ise/ize which is a good indicator) (should return 35.7% 64.3%)
cat MTNT/test/test.en-fr.en | python3 analysis/uk_us_ratio.py
# Count the number of informal pronouns (in japanese) (should return 35)
kytea -model ~/kytea/share/kytea/model.bin -notags MTNT/test/test.ja-en.ja | python3 analysis/count_keywords.py resources/informal_pronouns.ja
```

## Citing

If you use this code or the MTNT dataset, please cite the following publication:

```
@InProceedings{michel2018mtnt,
  author    = {Michel, Paul  and  Neubig, Graham},
  title     = {MTNT: A Testbed for Machine Translation of Noisy Text},
  booktitle = {Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing}
}
```

## License

The code is released under the [MIT License](LICENSE). The data is released under the terms of the [Reddit API]((https://www.reddit.com/wiki/api))
