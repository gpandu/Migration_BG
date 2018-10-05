
class jira(object):
  
     def __init__(self, summary):
         self.summary = summary

     def process_record_validation(bugzila_value,default_value):
        if(bugzila_value!=None and bugzila_value!='---'):
            jira_value=bugzila_value
        else:
            jira_value=default_value
        
        return jira_value
    
     def process_issue_type(bugzila_record,defalut_value):
        if(bugzila_record=='Defect'):
            issue_type = 'Bug'
        elif(bugzila_record=='Change Request'):
            issue_type = 'Improvement'
        else:
            issue_type = defalut_value
        return issue_type
    
     def process_browser(bugzila_record,default_value):
         if('IE' is bugzila_record):
             browser = 'Internet Explorer'
         elif('FireFox' is bugzila_record):
            browser = 'Mozila FireFox'
         elif('chrome' is bugzila_record):
            browser = 'Google Chrome'
         else :
            browser = default_value
         return browser
     
     def process_os(bugzila_record,default_value):
        if(bugzila_record.op_sys=='None'):
            os ='Others'
        elif(bugzila_record.op_sys=='All'):
            os = 'All'
        elif('Windows' is bugzila_record.op_sys):
            os = 'Windows'
        elif('RHEL' is bugzila_record.op_sys):
            os = 'Linux'
        elif('Sun' is bugzila_record.op_sys):
            os = 'Solaris Sparc'
        else :
            os = default_value
        return os
        
        


class comment(object):
    
    def __init__(self,comment_id):
        self.comment_id = comment_id
        
    def add_comment(self,date_time):
        self.c_date = date_time.isoformat()
        
    
    
    
    