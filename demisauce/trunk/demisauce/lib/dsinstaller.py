"""
Creates custom info for ini files for Demisauce
"""
import logging

from paste.script.appinstall import Installer


class DemisauceInstaller(Installer):
    use_cheetah = False

    def write_config(self, command, filename, vars):
        """
        Creates any local information for Demisauce that needs to 
        be included in the ini file
        
        Creates the custom api key 
        """
        import sha, random
        key = sha.new(str(random.random())).hexdigest()
        vars['demisuace_apikey'] = key
        vars['demisauce_file'] = filename.split('.')[0]
        # go back to normal processor
        Installer.write_config(self, command, filename, vars)
