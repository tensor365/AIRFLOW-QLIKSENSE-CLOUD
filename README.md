<p align="center" style="vertical-align:center;">

<img src="https://github.com/tensor365/AIRFLOW-QLIKSENSE-CLOUD/assets/13502563/780adaa3-9e0b-40e9-862f-7b0a3bb787a9" alt="qlik">

  
</p>

<h1 align="center">
  Airflow: Qlik Sense Cloud Provider
</h1>
  <h3 align="center">
    Qlik Sense Cloud Provider to reload application, automation from Airflow.
</h3>

<br/>

This repository provides basic qlik sense cloud hook and operators to trigger reloads of applications, automations, or tasks available in a Qlik Sense Cloud tenant.

## Road Map 

In development:

☑ Adding Qlik Talend Cloud Operator (Waiting new tenant to add it)

Test-Phase:

☑ Adding Report Operator (Added in production)
☑ Comptability with Airflow 3.0.1 (Added in production)


## Warnings

For version superior to Airflow 3.0.0, please use version superior to 0.0.7
For version below to Airflow 3.0.0, please use version under 0.0.7

## Requirements

The package has been tested with Python 3.9.

|  Package       |  Version  |
|----------------|-----------|
| apache-airflow | >2.10      |
| qlik-sdk       | >= 0.14.0 |

You also need a Qlik Sense Cloud tenant with API key activated. To get more informations about how to activate API key on Qlik Sense Cloud Tenant, see this section.


## How to install it ?


To install it, download and unzip source and launch the following pip install command: 

By using Pypi

```bash
pip install airflow-provider-qlik-sense-cloud
```

By Local Install

```bash
pip install .
```

You can also use 

```bash
python setup.py install
```

## How to use it ?
<br/>

To create connection, you need to get a API Token and your Qlik Cloud Tenant Activation

<br/>

### 1. Generating API Keys
<br/>
Follow these steps to get API Keys:
<br/>
<br/>

**Step 1**: Login to your Qlik Sense Cloud Tenant. 

**Step 2**: Click on your account logo and go into _Profile_. 

![parameters_demo](https://user-images.githubusercontent.com/13502563/198839712-37ae74df-da8f-47dc-9914-7b441e97170e.png)


**Step 3**: Go into API keys section.

![api_key](https://user-images.githubusercontent.com/13502563/198839717-628ed851-13f2-4972-a15e-7c67cd2e58ec.png)


<br/>

**Step 4**: Generate a new key.

![generate_api_key_1](https://user-images.githubusercontent.com/13502563/198839726-663f7a9c-59e0-480a-81c1-f9e9eb45f42d.png)

<br/>

**Step 5**: Give a description and an expiration date **_( ⚠️⚠️⚠️ Choose an expiration date with enough delay to avoid refresh all the time the token API ⚠️⚠️⚠️)_**.


![generate_api_key_2](https://user-images.githubusercontent.com/13502563/198839738-ef8190a5-0c3f-479a-84f7-08677bfe0f13.png)

<br/>

**Step 6**: The API key is displaying, copy it and save it.

![copyAPIKey](https://user-images.githubusercontent.com/13502563/198839741-5b004316-33c2-43aa-983a-904e55845529.png)

<br/>
<br/>

### 2. Get tenant id

**Step 1**: Login to your Qlik Sense Cloud Tenant and go into _About_ Section by clicking on your profile icon.

![about_tenant](https://user-images.githubusercontent.com/13502563/198840307-32b74dea-970e-4b94-a724-13077fa84e49.png)

**Step 2**: Get the value of your tenant hostname

![QlikSenseCloudTenantId](https://user-images.githubusercontent.com/13502563/198839951-bb479fc2-a05b-4a02-b200-4bb5c3d250aa.png)

### 3. Creating Qlik Sense Cloud Connection in Airflow

**Step 1**: Login to your Airflow Webserver. Go into _Admin_ > _Connection_ and creation a new connection by cliking on add icon.

<br/>

**Step 2**: Give a name to your connection id and selection Qlik Sense Cloud in _Connection Type_. Add tenant id hostname (without https) and Token API Key that you copy in Section 1 and 2.

![airflow_connection_illustration](https://user-images.githubusercontent.com/13502563/198840215-9d083b67-7778-4c69-9ca6-166901a2766e.png)


<br/>
<br/>




### 4. Example: Creating a DAG with Qlik Sense Cloud Operator to reload App 

You can now use the operators in your dags to trigger action in Qlik Sense Cloud from Airflow

Example: 


```python
from airflow import DAG
from airflow.providers.qlik_sense_cloud.operators.qlik_sense_cloud_reload import QlikSenseCloudReloadOperator
import pendulum
from datetime import timedelta
from textwrap import dedent


# [START default_args]
# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'schedule_interval':'@daily',

    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}
# [END default_args]


# [START instantiate_dag]
with DAG('test-airflow',
        default_args=default_args,
        description='A simple tutorial DAG to try',
        start_date=start_date=pendulum.datetime(2021, 1, 1, 10, 40, 0, tz="Europe/Paris"),tags=['qlik','example']) as dag:

        t1 = QlikSenseCloudReloadOperator(task_id='reload_app',appId='4d5ad6d0-92a1-47c3-b57d-5a07945377f8',qlik_sense_cloud_config_id='qliksensecloud')

        t1
# [END instantiate_dag]
```

<br/>

### 5. Example: Creating a DAG with Qlik Sense Cloud Operator to reload Qlik Automation and to send a Qlik Report

Here's an example of DAG using operator to reload automation 

```python

from airflow import DAG
from airflow.providers.qlik_sense_cloud.operators.qlik_sense_cloud_automation import QlikSenseCloudAutomationOperator
from airflow.providers.qlik_sense_cloud.operators.qlik_sense_cloud_report import QlikSenseCloudReportOperator

import pendulum
from datetime import timedelta
from textwrap import dedent

# [START default_args]
# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}
# [END default_args]


# [START instantiate_dag]
with DAG('test-automation-report',
        default_args=default_args,
        description='A simple tutorial DAG to try',
        start_date=start_date=pendulum.datetime(2021, 1, 1, 10, 40, 0, tz="Europe/Paris"),tags=['qlik','example']) as dag:
          
	t1 = QlikSenseCloudAutomationOperator(task_id='reload_automation',automationId='bab86470-578a-11ed-bee3-db20e15c9fd8',qlik_sense_cloud_config_id='qliksensecloud')

  	t2 = QlikSenseCloudReportOperator(task_id='reload_report',reportId='65f810a9e0f4697cb54b6e87',qlik_sense_cloud_config_id='qliksensecloud')

	t1 >> t2

```

### 6. (Appendix) Activate API Key on Qlik Sense Cloud Tenant

To get more informations about API Key in Qlik Sense Cloud, you can follow these topic:

https://qlik.dev/tutorials/generate-your-first-api-key


