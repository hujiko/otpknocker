# OTP Knocker

Implement "portknocking" in HAproxy by using OTP-Codes.

## How it works

HAProxy will hold a table in memory of all IPs that are successfully authenticated.

When trying to access the protected backend, HAProxy will deny your request unless your IP is marked as "whitelisted".

While using the authentication backend, HAProxy will wait for the backend server to send a specific response header to inform HAProxy that the authentication was successful.

## HAProxy configuraton

```
frontend http
  bind *:80
  bind *:443 ssl crt-list /etc/haproxy/certs/all.txt alpn h2,http/1.1 # Change this to point to your SSL certificates

  use_backend otpknocker if { ssl_fc_sni knock.example.com }
  use_backend secretStuff if { ssl_fc_sni secret.example.com }

backend secretStuff
  http-request track-sc0 src table table-ip-whitelist if TRUE # We might not need this line.
  acl authenticated src_get_gpc0(table-ip-whitelist) gt 0     # Create an ACL that's only true once the IP is authenticated

  http-request deny if !authenticated # Deny the request unless the IP is authenticated

  server mysecretBackendServer 10.10.10.55:80 # Add your backend servers here

backend table-ip-whitelist # This backend only exists to hold the stick table
  stick-table type ip size 1m expire 86400s store gpc0 # Change 86400s to the expiration of whitelisted IPs

backend otpknocker
  server otpknocker 192.168.5.10:8000 # Put the IP and Port of the python app here
  http-request track-sc0 src table table-ip-whitelist
  http-response sc-inc-gpc0(0) if { res.hdr(Authentication-Success) -m str "true" } # Once the app return the Authentication-Success header, the client IP will be whitelisted
```

## OTP Knocker configuration

OTP Knocker can run in a Docker container. A `Dockerfile` and `docker-compose.yaml` is included.

The OTP-Secret needs to be injected as `OTP_SECRET` environment variable. A sample value is provided but should be changed before usage!
