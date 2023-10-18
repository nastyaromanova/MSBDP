# Изменение использованного пространства на локальной ФС (фактор репликации 3)
```
hadoop@mts-hse-de-course-team-9-1:~$ hdfs dfs -put testfile /test/testfile
```

1. haddop1
```
hadoop@mts-hse-de-course-team-9-1:~$ du -shkb /hadoop/hdfs/datanode/
4096	/hadoop/hdfs/datanode/
hadoop@mts-hse-de-course-team-9-1:~$ du -shkb /hadoop/hdfs/namenode/
2107348	/hadoop/hdfs/namenode/
```

2. haddop2
```
team9@mts-hse-de-course-team-9-2:~$ sudo du -shkb /hadoop/hdfs/datanode/
132536	/hadoop/hdfs/datanode/
team9@mts-hse-de-course-team-9-2:~$ sudo du -shkb /hadoop/hdfs/namenode
4096	/hadoop/hdfs/namenode/
```

3. haddop3
```
team9@mts-hse-de-course-team-9-3:~$ sudo du -shkb /hadoop/hdfs/datanode
132517	/hadoop/hdfs/datanode/
team9@mts-hse-de-course-team-9-3:~$ sudo du -shkb /hadoop/hdfs/namenode/
4096	/hadoop/hdfs/namenode/
```

# Инструкция по установке

_Все действия делаем с sudo. Блоки, которые необходимо выполнить на всех трех нодах помечены через *._
 
1. Настроим брандмауэр (*)
```
iptables-legacy -I INPUT -p tcp --dport 9870 -j ACCEPT
iptables-legacy -I INPUT -p tcp --dport 8020 -j ACCEPT
iptables-legacy -I INPUT -p tcp --match multiport --dports 9866,9864,9867 -j ACCEPT
apt install iptables-persistent
netfilter-persistent save
```
 
2. Добавляем в /etc/hosts такие строчки (*)
```
10.0.10.28 haddop1
10.0.10.29 haddop2
10.0.10.30 haddop3
```
 
3. Устанавливаем java (*)
```
apt install default-jdk
```
 
4. Устанавливаем hadoop (*)
```
wget https://dlcdn.apache.org/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz
mkdir /usr/local/hadoop
tar -zxf hadoop-*.tar.gz -C /usr/local/hadoop --strip-components 1
```
 
5. Создаем пользователя hadoop (*)
```
useradd hadoop -m
passwd XXX // пишем пароль XXX (не hadoop!)
chown -R hadoop:hadoop /usr/local/hadoop
```
 
6. Добавляем профиль в /etc/profile.d/hadoop.sh (*)
```
export HADOOP_HOME=/usr/local/hadoop
export HADOOP_HDFS_HOME=$HADOOP_HOME
export HADOOP_MAPRED_HOME=$HADOOP_HOME
export HADOOP_COMMON_HOME=$HADOOP_HOME
export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native
export HADOOP_OPTS="$HADOOP_OPTS -Djava.library.path=$HADOOP_HOME/lib/native"
export YARN_HOME=$HADOOP_HOME
export PATH="$PATH:${HADOOP_HOME}/bin:${HADOOP_HOME}/sbin"
```

7. Меняем /usr/local/hadoop/etc/hadoop/hadoop-env.sh (*)

В `/usr/local/hadoop/etc/hadoop/hadoop-env.sh` меняем `export JAVA_HOME=` на `export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64`
и добавляем в конец
```
export HDFS_NAMENODE_USER="hadoop"
export HDFS_DATANODE_USER="hadoop"
export HDFS_SECONDARYNAMENODE_USER="hadoop"
export YARN_RESOURCEMANAGER_USER="hadoop"
export YARN_NODEMANAGER_USER="hadoop"
```
 
8. Применяем эти настройки на пользователе (*)
```
su - hadoop
source /usr/local/hadoop/etc/hadoop/hadoop-env.sh
```
 
9. Создаем ssh ключи (*)
```
su - hadoop // password XXX
ssh-keygen
```
Теперь получившиеся ключи пробрасываем между тачек, чтобы без проблем заходить с одной на другую без пароля
 
10. Создаем папку с данными (*)
```
mkdir -p /hadoop/hdfs/{datanode,namenode}
chown -R hadoop:hadoop /hadoop/hdfs
```
 
11. Меняем /usr/local/hadoop/etc/hadoop/core-site.xml (*)

В файле `/usr/local/hadoop/etc/hadoop/core-site.xml` меняем содержимое на следующее:
```
<configuration>
<property>
<name>fs.defaultFS</name>
<value>hdfs://haddop1:9000</value>
</property>
</configuration>
```
 
12. Меняем /usr/local/hadoop/etc/hadoop/hdfs-site.xml (*)

В файле `/usr/local/hadoop/etc/hadoop/hdfs-site.xml` меняем содержимое на следующее:
```
<configuration>
<property>
<name>dfs.replication</name>
<value>3</value>
</property>
<property>
<name>dfs.datanode.data.dir</name>
<value>file:///hadoop/hdfs/datanode</value>
</property>
</configuration>
```
 
13. Меняем только мастера

В файле `/usr/local/hadoop/etc/hadoop/mapred-site.xml` меняем содержимое на следующее:
```
<configuration>
<property>
<name>mapreduce.jobtracker.address</name>
<value>haddop1:54311</value>
</property>
<property>
<name>mapreduce.framework.name</name>
<value>yarn</value>
</property>
</configuration>
```
 
В файле `/usr/local/hadoop/etc/hadoop/yarn-site.xml` меняем содержимое на следующее: 
```
<configuration>
<property>
<name>yarn.nodemanager.aux-services</name>
<value>mapreduce_shuffle</value>
</property>
<property>
<name>yarn.nodemanager.aux-services.mapreduce.shuffle.class</name>
<value>org.apache.hadoop.mapred.ShuffleHandler</value>
</property>
<property>
<name>yarn.resourcemanager.hostname</name>
<value>haddop1</value>
</property>
</configuration>
```
 
 
В файле `/usr/local/hadoop/etc/hadoop/masters` меняем содержимое на следующее:
```
haddop1
```
 
В файле `/usr/local/hadoop/etc/hadoop/workers` меняем содержимое на следующее: 
```
localhost
haddop2
haddop3
```
 
13. Запускаем кластер
```
su - hadoop
cd /usr/local/hadoop
./bin/hdfs namenode -format
./sbin/start-dfs.sh
./sbin/start-yarn.sh
```
 
**Заходим на haddop1:9870 и все работает!**
