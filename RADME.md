# Mongo Blog Backend

Este proyecto es un backend para una aplicación tipo blog
# Diseño
las tecnologias utilizadas son
* FastAPI
* Odmantic
* Minio (Servicio semejante a S3)
* Mongodb
* Oauth con Bearer + JWT

También utiliza Pillow para convertir automaticamente las imagenes de usuario a webp, lo cual permitirá mejor tiempo de respuesta para el usuario y menor consumo de banda ancha.


![Descripción de la imagen](./docs/images/Diagrama%20de%20servicios.png)

Para la base de datos se utilizó el ODM para facilitar su construcción y configuración, asignando los indices correspondientes y las restricciones mediante un endpoint `/configure`

# Configuraciones

Como politicas del bucket seria preferible que el usuario no tenga permisos para mover nada pero que si pueda obtener el recurso desde el bucket directamente dado que se tratan de imagenes de perfil y articulos que no son información sensible.

## Minio
```sh
docker run -d -p 9000:9000 -p 9001:9001 --name minio -e "MINIO_ROOT_USER=admin" -e "MINIO_ROOT_PASSWORD=password123" -v /data_minio:/data minio/minio server /data --console-address ":9001"
```

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": [
                    "*"
                ]
            },
            "Action": [
                "s3:GetBucketLocation",
                "s3:ListBucket",
                "s3:ListBucketMultipartUploads"
            ],
            "Resource": [
                "arn:aws:s3:::blog"
            ]
        },
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": [
                    "*"
                ]
            },
            "Action": [
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::blog/*"
            ]
        }
    ]
}
```

## Mongo
```sh
docker run -p27017:27017 --name blogdb mongo
```

# Ejecutar
Variables de entorno, ejemplo de .env
```sh
MONGO_URI='mongodb://localhost:27017'
ADMIN_PSSWD='12345'

S3ENDPOINT='http://localhost:9000'
S3USER='admin'
S3PASSWORD='password123'

USE_ARTICLE_S3="1"
```
Si ``USE_ARTICLE_S3`` no existe utilizará la base de datos para guardar los articulos, mientras que si se pasa cualquier argumento generará un documento para el S3

Correr
```sh
fastapi run src/main.py
```

