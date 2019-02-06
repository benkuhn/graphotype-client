from typing import Optional, Callable

from mypy.plugin import Plugin, FunctionContext, DynamicClassDefContext
from mypy.types import Type, LiteralType
from mypy.nodes import TypeInfo, SymbolTable, ClassDef, Block, SymbolTableNode, LDEF, MDEF, GDEF, SymbolNode, Var
import mypy.nodes as mpn

class CustomPlugin(Plugin):
    def get_function_hook(self, fullname: str) -> Optional[Callable[[FunctionContext], Type]]:
        if fullname == 'graphotype.Schema':
            return schema_callback
    def get_dynamic_class_hook(self, fullname: str) -> Optional[Callable[[DynamicClassDefContext], TypeInfo]]:
        if fullname == 'graphotype.Query':
            return query_callback

def schema_callback(ctx: FunctionContext) -> Type:
    # todo assert ctx.args = [[StrExpr]]
    fname = ctx.args[0][0].value
    return ctx.default_return_type.copy_modified(
        args=[LiteralType(fname, ctx.arg_types[0][0])]
    )

def query_callback(ctx: DynamicClassDefContext) -> TypeInfo:
    # todo be defensive--ctx.type is Schema[Literal[fname]]
    #fname = ctx.arg_types[0].value
    query = ctx.call.args[1].value
    defn = ClassDef(
        ctx.name,
        defs=Block([
            mpn.AssignmentStmt(
                lvalues=mpn.NameExpr, rvalue=None, type=ctx.api.lookup_fully_qualified_or_none('builtins.str'),
                new_syntax=True
            )
        ])
    )
    defn.fullname = ctx.api.qualified_name(ctx.name)
    names = SymbolTable()
    var = Var('me', ctx.api.builtin_type('builtins.str'))
    var.info = var.type.type
    var.is_property = True
    names['me'] = SymbolTableNode(
        MDEF,
        var,
        plugin_generated=True
    )
    info = TypeInfo(
        names=names,
        defn=defn,
        module_name=ctx.api.cur_mod_id
    )
    obj = ctx.api.builtin_type('builtins.object')
    info.mro = [info, obj.type]
    info.bases = [obj]
    print(ctx.name, info)
    ctx.api.add_symbol_table_node(ctx.name, SymbolTableNode(GDEF, info))

def plugin(version: str):
    # ignore version argument if the plugin works with all mypy versions.
    return CustomPlugin
