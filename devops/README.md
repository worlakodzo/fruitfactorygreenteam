### DevOps Gan Shmuel


## Webhook Installation 

```
sudo apt update
sudo apt install webhook

```


## Webhook Configuration

```

[
    {
      "id": "billing-weight-app",
      "execute-command": "/media/worlako/MAC OSX/REALLY-GREAT-TECH/WORK-SPACE/ganshmuelgreenteam/devops/redeploy-nodejs-app.sh",
      "command-working-directory": "/media/worlako/MAC OSX/REALLY-GREAT-TECH/WORK-SPACE/ganshmuelgreenteam/devops",
      "response-message": "Deployed...",
      "trigger-rule": {
        "and": [
          {
            "match": {
              "type": "payload-hmac-sha256",
              "secret": "123456",
              "parameter": {
                "source": "header",
                "name": "X-Hub-Signature-256"
              }
            }
          },
          {
            "match": {
              "type": "value",
              "value": "refs/heads/main",
              "parameter": {
                "source": "payload",
                "name": "ref"
              }
            }
          }
        ]
      }
    }
  ]

```

### Start webhook

```
webhook -hooks ./hooks.json -hotreload -verbose -http-methods post

```