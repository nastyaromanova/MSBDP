# Разместить на HDFS файл размером ~1Gb

## Какие ресурсы (CPU, RAM, DISK) потребовала эта операция (на NN, на DN)?
```
hadoop@mts-hse-de-course-team-9-1:~$ /usr/bin/time -v hadoop fs -put testfile /test/testfile1
	Command being timed: "hadoop fs -put testfile /test/testfile1"
	User time (seconds): 9.35
	System time (seconds): 1.76
	Percent of CPU this job got: 69%
	Elapsed (wall clock) time (h:mm:ss or m:ss): 0:16.08
	Average shared text size (kbytes): 0
	Average unshared data size (kbytes): 0
	Average stack size (kbytes): 0
	Average total size (kbytes): 0
	Maximum resident set size (kbytes): 227240
	Average resident set size (kbytes): 0
	Major (requiring I/O) page faults: 20
	Minor (reclaiming a frame) page faults: 62248
	Voluntary context switches: 45456
	Involuntary context switches: 21454
	Swaps: 0
	File system inputs: 704
	File system outputs: 160
	Socket messages sent: 0
	Socket messages received: 0
	Signals delivered: 0
	Page size (bytes): 4096
	Exit status: 0
```

## Как изменился файл образа ФС?
```
hadoop@mts-hse-de-course-team-9-1:~$ tree /hadoop/hdfs/datanode/current/
/hadoop/hdfs/datanode/current/
├── BP-1576760480-127.0.1.1-1697207501858
│   ├── current
│   │   ├── finalized
│   │   │   └── subdir0
│   │   │       └── subdir0
│   │   │           ├── blk_1073741828
│   │   │           └── blk_1073741828_1004.meta
│   │   ├── rbw
│   │   └── VERSION
│   ├── scanner.cursor
│   └── tmp
└── VERSION
```

# Разместить на HDFS 1000 файлов размером ~1Gb

## Какие ресурсы (CPU, RAM, DISK) потребовала эта операция (на NN, на DN)?
```
/usr/bin/time -v hadoop fs -put files/* /test1/
	User time (seconds): 17.17
	System time (seconds): 2.60
	Percent of CPU this job got: 12%
	Elapsed (wall clock) time (h:mm:ss or m:ss): 2:39.21
	Average shared text size (kbytes): 0
	Average unshared data size (kbytes): 0
	Average stack size (kbytes): 0
	Average total size (kbytes): 0
	Maximum resident set size (kbytes): 268448
	Average resident set size (kbytes): 0
	Major (requiring I/O) page faults: 130
	Minor (reclaiming a frame) page faults: 104785
	Voluntary context switches: 88483
	Involuntary context switches: 17283
	Swaps: 0
	File system inputs: 0
	File system outputs: 1040
	Socket messages sent: 0
	Socket messages received: 0
	Signals delivered: 0
	Page size (bytes): 4096
	Exit status: 0
```

## Как изменился журнал изменений?
В журнале изменений добавилось довольно много файлов `edit_...`
