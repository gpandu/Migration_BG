
class jira_record(object):
  
     def __init__(self, summary):
         self.summary = summary

     def process_record_validation(self,bugzila_value,default_value):
        if(bugzila_value!=None and bugzila_value!='---'):
            jira_value=bugzila_value
        else:
            jira_value=default_value
        
        return jira_value
    
     def process_issue_type(self,bugzila_record,defalut_value):
        if(bugzila_record=='Defect'):
            issue_type = 'Bug'
        elif(bugzila_record=='Change Request'):
            issue_type = 'Improvement'
        else:
            issue_type = 'Bug'
        return issue_type
    
     def process_browser(self,bugzila_record,default_value):
         if('IE' is bugzila_record):
             browser = 'Internet Explorer'
         elif('FireFox' is bugzila_record):
            browser = 'Mozila FireFox'
         elif('chrome' is bugzila_record):
            browser = 'Google Chrome'
         else :
            browser = default_value
         return browser
     
     def process_os(self,bugzila_record,default_value):
        if(bugzila_record=='None'):
            os ='Others'
        elif(bugzila_record=='All'):
            os = 'All'
        elif('Windows' is bugzila_record):
            os = 'Windows'
        elif('RHEL' is bugzila_record):
            os = 'Linux'
        elif('Sun' is bugzila_record):
            os = 'Solaris Sparc'
        else :
            os = default_value
        return os
    
     def process_severity(self,bugzila_record,default_value):
         if(bugzila_record=='major'):
             severity = 'Major'
         elif(bugzila_record == 'minor' or bugzila_record == 'normal'):
             severity = 'Normal'
         elif(bugzila_record == 'critical'):
             severity = 'Critical'
         elif(bugzila_record == 'blocker'):
             severity = 'Blocker'
         elif(bugzila_record == 'trivial'):
             severity = 'Trivial'
         else:
             severity ='some deafult value'
         return severity
     
     def process_priority(self,bugzila_record,default_value):
        if(bugzila_record=='P1'):
            priority = 'P1 - Critical'
        elif(bugzila_record == 'P2'):
            priority = 'P2 - High'
        elif(bugzila_record == 'P3'):
            priority = 'P3 - Normal'
        elif(bugzila_record == 'P4'):
            priority = 'P4 - Minority/Request'
        elif(bugzila_record == 'P5'):
            priority = 'P5 - Review Priority'
        else:
            priority = 'Medium'
        return priority
        
    
    
    
    