## WiFi password changer for Omada controller

Rental wifi management application simplifies the process of changing passwords remotely. With this app you can easily change a WiFi password, or retrieve the current one for a guest wifi in your rental unit.

You can run it as standalone application or as a docker image.

---

### Running in Docker

Example docker-compose.yml:
```yml
version: '3'

services:
  my_omada:
    image: builder555/wifi_psk_randomizer_omada:latest
    ports:
      - "8700:8000"
    environment:
      - URL=https://192.168.0.100:8043/00000000000000000000000000000000
      - PASSWORD=abc123
      - USERNAME=admin
      - SSID=myssid
```

Required environmental variables:

| Variable | Description | 
|:--------:| ----------- |
|URL| The URL of the Omada controller.* | 
|USERNAME| Account that has access to WiFi credentials | 
|PASSWORD| Password to that account |
|SSID| The network you want to manage |

\* For version 5+ the URL has to contain the controller ID.

---

### Running as standalone application

```bash
# install prerequisites
$ pipenv install

# modify app/omada.cfg with the variables as mentioned above

# run
$ uvicorn app.main:app --host 0.0.0.0 --port 8700
```
---

### Usage

Here's how to use it once the container (or application) is running

```bash
# to get current WiFi password
$ curl http://ip-address:8700/todays-wifi
"WIFI:T:WPA;S:myssid;P:abra3cadabra;;"

# to set a new random WiFi password
$ curl http://ip-address:8700/todays-wifi/reset
"WIFI:T:WPA;S:myssid;P:@xNG?N?K}JjgR@yv;;"
```

---

### Additional Resources
* omada API: https://github.com/ghaberek/omada-api
* fixes for Omada 5: https://www.tp-link.com/us/support/faq/3231/
