# -*- coding: utf-8 -*-
import queries
import utilities
import jira_client
import attachment
 
class comment(object):
    
    def __init__(self,comment_id):
        self.comment_id = comment_id
        
    def add_date(self,date_time):
        self.c_date = date_time.isoformat()


def process_comments(bug_id,users):
    coms = utilities.getResultSetWith(queries.get_comments,bug_id)
    comments = []
    for com in coms:
        cmnt =  comment(com[0])
        cmnt.who = users[com[1]]
        cmnt.add_date(com[2])
        cmnt.text = com[3]
        cmnt.is_private = com[4]
        cmnt.attach = com[5]
        final_comment= "Originally commented by"+cmnt.who+"on"+ cmnt.c_date+".\n\n"+cmnt.text
        if(cmnt.attach is not None):
            descr = utilities.getQueryResultWith(queries.get_attachs,cmnt.attach)
            content, filename = attachment.get_attachment(cmnt.attach)
            final_comment = "Originally attached by"+cmnt.who+"on"+ cmnt.c_date+".\n"+filename+"\n"+descr +"\n\n"
            jira = jira_client.getJiraClient()
            issue = jira.issue('TEST-3726')
            jira_client.add_attachment(issue=issue, attachment=attachment, filename=filename)
        jira.add_comment(issue, final_comment, public = True if cmnt.is_private is not 0 else False)
            
        jira = jira_client.getJiraClient()
    return comments