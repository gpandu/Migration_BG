
import utilities
import queries
from bugzilla_record import bug_record
from jira_class import jira_record
from comment import process_comments
from attachment import process_attachment
import jira_client
import pre_hooks

users = {}
components_result = {}
users_map = {}
default_users = ()


def process_columns(record,jira):
    project_name = utilities.readProperty("Projects", "Destination_Project")
    #assignee  = utilities.getQueryResult(queries.assignee_name)
    #project_name = utilities.getQueryResultWith(queries.project_name)
    summary = record.summary
    #component = utilities.getQueryResultWith(queries.component_name,record.component_id)
    jira_obj = jira_record(summary)
    try:
        user = users[record.assigned_to]      
        if(user is None):
            jira_obj.assignee = default_users[0]
        else:
            jira_obj.assignee = user if users_map[user] == 'Y' else default_users[0]
    except Exception as e:
        jira_obj.assignee = default_users[0]
        
    jira_obj.components = components_result[record.component_id]
    #jira_obj.user_name = utilities.assignee_result[record.assigned_to]
    jira_obj.bug_severity = jira_obj.process_severity(record.bug_severity,'some_default_value')
    jira_obj.status = record.bug_status
    jira_obj.priority = jira_obj.process_priority(record.priority,'some_default_value')
    jira_obj.creation_ts = record.creation_ts.isoformat()
    jira_obj.product_id = record.product_id
    #jira_obj.component_id = record.component_id
    jira_obj.resolution = record.resolution
         
    jira_obj.phase_of_detection = jira_obj.process_record_validation(record.cf_client_phase,'UAT')
    jira_obj.fix_version =   jira_obj.process_record_validation(record.cf_fixes_available,'some_default_value')   
    jira_obj.test_engineer = default_users[2]
    jira_obj.issue_type = jira_obj.process_issue_type(record.cf_type,'some_default_value')
    jira_obj.test_caseid = record.cf_testcaseid        
    jira_obj.build = record.cf_build
    if(record.estimated_time!=None):
        jira_obj.estimated_time = utilities.formattime(record.estimated_time)
    else:
        jira_obj.estimated_time = record.record.estimated_time
    if(record.remaining_time != None):
        jira_obj.remaining_estimate = utilities.formattime(record.remaining_time)
    else:
        jira_obj.remaining_estimate = record.remaining_time
    if(record.deadline!=None):    
        jira_obj.due_date = record.deadline.isoformat()
        
    jira_obj.browser = jira_obj.process_browser(record.cf_browser,'some_default_value')     
    jira_obj.os = jira_obj.process_os(record.op_sys,'some_default_value')

    issue_dict = {
          "project": {"key": project_name},
          "summary": summary,
          "description": summary,
          "issuetype": {"name": jira_obj.issue_type},
          "customfield_10513": jira_obj.test_caseid,
          "components": [{"name": jira_obj.components}],
          "customfield_10503" : {"value": jira_obj.phase_of_detection},
          "versions": [{"name": "Wave 1"}],
          "priority":{"name": jira_obj.priority},
          "customfield_10300" : {"value": jira_obj.bug_severity},
          "customfield_10601": {"value": default_users[0]}  
            }
    
    
    #new_issue = jira.create_issue(fields=issue_dict)
    new_issue = jira.issue('TPFWD-2')
    jira.assign_issue(new_issue, jira_obj.assignee)
    process_comments(record.bug_id,jira,new_issue)
   
   # print(new_issue.fields)

def getColumns():
    columns = utilities.readProperty('LOG_ATTRIBUTES','COLUMNS')
    if columns is not None:
        columns = columns.split(',')
    return columns





if __name__ == "__main__":
    jira = jira_client.getJiraClient()
    get_project = queries.get_project
    get_bugCount = queries.get_bugCount
    default_users = pre_hooks.get_default_users()
    #users = utilities.get_users() 
    users_map,users = pre_hooks.get_existing_users(jira)
    components_result = utilities.getComponents()
    project_name = utilities.getQueryResult(get_project)
    bug_count = utilities.getQueryResult(get_bugCount)
    print(bug_count)
    get_bugIds = queries.get_bugIds
    bug_ids = utilities.getQueryResultSet(get_bugIds)
    i = 1
    for bug in bug_ids:
        try:
          connection = utilities.getConnection()
          cursor = connection.cursor()
          cursor.execute(queries.bug_details,(bug,))
          for bug_details in cursor:
              record = bug_record(bug_details[0])
              record.create_record(bug_details)
              print(record.bug_id)
              print(record.summary)
              process_columns(record,jira)
        except Exception as e:
            print('error occured while executing query {}'.format(e))
            break
        finally:
            cursor.close()
            connection.close()
        if(i>=1):
            break
        i+=1
    



#file = open('logs.csv','a')
#file.write('#Project Name:{} \n'.format(project_name))
#file.write('#Total Bugs count:{}\n'.format(bug_count))            
#columns = getColumns()
#df = [(1,2,'abc'),(3,4,'xyz'),(5,6,'wxy')]
#df = pd.DataFrame(data =df, columns= columns[0:3])
#df.to_csv(file)
#file.close()
#print(df)