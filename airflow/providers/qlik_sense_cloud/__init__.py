## This is needed to allow Airflow to pick up specific metadata fields it needs for certain features. We recognize it's a bit unclean to define these in multiple places, but at this point it's the only workaround if you'd like your custom conn type to show up in the Airflow UI.
def get_provider_info():
    return {
        "package-name": "airflow-provider-qlik-sense-cloud", # Required
        "name": "Qlik Sense Cloud Airflow Provider", # Required
        "description": 'Airflow package provider to reload apps/task/automation from Qlik Sense Cloud.', # Required
        "hook": [
            {
                "integration-name": "Qlik Cloud",
                "python-modules":"airflow.providers.qlik_sense_cloud.hooks.qlik_sense_hook.QlikSenseHook"

            }
            ],
        "operators":[
                {
                "integration-name": "Qlik Cloud",
                "python-modules":"airflow.providers.qlik_sense_cloud.operators.qlik_sense_cloud_reload.QlikSenseCloudReloadOperator"

            }
        ],
        'connection-types': [
            {
                'hook-class-name': 'airflow.providers.qlik_sense_cloud.hooks.qlik_sense_hook.QlikSenseHook',
                'connection-type': 'qlik_sense_cloud',
            }
        ],
        #"extra-links": ["qlik_sense_cloud.operators.sample_operator.ExtraLink"],
        "versions": ["0.0.1"] # Required
    }