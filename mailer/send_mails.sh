#!/bin/bash

python mailer.py \
    "rcvrs.txt" \
    'This is subject' \
    -b 'mail_body.txt' # -a 'attachment1.jpg' 'attachment2.jpg' 'attachment3.pdf'
