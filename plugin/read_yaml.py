from cylc.flow import LOG
from pathlib import Path
import yaml
#import logging
#
## set up logging
#logging.basicConfig(level=logging.INFO)
#logger = logging.getLogger(__name__)

def pre_configure(srcdir=None, opts=None, rundir=None):
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
        raise ValueError("Too many YAML configs in cylc-src dir- don't know which is experiment yaml")

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

    LOG.info(f"YAML FILE {yaml_file} DETECTED")
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
