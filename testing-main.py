import json
from jsonschema import validate, Draft7Validator

def build_constructor(schema_dictionary):
    required_properties = schema_dictionary["required"]
    constructor_string = "lambda self"

    for property in required_properties:
        constructor_string += ", " + property

    constructor_string += ": "

    for property in required_properties:
        constructor_string += ", " + property

    print(constructor_string)

def get_property_list(schema_dictionary):
    print(schema_dictionary["properties"])

# Read schema
filename = "openMINDS/v3.0/products/copyright.schema.json"    # Testing with dataset schema
with open(filename,'r') as f:
    schema_dictionary = json.loads(f.read())

# Verify schema
    Draft7Validator.check_schema(schema_dictionary)

# Convert schema to class
    #print(schema_dictionary)

    #test = get_property_list(schema_dictionary)

    class_dictionary = {"__doc__": schema_dictionary["description"]}

    for property in schema_dictionary["properties"]:
        #print(property)
        class_dictionary[property] = None

    class_dictionary["__init__"] = build_constructor(schema_dictionary)

    #print(class_dictionary)
    cls = type("Copyright", (object,), class_dictionary)

    print(cls)
    print(cls.__doc__)
    print(vars(cls))

    test_object = cls("Hello world")
