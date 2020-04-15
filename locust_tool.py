from locust import HttpLocust, TaskSet, between, task
from requests.auth import HTTPBasicAuth
from urllib import parse

import os
from functions import *

ACCESS_KEY = os.environ.get('ACCESS_KEY', 'token-9smjr')
SECRET_KEY = os.environ.get('SECRET_KEY', '9dqrwdrrqchcnbz9cffgcpgtz8tntqzql5tk9kx5w4fv9lr4qxt9qq')
BASE_URL = os.environ.get('BASE_URL', 'https://139.129.101.66/')
DURATION = os.environ.get('DURATION', '7d')


top_url = parse.urljoin(BASE_URL, get_expression('top_url_body'))
range_url = parse.urljoin(BASE_URL, get_expression('range_url_body'))


class UserTasks(TaskSet):

    @task
    def cluster_cpu_util_top5(self):
        cluster_cpu_top5_params = get_top_query_with_params('cluster_cpu_top')
        response = self.client.get(top_url, name='cluster_cpu_util_top5', auth=HTTPBasicAuth(ACCESS_KEY, SECRET_KEY),
                                   params=cluster_cpu_top5_params, verify=False)
        get_error_logs(response)
        params = get_range_query_with_params(response, 'cluster_cpu_util', 'prometheus_from')
        return params

    @task
    def cluster_cpu_util(self):
        # cluster_cpu_params = get_range_query_with_params('cluster_cpu_top', 'cluster_cpu', 'prometheus_from')
        params = self.cluster_cpu_util_top5
        response = self.client.get(range_url, name='cluster_cpu_util', auth=HTTPBasicAuth(ACCESS_KEY, SECRET_KEY),
                                   params=params, verify=False)
        get_error_logs(response)


    @task
    def cluster_mem_top5(self):
        cluster_mem_top5_params = get_top_query_with_params('cluster_memory_top')
        response = self.client.get(top_url, name='cluster_mem_top5', auth=HTTPBasicAuth(ACCESS_KEY, SECRET_KEY),
                                   params=cluster_mem_top5_params, verify=False)
        get_error_logs(response)

    @task
    def cluster_mem_util(self):
        cluster_mem_params = get_range_query_with_params('cluster_memory_top', 'cluster_memory', 'prometheus_from')
        response = self.client.get(range_url, name='cluster_mem_util', auth=HTTPBasicAuth(ACCESS_KEY, SECRET_KEY),
                                   params=cluster_mem_params, verify=False)
        get_error_logs(response)

    @task
    def cluster_disk_top5(self):
        cluster_disk_top5_params = get_top_query_with_params('cluster_disk_top')
        response = self.client.get(top_url, name='cluster_disk_top5', auth=HTTPBasicAuth(ACCESS_KEY, SECRET_KEY),
                                   params=cluster_disk_top5_params, verify=False)
        get_error_logs(response)

    @task
    def cluster_disk_utilization(self):
        cluster_disk_params = get_range_query_with_params('cluster_disk_top', 'cluster_disk', 'prometheus_from')
        response = self.client.get(range_url, name='cluster_disk_utilization',
                                   auth=HTTPBasicAuth(ACCESS_KEY, SECRET_KEY),
                                   params=cluster_disk_params, verify=False)
        get_error_logs(response)

    @task
    def cluster_leader_change_num_top5(self):
        cluster_leader_change_num_top5_params = get_top_query_with_params('cluster_leader_change_num_top')
        response = self.client.get(top_url, name='cluster_leader_change_num_top5',
                                   auth=HTTPBasicAuth(ACCESS_KEY, SECRET_KEY),
                                   params=cluster_leader_change_num_top5_params, verify=False)
        get_error_logs(response)

    @task
    def etcd_leader_change(self):
        cluster_leader_change_num_params = get_range_query_with_params('cluster_leader_change_num_top',
                                                                       'cluster_leader_change_num', 'prometheus_from')
        response = self.client.get(range_url, name='cluster_leader_change_num',
                                   auth=HTTPBasicAuth(ACCESS_KEY, SECRET_KEY),
                                   params=cluster_leader_change_num_params, verify=False)
        get_error_logs(response)

    @task
    def cluster_db_size_top5(self):
        cluster_db_size_top5_params = get_top_query_with_params('cluster_db_size_top')
        response = self.client.get(top_url, name='cluster_db_size_top5', auth=HTTPBasicAuth(ACCESS_KEY, SECRET_KEY),
                                   params=cluster_db_size_top5_params, verify=False)
        get_error_logs(response)

    @task
    def etcd_db_size(self):
        cluster_db_size_params = get_range_query_with_params('cluster_db_size_top', 'cluster_db_size', 'instance')
        response = self.client.get(range_url, name='cluster_db_size', auth=HTTPBasicAuth(ACCESS_KEY, SECRET_KEY),
                                   params=cluster_db_size_params, verify=False)
        get_error_logs(response)

    @task
    def cluster_api_server_latency_top5(self):
        cluster_api_server_latency_top5_params = get_top_query_with_params('cluster_api_server_latency_top')
        response = self.client.get(top_url, name='cluster_api_server_latency_top5',
                                   auth=HTTPBasicAuth(ACCESS_KEY, SECRET_KEY),
                                   params=cluster_api_server_latency_top5_params, verify=False)
        get_error_logs(response)

    @task
    def api_server_request_latency(self):
        cluster_api_server_latency_params = get_range_query_with_params('cluster_api_server_latency_top',
                                                                        'cluster_api_server_latency', 'instance')
        response = self.client.get(range_url, name='cluster_api_server_latency',
                                   auth=HTTPBasicAuth(ACCESS_KEY, SECRET_KEY),
                                   params=cluster_api_server_latency_params, verify=False)
        get_error_logs(response)

    @task
    def cluster_pod_restart_top5(self):
        cluster_pod_restart_top5_params = get_top_query_with_params('cluster_pod_restart_total_top')
        response = self.client.get(top_url, name='cluster_pod_restart_top5', auth=HTTPBasicAuth(ACCESS_KEY, SECRET_KEY),
                                   params=cluster_pod_restart_top5_params, verify=False)
        get_error_logs(response)

    @task
    def pod_restart(self):
        cluster_pod_restart_params = get_range_query_with_params('cluster_pod_restart_total_top',
                                                                 'cluster_pod_restart_total', 'prometheus_from')
        response = self.client.get(range_url, name='cluster_pod_restart', auth=HTTPBasicAuth(ACCESS_KEY, SECRET_KEY),
                                   params=cluster_pod_restart_params, verify=False)
        get_error_logs(response)

    @task
    def cluster_pod_unshedulable_top5(self):
        cluster_pod_nonschedulable_top5_params = get_top_query_with_params('cluster_pod_nonscheduled_total_top')
        response = self.client.get(top_url, name='cluster_pod_unshedulable_top5',
                                   auth=HTTPBasicAuth(ACCESS_KEY, SECRET_KEY),
                                   params=cluster_pod_nonschedulable_top5_params, verify=False)
        get_error_logs(response)

    @task
    def pod_unschedulable(self):
        cluster_pod_nonshedulable_params = get_range_query_with_params('cluster_pod_nonscheduled_total_top',
                                                                       'cluster_pod_nonscheduled_total',
                                                                       'prometheus_from')
        response = self.client.get(range_url, name='cluster_pod_unshedulable',
                                   auth=HTTPBasicAuth(ACCESS_KEY, SECRET_KEY),
                                   params=cluster_pod_nonshedulable_params, verify=False)
        get_error_logs(response)

    @task
    def cluster_pod_unhealthy_top5(self):
        cluster_pod_unhealthy_top5_params = get_top_query_with_params('cluster_unhealthy_pod_num_top')
        response = self.client.get(top_url, name='cluster_pod_unhealthy_top5',
                                   auth=HTTPBasicAuth(ACCESS_KEY, SECRET_KEY),
                                   params=cluster_pod_unhealthy_top5_params, verify=False)
        get_error_logs(response)

    @task
    def pod_unhealthy(self):
        cluster_pod_unhealthy_params = get_range_query_with_params('cluster_unhealthy_pod_num_top',
                                                                   'cluster_unhealthy_pod_num', 'prometheus_from')
        response = self.client.get(range_url, name='cluster_pod_unhealthy', auth=HTTPBasicAuth(ACCESS_KEY, SECRET_KEY),
                                   params=cluster_pod_unhealthy_params, verify=False)
        get_error_logs(response)

    @task
    def node_load_top5(self):
        node_load_top5_params = get_top_query_with_params('node_load_top')
        response = self.client.get(top_url, name='node_load_top5', auth=HTTPBasicAuth(ACCESS_KEY, SECRET_KEY),
                                   params=node_load_top5_params, verify=False)
        get_error_logs(response)

    @task
    def node_load(self):
        node_load_params = get_range_query_with_params('node_load_top', 'node_load', 'node_id')
        response = self.client.get(range_url, name='node_load', auth=HTTPBasicAuth(ACCESS_KEY, SECRET_KEY),
                                   params=node_load_params, verify=False)
        get_error_logs(response)

    @task
    def node_disk(self):
        node_disk = get_top_expression_dict('node_disk')
        response = self.client.get(top_url, name='node_disk_util', auth=HTTPBasicAuth(ACCESS_KEY, SECRET_KEY),
                                   params=node_disk, verify=False)
        get_error_logs(response)

    @task
    def node_cpu(self):
        node_cpu = get_top_expression_dict('node_cpu')
        response = self.client.get(top_url, name='node_cpu', auth=HTTPBasicAuth(ACCESS_KEY, SECRET_KEY),
                                   params=node_cpu, verify=False)
        get_error_logs(response)

    @task
    def node_mem(self):
        node_memory = get_top_expression_dict('node_memory')
        response = self.client.get(top_url, name='node_mem', auth=HTTPBasicAuth(ACCESS_KEY, SECRET_KEY),
                                   params=node_memory, verify=False)
        get_error_logs(response)

    @task
    def node_disk_write_top(self):
        node_disk_write_top5_params = get_top_query_with_params('node_disk_write_top')
        response = self.client.get(top_url, name='node_disk_write_top', auth=HTTPBasicAuth(ACCESS_KEY, SECRET_KEY),
                                   params=node_disk_write_top5_params, verify=False)
        get_error_logs(response)

    @task
    def node_disk_write(self):
        node_disk_write_params = get_range_query_with_params('node_disk_write_top', 'node_disk_write', 'node_id')
        response = self.client.get(range_url, name='node_disk_write', auth=HTTPBasicAuth(ACCESS_KEY, SECRET_KEY),
                                   params=node_disk_write_params, verify=False)
        get_error_logs(response)

    @task
    def node_disk_read_top(self):
        node_disk_read_top5_params = get_top_query_with_params('node_disk_read_top')
        response = self.client.get(top_url, name='node_disk_read_top', auth=HTTPBasicAuth(ACCESS_KEY, SECRET_KEY),
                                   params=node_disk_read_top5_params, verify=False)
        get_error_logs(response)

    @task
    def node_disk_read(self):
        node_disk_read_params = get_range_query_with_params('node_disk_read_top', 'node_disk_read', 'node_id')
        response = self.client.get(range_url, name='node_disk_read', auth=HTTPBasicAuth(ACCESS_KEY, SECRET_KEY),
                                   params=node_disk_read_params, verify=False)
        get_error_logs(response)

    @task
    def node_network_transmit_rate_top(self):
        node_network_transmit_rate_top5_params = get_top_query_with_params('node_network_transmit_rate_top')
        response = self.client.get(top_url, name='node_network_transmit_rate_top',
                                   auth=HTTPBasicAuth(ACCESS_KEY, SECRET_KEY),
                                   params=node_network_transmit_rate_top5_params, verify=False)
        get_error_logs(response)

    @task
    def node_network_transmit_rate(self):
        node_network_transmit_rate_params = get_range_query_with_params('node_network_transmit_rate_top',
                                                                        'node_network_transmit_rate', 'node_id')
        response = self.client.get(range_url, name='node_network_transmit_rate',
                                   auth=HTTPBasicAuth(ACCESS_KEY, SECRET_KEY),
                                   params=node_network_transmit_rate_params, verify=False)
        get_error_logs(response)

    @task
    def node_network_receive_rate_top(self):
        node_network_receive_rate_top_params = get_top_query_with_params('node_network_receive_rate_top')
        response = self.client.get(top_url, name='node_network_receive_rate_top',
                                   auth=HTTPBasicAuth(ACCESS_KEY, SECRET_KEY),
                                   params=node_network_receive_rate_top_params, verify=False)
        get_error_logs(response)

    @task
    def node_network_receive_rate(self):
        node_network_receive_rate_params = get_range_query_with_params('node_network_receive_rate_top',
                                                                       'node_network_receive_rate', 'node_id')
        response = self.client.get(range_url, name='node_network_receive_rate',
                                   auth=HTTPBasicAuth(ACCESS_KEY, SECRET_KEY),
                                   params=node_network_receive_rate_params, verify=False)
        get_error_logs(response)

    @task
    def pod_network_transmit_top(self):
        pod_network_transmit_top_params = get_top_query_with_params('pod_network_transmit_top')
        response = self.client.get(top_url, name='pod_network_transmit_top', auth=HTTPBasicAuth(ACCESS_KEY, SECRET_KEY),
                                   params=pod_network_transmit_top_params, verify=False)
        get_error_logs(response)

    @task
    def pod_network_transmit(self):
        pod_network_transmit_params = get_range_query_with_params('pod_network_transmit_top', 'pod_network_transmit',
                                                                  'pod_id')
        response = self.client.get(range_url, name='pod_network_transmit', auth=HTTPBasicAuth(ACCESS_KEY, SECRET_KEY),
                                   params=pod_network_transmit_params, verify=False)
        get_error_logs(response)

    @task
    def pod_network_receive_top(self):
        pod_network_receive_top_params = get_top_query_with_params('pod_network_receive_top')
        response = self.client.get(top_url, name='pod_network_receive_top', auth=HTTPBasicAuth(ACCESS_KEY, SECRET_KEY),
                                   params=pod_network_receive_top_params, verify=False)
        get_error_logs(response)

    @task
    def pod_network_receive(self):
        pod_network_receive_params = get_range_query_with_params('pod_network_receive_top', 'pod_network_receive',
                                                                 'pod_id')
        response = self.client.get(range_url, name='pod_network_receive', auth=HTTPBasicAuth(ACCESS_KEY, SECRET_KEY),
                                   params=pod_network_receive_params, verify=False)
        get_error_logs(response)

    @task
    def pod_memory_utilization_top(self):
        pod_memory_utilization_top_params = get_top_query_with_params('pod_memory_utilization_top')
        response = self.client.get(top_url, name='pod_memory_utilization_top',
                                   auth=HTTPBasicAuth(ACCESS_KEY, SECRET_KEY),
                                   params=pod_memory_utilization_top_params, verify=False)
        get_error_logs(response)

    @task
    def pod_memory_utilization(self):
        pod_memory_utilization_params = get_range_query_with_params('pod_memory_utilization_top',
                                                                    'pod_memory_utilization', 'pod_id')
        response = self.client.get(range_url, name='pod_memory_utilization', auth=HTTPBasicAuth(ACCESS_KEY, SECRET_KEY),
                                   params=pod_memory_utilization_params, verify=False)
        get_error_logs(response)

    @task
    def pod_cpu_utilization_top(self):
        pod_cpu_utilization_top_params = get_top_query_with_params('pod_cpu_utilization_top')
        response = self.client.get(top_url, name='pod_cpu_utilization_top', auth=HTTPBasicAuth(ACCESS_KEY, SECRET_KEY),
                                   params=pod_cpu_utilization_top_params, verify=False)
        get_error_logs(response)

    @task
    def pod_cpu_utilization(self):
        pod_cpu_utilization_params = get_range_query_with_params('pod_cpu_utilization_top', 'pod_cpu_utilization',
                                                                 'pod_id')
        response = self.client.get(range_url, name='pod_cpu_utilization', auth=HTTPBasicAuth(ACCESS_KEY, SECRET_KEY),
                                   params=pod_cpu_utilization_params, verify=False)
        get_error_logs(response)

    @task
    def container_memory_top(self):
        container_memory_top = get_top_expression_dict('container_memory_top')
        response = self.client.get(top_url, name='container_memory_top', auth=HTTPBasicAuth(ACCESS_KEY, SECRET_KEY),
                                   params=container_memory_top, verify=False)
        get_error_logs(response)

    @task
    def container_cpu_top(self):
        container_cpu_top = get_top_expression_dict('container_cpu_top')
        response = self.client.get(top_url, name='container_cpu_top', auth=HTTPBasicAuth(ACCESS_KEY, SECRET_KEY),
                                   params=container_cpu_top, verify=False)
        get_error_logs(response)

    @task
    def container_memory_top(self):
        container_memory_top = get_top_expression_dict('container_memory_top')
        response = self.client.get(top_url, name='container_memory_top', auth=HTTPBasicAuth(ACCESS_KEY, SECRET_KEY),
                                   params=container_memory_top, verify=False)
        get_error_logs(response)

    @task
    def container_cpu_top(self):
        container_cpu_top = get_top_expression_dict('container_cpu_top')
        response = self.client.get(top_url, name='container_cpu_top', auth=HTTPBasicAuth(ACCESS_KEY, SECRET_KEY),
                                   params=container_cpu_top, verify=False)
        get_error_logs(response)

    @task
    def node_cpu(self):
        node_cpu = get_top_expression_dict('node_cpu')
        response = self.client.get(top_url, name='node_cpu', auth=HTTPBasicAuth(ACCESS_KEY, SECRET_KEY),
                                   params=node_cpu, verify=False)
        get_error_logs(response)

    @task
    def node_memory(self):
        node_memory = get_top_expression_dict('node_memory')
        response = self.client.get(top_url, name='node_memory', auth=HTTPBasicAuth(ACCESS_KEY, SECRET_KEY),
                                   params=node_memory, verify=False)
        get_error_logs(response)

    @task
    def node_disk(self):
        node_disk = get_top_expression_dict('node_disk')
        response = self.client.get(top_url, name='node_disk', auth=HTTPBasicAuth(ACCESS_KEY, SECRET_KEY),
                                   params=node_disk, verify=False)
        get_error_logs(response)


class WebsiteUser(HttpLocust):
    wait_time = between(2, 5)
    task_set = UserTasks
