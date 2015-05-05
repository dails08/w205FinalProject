import boto

boto.config.add_section('Boto') 
boto.config.set('Boto','http_socket_timeout','300') 
