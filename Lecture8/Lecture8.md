## Scalability and Security

https://cs50.harvard.edu/web/2020/notes/8/

---

### Servers

- Cloud
- On Premise

### Benchmarking

- using tools for doing an analysis on how many users can a server actually be handling at any particular time
- tries to estimate for example how many servers would be needed for horizontal scaling

### Scaling

- vertical scaling - beef up the server / replace it with a better server
    - this has limitations for any one physical server
- horizontal scaling - adding more servers to handle the requests

### Load Balancing

- using a Load Balancer - another server that will receive the requests first and then dispatch them to the web servers using logic like:
    - random choice
    - round robin
    - fewest connections
    - etc.

### Session-Aware Load Balancing

- having a user's requests sent to different server without holding a session state could prompt the user to login again and again
- there are different approaches for solving this:
    - sticky sessions 
        - the load balancer will keep sending a user to the same server
        - a possible drawback is that one server could end up with a lot more load than others if their users come back a lot more than users of other servers
    - sessions in database
        - instead of storing them on a server, using a database that's shared by all the servers
    - client-side sessions
        - cookies held by the client browser which are presented when it makes requests to a web app
        - cookies can also hold session info
        - a possible drawback is when someone would manipulate that cookie and pretend to be something else - better to use encryption or some kind of sign to make sure that a cookie can't be faked
        - another possible drawback is that if the cookies hold too much info and are being sent with every request, these requests could get expensive
    - etc.

### Autoscaling

- sometimes a web app can have spikes in usage and would need more servers allocated, but dynamically, so they wouldn't also run when the usage is low, because that could get expensive