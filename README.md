# scheduler

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

## API

* http://localhost/execute?code=SOURCE_CODE&args=SEARCH_STR

