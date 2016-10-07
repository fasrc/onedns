# OneDNS
Dyanmic DNS for OpenNebula

## Usage
Global options:
```
$ onedns --help
usage: onedns [-h] [--debug] [-d DOMAIN] [--one-address ONE_ADDRESS]
              [--one-secret ONE_SECRET] [--one-proxy ONE_PROXY]
              {daemon,shell} ...

OneDNS - Dynamic DNS for OpenNebula

positional arguments:
  {daemon,shell}

optional arguments:
  -h, --help            show this help message and exit
  --debug               ONE controller host address
  -d DOMAIN, --domain DOMAIN
                        DNS domain to use
  --one-address ONE_ADDRESS
                        ONE controller host address
  --one-secret ONE_SECRET
                        ONE credentials to use (e.g. user:key)
  --one-proxy ONE_PROXY
                        proxy host to use to connect to ONE controller
```

Run the `daemon` command to kick off onedns:
```
$ onedns daemon --dns-port=53
```
