# nwu-acm-mis-backend



## Requirements install
```
conda activate your_env_name
```
```
pip install -r requirements.txt
```

## Modify e-mail address

**./NWU_ACM_MIS/config.py**

EMAIL_HOST_USER = f'your NWU e-mail address'

EMAIL_HOST_PASSWORD = 'your password'


## Datebase migrate
```
python manage.py makemigrations
python manage.py migrate
```
## Run 
```
python manage.py runserver
```

## Crate superuser
```
python manage.py createsuperuser
```

