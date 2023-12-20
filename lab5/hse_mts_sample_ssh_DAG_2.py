from datetime import timedelta, datetime
import airflow
from threading import Lock
from airflow import DAG
from airflow.providers.ssh.operators.ssh import SSHOperator
from airflow.providers.ssh.hooks.ssh import SSHHook

default_args = {
            'owner': 'airflow',
            'depends_on_past': False,
            'email': ['airflow@example.com'],
            'email_on_failure': False,
            'email_on_retry': False,
            'start_date': '2023-12-20',
            'retries': 1,
            'retry_delay': timedelta(minutes=6000),
            'catchup': False
}

dag = DAG(dag_id='testing_stuff_2',
          default_args=default_args,
          schedule='50 * * * *',
          dagrun_timeout=timedelta(seconds=6000))

LINK_HADOOP = "/usr/local/hadoop/bin/hadoop"
LINK_HDFS = "/usr/local/hadoop/bin/hdfs"
HW3_MAPPER = "https://raw.githubusercontent.com/nastyaromanova/MSBDP/main/lab3/mapper.py"
HW3_REDUCER = "https://raw.githubusercontent.com/nastyaromanova/MSBDP/main/lab3/reducer.py"
DATABASE = "https://media.githubusercontent.com/media/shaprunovk/data_for_misobd/master/dataset.csv"
DATABASE_TEST = "https://gist.githubusercontent.com/polarnights/c04ef82e66ec86120d8d5f6bbc0348d9/raw/8c64d15acceb3667ffe2773a841ea98ef5334992/dataset.csv"

t0_bash = """
if { set -C; 2>/dev/null >~/manual_lock.lock; }; then
    echo "Lock acquired!!! :D"
else
    echo "Lock file exists... exiting"
    exit 1
fi
"""

t1_bash = f"""
wget {DATABASE_TEST} -O dataset.csv && \
wget {HW3_MAPPER} -O mapper.py && \
wget {HW3_REDUCER} -O reducer.py
"""

t2_bash = f"""
{LINK_HDFS} dfs -mkdir /user && \
{LINK_HDFS} dfs -mkdir /user/hadoop && \
{LINK_HDFS} dfs -mkdir /user/hadoop/mapreduce_base_input && \
{LINK_HDFS} dfs -put ./dataset.csv /user/hadoop/mapreduce_base_input
"""

t3_bash = f"""
{LINK_HADOOP} jar 
/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar \
-mapper mapper.py \
-reducer reducer.py \
-input /user/hadoop/mapreduce_base_input/dataset.csv \
-output /user/hadoop/mapreduce_base_output
"""

t4_bash = f"{LINK_HDFS} dfs -cat /user/hadoop/mapreduce_base_output/*"

t5_bash = "source /home/airflow/venv/bin/activate && python3 spark.py"
t6_bash = f"{LINK_HDFS} dfs -ls 
/user/hadoop/mapreduce_base_output/dataset_formatted.json"

t7_bash = f"{LINK_HDFS} dfs -rm -r /user/hadoop/mapreduce_base_input/* && 
rm mapper.py && rm reducer.py"
t8_bash = f"{LINK_HDFS} dfs -rm -r /user/hadoop/mapreduce_base_output"

t9_bash = f'rm -f ~/manual_lock.lock'

t0 = SSHOperator(ssh_conn_id='ssh_default',
                 task_id='lock_tasks',
                 command=t0_bash,
                 dag=dag)

t1 = SSHOperator(ssh_conn_id='ssh_default',
                 task_id='get_data_and_mr',
                 command=t1_bash,
                 cmd_timeout=600,
                 banner_timeout=200,
                 dag=dag)

t2 = SSHOperator(ssh_conn_id='ssh_default',
                 task_id='load_to_hdfs',
                 command=t2_bash,
                 cmd_timeout=3000,
                 dag=dag)

t3 = SSHOperator(ssh_conn_id='ssh_default',
                 task_id='run_mr_job',
                 command=t3_bash,
                 cmd_timeout=3000,
                 dag=dag)

t4 = SSHOperator(ssh_conn_id='ssh_default',
                 task_id='show_results',
                 command=t4_bash,
                 dag=dag)

t5 = SSHOperator(ssh_conn_id='ssh_default',
                 task_id='execute_spark',
                 command=t5_bash,
                 dag=dag)

t6 = SSHOperator(ssh_conn_id='ssh_default',
                 task_id='show_json_results',
                 command=t6_bash,
                 dag=dag)

t7 = SSHOperator(ssh_conn_id='ssh_default',
                 task_id='remove_data',
                 command=t7_bash,
                 dag=dag)

t8 = SSHOperator(ssh_conn_id='ssh_default',
                 task_id='remove_results',
                 command=t8_bash,
                 dag=dag)

t9 = SSHOperator(ssh_conn_id='ssh_default',
                 task_id='unlock_tasks',
                 command=t9_bash,
                 dag=dag)


t0 >> t1 >> t2 >> t3 >> t4 >> t5 >> t6 >> t7 >> t8 >> t9