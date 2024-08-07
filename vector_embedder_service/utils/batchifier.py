import itertools


class Batchifier:
    @staticmethod
    def batchify(iterable, num_items_per_batch):
        it = iter(iterable)
        while batch := list(itertools.islice(it, num_items_per_batch)):
            yield batch
