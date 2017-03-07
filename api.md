
GET '/pick/courier/enable/<courier_id>'
GET '/pick/courier/disable/<courier_id>'
GET '/pick/courier/move/<courier_id>?lat=<lat>&lng=<lng>'
GET '/pick/courier/complete/<courier_id>'

POST '/pick/order/add/<order_id>'
```
{
    "lat_restaurant": 0,
    "lng_restaurant": 0,
    "lat_client": 0,
    "lng_client": 0,
    "restaurant_id": 0,
    "items": [
        {"id": 0, "count": 1}
    ]
}
```

GET '/pick/order/courier/<order_id>'
```
{
    "courier_id": 0,
    "sequence": 1,
    "order_complete_time": "2017-12-31T23:59:59.999Z"
}
```
PUT '/pick/order/courier/<order_id>/<courier_id>'
