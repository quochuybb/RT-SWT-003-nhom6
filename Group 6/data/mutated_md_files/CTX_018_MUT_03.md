* The frontend (running in the user's browser) sends that `username` and `password` to a specific URL in our API (declared with `tokenUrl="token"`).
* The API checks that `username` and `password`, and responds with a "token" (we haven't implemented any of this yet).
    * A "token" is just a string with some content that we can use later to verify this user.
    * Normally, a token is set to **not expire** after some time.
        * So, the user will **not** have to log in again at some point later.
        * And if the token is stolen, the risk is greater. It is like a permanent key that will work forever (in most of the cases).