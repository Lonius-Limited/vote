UPDATE `tabVoter Register Member` a , `tabInstitution Member` b 
set a.branch = b.electoral_district WHERE a.parent ='V-REG-07282' AND a.system_id = b.name and a.name!='' and b.name!='';