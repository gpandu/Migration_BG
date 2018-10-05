
import utilities
import queries
from bugzilla_record import bug_record
from jiraClass import jira
from comment import process_comments
from attachment import process_attachment

users = {}
components_result = {}


def process_columns(record):
    #assignee  = utilities.getQueryResult(queries.assignee_name)
    #project_name = utilities.getQueryResultWith(queries.project_name)
    summary = record.summary
    #component = utilities.getQueryResultWith(queries.component_name,record.component_id)
    comments = process_comments(record.bug_id,users)
    attachments = process_attachment(record.bug_id) 
    jira_obj = jira(summary)
    jira_obj.comments = comments
    jira_obj.assignee = users[record.assigned_to]
    jira_obj.components = components_result[record.component_id]
    #jira_obj.user_name = utilities.assignee_result[record.assigned_to]
    jira_obj.bug_severity = jira.process_severity(record.bug_severity,'some default value')
    jira_obj.status = record.bug_status
    jira_obj.priority = jira.process_priority(record.priority,'some default value')
    jira_obj.creation_ts = record.creation_ts.isoformat()
    jira_obj.product_id = record.product_id
    #jira_obj.component_id = record.component_id
    jira_obj.resolution = record.resolution
         
    jira_obj.phase_of_detection = jira.process_record_validation(record.cf_client_phase,'some default value')
    jira_obj.fix_version =   jira.process_record_validation(record.cf_fixes_available,'some default value')   
    jira_obj.test_engineer = users[record.assigned_to]
    jira_obj.issue_type = jira.process_issue_type(record.cf_type,'some default value')
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
        
    jira_obj.browser = jira.process_browser(record.cf_browser,'some default value')     
    jira_obj.os = jira.process_os(record.op_sys,'some default value')

    issue_dict = {
          "project": {"key": "TEST"},
          "summary": summary,
          "description": summary,
          "issuetype": {"name": "Bug"},
          "customfield_10513": "NA",
          "components": [{"name": "test"}],
          "customfield_10503" : {"value": "UAT"},
          "versions": [{"name": "Shatha1"}]
            }

    #jira = jira_client.getJiraClient()
   # new_issue = jira.create_issue(fields=issue_dict)
   # print(new_issue.fields)

def getColumns():
    columns = utilities.readProperty('LOG_ATTRIBUTES','COLUMNS')
    if columns is not None:
        columns = columns.split(',')
    return columns





if __name__ == "__main__":
    get_project = queries.get_project
    get_bugCount = queries.get_bugCount
    query_for_assignee = queries.get_assigne_name
    users = utilities.getAssignee(query_for_assignee)
    query_for_components = queries.fetch_components
    components_result = utilities.getComponents(query_for_components)
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
              process_columns(record)
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