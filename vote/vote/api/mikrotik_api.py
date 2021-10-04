from netmiko import ConnectHandler
MT1= dict(device_type='mikrotik_routeros', ip='41.89.186.67',username='jkbore',password='Technology@1')
# all_devices = [MT1]
net_connect = ConnectHandler(**MT1)


print(net_connect.__dict__)

# bench new-site wire.bizpok.com --admin-password 'velo@2020' --mariadb-root-username erpuser --mariadb-root-password 'velo@2020'
# sudo certbot delete --cert-name portal.nakuruentandaudiology.com