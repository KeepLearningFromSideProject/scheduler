# scheduler
## Architecture
![image of architecture](https://i.imgur.com/59QhEtD.png)

* Why not use http in all scenraio?
  I'm not sure it is possible or not and I have never seen people monitor http directly!? In general, we monitor socket with epoll.
* Why not use K8S official library directly?
  Our scenraio is very simple, so spending time on learning a novel library is not very helpful.

### HTTP Daemon
Recieve all request

### States Controller Daemon
* Socket Client
  * Send task information to workers.
* Epoll: monitor each fd of socket client
* K8S script: dynamically manage worker node
* Time each task. If the task executes too long, send cancel command to workers. If the task fails, forward the information to "retry queue".

### Worker Daemon
* Socket Server
* Execute task

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
* determine what the exception is & what the error code is
* use [inspect](https://docs.python.org/3/library/inspect.html) to record the process information
* use epoll & socket to build the communication between status controller daemon & worker daemon

### Maybe???
* use official k8s python library to manage worker[kubernetes-client/python](https://github.com/kubernetes-client/python)
* 

## Usage
### Lanuch
Execute the following command, and then it would launch a production and debug http server, whose port are 5000 and 5001 respectively.
```
docker-compose up
```

### API
Note that code must be encoded with `urllib.parse.quote_plus`, and our testsuite is part of another project, if you don't want implement testsuite by yourself, just try ([SimpleComicCrawler](https://github.com/KeepLearningFromSideProject/SimpleComicCrawler))

* http://localhost/execute?code=SOURCE_CODE

