from requests.auth import HTTPBasicAuth
from urllib import parse
import requests
import datetime
import os
import yaml
from urllib.parse import quote


ACCESS_KEY = os.environ.get('ACCESS_KEY', 'token-ck452')
SECRET_KEY = os.environ.get('SECRET_KEY', 'jnrzqsf9f5h2h9l7c98c8pblhcbmh22q68jgpq7hs9h664tzf8m6w6')
BASE_URL = os.environ.get('BASE_URL', 'https://13.114.251.136')
DURATION = os.environ.get('DURATION', '7d')
YAML_FILE_PATH = os.environ.get('YAML_FILE_PATH',
                                os.path.join(os.path.split(os.path.realpath(__file__))[0], 'resource/expression.yaml'))


def get_range_query_with_params(var_top, var_range, metric):
    top_response_dict = get_top_api_response(var_top)
    # print(top_response_dict)
    range_query_params = get_range_expression_params(top_response_dict, metric)
    # print('range_query_params: ', range_query_params)
    range_expression = get_expression(var_range)
    query_with_params = range_expression % {'params': range_query_params}
    start_time, end_time, step_size = query_params_other()
    return {'query': query_with_params, 'start': start_time, 'end': end_time, 'step': step_size}


def get_expression(var_top):
    with open(YAML_FILE_PATH, 'r') as yaml_file_content:
        yaml_obj = yaml.safe_load(yaml_file_content.read())
        expression = yaml_obj[var_top]
        return expression


def get_top_expression_dict(var_top):
    expression = get_expression(var_top)
    expression_dict = {'query': expression}
    return expression_dict


def get_top_query_with_params(var_top):
    expression = get_expression(var_top)
    request_query_dict = {'query': (expression % {'duration': DURATION})}
    return request_query_dict


def get_top_api_response(var_top):
    top_url_body = get_expression('top_url_body')
    request_url = parse.urljoin(BASE_URL, top_url_body)
    expression = get_expression(var_top)
    request_query_dict = {'query': (expression % {'duration': DURATION})}
    # print(request_query_dict)
    # print(request_url)
    response = requests.get(url=request_url, auth=HTTPBasicAuth(ACCESS_KEY, SECRET_KEY), params=request_query_dict,
                            verify=False)
    # print(response)
    response_dict = response.json()
    return response_dict


# This method is to build up the range expression's parameters that separates by '|'. For example: test-01|test-02|
def get_range_expression_params(response_dict, metric_type):
    if 'data' in response_dict.keys():
        if 'result' in response_dict['data'].keys():
            result_list = response_dict['data']['result']
            print(result_list)
            if metric_type == 'prometheus_from':
                metric_list = []
                for item in result_list:
                    metric_value = item['metric']['prometheus_from']
                    metric_list.append(metric_value)
                params = '|'.join(metric_list)

                return params

            elif metric_type == 'instance':
                metric_list = []
                for item in result_list:
                    metric_value = item['metric']['instance']
                    metric_list.append(metric_value)
                params = '|'.join(metric_list)

                return params

            elif metric_type == 'node':
                metric_list = []
                for item in result_list:
                    metric_value = item['metric']['node']
                    metric_list.append(metric_value)
                params = '|'.join(metric_list)

                return params

            elif metric_type == 'node_id':
                metric_list = []
                for item in result_list:
                    metric_value = item['metric']['node_id']
                    metric_list.append(metric_value)
                params = '|'.join(metric_list)

                return params

            elif metric_type == 'pod_id':
                metric_list = []
                for item in result_list:
                    metric_value = item['metric']['pod_id']
                    metric_list.append(metric_value)
                params = '|'.join(metric_list)

                return params

            elif metric_type == 'pod':
                metric_list = []
                for item in result_list:
                    metric_value = item['metric']['pod']
                    metric_list.append(metric_value)
                params = '|'.join(metric_list)

                return params
        else:
            print("Data point 'result' is not found in API response!")
            return 0
    else:
        print("Data point 'data' is not found in API response!")
        return 0


# This method is to fetch start time, end time, and step
def query_params_other():
    if DURATION == '5m':
        end_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        start_time = (datetime.datetime.utcnow() - datetime.timedelta(minutes=5)).strftime('%Y-%m-%dT%H:%M:%SZ')
        step_size = '10s'
    elif DURATION == '1h':
        end_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        start_time = (datetime.datetime.utcnow() - datetime.timedelta(minutes=60)).strftime('%Y-%m-%dT%H:%M:%SZ')
        step_size = '60s'
    elif DURATION == '6h':
        end_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        start_time = (datetime.datetime.utcnow() - datetime.timedelta(hours=6)).strftime('%Y-%m-%dT%H:%M:%SZ')
        step_size = '60s'
    elif DURATION == '24h':
        end_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        start_time = (datetime.datetime.utcnow() - datetime.timedelta(hours=24)).strftime('%Y-%m-%dT%H:%M:%SZ')
        step_size = '5m'
    elif DURATION == '7d':
        end_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        start_time = (datetime.datetime.utcnow() - datetime.timedelta(days=7)).strftime('%Y-%m-%dT%H:%M:%SZ')
        step_size = '30m'

    return start_time, end_time, step_size






