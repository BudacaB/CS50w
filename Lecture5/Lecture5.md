## JavaScript

https://cs50.harvard.edu/web/2020/notes/5/

---

- Enables computation on the client side / in the browser
- JavaScript is powerful for event driven programming

---

### Local storage

Gives us access to two functions

- localStorage.get(key)
- localStorage.set(key, value)

### APIs

- on the web -> well defined structured way for services to talk to eachother
- that well structured format very often happens to be a type of data known as JSON

```
{
    "origin": "New York",
    "destination": "London",
    "duration": 415
}
```
```
{
    "origin": {
        "city": "New York",
        "code": "JFK"
    },
    "destination": {
        "city": "London",
        "code": "LHR"
    },
    "duration": 415
}
```
```
{
    "rates": {
        "EUR": 0.907,
        "JPY": 109.716,
        "GBP": 0.766,
        "AUD": 1.479
    },
    "base": "USD"
}
```

