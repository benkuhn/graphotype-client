from typing import Optional, Callable

from mypy.plugin import Plugin, FunctionContext, DynamicClassDefContext
from mypy.types import Type, LiteralType
from mypy.nodes import TypeInfo, SymbolTable, ClassDef, Block

class CustomPlugin(Plugin):
    def get_function_hook(self, fullname: str) -> Optional[Callable[[FunctionContext], Type]]:
        if fullname == 'graphotype.Schema':
            return schema_callback
    def get_dynamic_class_hook(self, fullname: str) -> Optional[Callable[[DynamicClassDefContext], TypeInfo]]:
        if fullname == 'graphotype.Schema.query':
            return query_callback

def schema_callback(ctx: FunctionContext) -> Type:
    # todo assert ctx.args = [[StrExpr]]
    fname = ctx.args[0][0].value
    return ctx.default_return_type.copy_modified(
        args=[LiteralType(fname, ctx.arg_types[0][0])]
    )

def query_callback(ctx: DynamicClassDefContext) -> TypeInfo:
    # todo be defensive--ctx.type is Schema[Literal[fname]]
    fname = ctx.type.args[0].value
    query = ctx.args[0][0].value
    print(fname, query)
    return TypeInfo(
        names=SymbolTable(),
        defn=ClassDef(
            'Query',
            defs=Block([])
        ),
        module_name='example'
    )

def plugin(version: str):
    # ignore version argument if the plugin works with all mypy versions.
    return CustomPlugin
