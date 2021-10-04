import frappe

def execute():
    # INSERT SCHEDULED JOB FOR REQUESTING REQUIRED DRUGS
    # the_job = 'vote.start_scheduled'
    # if not is_job_scheduled(the_job):
    #     # return
    #     doc = frappe.get_doc({"name":"vote.start_scheduled","owner":"Administrator","creation":"2021-05-31 14:36:26.237459","docstatus":0,"stopped":0,"method":"vote.utils.election_details.election_status_switch","frequency":"Cron","cron_format":"*/2 * * * *","create_log":1,"doctype":"Scheduled Job Type"})
    #     doc.insert()
    # the_job = 'vote.ship_voter_card'
    # if not is_job_scheduled(the_job):
    #     doc = frappe.get_doc({"name":"vote.ship_voter_card","owner":"Administrator","creation":"2021-05-31 14:36:26.237459","docstatus":0,"stopped":0,"method":"vote.utils.election_details.dispatch_election_cards","frequency":"Cron","cron_format":"*/2 * * * *","create_log":1,"doctype":"Scheduled Job Type"})
    #     doc.insert()
    the_job = "vote.post_ballot_entries"
    if not is_job_scheduled(the_job):
        doc = frappe.get_doc({"name":"vote.post_ballot_entries","owner":"Administrator","creation":"2021-05-31 14:36:26.237459","docstatus":0,"stopped":0,"method":"vote.utils.election_details.post_ballot_entries","frequency":"Cron","cron_format":"* * * * *","create_log":1,"doctype":"Scheduled Job Type"})
        doc.insert()
   

def is_job_scheduled(the_job):
    return frappe.db.exists('Scheduled Job Type', the_job) 