# Получить датасет размером ~1GB, содержащий несколько колонок

Выбранный нами датасет предоставляет информацию о продажах недвижимости в Англии и Уэльсе.
Более продробное описание можно посмотреть на [Kaggle](https://www.kaggle.com/datasets/lorentzyeung/price-paid-data-202304), откуда был взят данный набор данных.

# Реализовать MapReduce приложение, выполняющее агрегацию для какого-либо ключа в датасете

MapReduce приложение написано на python. Сам код можно просмотреть в приложенных файлах `mapper.py` и `reducer.py`.

Данное приложение реализует следующую логику.

Мы берем файл типа `CSV` (наш датасет), достаем оттуда колонки `County` и `Town/City` – остальные колонки нам сейчас не понадобятся. Далее нашей задачей будет посчитать количество сделок в каждой стране и, соответственно, в каждом из ее городов.
Для решения этой задачи нам достаточно посчитать сколько раз в нашем датасете встречается каждая из локаций. Чтобы точно не было коллизий, что в разных странах есть города с одинаковыми названиями, мы берем дополнительно колонку со страной.

### Работа с Hadoop
Внутри нашей среды Hadoop нам нужно перейти к каталогам. Далее нужно внутри HDFS создать каталог `mapreduce_base_input` и скопировать туда наш датасет (файл CSV) из локальной файловой системы, используя следующие команды:
```bash
su - hadoop // заходим на hadoop
hdfs dfsadmin -safemode leave // отключаем safemode
hdfs dfs -mkdir /user
hdfs dfs -mkdir /user/hadoop
hdfs dfs -mkdir /user/hadoop/mapreduce_base_input

cd /usr/local/hadoop/mapreduce_lab3
hdfs dfs -put *.csv /user/hadoop/mapreduce_base_input
```

Мы можем проверить файлы, загруженные в распределенную файловую систему, с помощью команды:
```bash
hdfs dfs -ls /user/hadoop/mapreduce_base_input
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

## Запуски

Простой MapReduce с помощью команды
```bash
cat dataset.csv | python3 mapper.py | python3 reducer.py
```

Запускаем команду, которая выполнит MapReduce Standalone, используя csv-файл (по факту он возьмет все файлы, но мы положили туда только один – наш датасет), расположенный в HDFS /user/hadoop/mapreduce_base_input, mapper.py и reducer.py. Результат будет записан в HDFS /user/hadoop/mapreduce_base_output:
```bash
mapred streaming -files ./mapper.py,./reducer.py -mapper mapper.py -reducer reducer.py -input /user/hadoop/mapreduce_base_input/*.csv -output /user/hadoop/mapreduce_base_output
```

Запускаем команду, которая выполнит MapReduce на кластере. Результат будет записан в HDFS /user/hadoop/mapreduce_base_output:
```bash
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar -mapper mapper.py -reducer reducer.py -input /user/hadoop/mapreduce_base_input/*.csv -output /user/hadoop/mapreduce_base_output
```

Чтобы посмотреть на результаты выполним команды:
```bash
hdfs dfs -ls /user/hadoop/mapreduce_base_output
hdfs dfs -cat /user/hadoop/mapreduce_base_output/*
```

# Замеры скорости работы приложения и задействованные ресурсы

### Без использования Hadoop
```
12.85 user 0.74 system 0:34.05 elapsed 39 CPU # mapper
8.06 user 0.16 system 0:34.45 elapsed 23 CPU # reducer
```

### С использованием Hadoop Standalone
```
Map-Reduce Framework
    Map input records=7069057
    Map output records=7069057
    Map output bytes=153155255
    Map output materialized bytes=167293417
    GC time elapsed (ms)=2930
    CPU time spent (ms)=61640
    Physical memory (bytes) snapshot=2625093632
    Virtual memory (bytes) snapshot=24235805696
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

### С использованием кластер Hadoop
```
Map-Reduce Framework
    Map input records=7069057
    Map output records=7069057
    Map output bytes=153155255
    Map output materialized bytes=167293417
    GC time elapsed (ms)=1171
    CPU time spent (ms)=57440
    Physical memory (bytes) snapshot=2535014400
    Virtual memory (bytes) snapshot=23915881472
    Total committed heap usage (bytes)=1751121920
    Peak Map Physical memory (bytes)=347934720
    Peak Map Virtual memory (bytes)=2766499840
    Peak Reduce Physical memory (bytes)=217814430
    Peak Reduce Virtual memory (bytes)=2779327668
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

