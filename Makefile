loaddata:
	python manage.py loaddata venues
	python manage.py loaddata country
	python manage.py loaddata city
	python manage.py loaddata category
	python manage.py loaddata event
	python manage.py loaddata promoCode
	python manage.py loaddata like

	python manage.py loaddata basket
	python manage.py loaddata courier
	python manage.py loaddata location
	python manage.py loaddata promotion
	python manage.py loaddata order
	python manage.py loaddata session

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