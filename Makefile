mig:
	python3 manage.py makemigrations && python3 manage.py migrate

admin:
	python3 manage.py createsuperuser

run:
	sudo chmod 666 /var/run/docker.sock
	docker start iticket-postgres_service-1


mk:
	docker exec -itu postgres iticket-postgres_service-1 psql -c 'create database iticket_db'

rm:
	docker exec -itu postgres iticket-postgres_service-1 psql -c 'drop database iticket_db'

minio:
	docker run -p 9000:9000 -p 9001:9001 minio/minio server /data --console-address ":9001"