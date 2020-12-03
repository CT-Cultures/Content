# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 23:32:35 2019

@author: VSurfacePro3
"""
#%%
import dy_Registration
#from IO_Storage import File
#%%
# Check if Data Files exist, if not, create files
#opener = File()
#dir_root_result = "C:\\Users\\VSurfacePro3\\Desktop\\Degree Classes\\Trade University\\CTAI\\R_looklook\\results"
#filename_links_of_publications = "PubThreatricalRegistration_links_allpublishes"
#filename_links_of_registrations = "PubThreatricalRegistration_links_allregistrations"
#filename_contents_of_registrations = "PubTheatricalRegistration_info_allregistrations"
#GR = MovieCN.GetRegistration()

# Update and Save Registration
#links_of_publications = dyreg.links_of_publications()
#links_of_registrations = dyreg.links_of_registrations()
#contents_of_registrations= dyreg.contents_of_registrations()

dyreg = dy_Registration.Registration()
dyreg.update_records(save_update=True)

#UR = MovieCN.update_records()
#links_of_newregpub = UR.links_of_newpublications()
#links_of_newreg = UR.links_of_newregistrations()
#contents_of_newreg = UR.contents_of_newregistrations(savefile=True)

# Update and Save Release
#URS = MovieCN.UpdateRelease()
#links_of_newrelpub = URS.links_of_newpublications()
#contents_of_newrelpub = URS.contents_of_newpublications(savefile=True)
