# Anthe - performance testing playground for bots
Using Roman to test performance of multiple bots.

## Deployment and runtime
The docker image is deployed to docker hub as `lukaswire/anthe`. 
To run the instance one needs to set following env variables:
```bash
# URL of roman
ROMAN_URL=http://proxy.services.zinfra.io
# Bearer token which is send by Roman to the bot
ROMAN_TOKEN=<token> 
```
