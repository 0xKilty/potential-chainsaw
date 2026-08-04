Verify certs
```bash
cat cert2.pem cert3.pem > intermediates.pem

openssl verify \
    -verbose \
    -show_chain \
    -CAfile cert4.pem \
    -untrusted intermediates.pem \
    cert1.pem
```

Custom verify callback
```
SSL_CTX_set_verify(ctx, SSL_VERIFY_PEER, verify_callback);
```
```
int verify_callback(int preverify_ok, X509_STORE_CTX *x509_ctx)
{
    int err = X509_STORE_CTX_get_error(x509_ctx);
    int depth = X509_STORE_CTX_get_error_depth(x509_ctx);
    X509 *cert = X509_STORE_CTX_get_current_cert(x509_ctx);

    char subject[256];
    X509_NAME_oneline(X509_get_subject_name(cert), subject, sizeof(subject));

    printf("depth=%d subject=%s\n", depth, subject);
    printf("preverify=%d error=%d (%s)\n",
           preverify_ok,
           err,
           X509_verify_cert_error_string(err));

    return preverify_ok;
}
```

Only add the last certificate in the chain as the trusted root CA.

Check if the cert is the CA
```
int is_ca = X509_check_ca(cert);

printf("is_ca = %d\n", is_ca);
```

Consider using `fullchain.pem` instead of just `cert.pem` on the server side.
