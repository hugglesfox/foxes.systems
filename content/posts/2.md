# Host all the Hidden Services with Traefik
*November 16, 2018*

This is a follow up to the last post which introduces the idea of using Docker,
Tor and Traefik to host a tor hidden service which can be found [here](https://insert_url_here).
Although the last post didn't cover the use case of wanting to host multiple hidden services.

Again this is just ramblings not a tutorial so you should already have experience
with Docker, docker-compose, Traefik and tor.

So just like before we want to make our Nextcloud container a hidden service although
this time I also what to make my website a hidden service.

So here is the docker-compose.yml from last time with the addition my beautiful Nginx hello world website.

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

  website:
    image: nginx
    restart: always
    networks:
      - tor_net
    labels:
      - "traefik.backend=website"
      - "traefik.enable=true"
      - "traefik.frontend.rule=Host:insert_clearnet_url_here"
      - "traefik.port=80"
      - "traefik.protocol=http"

networks:
  tor_net:
    external: true
```

And the torrc

```
HiddenServiceDir /var/lib/tor/http
HiddenServiceVersion 3
HiddenServicePort 80 nextcloud:80
```

So how can we go about doing torifing both services?

Traefik has a concept called [segments](https://docs.traefik.io/configuration/backends/docker/#on-containers-with-multiple-ports-segment-labels)
which allows the container to have a different frontend rule for different ports.
So we will tell tor to host each service on a different port, Nextcloud can have 8080
and Nginx will be 80. Then we can make the tor container have 2 segments and get
traefik to route all requests for `insert_onion_url_here.onion` to port 80 of the
tor container and `nextcloud.insert_onion_url_here.onion` to port 8080 of the tor container.

The revised `docker-compose.yml` using segments:

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

  tor:
    image: registry.gitlab.com/huggles/tor-docker:latest
    restart: always
    networks:
      - tor_net
    volumes:
      - /home/volumes/website_tor/:/etc/tor/
      - /home/volumes/tor/services/:/var/lib/tor/
    labels:
      - "traefik.enable=true"
      - "traefik.website.backend=website_tor"
      - "traefik.website.frontend.rule=Host:insert_onion_url_here.onion"
      - "traefik.website.port=80"
      - "traefik.website.protocol=http"
      - "traefik.nextcloud.backend=nextcloud_tor"
      - "traefik.nextcloud.frontend.rule=Host:nextcloud.insert_onion_url_here.onion"
      - "traefik.nextcloud.port=8080"
      - "traefik.nextcloud.protocol=http"

  nextcloud:
    image: nextcloud
    restart: always
    networks:
      - tor_net
    labels:
      - "traefik.backend=nextcloud"
      - "traefik.enable=true"
      - "traefik.frontend.rule=Host:nextcloud.insert_clearnet_url_here"
      - "traefik.port=80"
      - "traefik.protocol=http"

  website:
    image: nginx
    restart: always
    networks:
      - tor_net
    labels:
      - "traefik.backend=website"
      - "traefik.enable=true"
      - "traefik.frontend.rule=Host:insert_clearnet_url_here"
      - "traefik.port=80"
      - "traefik.protocol=http"

networks:
  tor_net:
    external: true
```

And the corresponding `torrc`:

```
HiddenServiceDir /var/lib/tor/http
HiddenServiceVersion 3
HiddenServicePort 80 website:80
HiddenServicePort 8080 nextcloud:80
```

Thats all there us to it! So expand the tor network and increase privacy and
security for your users with tor hidden services with help from Traefik.

That should be about all for now, stay safe on the internet and I'll 'see' you next time!

Hayden (aka Huggles)
