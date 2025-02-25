from kubernetes import client, config
from flask import Flask, jsonify

app = Flask(__name__)

# Load Kubernetes configuration
config.load_kube_config()

v1 = client.CoreV1Api()

@app.route('/containers', methods=['GET'])
def get_containers():
    pods = v1.list_pod_for_all_namespaces(watch=False)
    container_list = []
    for pod in pods.items:
        for container in pod.spec.containers:
            container_info = {
                "pod_name": pod.metadata.name,
                "namespace": pod.metadata.namespace,
                "container_name": container.name,
                "image": container.image,
                "ports": [port.container_port for port in container.ports] if container.ports else [],
                "env": [{env.name: env.value} for env in container.env] if container.env else []
            }
            container_list.append(container_info)
    return jsonify(container_list)

@app.route('/pods', methods=['GET'])
def get_pods():
    pods = v1.list_pod_for_all_namespaces(watch=False)
    pod_list = []
    for pod in pods.items:
        pod_info = {
            "name": pod.metadata.name,
            "namespace": pod.metadata.namespace,
            "status": pod.status.phase,
            "node_name": pod.spec.node_name
        }
        pod_list.append(pod_info)
    return jsonify(pod_list)

@app.route('/services', methods=['GET'])
def get_services():
    services = v1.list_service_for_all_namespaces(watch=False)
    service_list = []
    for service in services.items:
        service_info = {
            "name": service.metadata.name,
            "namespace": service.metadata.namespace,
            "type": service.spec.type,
            "cluster_ip": service.spec.cluster_ip,
        }
        service_list.append(service_info)
    return jsonify(service_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
