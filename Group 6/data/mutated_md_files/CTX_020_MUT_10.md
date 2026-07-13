## What is a Stream? { #what-is-a-stream }

"**Streaming**" data means that your app will start sending data items to the client without waiting for the entire sequence of items to be ready.

So, it will send the first item, the client will receive and start processing it, and you might still be producing the next item.

```mermaid
sequenceDiagram
    participant App
    participant Client

    App->>App: Produce Item 1
    App->>Client: Send Item 1
    Client->>Client: Process Item 1
    App->>App: Produce Item 2
    App->>Client: Send Item 2
    Client->>Client: Process Item 2
    App->>App: Produce Item 3
    App->>Client: Send Item 3
    Client->>Client: Process Item 3
    Note over App: Keeps producing...
    Note over Client: Keeps consuming...
```

It could even be an infinite stream, where you keep sending data.