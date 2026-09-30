import hashlib
import json
import itertools
import pathlib
import types


class UserError(Exception):
    pass


class Address(str):
    pass


class TreeMap(dict):
    @classmethod
    def __class_getitem__(cls, _item):
        return cls


class DynArray(list):
    def __init__(self, *args, **kwargs):
        raise TypeError("this class can't be instantiated by user")

    @classmethod
    def __class_getitem__(cls, _item):
        return cls


class Keccak256:
    def __init__(self):
        self.value = hashlib.sha3_256()

    def update(self, data):
        self.value.update(data)

    def hexdigest(self):
        return self.value.hexdigest()


class Event:
    def emit(self):
        pass


class Public:
    write = staticmethod(lambda fn: fn)
    view = staticmethod(lambda fn: fn)


class Nondet:
    responses = []

    @classmethod
    def exec_prompt(cls, _prompt, **_kwargs):
        return cls.responses.pop(0)


class EqPrinciple:
    @staticmethod
    def prompt_comparative(fn, *_args, **_kwargs):
        return fn()


gl = types.SimpleNamespace(
    Contract=object,
    Event=Event,
    public=Public(),
    vm=types.SimpleNamespace(UserError=UserError),
    message=types.SimpleNamespace(sender_address=Address("0xaaa")),
    nondet=Nondet,
    eq_principle=EqPrinciple(),
)

namespace = {
    "Address": Address,
    "TreeMap": TreeMap,
    "DynArray": DynArray,
    "Keccak256": Keccak256,
    "allow_storage": lambda cls: cls,
    "u32": int,
    "gl": gl,
}
root = pathlib.Path(__file__).resolve().parents[1]
source = (root / "contract.py").read_text().replace("from genlayer import *", "")
exec(compile(source, str(root / "contract.py"), "exec"), namespace)


def fresh():
    ranker = namespace["Ranker"]()
    ranker.rankings = TreeMap()
    return ranker


def open_three(ranker):
    ranker.open_ranking("case", "higher priority")
    ranker.submit_items("case", ["A", "B", "C"])


def must_raise(fn, code):
    try:
        fn()
    except UserError as exc:
        assert str(exc) == code
        return
    raise AssertionError(code)


def ranked():
    ranker = fresh()
    open_three(ranker)
    Nondet.responses = ['{"verdicts":["a","a","a"]}']
    ranker.rank("case")
    assert ranker.get_outcome("case") == namespace["R_RANKED"]
    assert ranker.get_order("case") == ["A", "B", "C"]


def cyclic():
    ranker = fresh()
    open_three(ranker)
    Nondet.responses = ['{"verdicts":["a","b","a"]}']
    ranker.rank("case")
    assert ranker.get_outcome("case") == namespace["R_UNDETERMINED"]


def tied():
    ranker = fresh()
    open_three(ranker)
    Nondet.responses = ['{"verdicts":["=","a","a"]}']
    ranker.rank("case")
    assert json.loads(ranker.rankings["case"].unseparated) == ["0-1"]
    result = json.loads(ranker.get_result("case"))
    assert result["unseparated"] == ["0-1"]
    assert result["order_indices"] == [0, 1, 2]


def incoherent_tie():
    ranker = fresh()
    open_three(ranker)
    Nondet.responses = ['{"verdicts":["=","a","b"]}']
    ranker.rank("case")
    assert ranker.get_outcome("case") == namespace["R_UNDETERMINED"]


def guards():
    ranker = fresh()
    ranker.open_ranking("case", "criterion")
    must_raise(lambda: ranker.submit_items("case", ["A"]), "ITEM_COUNT_OUT_OF_RANGE")
    must_raise(lambda: ranker.submit_items("case", ["A", "a"]), "DUPLICATE_ITEM")


def all_strict_orders():
    for order in itertools.permutations(range(3)):
        ranker = fresh()
        open_three(ranker)
        positions = {item: index for index, item in enumerate(order)}
        verdicts = [
            "a" if positions[i] < positions[j] else "b"
            for i, j in [(0, 1), (0, 2), (1, 2)]
        ]
        Nondet.responses = [json.dumps({"verdicts": verdicts})]
        ranker.rank("case")
        assert ranker.get_outcome("case") == namespace["R_RANKED"]
        assert ranker.get_order("case") == [["A", "B", "C"][i] for i in order]


def malformed_judgments():
    for response in ['{"verdicts":"aaa"}', '{"verdicts":["a"]}',
                     '{"verdicts":["a","invalid","b"]}', 'null', 'not json']:
        ranker = fresh()
        open_three(ranker)
        Nondet.responses = [response]
        ranker.rank("case")
        assert ranker.get_outcome("case") == namespace["R_UNDETERMINED"]
        assert ranker.get_order("case") == []


def settlement_is_terminal():
    for response in ['{"verdicts":["a","a","a"]}', 'not json']:
        ranker = fresh()
        open_three(ranker)
        Nondet.responses = [response]
        ranker.rank("case")
        must_raise(lambda: ranker.rank("case"), "ALREADY_SETTLED")


def commitments_and_authorization():
    ranker = fresh()
    ranker.open_ranking("case", "criterion")
    must_raise(lambda: ranker.rank("case"), "ITEMS_NOT_SUBMITTED")
    original = gl.message.sender_address
    gl.message.sender_address = Address("other")
    try:
        must_raise(lambda: ranker.submit_items("case", ["A", "B"]), "NOT_CREATOR")
    finally:
        gl.message.sender_address = original
    ranker.submit_items("case", ["A", "B"])
    must_raise(lambda: ranker.submit_items("case", ["C", "D"]), "ITEMS_ALREADY_SUBMITTED")
    for field, value in [("items", '["changed","B"]'), ("criterion", "changed")]:
        ranker = fresh()
        open_three(ranker)
        setattr(ranker.rankings["case"], field, value)
        Nondet.responses = []
        ranker.rank("case")
        assert ranker.get_outcome("case") == namespace["R_UNDETERMINED"]


tests = [ranked, cyclic, tied, incoherent_tie, guards, all_strict_orders,
         malformed_judgments, settlement_is_terminal, commitments_and_authorization]
for test in tests:
    test()
    print("PASS", test.__name__)
print(f"{len(tests)}/{len(tests)} pass")
