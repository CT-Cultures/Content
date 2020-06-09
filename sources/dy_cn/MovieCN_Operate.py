# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 23:32:35 2019

@author: VSurfacePro3
"""
#%%
import MovieCN
from IO_Storage import File
from pathlib import Path
#from IO_Storage import File
#%%
GRS = MovieCN.GetRelease()
links_release_publications = GRS.links_of_publications(heading=True)
links_release_info = GRS.contents_of_publications(links_release_publications, heading=True)


opener = File()
dir_root_result = "C:\\Users\\VSurfacePro3\\Desktop\\Degree Classes\\Trade University\\CTAI\\R_looklook\\results"
filename = "Release_w_Reg"
Release_w_reg_import = opener.open_to_list_of_list(Path(dir_root_result + "\\" + filename + ".csv"))

for rel in Release_w_reg_import:
    rel[7] = rel[7].lstrip(' ').rstrip(' ')

opener.write_to_cvs_wbk(Release_w_reg_import, dir_root_result, filename)


# Check if Data Files exist, if not, create files
#opener = File()
#dir_root_result = "C:\\Users\\VSurfacePro3\\Desktop\\Degree Classes\\Trade University\\CTAI\\R_looklook\\results"
#filename_links_of_publications = "PubThreatricalRegistration_links_allpublishes"
#filename_links_of_registrations = "PubThreatricalRegistration_links_allregistrations"
#filename_contents_of_registrations = "PubTheatricalRegistration_info_allregistrations"
#GR = MovieCN.GetRegistration()

# Update and Save Registration
#UR = MovieCN.UpdateRegistration()
#links_of_newregpub = UR.links_of_newpublications()
#links_of_newreg = UR.links_of_newregistrations()
#contents_of_newreg = UR.contents_of_newregistrations(savefile=True)

# Update and Save Release
#URS = MovieCN.UpdateRelease()
#links_of_newrelpub = URS.links_of_newpublications()
#contents_of_newrelpub = URS.contents_of_newpublications(savefile=True)
