# read settings from YAML
# check ok
# generate LaTeX
# call pdflatex to generate pdf

import subprocess

import yaml
from jinja2 import Environment, PackageLoader

config = None
with open("config.yaml") as config_file:
    config = yaml.safe_load(config_file)

config['row_number'] = config['first_line_number']

print(config)

env = Environment(loader=PackageLoader('geocachelog', 'templates'), variable_start_string="[[", variable_end_string="]]")

header = env.get_template('header.tex')
table_header = env.get_template('table_header.tex')
table_row = env.get_template('table_row.tex')
table_row_replace = env.get_template('table_row_replace.tex')
table_footer = env.get_template('table_footer.tex')
page_break = env.get_template('page_break.tex')
footer = env.get_template('footer.tex')


output_file = "%s.tex" % config["geocache_name"]

page_1_rows = 36
page_2_rows = 42

with open(output_file , "w") as log_tex:
    log_tex.write(header.render(config = config))
    log_tex.write(table_header.render(config = config))
    for i in range(page_1_rows):
        log_tex.write(table_row.render(config = config))
        config['row_number'] += 1
    log_tex.write(table_footer.render(config = config))
    log_tex.write(page_break.render(config = config))
    log_tex.write(table_header.render(config = config))
    for i in range(page_2_rows-11):
        log_tex.write(table_row.render(config = config))
        config['row_number'] += 1
    log_tex.write(table_row_replace.render(config = config))
    for i in range(10):
        log_tex.write(table_row.render(config = config))
        config['row_number'] += 1
    log_tex.write(table_footer.render(config = config))
    log_tex.write(footer.render(config = config))


process = subprocess.Popen(["pdflatex", output_file])
output, errors = process.communicate()
    
