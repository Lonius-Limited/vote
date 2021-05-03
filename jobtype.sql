DELETE FROM  `tabScheduled Job Type` WHERE name ='bulk_sms_switch';

INSERT INTO `tabScheduled Job Type` (`name`,method,frequency,cron_format,create_log)
VALUES('bulk_sms_switch','vote.vote.doctype.bulk_messaging.handler.handle_sms_cron','Cron','* * * * * *',1);
