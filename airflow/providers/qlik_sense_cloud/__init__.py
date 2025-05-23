def get_provider_info():
    return {
        "package-name": "airflow-provider-qlik-sense-cloud",
        "name": "Qlik Sense Cloud Airflow Provider",
        "description": 'Airflow package provider to reload apps/task/automation from Qlik Sense Cloud.', # Required
        "hook": [
            {
                "integration-name": "Qlik Cloud",
                "python-modules":["airflow.providers.qlik_sense_cloud.hooks.qlik_sense_hook.QlikSenseHook"]

            }
            ],
        "operators":[
                {
                "integration-name": "Qlik Cloud Reload",
                "python-modules":["airflow.providers.qlik_sense_cloud.operators.qlik_sense_cloud_reload"]
            },
            {
                "integration-name": "Qlik Cloud Automation",
                "python-modules":["airflow.providers.qlik_sense_cloud.operators.qlik_sense_cloud_automation"]
            },
            {
                "integration-name": "Qlik Cloud Report",
                "python-modules":["airflow.providers.qlik_sense_cloud.operators.qlik_sense_cloud_report"]
            },
        ],
        'connection-types': [
            {
                'hook-class-name': 'airflow.providers.qlik_sense_cloud.hooks.qlik_sense_hook.QlikSenseHook',
                'connection-type': 'qlik_sense_cloud',
            }
        ],
        "versions": ["0.0.2"]
    }