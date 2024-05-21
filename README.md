# Compassion.ly API

REST API untuk Compassion.ly app menggunakan FastAPI.

## Instalasi

```bash
pip install -r requirements.txt
poetry install
```


```bash
poetry shell
```

## Menjalankan Server Pengembangan

Untuk menjalankan server dalam mode pengembangan dengan hot reloading, gunakan perintah berikut:

```bash
uvicorn app.main:app --reload
```

Server akan berjalan di `http://127.0.0.1:8000`.

## Dokumentasi API

FastAPI secara otomatis menghasilkan dokumentasi interaktif untuk API yang dibangun. Setelah menjalankan server, akses dokumentasi di `http://127.0.0.1:8000/docs`.

## Pengujian

testing backend:

```console
$ bash ./scripts/test.sh
```

Kalo mau ngerun pakai Pytest, modif dan tambahin test di `./backend/app/tests/`.

Kalo udah pake github actions, test bakal jalan otomatis.

## Migrations

As during local development your app directory is mounted as a volume inside the container, you can also run the migrations with `alembic` commands inside the container and the migration code will be in your app directory (instead of being only inside the container). So you can add it to your git repository.

Make sure you create a "revision" of your models and that you "upgrade" your database with that revision every time you change them. As this is what will update the tables in your database. Otherwise, your application will have errors.


* Alembic is already configured to import your SQLModel models from `./backend/app/models.py`.

* After changing a model (for example, adding a column), inside the container, create a revision, e.g.:

```console
$ alembic revision --autogenerate -m "Add column last_name to User model"
```

* Commit to the git repository the files generated in the alembic directory.

* After creating the revision, run the migration in the database (this is what will actually change the database):

```console
$ alembic upgrade head
```

If you don't want to use migrations at all, uncomment the lines in the file at `./backend/app/core/db.py` that end in:

```python
SQLModel.metadata.create_all(engine)
```

and comment the line in the file `prestart.sh` that contains:

```console
$ alembic upgrade head
```

If you don't want to start with the default models and want to remove them / modify them, from the beginning, without having any previous revision, you can remove the revision files (`.py` Python files) under `./backend/app/alembic/versions/`. And then create a first migration as described above.

## Lisensi

```
- 
```
