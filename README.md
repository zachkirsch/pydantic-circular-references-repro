## Pydantic circular references repro

This repo is a repro of \<ISSUE\>. 

There are three pydantic models:

```python
# foo.py
import typing
import pydantic

from .baz import Baz

class Foo(pydantic.BaseModel):
    foo_field: typing.Optional[Baz]
```

```python
# baz.py
import pydantic

from .bar import Bar 

# we're inherited from Bar (defined below)
class Baz(Bar):
    ...

Baz.update_forward_refs()
```

```python
# bar.py
import pydantic

class Bar(pydantic.BaseModel):
    bar_field: "Foo"

from .foo import Foo

Bar.update_forward_refs()
```

To repro the error, run:
```
pyenv shell 3.7.13
poetry env use $(which python)
poetry install
poetry run python src/main.py
```

`Baz.update_forward_refs()` fails with the following errors:

```
$ poetry run python src/main.py
Traceback (most recent call last):
  File "src/main.py", line 1, in <module>
    from circular_pydantic_models.bar import Bar
  File "/private/var/folders/zb/sncxfc0n1y96dwgkk2phgb9w0000gn/T/pytest-of-zachkirsch/pytest-39/test_ir_pydantic_model0/repro2/src/circular_pydantic_models/bar.py", line 9, in <module>
    from .foo import Foo
  File "/private/var/folders/zb/sncxfc0n1y96dwgkk2phgb9w0000gn/T/pytest-of-zachkirsch/pytest-39/test_ir_pydantic_model0/repro2/src/circular_pydantic_models/foo.py", line 4, in <module>
    from .baz import Baz
  File "/private/var/folders/zb/sncxfc0n1y96dwgkk2phgb9w0000gn/T/pytest-of-zachkirsch/pytest-39/test_ir_pydantic_model0/repro2/src/circular_pydantic_models/baz.py", line 18, in <module>
    Baz.update_forward_refs()
  File "pydantic/main.py", line 816, in pydantic.main.BaseModel.update_forward_refs
  File "pydantic/typing.py", line 553, in pydantic.typing.update_model_forward_refs
    def_mod = sys._getframe(1).f_globals.get('__name__', '__main__')  # for pickling
  File "pydantic/typing.py", line 519, in pydantic.typing.update_field_forward_refs
    in all type variables.
  File "pydantic/typing.py", line 58, in pydantic.typing.evaluate_forwardref
    'MappingView',
  File "/Users/zachkirsch/.pyenv/versions/3.7.13/lib/python3.7/typing.py", line 467, in _evaluate
    eval(self.__forward_code__, globalns, localns),
  File "<string>", line 1, in <module>
NameError: name 'Foo' is not defined
```

`Baz` inherits a field `bar_field: "Foo"` from its superclass `Bar`.
`Baz.update_forward_refs()` tries to resolve this forward ref by looking at
`module.__dict__`, but `Foo` is not in scope in `baz.py`, so it throws.

Possible solution: Pydantic should recognize that `bar_field` is actually defined
in `bar.py`, and use the `module.__dict__` of `bar.py` when resolving `Foo`.