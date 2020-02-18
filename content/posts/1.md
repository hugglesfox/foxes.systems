# Docker, Traefik and Tor Hidden services
*September 2, 2018*

[Traefik](https://traefik.io/) is amazing! I use it all the time to manage my docker
web services. Although I've been trying to move more things over to use tor for increased
security and privacy so I wanted to have all my services as tor hidden services. A brief DuckDuckgo search
doesn't come up with anything about using hidden services with traefik so here we go!

The end goal will be to create

`Internet <-(onion)-> Traefik <-(onion)-> Tor <-(http)-> Nextcloud`


This won't be a tutorial, mostly just me rambling, so
I assume you already have experience with traefik, docker-compose and tor.

For the example I'll use Nextcloud as the service to torify.
So here's the `docker-compose.yml`

```yaml
version: "3"

services:
  reverse-proxy:
    image: traefik
    command: --api --docker
    ports:
      - "80:80"
      - "8080:8080"
    networks:
      - tor_net
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock

  nextcloud_tor:
    image: registry.gitlab.com/huggles/tor-docker:latest
    restart: always
    networks:
      - tor_net
    volumes:
      - /home/volumes/tor/:/etc/tor/
      - /home/volumes/tor/services/:/var/lib/tor/
    labels:
      - "traefik.backend=nextcloud_tor"
      - "traefik.enable=true"
      - "traefik.frontend.rule=Host:insert_onion_url_here.onion"
      - "traefik.port=80"
      - "traefik.protocol=http"

  nextcloud:
    image: nextcloud
    restart: always
    networks:
      - tor_net
    labels:
      - "traefik.backend=nextcloud"
      - "traefik.enable=true"
      - "traefik.frontend.rule=Host:insert_clearnet_url_here"
      - "traefik.port=80"
      - "traefik.protocol=http"

networks:
  tor_net:
    external: true
```

So whats happening above is when traefik gets a request to the onion url and will
foward it to the nextcloud_tor container to get detorified. The nextcloud container
can still accept clear net traffic from traefik as normal by replacing `insert_clearnet_url_here` with your url.

Note that nextcloud_tor must use http as currently letsencyrpt doesn't
support hidden services. [Although this isn't a problem when it comes to security.](https://riseup.net/en/security/network-security/tor/onionservices-best-practices#ssltls-isnt-necessary)

You also might notice that I created my own image for nextcloud_tor. Armhf builds are also available and can be found [here](https://gitlab.com/huggles/tor-docker)
although all it is, is a debian buster base with tor installed.

Next tor needs to be configured. With the docker-compose file above the torrc file
can be found at `/home/volumes/tor/torrc`. If torrc doesn't exist then create it.
Just make sure it looks like something below.

```
HiddenServiceDir /var/lib/tor/http
HiddenServiceVersion 3
HiddenServicePort 80 nextcloud:80
```

So when the tor container first starts it will create a onion URL which can be found
by `cat /home/volumes/tor/services/http/hostname`, if you used the same tor configuration and
docker-compose file. This URL then needs to be given to traefik, so replace `insert_onion_url_here.onion`
with the onion URL. Note that if the `hs_ed25519_public_key` and `hs_ed25519_secret_key` get deleted then
the URL will change and so you would have to tell traefik about the new URL.

That should be about all for now, stay safe on the internet and I'll 'see' you next time!

Hayden
