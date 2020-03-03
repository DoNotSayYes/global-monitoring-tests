from env_rancher.lib.aws import AmazonWebServices
from env_rancher.tools.common import *
import os
import paramiko
import time


RANCHER_CLEANUP_CLUSTER = os.environ.get('RANCHER_CLEANUP_CLUSTER', "True")

DATA_SUBDIR = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                           'resource')
AWS_SSH_KEY_NAME = os.environ.get("AWS_SSH_KEY_NAME")


def test_import_rke_cluster():

    client = get_admin_client()

    # Create nodes in AWS
    aws_node = create_single_node()
    clusterfilepath = create_rke_cluster_config(aws_node)

    is_file = os.path.isfile(clusterfilepath)
    assert is_file

    # install docker
    install_docker(aws_node)

    # remove rkestate and kube_config files
    remove_files()

    # Create RKE K8s Cluster
    clustername = random_test_name("testimport")
    rkecommand = 'rke ' + "up" \
                 + ' --config ' + clusterfilepath
    print(rkecommand)
    result, return_code = run_command_with_stderr(rkecommand)
    while return_code != 0:
        remove_files()
        result, return_code = run_command_with_stderr(rkecommand)

    cluster = client.create_cluster(name=clustername)
    print(cluster)
    cluster_token = create_custom_host_registration_token(client, cluster)
    command = cluster_token.insecureCommand
    print(command)
    rke_config_file = "kube_config_clusternew.yml"
    finalimportcommand = command + " --kubeconfig " + DATA_SUBDIR + "/" + \
        rke_config_file
    print("Final command to import cluster is:")
    print(finalimportcommand)
    result = run_command(finalimportcommand)
    print(result)
    clusters = client.list_cluster(name=clustername).data
    assert len(clusters) > 0
    print("Cluster is")
    print(clusters[0])
    print(clustername + ' has been imported successfully!')
    print('------------------------------------------------')
    time.sleep(3)

    # Validate the cluster
    # cluster = validate_cluster(client, clusters[0],
    #                            check_intermediate_state=False)

    # cluster_cleanup(client, cluster, aws_node)


def create_single_node():

    aws_node = AmazonWebServices().create_node(random_test_name('test'), wait_for_ready=True)
    print(aws_node)
    print(aws_node.public_ip_address)

    return aws_node


def remove_files():
    rkestate_file = os.path.join(os.getcwd(), 'resource/clusternew.rkestate')
    kube_config_file = os.path.join(os.getcwd(), 'resource/kube_config_clusternew.yml')
    print(os.getcwd())
    print(rkestate_file)
    print(kube_config_file)
    if os.path.isfile(rkestate_file):
        os.remove(rkestate_file)
        print('rkestate file has been removed!')
    if os.path.isfile(kube_config_file):
        os.remove(kube_config_file)
        print('kube_config file has been removed!')


def install_docker(aws_node):

    key_path = os.path.join(os.getcwd(), 'resource', AWS_SSH_KEY_NAME)
    key = paramiko.RSAKey.from_private_key_file(key_path)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    pub_address = aws_node.public_ip_address
    print('public address is: ' + pub_address)

    try:
        client.connect(hostname=pub_address, username='ubuntu', pkey=key)
        cmd = "curl https://releases.rancher.com/install-docker/18.09.sh | sh;" \
              "sudo -S -p '' sudo usermod -aG docker ubuntu"
        stdin, stdout, stderr = client.exec_command(cmd, get_pty=True)
        for std in stdout.readlines():
            print(std)
    except Exception as e:
        print(e)
    finally:
        client.close()
    print('Finish installing docker in ', pub_address)


def create_rke_cluster_config(aws_node):

    configfile = "cluster.yml"

    rkeconfig = readDataFile(DATA_SUBDIR, configfile)
    rkeconfig = rkeconfig.replace("$ip1", aws_node.public_ip_address)
    rkeconfig = rkeconfig.replace("$AWS_SSH_KEY_NAME", AWS_SSH_KEY_NAME)

    print(rkeconfig)
    clusterfilepath = DATA_SUBDIR + "/" + "clusternew.yml"
    print(clusterfilepath)

    f = open(clusterfilepath, "w")
    f.write(rkeconfig)
    f.close()
    return clusterfilepath


def readDataFile(data_dir, name):

    fname = os.path.join(data_dir, name)
    print("File Name is: ")
    print(fname)
    is_file = os.path.isfile(fname)
    assert is_file
    with open(fname) as f:
        return f.read()


test_import_rke_cluster()

# i = 5
# while i > 0:
#     test_import_rke_cluster()
#     i = i - 1
# print('Clusters import finished!')
