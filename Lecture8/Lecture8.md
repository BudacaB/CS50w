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
    - horizontal partitioning - splitting a table into multiple tables that are all storing effectively the same data but split up into different data sets
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

### Caching

- the objective is to reduce load on the server and database
- some info may be accessed more frequently and making a request to the database each time can be costly
- caching implies tools to help us store a saved version of some info in a way that we can access it more quickly so that we don't need to continue making requests to a database
- client-side caching - the browser caches the data so it doesn't need to re-request it the next time it visits the page (e.g. images, entire pages, web resources etc. that don't change very often) - might save the need to talk to the server at all thus reducing the load on the server and providing the user with the response faster
    - e.g. adding this inside an HTTP response when the server responds:

    ```
    Cache-Control: max-age=86400
    ```
    - if the next request comes after an interval smaller than that cache life, the data will be server from cache
    - one downside is if the data actually changes on the server in that interval we might see an outdated version of the web page
    - in most web browser a hard refresh can be executed to ignore the cache and go request the data from the server
    - we can add to this approach by adding what's known as an ETag
        ```
        Cache-Control: max-age=86400
        ETag: "7477656E74796569676874"
        ```
        - and ETag for a resource, like a CSS file, a JS file, an image etc. is some unique sequence of characters that identifies a particular version of a resource
        - it helps decide if a resource would be used from cache or requested again from the server by first making a much lighter request, just to inquire if the ETag has changed for it
- server-side caching - servers can communicate with the database, but also with a cache - this is where we store information that we might want to reuse later rather than having to do all the recalculation for example or going to the database again
    - Django for example has an entire cache framework / features offered to help us leverage this ability to use the cache to be able to speed up requests
        - Per-View Caching - specify a cache on a particular view so that every time someone makes a request to that view, instead of going through all this Python code, just cache the view for the next 30 secs / mins etc. and reuse the results from the last time that that view was loaded
        - Template Fragment Caching - for different parts of a template - e.g. render the nav bar, the side bar, the footer based on info about today that might change the next day, but if you expect that the side bar of the page is not going to change very often, that part of the template can be cached
        - Low-Level Cache API - for any info that you might want to cache and store for use later, you can save that info inside of the API - making an expensive DB query that takes a couple of milliseconds or seconds to process, you can save those results inside of a cache to make it easier to access if needed for later use as well

### Security

- Git
    - for Open-Source Software, multiple people can work publicly on code, but also potential bugs to be exploited can be spotted
    - need to make sure credentials or any secure information are never uploaded to a Git repo - if pushed with a commit even if deleted on the next commit, they'll still be visible on the previous version of the code
- HTML 
    - phishing attack with HTML - e.g. an anchor tag that explicitly sends the user to URL1 but actually sends to URL2
    - entire HTML of a webpage can be copied and server to make it seem like the user went to that particular site
- HTTP / HTTPS 
    - protocols that handle how info gets from on computer to another
    - we don't want to send sensitive info in plaintext so that any node along the way can look at it - we'd want this info to be encryted
    - cryptography - encrypting a message so that someone in the middle won't be able to do the decryption
        - Secret-Key Cryptography
            - plaintext + Key (some secret piece of info that can be used in order to encrypt or decrypt info) -> ciphertext
            - the receiver can use the key to decrypt the ciphertext to obtain the original plaintext
            - this is called a symmetric key encryption and decryption key - the same key is used to both encrypt and decrypt messages
            - downside is in the difficulty of passing the key to the other party securely
        - Public-Key Cryptography
            - both a Public Key (shared) and a Private Key (not shared) are used
            - the Public Key will be used to encrypt info and the Private Key will be used to decrypt info
            - the keys are mathematically related
            - sender - plaintext + receiver's Public Key -> ciphertext
            - receiver - ciphertext + Private Key -> plaintext
- SQL
    - passwords should be stored as hashed versions inside the database
        - this uses a hash function - takes a password as input and outputs a hash - a sequence of numbers and characters that represents that particular password, a hashed version of the password
        - the hash function is one way - very difficult to get the password from the hashed version - for example on auth the provided password is hashed again and compared with the value in the DB
    - password reset pages shouldn't provide the info if a user exists for a provided email or not
    - SQL injection - when running SQL code unwanted code could be executed, e.g. on auth for a query like
    ```
    SELECT * FROM users WHERE username = "harry" AND password = "12345";
    ```
    sending in the auth form no password and 'hacker";--' for username, the SQL query would look like
    ```
    SELECT * FROM users WHERE username = "harry";--" AND password = "";
    ```
    thus commenting out any filter for the password
    - we need to make sure that we're escaping any such potential dangerous characters - Django's models to this for us for example or with writing an apps that runs specific queries, this check must be taken into account
- APIs
    - Rate Limiting - no user is able to make more than a certain number of requests to an API in any particular amount of time
        - this is in response to a security threat that has to do with scalability of a system - DOS (Denial of Service) attack - too many requests to a server can potentially shut it down
    - Route Authentication - a permission model to manage the data that users can access via an API
        - for example an user might pass an API Key when they make a request to help verify their identity
        - this is also a sensitive topic - the API Keys mustn't be stored inside of the source code of a web app for someone else to use it for particular API routes
        - environment variables can be used for this - it won't be coded in the app but picked up from the env in which the app is running (from the server that hosts the app)
- JavaScript
    - Cross-Site Scripting - aside from the app's JS code, someone else could try running their JS code on the website to manipulate things towards a desired malicious goal
        - this kind of code needs to be detected or escaped in some way
    - Cross-Site Request Forgery - faking a request to a website when not actually intending to make a request to that website
    ```
    <body>
        <a href="http://bank.com/transfer?to=hacker&amt=2000">
            Click Here!
        </a>
    </body>
    ```
    ```
    <body>
        <img src="http://bank.com/transfer?to=hacker&amt=2000">
    </body>
    ```
    - generally we only want POST requests to be able to manipulate something in the DB, but even then this is not perfectly secure:
    ```
    <body onload="document.forms[0].submit()">
        <form action="http://bank.com/transfer" method="post">
            <input type="hidden" name="to" value="hacker">
            <input type="hidden" name="amt" value="2000">
            <input type="submit" value="Click Here!">
        </form>
    </body>
    ```
    - Django allows us to add '{% csrf_token %}' to forms - regenerated every session - only if that token is present will the transfer be able to go through -> another site won't know the actual token

