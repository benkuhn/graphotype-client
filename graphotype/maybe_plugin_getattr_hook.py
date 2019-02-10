from typing import Optional, Callable, Union, List

from mypy.nodes import TypeInfo, SymbolTable, ClassDef, Block, MemberExpr, NameExpr
from mypy.plugin import AnalyzeTypeContext, Plugin, AttributeContext
from mypy.types import Type, AnyType, TypeOfAny, JsonDict, deserialize_type, Instance, TypeVarType, UnionType, NoneTyp


class MaybePlugin(Plugin):
    def get_attribute_hook(self, fullname: str
                           ) -> Optional[Callable[[AttributeContext], Type]]:
        if fullname.startswith('graphotype.maybe.Maybe'):
            print(f"Getattr({fullname})")
            return maybe_getattr_hook

def maybe_getattr_hook(ctx: AttributeContext) -> Type:
    """Called when we recognize a Maybe attribute access"""

    if isinstance(ctx.type, Instance):
        # a Maybe instance! let's see if we can resolve the argument.
        arg = ctx.type.args[0]
        if isinstance(arg, Instance) and isinstance(ctx.context, MemberExpr):
            # Ok, we can check this Maybe[Thingy].attrib attribute access by returning the
            # Thingy.attrib
            return get_type_of_maybe_attrib_access(ctx, arg, ctx.context.name)

    # Either this is not an instance of Maybe[Thingy], or Thingy is something we don't know
    # (yet?) how to introspect. Either way, fallback to the default attribute handler.
    return ctx.default_attr_type

def get_type_of_maybe_attrib_access(ctx: AttributeContext, arg: Instance, name: str) -> Type:
    use_maybe_handler = False
    if name.endswith("_"):
        # Use the Maybe handler
        orig_type_stnode = arg.type.get(name[:-1])
        use_maybe_handler = True
    else:
        orig_type_stnode = arg.type.get(name)

    if orig_type_stnode:
        # The name exists in the original context
        orig_type = make_required(orig_type_stnode.type)
        print(f"Use {'maybe' if use_maybe_handler else 'opt'} handler: {orig_type}")

        if use_maybe_handler:
            # Wrap orig_type in Maybe[]
            return ctx.api.named_generic_type('graphotype.maybe.Maybe', [orig_type])
        else:
            # Wrap orig_type in Optional[]
            return make_optional(orig_type)

    else:
        ctx.api.fail(f"No attribute named {arg}.{name} (via Maybe[{arg}])", ctx.context)

    return ctx.default_attr_type

def plugin(version: str):
    # ignore version argument if the plugin works with all mypy versions.
    print("Plugin init")
    return MaybePlugin

# These 2 helpers from https://github.com/python/mypy/issues/5409
def make_required(typ: Type):
    if not isinstance(typ, UnionType):
        return typ
    items = [item for item in typ.items if not isinstance(item, NoneTyp)]
    return UnionType.make_union(items)

def make_optional(typ: Type):
    return UnionType.make_simplified_union([typ, NoneTyp()])
