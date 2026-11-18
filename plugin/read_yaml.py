"""
This cylc pre-configure plugin allows the workflow to read an
experiment or workflow YAML file and parse it directly in the
workflow definition file.

If no YAML file is found or if it is empty, the current behavior
is to continue with warning. 
"""
from pathlib import Path
import yaml
from cylc.flow import LOG

def pre_configure(srcdir=None, opts=None, rundir=None):
    """
    The pre-configure plugin function finds the experiment YAML
    file, reads/loads the information, and returns the YAML
    information in a dictionary to be parse by the workflow
    definition file. 

    :param srcdir: is the directory containing the workflow
                   definition file to install
    :type srcdir: path or string
    :param opts: are CLI options set for a cylc script
    :type opts: object containing CLI options
    :param rundir: is the location of the cylc-run directory
    :type rundir: path or string

    :return:
    :rtype: dict
    """
    LOG.info(" *** CALLING READ_YAML PLUGIN *** ")

    yml_info = {}

    # Find yaml file
    yaml_files = Path(srcdir).glob("*.yaml")
    yamls = []
    for yf in yaml_files:
        if yf.name != "environment.yaml":
            yamls.append(yf)

    if not yamls:
        LOG.warning("NO YAML DETECTED.")
        return {}
    if len(yamls) > 1:
        raise ValueError("Too many YAML configs in src dir - Need"
                         "clarification for which is the experiment yaml")

    LOG.info(yamls[0])
    yaml_file = yamls[0]

    # Load yaml file
    with open(yaml_file, 'r') as f:
        yml_info = yaml.safe_load(f)

    if yml_info is None:
        LOG.warning("YAML IS EMPTY.")
        return {}
    if yml_info is not None and not isinstance(yml_info, dict):
        raise ValueError("Expected dictionary mapping in YAML file")

    LOG.info("YAML FILE %s DETECTED", yaml_file)
    return {'template_variables': yml_info,
            'templating_detected': 'jinja2'}

####another thing to try
#    # inject/mutate jinja2_vars directly
#    if yml_info and jinja2_vars is not None:
#        jinja2_vars['yml'] = yml_info
#
#    return {'template_variables': {'yml': yml_info},
#            'templating_detected': 'jinja2'}
####

## want this script to accept resolved yaml and create everything needed to run workflow
# - in dictionary format
# - gets rid of rose-suite.conf
# - removes dependency on cylc-rose
