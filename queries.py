# -*- coding: utf-8 -*-

get_project = "select name as project_name from bugs.products where id = '1073'"
get_bugCount = "Select count(*) as bugcount From bugs.bugs Where product_id = '1073'"
get_bugIds = "Select DISTINCT(bug_id) From bugs.bugs Where product_id = '1073'"
bug_details =  "Select * from bugs.bugs where bug_id = %s"
project_name = "select name from products where id = %s"
assignee_name =  "select realname from profiles where userid = %s"
component_name = "select name from components where id = %s and product_id = %s"
get_comments = "select * from bugs.longdescs where bug_id = %s order by comment_id;"
get_assigne_name ="select userid,login_name from bugs.profiles where userid in (select distinct(assigned_to) from bugs.bugs where product_id ='1073')"
fetch_distinct_type = "select distinct(bugs.cf_type) from bugs.bugs where product_id = '1073'"
fetch_cclist = "select userid,login_name from bugs.profiles where userid in(select who from bugs.cc)"