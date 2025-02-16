import boto3

def terminate_emr_cluster():
    emr = boto3.client('emr')
    
    # List active clusters
    clusters = emr.list_clusters(
        ClusterStates=['STARTING', 'BOOTSTRAPPING', 'RUNNING', 'WAITING']
    )
    
    for cluster in clusters.get('Clusters', []):
        if cluster['Name'] == 'Budget-EMR-Cluster':
            emr.terminate_job_flows(
                JobFlowIds=[cluster['Id']]
            )
            print(f"Terminating cluster: {cluster['Id']}")
    
    return True

    

if __name__ == "__main__":
    terminate_emr_cluster()