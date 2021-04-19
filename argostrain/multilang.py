from argostrain.dataset import *
from argostrain.utils import *

from collections import deque

def multilang_special_token(code):
    return f'<translate-to-{code}>'

"""
<translate-to-es>Hello
Hola

<translate-to-fr>Hello
Bonjour
"""

def generate_multilang_data(datasets):
    """Generates data for doing multi-lang translation

    Args:
        datasets [(IDataset, code), ...]: Dataset of language data.
                A list of tuples where each tuple contains data and the target
                language's ISO code
    
    Returns:
        IDataset: Multilang dataset
    """
    to_return = CompositeDataset()
    for dataset, code in datasets:
        source, target = dataset.data()
        source = [multilang_special_token(code) + source_line for source_line in source]
        to_return += CompositeDataset(Dataset(source, target))
    return to_return


