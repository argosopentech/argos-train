from argostrain.dataset import *
from argostrain.utils import *

from collections import deque
import random


def generate_sbd_data(dataset):
    """Generates data for doing sentence boundary detection.

    Args:
        dataset (IDataset): Dataset of language data

    Returns:
        IDataset: Sbd dataset
    """
    source_lang_data = dataset.data()[0]

    def strip_tail_newline(x):
        if len(x) > 0 and x[-1] == "\n":
            return x[:-1]
        return x

    sbd_source = deque()
    sbd_target = deque()
    for i in range(len(source_lang_data)):
        # Take each sentence and add a fragment of two random sentences
        sentence = source_lang_data[i]
        if len(sentence) == 0:
            continue
        rand_sentence = source_lang_data[randrange(len(source_lang_data))]
        rand_sentence2 = source_lang_data[randrange(len(source_lang_data))]
        sentence = strip_tail_newline(sentence)
        rand_sentence = strip_tail_newline(rand_sentence)
        rand_sentence2 = strip_tail_newline(rand_sentence2)
        rand_sentences = rand_sentence + rand_sentence2
        sentence_fragment = rand_sentences[: randrange(len(rand_sentences)) + 1]

        sbd_source.append(
            "<detect-sentence-boundaries>" + sentence + sentence_fragment + "\n"
        )
        sbd_target.append(sentence + "<sentence-boundary>" + "\n")

        # Include a fraction of sentences that don't contain a sentence boundary.
        # When this happens the model should return the source without the
        # <sentence-boundary> token.
        SENTENCE_BOUNDARY_MISS_RATIO = 0.1
        if random.random() < SENTENCE_BOUNDARY_MISS_RATIO:
            sb_miss = sentence[: randrange(len(sentence))]
            sbd_source.append("<detect-sentence-boundaries>" + sb_miss)
            sbd_target.append(sb_miss)

        if i % 1000 == 0:
            info(f"Generating sbd data {i}/{len(source_lang_data)}")

    return Dataset(sbd_source, sbd_target)
