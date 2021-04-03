# Auto data downloader

### Metadata example
```
{
  "name": "WikiMatrix",
  "type": "parallel_corpus",
  "from_code": "en",
  "to_code": "de",
  "size": "1000000",
  "reference": "Holger Schwenk, Vishrav Chaudhary, Shuo Sun, Hongyu Gong and Paco Guzman, WikiMatrix: Mining 135M Parallel Sentences in 1620 Language Pairs from Wikipedia, arXiv, July 11 2019."
}
```

### Overview
Packages are a zip archive with the .argosdata extension. `metadata.json` is in the root like for packages. The data is in two text files `source` and `target`. Each parallel line in each file is a data point.

Optionally data packages can contain a `README` and `LICENSE` file.

