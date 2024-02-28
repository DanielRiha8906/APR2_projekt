DOCKER:
        docker build -t apr:sem .
        docker-compose up --build

        (ps: nekdy pripojeni na volume trochu dele trva, reload vzdy pomuze...)

overeni cachovani pres redis - redis comander:
    localhost:8081
    user: root
    passw: qwerty

pristup do databaze (volitelne) - mongodbcompass:
    admin:admin