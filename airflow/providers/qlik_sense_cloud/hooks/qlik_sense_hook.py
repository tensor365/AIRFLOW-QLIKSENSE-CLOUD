from typing import Any, Callable, Dict, Optional, Union
import uuid

from qlik_sdk import (
    AuthType,
    Config,
    Qlik,
)

from airflow.exceptions import AirflowException
from airflow.hooks.base import BaseHook

class QlikSenseHook(BaseHook):
    """
 
    :param method: the API method to be called
    :type method: str
    :param sample_conn_id: connection that has the base API url i.e https://www.google.com/
        and optional authentication credentials. Default headers can also be specified in
        the Extra field in json format.
    :type sample_conn_id: str
    :param auth_type: The auth type for the service
    :type auth_type: AuthBase of python requests lib
    
    """

    conn_name_attr = 'sample_conn_id'
    default_conn_name = 'qlik_sense_default'
    conn_type = 'qlik_sense_cloud'
    hook_name = 'Qlik Sense Cloud'
    __qlik_connexion = None


    def __init__(self,conn_id: str = default_conn_name,auth_type: str = 'api_key',) -> None:
        super().__init__()
        self.conn_id = conn_id
        self.base_url: str = ""
        self.auth_type: str = auth_type

    def test_connection(self) -> tuple[bool, str]:
        """Test the access to tenant Qlik Sense Cloud."""
        try:
            conn = self.get_conn()
            user = conn.users.get_me()
            return True, f"Connection successfully tested with user: {user.name}"
        except Exception as e:
            return False, str(e)


    def get_status_reload_app(self, reloadId: str):
        """
        
        Getting status from an app reload    

        """
        
        if self.__qlik_connexion is None:
            self.get_conn()
        
        ans = self.__qlik_connexion.reloads.get(reloadId=reloadId)
        return ans

    def reload_app(self, appId: str, partial=False):
        """

        Triggering an app reload
        
        """

        if self.__qlik_connexion is None:
            self.get_conn()
        
        ans = self.__qlik_connexion.reloads.create(data={"appId":appId, "partial": partial})
        
        return ans
    
    def get_status_reload_automation(self, automationId: str ,runId: str):
        """
        
        Getting status from an automation reload    

        """
        
        if self.__qlik_connexion is None:
            self.get_conn()
        
        automation = self.__qlik_connexion.automations.get(id=automationId)        
        
        ans = automation.get_run(runId=runId)
        return ans

    def reload_automation(self, automationId: str, input: dict={}):
        """
        
        Triggering an automation reload
        
        """

        if self.__qlik_connexion is None:
            self.get_conn()

        automation = self.__qlik_connexion.automations.get(id=automationId)        
        
        ans = automation.create_run({
                                "id": self.__generate_uuid(),
                                "inputs": self.input,
                                "context": "api"
                                })

        return ans
    
    def send_report(self, reportId: str):
        """
        
        Trigger a send of Qlik Sense Report Service from Airflow
  
        """

        if self.__qlik_connexion is None:
            self.get_conn()

        ans = self.__qlik_connexion.rest(path='/sharing-tasks/actions/execute', method='POST', data={"sharingTaskID": reportId})
        return ans

    def __generate_uuid():
        return str(uuid.uuid4())
        
    def get_conn(self):
        """

        Initializing the Qlik Connection Interface
    
        """

        if self.conn_id:
            conn = self.get_connection(self.conn_id)

            host = conn.host if conn.host else ""
            if not host.startswith('https://'):
                host = 'https://' + host

            config = Config(host=host, auth_type=AuthType.APIKey, api_key=conn.password)
            self.__qlik_connexion =  Qlik(config=config)
        
    @staticmethod
    def get_ui_field_behaviour() -> Dict:
            """Returns custom field behaviour"""
            import json

            return {
                "hidden_fields": ['port', 'login', 'extra', 'schema',],
                "relabeling": {'password':'Qlik Sense Token API', 'host':'Qlik Sense Cloud Tenant',},
                "placeholders": {
                    'host': 'Tenant Id URI',  
                    'password': 'API Token'
                },
            }