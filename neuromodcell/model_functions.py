""" Based on BluePyOpt example code by Werner van Geit,
modified by Johannes Hjorth """

import os
import json
import numpy as np
import glob
import bluepyopt.ephys as ephys

##############################################################################
def files(modeldir):

    modeldir = os.path.abspath(modeldir)
    
    param_file = os.path.join(modeldir,"parameters.json")
    mod_file = os.path.join(modeldir,"modulation.json")
       
    if len(glob.glob(os.path.join( modeldir,"*.swc"))) == 1:
        morph_file = glob.glob(os.path.join(modeldir,"*.swc"))[0]
    else:
        import pdb
        pdb.set_trace()
        raise ValueError("There should be only one swc file.")

    mech_file = os.path.join(modeldir,"mechanisms.json")


    return param_file, morph_file, mod_file, mech_file


def define_mechanisms(mechanism_config=None, script_dir = None):
    """Define mechanisms"""

    assert (mechanism_config is not None)
    # print("Using mechanism config: " + mechanism_config)

    mech_definitions = json.load(
        open(
            os.path.join(mechanism_config)))

    if "modpath" in mech_definitions:
        mod_path = os.path.join(script_dir, mech_definitions["modpath"])
        print("mod_path set to " + mod_path + " (not yet implemented)")
    else:
        mod_path = None

    mechanisms = []
    for sectionlist in mech_definitions:

        channels = mech_definitions[sectionlist]

        # This allows us to specify a modpath in the file
        if sectionlist == "modpath":
            continue

        seclist_loc = ephys.locations.NrnSeclistLocation(
            sectionlist,
            seclist_name=sectionlist)
        for channel in channels:
            mechanisms.append(ephys.mechanisms.NrnMODMechanism(
                name='%s.%s' % (channel, sectionlist),
                mod_path=mod_path,
                suffix=channel,
                locations=[seclist_loc],
                preloaded=True))

    return mechanisms


##############################################################################

def define_modulation(param_set):

        modulation_params = list()

        for param_config in param_set:
            if 'value' in param_config:
                frozen = True
                value = param_config['value']
                bounds = None
            elif 'bounds' in param_config:
                frozen = False
                bounds = param_config['bounds']
                value = None
            else:
                raise Exception(
                    'Parameter config has to have bounds or value: %s'
                    % param_config)

            if param_config['type'] == 'global':
                modulation_params.append(
                    ephys.parameters.NrnGlobalParameter(
                        name=param_config['param_name'],
                        param_name=param_config['param_name'],
                        frozen=frozen,
                        bounds=bounds,
                        value=value))
            elif param_config['type'] in ['section', 'range']:
                if param_config['dist_type'] == 'uniform':
                    scaler = ephys.parameterscalers.NrnSegmentLinearScaler()
                elif param_config['dist_type'] in ['exp', 'distance']:
                    scaler = ephys.parameterscalers.NrnSegmentSomaDistanceScaler(
                        distribution=param_config['dist'])
                seclist_loc = ephys.locations.NrnSeclistLocation(
                    param_config['sectionlist'],
                    seclist_name=param_config['sectionlist'])

                name = '%s.%s' % (param_config['param_name'], param_config['sectionlist'])

                if param_config['type'] == 'section':
                    modulation_params.append(
                        ephys.parameters.NrnSectionParameter(
                            name=name,
                            param_name=param_config['param_name'],
                            value_scaler=scaler,
                            value=value,
                            frozen=frozen,
                            bounds=bounds,
                            locations=[seclist_loc]))
                elif param_config['type'] == 'range':
                    modulation_params.append(
                        ephys.parameters.NrnRangeParameter(
                            name=name,
                            param_name=param_config['param_name'],
                            value_scaler=scaler,
                            value=value,
                            frozen=frozen,
                            bounds=bounds,
                            locations=[seclist_loc]))
            else:
                raise Exception(
                    'Param config type has to be global, section or range: %s' %
                    param_config)

        return modulation_params

        
def define_parameters(parameter_config=None, parameter_id=None):
        """Define parameters"""

        assert (parameter_config is not None)

        # print("Using parameter config: " + parameter_config)

        try:
            param_configs = json.load(open(parameter_config))
        except:
            import traceback
            tstr = traceback.format_exc()
            print(tstr)
            import pdb
            pdb.set_trace()

        parameters = []

        if type(param_configs[0]) == list:
            # If it was a dict, then we have one parameterset,
            # if it was a list we have multiple parametersets, pick one.

            assert parameter_id is not None, \
                "Multiple parametersets require parameterID set"

            num_params = len(param_configs)

            assert num_params > parameter_id
            
            param_configs = param_configs[parameter_id]


        for param_config in param_configs:
            if 'value' in param_config:
                frozen = True
                value = param_config['value']
                bounds = None
            elif 'bounds' in param_config:
                frozen = False
                bounds = param_config['bounds']
                value = None
            else:
                raise Exception(
                    'Parameter config has to have bounds or value: %s'
                    % param_config)

            if param_config['type'] == 'global':
                parameters.append(
                    ephys.parameters.NrnGlobalParameter(
                        name=param_config['param_name'],
                        param_name=param_config['param_name'],
                        frozen=frozen,
                        bounds=bounds,
                        value=value))
            elif param_config['type'] in ['section', 'range']:
                if param_config['dist_type'] == 'uniform':
                    scaler = ephys.parameterscalers.NrnSegmentLinearScaler()
                elif param_config['dist_type'] in ['exp', 'distance']:
                    scaler = ephys.parameterscalers.NrnSegmentSomaDistanceScaler(
                        distribution=param_config['dist'])
                seclist_loc = ephys.locations.NrnSeclistLocation(
                    param_config['sectionlist'],
                    seclist_name=param_config['sectionlist'])

                name = '%s.%s' % (param_config['param_name'],
                                  param_config['sectionlist'])

                if param_config['type'] == 'section':
                    parameters.append(
                        ephys.parameters.NrnSectionParameter(
                            name=name,
                            param_name=param_config['param_name'],
                            value_scaler=scaler,
                            value=value,
                            frozen=frozen,
                            bounds=bounds,
                            locations=[seclist_loc]))
                elif param_config['type'] == 'range':
                    parameters.append(
                        ephys.parameters.NrnRangeParameter(
                            name=name,
                            param_name=param_config['param_name'],
                            value_scaler=scaler,
                            value=value,
                            frozen=frozen,
                            bounds=bounds,
                            locations=[seclist_loc]))
            else:
                raise Exception(
                    'Param config type has to be global, section or range: %s' %
                    param_config)

            # import pdb
            # pdb.set_trace()

        return parameters


##############################################################################

def define_morphology(replaceAxon=True, morph_file=None):
    """Define morphology. Handles SWC and ASC."""

    assert (morph_file is not None)

    # print("Using morphology: " + morph_file)

    return ephys.morphologies.NrnFileMorphology(morph_file, do_replace_axon=replaceAxon)


