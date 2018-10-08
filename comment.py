# -*- coding: utf-8 -*-
import queries
import utilities
import attachment
import pre_hooks
 
class comment(object):
    
    def __init__(self,comment_id):
        self.comment_id = comment_id
        
    def add_date(self,date_time):
        self.c_date = date_time.isoformat()


def process_comments(bug_id,jira,issue):
    comments = utilities.getResultSetWith(queries.get_comments,bug_id)
    for com in comments:
        cmnt =  comment(com[0])
        cmnt.who = com[1]
        cmnt.add_date(com[2])
        cmnt.text = com[3]
        cmnt.is_private = com[4]
        cmnt.attach = com[5]
        user_id = get_user(cmnt.who,jira)
        final_comment= "Originally commented by [~"+user_id+"] on "+ cmnt.c_date +".\n\n"+cmnt.text
        if(cmnt.attach is not None):
            (filename,descr) = utilities.getQueryResultWith(queries.get_attachs,cmnt.attach)
            if(filename is not None):
                content = utilities.getQueryResultWith(queries.get_attachs,cmnt.attach)
                #content, filename = attachment.get_attachment(cmnt.attach)
                final_comment = "Originally attached by [~"+user_id+"] on "+ cmnt.c_date+".\n [^"+filename+"] \n"+descr +"\n\n"
                jira.add_attachment(issue=issue, attachment=attachment, filename=filename)
        #jira.add_comment(issue, final_comment)

def get_user(user_id,jira):        
    try:
        users_map,users = pre_hooks.get_existing_users(jira)
        default_users = pre_hooks.get_default_users()
        user = users[user_id]      
        if(user is None):
            user_id = default_users[0]
        else:
            user_id = user if users_map[user] == 'Y' else default_users[0]
    except Exception as e:
        user_id = default_users[0]
    return user_id