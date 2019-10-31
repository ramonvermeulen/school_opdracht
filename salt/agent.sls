agent:
  pkg.installed:
    - pkgs:
      - docker
      - docker-compose
      - git
  cmd.run:
    - name: |
        systemctl start docker
        systemctl enable docker
        cd /srv
        rm -rf school_opdracht
        git clone -b develop https://www.github.com/ramonvermeulen/school_opdracht.git
        cd school_opdracht/src
        export EXTERNAL_IP=`hostname -I`
        docker-compose build agent
        docker-compose up -d agent
