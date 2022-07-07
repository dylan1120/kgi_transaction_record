#!/usr/bin/env bash



docker buildx build --platform linux/amd64 -t gcr.io/tsaitung-dev/kgi_transaction_record .

