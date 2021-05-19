DELETE FROM  `tabScheduled Job Type` WHERE name ='post_to_blockchainv2';

INSERT INTO `tabScheduled Job Type` (`name`,method,frequency,cron_format,create_log)
VALUES('post_to_blockchainv3','vote.utils.election_details.handle_unposted_ballots','Cron','*/15 * * * *',1);
