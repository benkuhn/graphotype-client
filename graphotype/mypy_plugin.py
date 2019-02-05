from typing import Optional, Callable

from mypy.plugin import Plugin, FunctionContext, MethodContext
from mypy.types import Type, LiteralType

class CustomPlugin(Plugin):
    def get_function_hook(self, fullname: str) -> Optional[Callable[[FunctionContext], Type]]:
        if fullname == 'graphotype.Schema':
            return schema_callback
    def get_method_hook(self, fullname: str) -> Optional[Callable[[MethodContext], Type]]:
        if fullname == 'graphotype.Schema.query':
            return query_callback

def schema_callback(ctx: FunctionContext) -> Type:
    # todo assert ctx.args = [[StrExpr]]
    fname = ctx.args[0][0].value
    return ctx.default_return_type.copy_modified(
        args=[LiteralType(fname, ctx.arg_types[0][0])]
    )

def query_callback(ctx: MethodContext) -> Type:
    # todo be defensive--ctx.type is Schema[Literal[fname]]
    fname = ctx.type.args[0].value
    query = ctx.args[0][0].value
    print(fname, query)
    return ctx.default_return_type

def plugin(version: str):
    # ignore version argument if the plugin works with all mypy versions.
    return CustomPlugin
