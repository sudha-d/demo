 #!/usr/bin/env python3
import sys 
import yaml
import pprint
##################### READ #####################

connection_filename = "connection.yaml"
job_filename = "job.yaml"
route_filename = "route.yaml"
defaults_filename = "defaults.yaml"
expect_struct_filename = "combined_expected.yaml"
connection_vars = {}
job_vars = {}
route_vars = {}
defaults_vars = {}
result = {}
pp = pprint.PrettyPrinter(indent=4)

# Open connection_vars file
connection = yaml.safe_load(open(connection_filename, 'r'))
job = yaml.safe_load(open(job_filename, 'r'))
route = yaml.safe_load(open(route_filename, 'r'))
defaults = yaml.safe_load(open(defaults_filename, 'r'))
expected = yaml.safe_load(open(expect_struct_filename, 'r'))

pp.pprint(connection)


combined = connection | job | route

##################### MERGE #####################

categories = ['connection', 'job', 'route']

def recursive_merge(dict1, dict2):
    for key, value in dict2.items():
        if key in dict1 and isinstance(dict1[key], dict) and isinstance(value, dict):
            dict1[key] = recursive_merge(dict1[key], value)
        elif value is not None:
            dict1[key] = value
    return dict1
result = recursive_merge(defaults, combined)    
result_keys = []
expected_keys = []
def get_keys(result, lst, pre = None):
    for k, v in result.items():
     ck = (pre + "." + k) if pre is not None else k
     lst.append(ck)
     if isinstance(v, dict):
        get_keys(v, lst, ck)
get_keys(result, result_keys)
get_keys(expected, expected_keys)

print(result_keys)
print(expected_keys)

missing_keys = set(expected_keys) - set(result_keys)

if len(missing_keys) > 0:
   missing_keys_str = f"Following  keys are missing in the YAML - {','.join(missing_keys)}"
   raise Exception(missing_keys_str)

with open('combined_actual.yaml', 'w') as file:
     yaml.dump(result, file, default_flow_style=False, indent=4)
 
