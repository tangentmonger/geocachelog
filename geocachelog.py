"""
Geocache log sheet generator. Takes configuration from config.yaml, 
generates a LaTeX file, and runs pdflatex to produce a printable 
PDF log sheet.
"""

#stdlib
import subprocess

#third party
import yaml
from jinja2 import Environment, PackageLoader

def get_config(config_filename):
    """
    Load config from YAML file
    """
    config = None
    with open(config_filename) as config_file:
        config = yaml.safe_load(config_file)

    config['row_number'] = config['first_line_number']
    return config


def generate_tex(config, tex_filename):
    """
    Generate the intermediate .tex representation of the log sheet
    and write it to the given filename
    """
    # Hard coded the number of rows per page because this is 
    # awkward to calculate in LaTeX. Revisit if the paper size changes.
    PAGE_1_ROWS = 36
    PAGE_2_ROWS = 42
    REMINDER_ROW = 10

    # Change the Jinja variable start and end strings because LaTeX
    # already uses curly braces
    env = Environment(  loader=PackageLoader('geocachelog', 'templates'),
                        variable_start_string="[[", 
                        variable_end_string="]]")

    # Load Jinja template files
    header = env.get_template('header.tex')
    table_header = env.get_template('table_header.tex')
    table_row = env.get_template('table_row.tex')
    table_row_replace = env.get_template('table_row_replace.tex')
    table_footer = env.get_template('table_footer.tex')
    page_break = env.get_template('page_break.tex')
    footer = env.get_template('footer.tex')


    # Generate and write the .tex file
    with open(tex_filename , "w") as log_tex:
        log_tex.write(header.render(config = config))
        log_tex.write(table_header.render(config = config))
        for _ in range(PAGE_1_ROWS):
            log_tex.write(table_row.render(config = config))
            config['row_number'] += 1
        log_tex.write(table_footer.render(config = config))
        log_tex.write(page_break.render(config = config))
        log_tex.write(table_header.render(config = config))
        for _ in range(PAGE_2_ROWS-REMINDER_ROW-1):
            log_tex.write(table_row.render(config = config))
            config['row_number'] += 1
        log_tex.write(table_row_replace.render(config = config))
        for _ in range(REMINDER_ROW):
            log_tex.write(table_row.render(config = config))
            config['row_number'] += 1
        log_tex.write(table_footer.render(config = config))
        log_tex.write(footer.render(config = config))

def generate_pdf(tex_filename):
    """
    Run pdflatex on the given .tex file to generate a PDF
    """
    process = subprocess.Popen(["pdflatex", tex_filename])
    process.communicate()
 

def generate_logsheet(config_filename):
    """
    Given a YAML configuration, generate a PDF geocache logfile.
    """
    config = get_config(config_filename)
    tex_filename = "%s.tex" % config["geocache_name"]
    generate_tex(config, tex_filename)
    generate_pdf(tex_filename)
   
   
generate_logsheet("config.yaml")
