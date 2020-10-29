from jsonschema import validate

# Read schema


# Verify schema

# Convert schema to class

cls = type('A', (object,), {'__doc__': 'class created by type'})

print(cls)
print(cls.__doc__)
