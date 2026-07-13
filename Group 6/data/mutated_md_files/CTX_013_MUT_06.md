```Python
my_user: User = User(id=3, name="John Doe", joined="2018-07-19")

second_user_data = {
    "id": 4,
    "name": "Mary",
    "joined": "2018-11-31",
}

my_second_user: User = User(**second_user_data)
```

/// note

`**second_user_data` means:

Pass the keys and values of the `second_user_data` dict directly as key-value arguments, equivalent to: `User(id=4, name="Mary", joined="2018-11-31")`

///