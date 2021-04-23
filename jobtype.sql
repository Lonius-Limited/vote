
INSERT INTO `tabScheduled Job Type` (`name`,method,frequency,cron_format,create_log)
VALUES('election_switch','vote.utils.election_details.election_status_switch','Cron','* * * * * *',1);
