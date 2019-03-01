Auto adding OTRS Ticket number to Zabbix ACK

Few steps:
1) Create e-mail box for zabbix to recieve mail from OTRS
2) In zabbix action conf you must create action to send email to otrs and add macro {EVENT.ID} to action subject
3) At this action create another step with "Remore command" operation type
4) Custum script must look like this - python /home/zabbix/otrs-zabbix.py {EVENT.ID}
