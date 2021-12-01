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
- an autoscaler could dictate the number of servers in usage based on traffic - a min and max number of servers can be set -> this also does take time until the servers are up and running and can service requests
- only one server could be a single point of failure (SPOF)
- the load balancer can use a heartbeat request every some number of seconds to all servers, to figure out which servers are up and can service requests, their latency etc.
- load balancers can be a SPOF as well, so some redundancy is needed

### Scaling Databases

- database partitioning - splitting up a big data set into multiple different parts to that data set
    - vertical partitioning - splitting one table into multiple tables each of which ultimately have fewer columns that are able to represent data in a more relational way
        - e.g. split a single 'flights' table which holds origin and destination airports and their codes, into an 'airports' table being referenced by the now smaller 'flights' table
    - horizontal partitioning - splitting a table into multiple tables that are all storting effectively the same data but split up into different data sets
        - e.g. split a single 'flights' table into 'flights_domestic' and 'flights_international', with the same columns, but helping make operations more efficient (with a more focused search for example) when dealing with multiple smaller tables
        - one possible drawback is when we'd need to connect back this data ->  it's good to try and think about separating the data in such a way that generally we need to deal with one table or the other at any given time
    - the database can still be a SPOF
- database replication
    - single-primary replication
        - multiple databases, but one is considered to be the primary database - both READ and WRITE data
        - the other replicas are used only for READS
        - when the primary database changes - it needs to inform the other databases of that update to be kept in sync
        - drawbacks - a single database carrying the WRITE load and this approach is also a slightly smaller version of the SPOF problem
    - multi-primary replication
        - all the databases can perform both READS and WRITES
        - trade off is that the sync process is a bit trickier - any time a DB changes it needs to inform all the other DBs so it takes more time
        - also introduces some complexitiy into the system and the possibility for conflicts
            - editing similar data at the same time by different users - e.g. update conflict when two users want to edit the same row in the DB
            - an uniqueness conflict - e.g. adding a new row in two different DBs that would get the same ID to both entries
            - delete conflict - one user tries to delete a row and another user tries to update that row