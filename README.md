# ICD Coding Benchmark
Automatic ICD coding benchmark based on the MIMIC dataset.

**NOTE: 🚧 The repo is under construction. Please see below for available datasets/models.**

Automatic diagnosis coding[^1] in clinical NLP is a task to predict the diagnoses and the procedures during a hospital stay given the summary of the stay (discharge summary).
The labels of the task are mostly represented in ICD (international classification of disease) codes which are alpha-numeric codes widely adopted by hospitals in the US.
The most popular database used in automatic diagnosis coding is the MIMIC-III dataset, but the preprocessing varies among the literature, and some of them are done incorrectly.
Such inconsistency and error make it hard to compare different methods on automatic diagnosis coding and, arguably, results in incorrect evaluations of the methods.

This code repository aims to provide a standardized benchmark of automatic diagnosis coding with the MIMIC-III database.
The benchmark encompasses all the procedures of ICD coding: dataset pre-processing, model training/evaluation, and interactive web demo.

We currently provide (items in parentheses are under development):
- Four preset of preprocessed datasets: MIMIC-III full, top-50, full (old), top-50 (old), where we referred to (old) as the version of CAML[^2].
- ICD coding models: CNN, CAML, DCAN, (MultiResCNN, LAAT, Fusion)
- (Interactive demo)

## Preparation
Please put the MIMIC-III `csv.gz` files (v1.4) under `datasets/mimic3/csv/`. You can also create symbolic links pointing to the files.

## Pre-processing
Please run the following command to generate the MIMIC-III top-50 dataset or generate other versions using the config files in `configs/preprocessing`.
```
$ python run_preprocessing.py --config_path configs/preprocessing/mimic3_50.yml
```

## Training / Testing
Please run the following command to train, or resume training of, the CAML model on the MIMIC-III top-50 dataset. You can evaluate the model with `--test` options and use other config files under `configs`.
```
$ python run.py --config_path configs/caml_mimic3_50.yml         # Train
$ python run.py --config_path configs/caml_mimic3_50.yml --test  # Test
```

## Results
- MIMIC-III full

| Model        | macro AUC | micro AUC | macro F1 | micro F1 | P@8      | P@15     |
|--------------|-----------|-----------|----------|----------|----------|----------|
| CAML         | 0.890823  | 0.984352  | 0.048890 | 0.498832 | 0.703181 | 0.553875 |
| DCAN         | 0.854977  | 0.980384  | 0.057142 | 0.522896 | 0.718491 | 0.568149 |

- MIMIC-III top-50

| Model        | macro AUC | micro AUC | macro F1 | micro F1 | P@5      |
|--------------|-----------|-----------|----------|----------|----------|
| CAML         | 0.917969  | 0.942569  | 0.608479 | 0.688646 | 0.662709 |
| DCAN         | 0.933557  | 0.953008  | 0.658478 | 0.727083 | 0.681014 |

- MIMIC-III full (old)

| Model        | macro AUC | micro AUC | macro F1 | micro F1 | P@8      | P@15     |
|--------------|-----------|-----------|----------|----------|----------|----------|
| CAML         | 0.880379  | 0.983444  | 0.057407 | 0.500574 | 0.696582 | 0.546777 |
| DCAN         | 0.844949  | 0.978251  | 0.063707 | 0.524617 | 0.722160 | 0.570087 |

- MIMIC-III top-50 (old)

| Model        | macro AUC | micro AUC | macro F1 | micro F1 | P@5      |
|--------------|-----------|-----------|----------|----------|----------|
| CAML         | 0.881043  | 0.908731  | 0.519399 | 0.610033 | 0.612955 |
| DCAN         | 0.913397  | 0.937868  | 0.611135 | 0.688379 | 0.649393 |


## Cite this work
```
@misc{juyong2022icdcodinggithub,
  author = {Juyong Kim and Abheesht Sharma and Suhas Shanbhogue},
  title = {dalgu90/icd-coding-benchmark},
  year = {2022},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/dalgu90/icd-coding-benchmark}},
}
```

## Authors
(in alphabetical order)
- Abheesht Sharma [@abheesht17](https://github.com/abheesht17)
- Juyong Kim [@dalgu90](https://github.com/dalgu90)
- Suhas Shanbhogue [@SuhasShanbhogue](https://github.com/SuhasShanbhogue)

[^1]: Also referred to as medical coding, clinical coding, or simply ICD coding in other literature. They may have different meanings in detail.
[^2]: Mullenbach, et al., Explainable Prediction of Medical Codes from Clinical Text, NAACL 2018 ([paper](https://arxiv.org/abs/1802.05695), [code](https://github.com/jamesmullenbach/caml-mimic))
