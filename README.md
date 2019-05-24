# What is terraform-generator ?

The aim of this project is to load jinja2 templates of Terraform code (files with .tf.j2 extension), and to render it with one (or multiple) .tfvars files. This will generate Terraform code from this rendering.

This tool can be used as a Python library, and as a CLI.

# terraform_generator

## Setup

Either use a virtualenv or install globally:
```
python setup.py install
```

This will install the packages required and give you access to the `terraform_generator` executable

## Usage

Locally, either in your virtualenv or globally:

```
(terraform_generator) ➜ terraform_generator
usage: Generate Terraform files from Jinja2 templates. [-h]
                                                       [--templates-dir TEMPLATES_DIR]
                                                       [--tfvars TFVARS [TFVARS ...]]
                                                       [--debug]

optional arguments:
  -h, --help            show this help message and exit
  --templates-dir TEMPLATES_DIR
                        Location of the jinja2 template files. Default is
                        current directory.
  --tfvars TFVARS [TFVARS ...]
                        tfvars file to use with the templates.
  --debug               DEBUG Level of verbosity.