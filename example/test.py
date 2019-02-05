from graphotype import Schema

s = Schema('schema.graphql')
reveal_type(s)
result = s.query('{ me { id }}')
reveal_type(result)
