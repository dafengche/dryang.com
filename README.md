dryang.com
==========

Scalable Django tutorial, jQuery, Celery (RabbitMQ + Redis), Memcached

- web01.dryang.com
  - Apache HTTP server  : SSL terminating reverse proxy server; also serves
                          downloadable files stored on NFS
  - Django

- mw01.dryang.com
  - Celery worker server
  - Memcached           : Cache Celery worker results
  - NFS                 : Storage for downloadable files
  - RabbitMQ            : Broker for Celery
  - Redis               : Backend for Celery

- db01.dryang.com
  - MongoDB
  - PostgreSQL
