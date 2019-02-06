from graphotype import Schema, Query

s = Schema('schema.graphql')
result = Query(s, '{ me { id }}')

reveal_type(result)
reveal_type(result())
reveal_type(result().me)
