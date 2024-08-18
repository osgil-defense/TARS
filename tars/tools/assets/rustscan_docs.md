# RustScan Documentation

## Updated

April 28, 2024

## About

Here are some things you may want to do with RustScan!

## Usage

The help menu can be accessed with `rustscan --help`

### WARNING

By default, RustScan scans 3000 ports per second.

This may cause damage to a server or make it very obvious you are scanning the server, thus triggering an unwelcome response like having your IP address blocked.

There are 2 ways to deal with this:

1. Decrease batch size:
   `rustscan -b 10` will scan 10 ports at a time, each with a default timeout of 1000 (1 second). So, the maximum batch duration can be longer than the timeout: however long it takes to start (and finish processing) all the scans in the batch.
2. Increase timeout:
   `rustscan -T 5000` means RustScan will wait for a response on a port for up to 5 seconds.

You can use both of these at the same time, to make it as slow or as fast as you want. A fun favourite is 65535 batch size with 1 second timeout. Practically speaking, that translates to getting results from nmap in less than 2 wall clock seconds.

## Multiple IP Scanning

You can scan multiple IPs using a comma separated list like so:

```console
rustscan -a 127.0.0.1,0.0.0.0
```

## Host Scanning

RustScan can also scan hosts, like so:

```console
➜ rustscan -a www.google.com, 127.0.0.1
Open 216.58.210.36:1
Open 216.58.210.36:80
Open 216.58.210.36:443
Open 127.0.0.1:53
Open 127.0.0.1:631
```

## CIDR support

RustScan supports CIDR:

```console
➜ rustscan -a 192.168.0.0/30
```

## Hosts file as input

The file is a new line separated list of IPs / Hosts to scan:

**hosts.txt**

```
192.168.0.1
192.168.0.2
google.com
192.168.0.0/30
127.0.0.1
```

The argument is:

```
rustscan -a 'hosts.txt'
```

## Individual Port Scanning

RustScan can scan individual ports, like so:

```console
➜ rustscan -a 127.0.0.1 -p 53
53
```

## Multiple selected port scanning

You can input a comma separated list of ports to scan:

```console
➜ rustscan -a 127.0.0.1 -p 53,80,121,65535
53
```

## Ranges of ports

To scan a range of ports:

To run:

```console
➜ rustscan -a 127.0.0.1 --range 1-1000
53,631
```

## Adjusting the Nmap arguments

RustScan, at the moment, runs Nmap by default.

You can adjust the arguments like so:

```console
rustscan -a 127.0.0.1 -- -A -sC
```

To run:

```console
nmap -Pn -vvv -p $PORTS -A -sC 127.0.0.1
```

## Random Port Ordering

If you want to scan ports in a random order (which will help with not setting off firewalls) run RustScan like this:

```console
➜ rustscan -a 127.0.0.1 --range 1-1000 --scan-order "Random"
53,631
```
