import json
import jsonschema

def __fix_property_name(property):
    if property[0] == "@":
        return "at_" + property[1:]
    else:
        return property


def __fix_property_names(properties):
    out = []
    for property in properties:
        out.append(__fix_property_name(property))

    return out

def __build_generate_dict_function(schema_dictionary):
    dict_fun_string = "def generate_dict():\n"
    dict_fun_string += "\tobject_dictionary = {}\n"

    for property in schema_dictionary["properties"]:
        dict_fun_string += "\tobject_dictionary['" + property + "'] = self." + property + "\n"

    dict_fun_string += "\treturn dict_fun_string"

    print(dict_fun_string)


def build_constructor(schema_dictionary):
    required_properties = schema_dictionary["required"]

    required_properties = __fix_property_names(required_properties)

    constructor_string = "def f(self "
    for property in required_properties:
        constructor_string += ", " + property

    constructor_string += "): \n"

    for property in required_properties:
        constructor_string += "\tself." + property + " = " + property + " \n"

    d = {}
    exec(constructor_string, d)

    return(d['f'])

def generate(schema_name):
    filename = "openMINDS/v3.0/products/" + schema_name + ".schema.json"

    with open(filename,'r') as f:
        schema_dictionary = json.loads(f.read())

        jsonschema.Draft7Validator.check_schema(schema_dictionary)

        class_dictionary = {"__doc__": schema_dictionary["description"]}

        for property in schema_dictionary["properties"]:
            class_dictionary[__fix_property_name(property)] = None

        class_dictionary["__init__"] = build_constructor(schema_dictionary)
        __build_generate_dict_function(schema_dictionary)

        return type(schema_name, (object,), class_dictionary)
