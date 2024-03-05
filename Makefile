loaddata:
	python manage.py loaddata Venues
	python manage.py loaddata Country
	python manage.py loaddata City
	python manage.py loaddata Category
	python manage.py loaddata Event
	python manage.py loaddata PromoCode
	python manage.py loaddata Like
	python manage.py loaddata Basket
	python manage.py loaddata Courier
	python manage.py loaddata Location
	python manage.py loaddata Promotion
	python manage.py loaddata Order
	python manage.py loaddata Session

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