from typing import Any, Callable, Dict, Optional, Union

import requests
from requests.auth import HTTPBasicAuth

from airflow.exceptions import AirflowException
from airflow.hooks.base import BaseHook


class QlikSenseHook(BaseHook):
    """
    Sample Hook that interacts with an HTTP endpoint the Python requests library.

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

    def __init__(self,method: str = 'POST',conn_id: str = default_conn_name,auth_type: Any = HTTPBasicAuth,) -> None:
        super().__init__()
        self.conn_id = conn_id
        self.method = method.upper()
        self.base_url: str = ""
        self.auth_type: Any = auth_type


    def get_conn(self) -> requests.Session:
        """
        Returns http session to use with requests.

        :param headers: additional headers to be passed through as a dictionary
        :type headers: dict
        """
        session = requests.Session()

        if self.conn_id:
            conn = self.get_connection(self.conn_id)

            host = conn.host if conn.host else ""
            self.base_url = "https://" + host

            headers = {'Authorization': 'Bearer ' + conn.password,'Content-Type': 'application/json'}
            self.log.info("Token api %s", conn.password)

            session.headers.update(headers)

        return session

    def run(
        self,
        endpoint: Optional[str] = None,
        data: Optional[Union[Dict[str, Any], str]] = None,
        headers: Optional[Dict[str, Any]] = None,
        **request_kwargs: Any,
    ) -> Any:
        r"""
        Performs the request

        :param endpoint: the endpoint to be called i.e. resource/v1/query?
        :type endpoint: str
        :param data: payload to be uploaded or request parameters
        :type data: dict
        :param headers: additional headers to be passed through as a dictionary
        :type headers: dict
        """

        session = self.get_conn()

        if self.base_url and not self.base_url.endswith('/') and endpoint and not endpoint.startswith('/'):
            url = self.base_url + '/' + endpoint
        else:
            url = (self.base_url or '') + (endpoint or '')

        if self.method == 'GET':
            # GET uses params
            req = requests.Request(
                self.method, url, headers=headers)
        else:
            # Others use data
            import json
            req = requests.Request(
                self.method, url, data=json.dumps(data), headers=headers)


        self.log.info("Sending '%s' to url: %s", self.method, url)

        prepped = session.prepare_request(req)
        try:

            response = session.send(prepped)
            return response

        except requests.exceptions.ConnectionError as ex:
            self.log.warning(
                '%s Tenacity will retry to execute the operation', ex)
            raise ex


    @staticmethod
    def get_ui_field_behaviour() -> Dict:
            """Returns custom field behaviour"""
            import json

            return {
                "hidden_fields": ['port', 'login', 'extra', 'schema',],
                "relabeling": {'password':'Qlik Sense Token API', 'host':'Qlik Sense Cloud Tenant',},
                "placeholders": {
                    'host': 'tenant id without https',  
                    'password': 'API Token'
                },
            }