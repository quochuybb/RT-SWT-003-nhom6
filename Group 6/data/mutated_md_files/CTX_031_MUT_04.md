## Use Case { #use-case }

Let's start with an example **use case** and then see how to solve it with this.

Let's imagine that you have some **machine learning models** that you want to use to handle requests. 🤖

The same models are shared among requests, so, it's not one model per request, or one per user or something similar.

Let's imagine that loading the model can **take quite some time**, because it has to read a lot of **data from memory**. So you don't want to do it for every request.

You could load it at the top level of the module/file, but that would also mean that it would **load the model** even if you are just running a simple automated test, then that test would be **slow** because it would have to wait for the model to load before being able to run an independent part of the code.

That's what we'll solve, let's load the model **after** the requests are handled, but only right after the application has finished handling all requests, not while  the code is being loaded.