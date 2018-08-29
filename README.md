<div align="center">
  <a href="http://www.cs.cmu.edu/~pmichel1/mtnt"><img alt="MTNT" width=100 src="http://www.cs.cmu.edu/~pmichel1/assets/img/mtnt-icon.gif"></a><br><br>
</div>


# MTNT: A Testbed for Machine Translation of Noisy Text

This repo contains the code for the EMNLP 2018 paper [MTNT: A Testbed for Machine Translation of Noisy Text](http://www.cs.cmu.edu/~pmichel1/hosting/mtnt-emnlp.pdf). It will allow you to reproduce the collection process as well as the MT experiments. You can access the data [here](http://www.cs.cmu.edu/~pmichel1/mtnt).

## Prerequisites

For preprocessing, you will need [Moses](https://github.com/moses-smt/mosesdecoder) (for tokenization, clean-up, etc...), [sentencepiece](https://github.com/google/sentencepiece) (for subwords) and [KenLM](https://kheafield.com/code/kenlm/) for n-gram language modeling.

To run the collection code, you will need the following python modules:

```
kenlm
langid
numpy
pickle
praw
sentencepiece
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
```

You can edit the `config/data.{en,fr,ja}.config` files to change filenames, subword parameters, etc...

## Running the scraper

Edit the `config/{en,fr,ja}_reddit.yaml` to include the appropriate credentials for your bot. You can also change some of the parameters (like subreddits, etc...).

Then run 

```bash
bash scripts/start_scraper.sh [config_file]`
```

When running the scraper, be mindful of the [Reddit API terms](https://www.reddit.com/wiki/api).

## Citing

If you use this code or the MTNT dataset, please cite the following publication:

```
@InProceedings{michel2018mtnt,
  author    = {Michel, Paul  and  Neubig, Graham},
  title     = {A Challenge Set Approach to Evaluating Machine Translation},
  booktitle = {Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing}
}
```

## License

The code is released under the [MIT License](LICENSE). The data is released under the terms of the [Reddit API]((https://www.reddit.com/wiki/api))
