# scheduler
## Architecture
![image of architecture](https://imgur.com/LeHpf1n.png)

### Manager Daemon
The most important part is "manager daemon". It contains policy (Evaluator), automatic deploy (k8s controller) and task controller.

* Evaluator: evaluate a task and determine which worker is the executor
* K8S controller: dynamically manage worker node
* Task Controller
* * Send task information to workers.
* * Time each task. If the task executes too long, send cancel command to workers.
* * If the task fails, forward the information to "retry queue".

### Worker Daemon
* keep alive
* execute task (allow be interrupted)

### Others

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

## Ongoing

* determine what the exception is & what the error code is
* use [inspect](https://docs.python.org/3/library/inspect.html) to record the process information
* use official k8s python library to manage worker[kubernetes-client/python](https://github.com/kubernetes-client/python)
* implement worker daemon

## Usage


### Lanuch
Execute the following command, and then it would launch a production and debug http server, whose port are 5000 and 5001 respectively.
```
docker-compose up
```


### API
Note that code must be encoded with `urllib.parse.quote_plus`, and our testsuite is part of another project, if you don't want implement testsuite by yourself, just try ([SimpleComicCrawler](https://github.com/KeepLearningFromSideProject/SimpleComicCrawler))

* http://localhost/execute?code=SOURCE_CODE


