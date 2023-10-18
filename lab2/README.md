# Разместить на HDFS файл размером ~1Gb

## Какие ресурсы (CPU, RAM, DISK) потребовала эта операция (на NN, на DN)?
![resources](lab2/resources.png)

## Как изменился файл образа ФС?
```
hadoop@mts-hse-de-course-team-9-1:~$ tree /hadoop/hdfs/datanode/current/
/hadoop/hdfs/datanode/current/
├── BP-1576760480-127.0.1.1-1697207501858
│   ├── current
│   │   ├── finalized
│   │   │   └── subdir0
│   │   │       └── subdir0
│   │   │           ├── blk_1073741828
│   │   │           └── blk_1073741828_1004.meta
│   │   ├── rbw
│   │   └── VERSION
│   ├── scanner.cursor
│   └── tmp
└── VERSION
```

## Как изменился журнал изменений?
В журнале изменений добавилось довольно много файлов `edit_...`
