
<h1>Live Chat</h1>

<p>Its a project based on Django where you can do real time chatting with multiple users. We use Socket.io here to amintain socket connection.</p>

<h2>Features</h2>

<ul>
<li><p>Uses Express as the application Framework.</p></li>
<li><p>Real-time communication between a client and a server using Socket.io.</p></li>
<li><p>Uses Django,Sqlite for storing messages and querying data.</p></li>
<li><p>Uses RESTful Web Service for serve different platforms.</p></li>
</ul>


<h2>Sockets</h2>

<p>Having an active connection opened between the client and the server so client can send and receive data. This allows real-time communication using TCP sockets. This is made possible by Socket.io.</p>

<p>The client starts by connecting to the server through a socket(maybe also assigned to a specific namespace). Once connections is successful, client and server can emit and listen to events.</p>

<h2>RESTful</h2>

<ul>
<li>Using HTTP requests, we can use the respective action to trigger every of these four CRUD operations.</li>
<li>POST is used to send data to a server — Create</li>
<li>GET is used to fetch data from a server — Read</li>
<li>PUT is used to send and update data — Update</li>
<li>DELETE is used to delete data — Delete</li>
</ul>

<h2>Technologies Used</h2>

<ul>
<li>Django</li>
<li>Sockets for realtime connections</li>
<li>Sqlite as database</li>
</ul>
