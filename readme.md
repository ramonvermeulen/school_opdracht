# Installation guide

## saltstack

Be sure to have saltstack master configured using their quickstart guide.

#### Agent:
Use the kickstart file ks.cfg for automatically installing the minions.

1. use `salt-key -L` to list your invited minion keys and `salt-key -A $key` to accept the minion key.
2. be sure to have the `/salt/agent.sls` on your server in the `/srv/salt/` directory
3. use `salt '*' state.apply agent` to build and start the agent container on all salt minions

#### Management
Use the steps explained in Docker compose -> management

## docker compose

Be sure to have `docker`, `docker-compose` and `git` installed on your server.

#### Agent:

1. clone the git repo using `git clone https://www.github.com/ramonvermeulen/school_opdracht`
2. edit the `.env` file and set `DESTINATION_HOST` to your management script server
3. cd to the `/src` folder inside the cloned git repo
4. use the command `docker-compose build agent && docker-compose up -d agent`
5. check if the agent script is running fine using `docker ps` and `docker logs $container_id`

#### Management
1. clone the git repo using `git clone https://www.github.com/ramonvermeulen/school_opdracht`
2. make a `/data` folder on the server using `mkdir /data` and give permissions using `chmod 775 /data`
3. cd to the `src` folder inside the cloned git repo
4. use the command `docker-compose build management && docker-compose up -d management`
5. check if the management script is running fine by cURL-ing `localhost:8081/cgi-bin/management.py`