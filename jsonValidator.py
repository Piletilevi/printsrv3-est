import jsonschema
from json import load as loadJSON

SCHEMA_FILENAME = path.join(BASEDIR, 'jsonschema', 'plp.json')
with open(SCHEMA_FILENAME, 'rU') as schema_file:
    schema = loadJSON(schema_file)

print('Validating against {0}: {1}'.format(SCHEMA_FILENAME, PLP_FILENAME))
try:
    print('S: {0}'.format(schema))
    print('D: {0}'.format(PLP_JSON_DATA))
    jsonschema.validate(PLP_JSON_DATA, schema)
except jsonschema.exceptions.ValidationError as ve:
    print("JSON validation ERROR\n")
    print( "{0}\n".format(ve))
    raise ve
