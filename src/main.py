from circular_pydantic_models.bar import Bar
from circular_pydantic_models.foo import Foo

Foo.parse_raw("""
{
    "foo_field": null
}
""")