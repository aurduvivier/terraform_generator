from jinja2 import Template, exceptions
from glob import glob
from hcl import load
import re
import sys
import os
import logging
import argparse

logging.basicConfig()
logger = logging.getLogger('resolver')
log_lvl = 'ERROR'

class ResolverError(Exception):
  pass

def get_j2_files(directory):
  """
  Return all .tf.j2 files in a directory
  """
  if not directory.endswith("/"):
    directory = directory + '/'
    return get_j2_files(directory)
  else:
    j2_files = glob(directory + "*.tf.j2")
    logger.info
    if len(j2_files) > 0:
      logger.info('Listing .tf.j2 files.')
      return j2_files
    else:
      raise ResolverError("There are no .tf.j2 files, or the directory doesn't exist.")

def tfvars_to_dictionnary(tfvars_file):
  """
  Load a tfvars file and return a python dictionnary
  """
  try:
    with open(tfvars_file, 'r') as tfvars:
      return load(tfvars)
  except FileNotFoundError as error:
    raise ResolverError(error)
  except ValueError as error:
    raise ResolverError("Loading tfvars file : {}".format(error))

def render_j2(jinja2_file, values):
  """
  From the j2 template and the terraform values, render the j2 template with the Terraform variables
  """
  with open(jinja2_file) as jinja2:
    logger.info('Rendering {} template with the tfvars.'.format(jinja2_file))
    jinja_template = Template(jinja2.read())
    return jinja_template.render(values)

def generate_render_files(j2_files, tfvars):
  """
  From j2_files and tfvars dictionnary, generate .tf files and delete .tf.j2 files, and return the list of resolved Terraform code.
  """
  rendering_list = [] 
  for file in j2_files:
    file_tf = re.sub(".j2", "", file)
    logger.info('Creating {} file.'.format(file_tf))
    with open(file_tf, "w+") as render_file:
      logger.info('{} file created.'.format(file_tf))
      try:
        rendering = render_j2(file, tfvars)
        logger.debug('Rendering {0} :\n{1}'.format(file, rendering))
        logger.info('Write render result in {}'.format(file_tf))
        rendering_list.append(rendering)
        render_file.write(rendering)
      except exceptions.UndefinedError as error:
        raise ResolverError(error)
  return(rendering_list)

def resolve(directory, tfvars_files):
  """
  From the directory and a list of tfvars files, generate .tf files and delete .tf.j2 files, and return the list of resolved Terraform code.
  """
  logger.info('Starting the resolve on \'{0}\' directory with tfvars files {1}.'.format(directory, tfvars_files))
  j2_files = get_j2_files(directory)
  tfvars = {}
  for file in tfvars_files:
    logger.info('Aggregating {} to a central tfvars dictionnary.'.format(file))
    tfvars.update(tfvars_to_dictionnary(file))
  logger.debug('Aggregated tfvars : {}'.format(tfvars))
  generate_render_files(j2_files, tfvars)
  logger.info('Resolve completed.')
  return(generate_render_files(j2_files, tfvars))

def get_args():
  """
  Get the command line parameters
  """
  parser = argparse.ArgumentParser('Generate Terraform files from Jinja2 templates.')
  parser.add_argument('--templates-dir', default='.', help='Location of the jinja2 template files. Default is current directory.')
  parser.add_argument('--tfvars', default=None, nargs='+', help='tfvars file to use with the templates.')
  parser.add_argument('--debug', action='store_const', const='DEBUG', help='DEBUG Level of verbosity.')

  args = parser.parse_args()
  return args


def main():
  """
  Entrypoint
  """
  args = get_args()

  if args.debug:
    log_level = args.debug
  else:
    log_level = 'ERROR'
  logger.setLevel(getattr(logging, log_level))

  try:
    resolve(args.templates_dir, args.tfvars)
  except ResolverError as error:
      if os.getenv('DEBUG', None):
          import traceback
          traceback.print_exc()
      else:
          logger.error(error)
      sys.exit(1)

if __name__ == "__main__":
    main()