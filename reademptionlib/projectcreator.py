import json
import os
import sys
import Bio
import matplotlib
import pandas as pd
import pysam


class ProjectCreator(object):
    def create_root_folder(self, project_name):
        """Create the root folder of a new project with the given name.

        Arguments:
        - `project_name`: Name of the project root folder

        """
        if not os.path.exists(project_name):
            os.mkdir(project_name)
        else:
            sys.stderr.write(
                'Cannot create folder "%s"! File/folder with '
                "the same name exists already.\n" % project_name
            )
            sys.exit(2)

    def create_subfolders(self, subfolders):
        """Create required subfolders in the given folder.

        Arguments:
        - `project_name`: Name of the project root folder

        """
        for folder in subfolders:
            if not os.path.exists(folder):
                os.mkdir(folder)

    def create_config_file(
        self, config_file_path: str, species: list
    ) -> None:
        """
        Creates a json text file that contains the species information
        for each species, which is:
        - a name for the species' subfolders
        - a display name for figures and output files
        :param config_file_path: path of json file that holds
         the species information and other configurations
        :param species: a list containing species information give by the user
         when creating a new project via the parameter --species
        """
        species_dict = self._get_species_dictionary(species)
        with open(config_file_path, "w") as config_json:
            json.dump(species_dict, config_json)

    def _get_species_dictionary(self, species: list) -> dict:
        """
        makes a dictionary from the species argument list
        :param species: a list containing species information give by the user
         when creating a new project via the parameter --species
        :return: dictionary containing the species sub folder name as keys and
        the species display name as values
        """
        species_dict = {}
        for sp in species:
            sub_folder_name, display_name = sp.split("=")
            species_dict[sub_folder_name] = display_name
        return species_dict

    def create_version_file(self, version_file_path, version):
        python_version = sys.version.replace("\n", " ")
        with open(version_file_path, "w") as fh:
            fh.write(f"READemption version: {version}\n")
            fh.write(f"Python version: {python_version}\n")
            fh.write(f"Biopython version: {Bio.__version__}\n")
            fh.write(f"pysam version: {pysam.__version__}\n")
            fh.write(f"matplotlib version: {matplotlib.__version__}\n")
            fh.write(f"pandas version: {pd.__version__}\n")
