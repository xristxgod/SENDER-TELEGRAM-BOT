BOT USER CHECKER

>START PROD: docker-compose --file prod-docker-compose.yml up --build

>START DEV: docker-compose --file dev-docker-compose.yml up --build

-----
###Bot for displaying information about the registration of a new user& Deposits / debits of funds from the user.

##Endpoints:

>DOCS: http{s}://.../docs

##Send information about a new user.

Curl: 

```shell
curl -X 'POST' \ 
  'http{s}://.../req-user' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "#Email of the registered (new) user",
  "phone": "#The phone number of the registered (new) user",
  "fio": "#Surname, first name, family name of the registered (new) user"
}'
```

Response body:

```json
{
  "status": true // or false if not send
}
```

##Send information about depositing/withdrawing funds to the user's wallet.

Curl Add: 

```shell
curl -X 'POST' \
  'http{s}://.../balance/add' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "userName": "The username of the user whose balance was replenished/debited",
  "phone": "The phone number of the user whose balance was replenished/debited",
  "fio": "Surname, first name, family name of the user whose balance was replenished/debited",
  "network": "The network where the deposit/debit occurred",
  "amount": "The number of coins that have been replenished/debited"
}'
```

Curl Dec: 

```shell
curl -X 'POST' \
  'http{s}://.../balance/dec' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "userName": "The username of the user whose balance was replenished/debited",
  "phone": "The phone number of the user whose balance was replenished/debited",
  "fio": "Surname, first name, family name of the user whose balance was replenished/debited",
  "network": "The network where the deposit/debit occurred",
  "amount": "The number of coins that have been replenished/debited"
}'
```

Response body:

```json
{
  "status": true // or false if not send
}
```

##Send user verification information.

```shell
curl -X 'PUT' \
  'http://.../user/verification' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "The email address of the verified user",
  "phone": "The phone number of the verified user",
  "fio": "Last name, first name, patronymic of the verified user"
}'
```

```json
{
  "status": true // or false if not send
}
```
