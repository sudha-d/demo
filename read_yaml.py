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

