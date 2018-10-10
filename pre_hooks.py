# -*- coding: utf-8 -*-
from jira_client import getJiraClient
import utilities
from utilities import readProperty

def check_component(key, jira_components):
    for comp in jira_components:
        if(comp.name == key):
            return True
    return False    
    
    
def add_components(project_name,jira):
    components = utilities.getComponents()
    jira_components = jira.project_components(project_name) 
    for key in components:
        if(check_component(components[key],jira_components)):
            continue
        jira.create_component(components[key], project_name, description="Migration related component", leadUserName=None, assigneeType=None, isAssigneeTypeValid=False)



 
def get_default_values():
    return readProperty("DEFAULT_FIELD_VALUES", "SEVERITY"),readProperty("DEFAULT_FIELD_VALUES", "PRIORITY"),readProperty("DEFAULT_FIELD_VALUES", "PHASE_OF_DETECTION"),readProperty("DEFAULT_FIELD_VALUES", "FIX_VERSION"),readProperty("DEFAULT_FIELD_VALUES", "ISSUE_TYPE") ,readProperty("DEFAULT_FIELD_VALUES", "BROWSER"),readProperty("DEFAULT_FIELD_VALUES", "OS")     
        

#users_map = get_existing_users()
        
