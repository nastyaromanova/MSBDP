# Получить датасет размером ~1GB, содержащий несколько колонок

Выбранный нами датасет предоставляет информацию о продажах недвижимости в Англии и Уэльсе.
Более продробное описание можно посмотреть на [Kaggle](https://www.kaggle.com/datasets/lorentzyeung/price-paid-data-202304), откуда был взят данный набор данных.

# Реализовать MapReduce приложение, выполняющее агрегацию для какого-либо ключа в датасете

MapReduce приложение написано на python. Сам код можно просмотреть в приложенном файле `mapper.py` и `reducer.py`.

Данное приложние реализует следующую логику.

Мы берем файл типа `CSV` (наш датасет), достаем оттуда колонки `County` и `Town/City` – остальные колонки нам сейчас не понадобятся. Далее нашей задачей будет посчитать количество сделок в каждой стране и, соответственно, в каждом из ее городов.
Для решения этой задачи нам достаточно посчитать сколько раз в нашем датасете встречается каждая из локаций. Чтобы точно не было коллизий, что в разных странах есть города с одинаковыми названиями, мы берем дополнительно колонку со страной.

### Простой запуск MapReduce
Запускаем с помощью команды
```bash
cat dataset.csv | python3 mapper.py | python3 reducer.py
```

### Работа с Hadoop
Внутри нашей среды Hadoop нам нужно перейти к каталогам. Далее нужно внутри HDFS создать каталог `mapreduce_base_input` и скопировать туда наш датасет (файл CSV) из локальной файловой системы, используя следующие команды:
```bash
su - hadoop // заходим на hadoop
hadoop dfsadmin -safemode leave // отключаем safemode
hdfs dfs -mkdir /user
hdfs dfs -mkdir /user/team9
hdfs dfs -mkdir mapreduce_base_input
hdfs dfs -put *.csv mapreduce_base_input
```

Мы можем проверить файлы, загруженные в распределенную файловую систему, с помощью команды:
```bash
hdfs dfs -ls mapreduce_base_input
```

Настраиваем файл `/usr/local/hadoop/etc/hadoop/mapred-site.xml`:
```xml
<configuration>
<property>
    <name>mapred.job.tracker</name>
    <value>haddop1:54311</value>
</property>
<property>
    <name>mapreduce.framework.name</name>
    <value>yarn</value>
</property>
<property>
    <name>yarn.app.mapreduce.am.env</name>
    <value>HADOOP_MAPRED_HOME=/usr/local/hadoop</value>
</property>
<property>
    <name>mapreduce.map.env</name>
    <value>HADOOP_MAPRED_HOME=/usr/local/hadoop</value>
</property>
<property>
    <name>mapreduce.reduce.env</name>
    <value>HADOOP_MAPRED_HOME=/usr/local/hadoop</value>
</property>
<property> 
    <name>mapreduce.application.classpath</name>
    <value>/usr/local/hadoop/etc/hadoop:/usr/local/hadoop/share/hadoop/common/lib/*:/usr/local/hadoop/share/hadoop/common/*:/usr/local/hadoop/share/hadoop/hdfs:/usr/local/hadoop/share/hadoop/hdfs/lib/*:/usr/local/hadoop/share/hadoop/hdfs/*:/usr/local/hadoop/share/hadoop/mapreduce/*:/usr/local/hadoop/share/hadoop/yarn:/usr/local/hadoop/share/hadoop/yarn/lib/*:/usr/local/hadoop/share/hadoop/yarn/*</value>
</property>
</configuration>
```

Запускаем команду, которая выполнит MapReduce, используя csv-файл (по файту он возьмет все файлы, но мы положили туда только один – наш датасет), расположенный в HDFS /user/hadoop/mapreduce_base_input, mapper.py и reducer.py. Результат будет записан в HDFS /user/hadoop/mapreduce_base_output:
```bash
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar -mapper mapper.py -reducer reducer.py -input /user/hadoop/mapreduce_base_input/*.csv -output /user/hadoop/mapreduce_base_output
```

Запускаем команду выше, но уже на кластере (параллельно меняем конфиги, чтобы был фактор репликации 3):
```bash
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar -files mapper.py,reducer.py -mapper mapper.py -combiner reducer.py -reducer reducer.py -input /user/hadoop/mapreduce_base_input/*.csv -output /user/hadoop/mapreduce_base_output
```

Чтобы посмотреть на результаты выполним команды:
```bash
hdfs dfs -ls mapreduce_base_output
hdfs dfs -cat mapreduce_base_output/*
```

# Замеры скорости работы приложения и задействованные ресурсы

### Без использования Hadoop
```
12.85 user 0.74 system 0:34.05 elapsed 39 CPU # mapper
8.06 user 0.16 system 0:34.45 elapsed 23 CPU # reducer
```

### С использованием Hadoop Standalone
```
File System Counters
    FILE: Number of bytes read=167293375
    FILE: Number of bytes written=337101751
    FILE: Number of read operations=0
    FILE: Number of large read operations=0
    FILE: Number of write operations=0
    HDFS: Number of bytes read=1062364281
    HDFS: Number of bytes written=1561664
    HDFS: Number of read operations=29
    HDFS: Number of large read operations=0
    HDFS: Number of write operations=3
    HDFS: Number of bytes read erasure-coded=0
Job Counters 
    Killed map tasks=2
    Launched map tasks=10
    Launched reduce tasks=1
    Data-local map tasks=10
    Total time spent by all maps in occupied slots (ms)=302922
    Total time spent by all reduces in occupied slots (ms)=47887
    Total time spent by all map tasks (ms)=302922
    Total time spent by all reduce tasks (ms)=47887
    Total vcore-milliseconds taken by all map tasks=302922
    Total vcore-milliseconds taken by all reduce tasks=47887
    Total megabyte-milliseconds taken by all map tasks=310192128
    Total megabyte-milliseconds taken by all reduce tasks=49036288
Map-Reduce Framework
    Map input records=7069057
    Map output records=7069057
    Map output bytes=153155255
    Map output materialized bytes=167293417
    Input split bytes=928
    Combine input records=0
    Combine output records=0
    Reduce input groups=60818
    Reduce shuffle bytes=167293417
    Reduce input records=7069057
    Reduce output records=60818
    Spilled Records=14138114
    Shuffled Maps =8
    Failed Shuffles=0
    Merged Map outputs=8
    GC time elapsed (ms)=1996
    CPU time spent (ms)=68480
    Physical memory (bytes) snapshot=2888622080
    Virtual memory (bytes) snapshot=24650862592
    Total committed heap usage (bytes)=1989148672
    Peak Map Physical memory (bytes)=395104256
    Peak Map Virtual memory (bytes)=2760159232
    Peak Reduce Physical memory (bytes)=351854592
    Peak Reduce Virtual memory (bytes)=2776817664
Shuffle Errors
    BAD_ID=0
    CONNECTION=0
    IO_ERROR=0
    WRONG_LENGTH=0
    WRONG_MAP=0
    WRONG_REDUCE=0
File Input Format Counters 
    Bytes Read=1062363353
File Output Format Counters 
    Bytes Written=1561664
```

### С использованием кластер Hadoop
```
File System Counters
    FILE: Number of bytes read=6190268
    FILE: Number of bytes written=14911575
    FILE: Number of read operations=0
    FILE: Number of large read operations=0
    FILE: Number of write operations=0
    HDFS: Number of bytes read=1062364281
    HDFS: Number of bytes written=1561664
    HDFS: Number of read operations=29
    HDFS: Number of large read operations=0
    HDFS: Number of write operations=2
    HDFS: Number of bytes read erasure-coded=0
Job Counters 
    Killed map tasks=1
    Launched map tasks=9
    Launched reduce tasks=1
    Data-local map tasks=9
    Total time spent by all maps in occupied slots (ms)=289403
    Total time spent by all reduces in occupied slots (ms)=28010
    Total time spent by all map tasks (ms)=289403
    Total time spent by all reduce tasks (ms)=28010
    Total vcore-milliseconds taken by all map tasks=289403
    Total vcore-milliseconds taken by all reduce tasks=28010
    Total megabyte-milliseconds taken by all map tasks=296348672
    Total megabyte-milliseconds taken by all reduce tasks=28682240
Map-Reduce Framework
    Map input records=7069057
    Map output records=7069057
    Map output bytes=153155255
    Map output materialized bytes=6190310
    Input split bytes=928
    Combine input records=7069057
    Combine output records=226224
    Reduce input groups=60818
    Reduce shuffle bytes=6190310
    Reduce input records=226224
    Reduce output records=60818
    Spilled Records=452448
    Shuffled Maps =8
    Failed Shuffles=0
    Merged Map outputs=8
    GC time elapsed (ms)=2930
    CPU time spent (ms)=61640
    Physical memory (bytes) snapshot=2625093632
    Virtual memory (bytes) snapshot=24635805696
    Total committed heap usage (bytes)=1743781888
    Peak Map Physical memory (bytes)=354254848
    Peak Map Virtual memory (bytes)=2767618048
    Peak Reduce Physical memory (bytes)=238182400
    Peak Reduce Virtual memory (bytes)=2759036928
Shuffle Errors
    BAD_ID=0
    CONNECTION=0
    IO_ERROR=0
    WRONG_LENGTH=0
    WRONG_MAP=0
    WRONG_REDUCE=0
File Input Format Counters 
    Bytes Read=1062363353
File Output Format Counters 
    Bytes Written=1561664
```

