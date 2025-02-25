import requests

# Base URL of the xApp
BASE_URL = "http://localhost:8081"

def get_pods():
    response = requests.get(f"{BASE_URL}/pods")
    if response.status_code == 200:
        pods = response.json()
        print("Pods Information:")
        for pod in pods:
            print(f"Pod Name: {pod['name']}, Namespace: {pod['namespace']}, Status: {pod['status']}, Node: {pod['node_name']}")
    else:
        print("Failed to retrieve pods information")

def get_services():
    response = requests.get(f"{BASE_URL}/services")
    if response.status_code == 200:
        services = response.json()
        print("\nServices Information:")
        for service in services:
            print(f"Service Name: {service['name']}, Namespace: {service['namespace']}, Type: {service['type']}, Cluster IP: {service['cluster_ip']}")
    else:
        print("Failed to retrieve services information")

def get_containers():
    response = requests.get(f"{BASE_URL}/containers")
    if response.status_code == 200:
        containers = response.json()
        print("\nContainers Information:")
        for container in containers:
            print(f"Pod Name: {container['pod_name']}, Namespace: {container['namespace']}, Container Name: {container['container_name']}")
            print(f"    Image: {container['image']}")
            print(f"    Ports: {container['ports']}")
            if container['env']:
                print(f"    Environment Variables: {container['env']}")
            else:
                print("    Environment Variables: None")
    else:
        print("Failed to retrieve containers information")

if __name__ == "__main__":
    get_pods()
    get_services()
    get_containers()
