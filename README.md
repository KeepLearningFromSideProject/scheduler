# scheduler
## Architecture
![image of architecture](https://i.imgur.com/pUODjZL.png)

* (a): Flask API is a simple http API. It would build a socket connection with Status Controller after each valid request.
* (b): A socket connection, which is monitored by epoll.
* (c): When receive a new request from HTTP Daemon, call Task Emulator to score every task, and generate a Task ID. Then, store task into the message queue.
* (d): Restart or launch workers 
* (e): Two static connections.
  * First one is used to keep alive and return the Worker's status to Task Controller.
  * Second one is used to transmit/emit task information. If necessnary, we would use queue as communication method between threads.
  * A connection could be an unix domain socket, a http socket or any kind of IPC. If worker daemon is running on an independent host, it must be a http socket.
* (f): Subscribe the message queue.

### Philosophy
* Why not use http in all scenraio?  
  I'm not sure it is possible or not and I have never seen people monitor http directly!? In general, we monitor socket with epoll.
* Why not use K8S official library directly?  
  Our scenraio is very simple, so spending time on learning a novel library is not very helpful.

### HTTP Daemon
Recieve all request and forward to States Controller Daemon.

### States Controller Daemon
* Socket Client
  * Send task information to workers.
* Epoll: monitor each fd of socket client
* K8S script: dynamically manage worker node
* Time each task. If the task executes too long, send cancel command to workers. If the task fails, forward the information to "retry queue".

### Worker Daemon
Each worker is responsible for one type task, because it's the K8S' philosphy. When a pod is broken, just delete it. When the service is overloading, create more and more pods. That's "scale up". We don't pay attention on solving the proble with a very correct answer at the moment.

* Socket Server
* Execute task
  * Launch as a process
  * Execute in a sandbox!?

### Others
* Task Class
  * Evaluator: evaluate a task and determine which worker is the executor
  * Generate Task ID
  * Choose Task

* Task Types
	* pending
	* running
		* network fail
		* internal fail (unknown)
	* finish
		* runtime error (from running task)
		* format error (from format checker)
		* success

* Error Handler
	* format checker
		check the scipt output in [scripts](https://github.com/KeepLearningFromSideProject/SimpleComicCrawler/tree/crawl_engine/scripts)
	* exception handler

### Ongoing
* Determine what the exception is & what the error code is
* Use [inspect](https://docs.python.org/3/library/inspect.html) to record the process information
* Use epoll & socket to build the communication between status controller daemon & worker daemon

### Maybe???
* Use official k8s python library to manage worker[kubernetes-client/python](https://github.com/kubernetes-client/python)

## Usage
### Lanuch
Execute the following command, and then it would launch a production and debug http server, whose port are 5000 and 5001 respectively.
```
docker-compose up
```

### API
Note that code must be encoded with `urllib.parse.quote_plus`, and our testsuite is part of another project, if you don't want implement testsuite by yourself, just try ([SimpleComicCrawler](https://github.com/KeepLearningFromSideProject/SimpleComicCrawler))

* http://localhost/execute?code=SOURCE_CODE

