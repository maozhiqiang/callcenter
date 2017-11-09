
server_ip = '192.168.57.128'
PostgresqlDbConfig = {
   'minconn'   : 1,
   'maxconn'   : 20,
   'host'      : server_ip,
   'database'  : 'tradebook',
   'user'      : 'admin',
   'password'  : 'admin',
   'port'      :  5432,
}

RedisConfig={
    'host'     : server_ip,
    'port'     : 6379,
    'db'       : '10',
    'password' : 'rdszpwd'
}

