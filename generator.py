import json
import jsonschema

from string import Template

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


def _build_constructor_string(schema_dictionary):
    required_properties = schema_dictionary["required"]

    required_properties = __fix_property_names(required_properties)

    constructor_string = "def __init__(self "
    for property in required_properties:
        constructor_string += ", " + property

    constructor_string += "): \n"

    for property in required_properties:
        constructor_string += "\tself." + property + " = " + property + " \n"

    return constructor_string

def _indent_function(function_string):
    new_function_string = ""
    for line in range(0, len(function_string)):
        new_function_string += "\t" + function_string[line] + "\n"

    return new_function_string


def build_constructor(schema_dictionary):
    d = {}
    exec(_build_constructor_string(schema_dictionary), d)

    return(d['__init__'])

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


def generate_file(schema_name):
    filename = "openMINDS/v3.0/products/" + schema_name + ".schema.json"

    with open(filename,'r') as f:
        schema_dictionary = json.loads(f.read())
        template_string = "class $schema_name:\n"
        constructor_string = _indent_function(_build_constructor_string(schema_dictionary).split("\n"))

        for property in schema_dictionary["properties"]:
            template_string += "\t" + __fix_property_name(property) + " = None\n"

        # Add constructor
        template_string += "\n$init"
        # Prepare template for substitution
        class_string_template = Template(template_string)
        # Print the "file", for now
        print(class_string_template.substitute({"schema_name": schema_name, "init":constructor_string}))
