set -x
./scripts/down.sh

if [ ! -f .env ]
then
    cp env.sample .env
fi

docker compose up --build
sudo chown -R $USER:$USER  out/