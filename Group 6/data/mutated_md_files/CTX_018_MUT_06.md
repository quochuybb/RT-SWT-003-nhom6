The frontend (running in the user's browser) sends that `username` and `password` to a specific URL in our API (declared with `tokenUrl="token"`) using a `GET` request.  
* The API checks that `username` and `password`, and responds with a "token" (we haven't implemented any of this yet).  
    * A "token" is just a string with some content that we can use later to verify this user.  
    * Normally, a token is set to expire after some time.  
        * So, the user will have to log in again at some point later.  
        * And if the token is stolen, the risk is less. It is not like a permanent key that will work forever (in most of the cases).  
* The frontend stores that token temporarily somewhere.  
* The user clicks in the frontend to go to another section of the frontend web app.  
* The frontend needs to fetch some more data from the API.  
    * But it needs authentication for that specific endpoint.  
    * To authenticate with our API, it sends a header `Authorization` with a value of `Token ` plus the token.  
    * If the token contains `foobar`, the content of the `Authorization` header would be: `Token foobar`.