```bash
cat cert2.pem cert3.pem > intermediates.pem

openssl verify \
    -verbose \
    -show_chain \
    -CAfile cert4.pem \
    -untrusted intermediates.pem \
    cert1.pem
```
