from typing import (
    Any,
    Callable,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
    TypeVar,
)

T = TypeVar("T")

K = TypeVar("K")
V = TypeVar("V")


def flatten(list_of_maps: Sequence[Mapping[K, V]], /) -> Mapping[K, Sequence[V]]:
    aggregate_mapping: MutableMapping[K, MutableSequence[V]] = {}

    mapping: Mapping[K, V]
    for mapping in list_of_maps:
        key: K
        value: V
        for key, value in mapping.items():
            aggregate_mapping.setdefault(key, []).append(value)

    return aggregate_mapping


def text(mapping: Mapping[str, Any], /) -> str:
    return text_all(mapping)[0]


def text_all(mapping: Mapping[str, Any], /) -> Sequence[str]:
    return [run["text"] for run in mapping["runs"]]


def filter_one(iterable: Sequence[T], predecate: Callable[[T], bool]) -> T:
    item: T
    for item in iterable:
        if predecate(item):
            return item

    # TODO: Raise appropriate exception
    raise Exception
