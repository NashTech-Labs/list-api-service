from kubernetes import client, utils 
import kubernetes.client
from kubernetes.client import ApiClient

from kubernetes.client.rest import ApiException
from kubernetes import client, config

def __get_kubernetes_client(bearer_token,api_server_endpoint):
    try:
        configuration = kubernetes.client.Configuration()
        configuration.host = api_server_endpoint
        configuration.verify_ssl = False
        configuration.api_key = {"authorization": "Bearer " + bearer_token}
        client.Configuration.set_default(configuration)
        with kubernetes.client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
            api_instance1 = kubernetes.client.ApiregistrationV1Api(api_client)
        return api_instance1

    except ApiException as e:
        print("Error getting kubernetes client:\n{}".format(e.body))
        print("TYPE :{}".format(type(e)))
        return None

def __format_data_for_cluster_role(client_output):
        temp_dict={}
        temp_list=[]
        
        json_data=ApiClient().sanitize_for_serialization(client_output)
        if len(json_data["items"]) != 0:
            for ls in json_data["items"]:
                temp_dict={
                    "name": ls["metadata"]["name"],  

                }
                temp_list.append(temp_dict)
        return temp_list


def get_api_services(cluster_details,namespace="default",all_namespaces=False):
        client_api= __get_kubernetes_client(
            bearer_token=cluster_details["bearer_token"],
            api_server_endpoint=cluster_details["api_server_endpoint"],
        )
        
        daemonset_list =client_api.list_api_service()
        data=__format_data_for_cluster_role(daemonset_list)
        print("list all the api services: {}".format(data))
       
if __name__ == '__main__':
    cluster_details={
        "bearer_token":"GKE-Bearer-Token",
        "api_server_endpoint":"Ip-k8s-control-plane"
    }
    get_api_services(cluster_details)