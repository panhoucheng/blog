#Jekyll on Docker
---
## How To Run
Please use `docker-compose up` start run.

## How To setup auto update env.
1. run ``` python webhook.py``` to start webhook server and expose port.
2. log in to git server and set push to trigger notice webhook update posts.

## How to use
1. clone repository to local disk
2. write post and save to ```blog/_posts/xxx.md
3. commit and push changes.
4. wait a minute or so then check website.