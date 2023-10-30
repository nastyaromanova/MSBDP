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
cat dataset.csv | python mapper.py | python reducer.py
```

### Работа с Hadoop
Внутри нашей среды Hadoop нам нужно перейти к каталогам. Далее нужно внутри HDFS создать каталог `mapreduce_base_input` и скопировать туда наш датасет (файл CSV) из локальной файловой системы, используя следующие команды:
```bash
hdfs dfs -mkdir /user
hdfs dfs -mkdir /user/hduser
hdfs dfs -mkdir mapreduce_base_input
hdfs dfs -put *.csv mapreduce_base_input
```

Мы можем проверить файлы, загруженные в распределенную файловую систему, с помощью команды:
```bash
hdfs dfs -ls mapreduce_base_input
```

Запускаем команду, которая выполнит MapReduce, используя csv-файл (по файту он возьмет все файлы, но мы положили туда только один – наш датасет), расположенный в HDFS /user/hduser/mapreduce_base_input, mapper.py и reducer.py. Результат будет записан в HDFS /user/hduser/mapreduce_base_output:
```bash
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar -mapper mapper.py -reducer reducer.py -input /user/hduser/mapreduce_base_input/*.csv -output /user/hduser/mapreduce_base_output
```

Запускаем команду выше, но уже на кластере:
```bash
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar -files mapper.py,reducer.py -mapper mapper.py -combiner reducer.py -reducer reducer.py -input /user/hduser/mapreduce_base_input/*.csv -output /user/hduser/mapreduce_base_output
```

Чтобы посмотреть на результаты выполним команды:
```bash
hdfs dfs -ls mapreduce_base_output
hdfs dfs -cat mapreduce_base_output/*
```

# Замеры скорости работы приложения и задействованные ресурсы

### Без использования Hadoop
### С использованием Hadoop Standalone
### С использованием кластер Hadoop

