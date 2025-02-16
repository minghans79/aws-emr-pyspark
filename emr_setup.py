import boto3

def create_emr_cluster(sg_id,ec2_key):
    emr = boto3.client('emr')
    account_id = boto3.client('sts').get_caller_identity()['Account']
    region = boto3.session.Session().region_name
    
    cluster_id = emr.run_job_flow(
        Name='Budget-EMR-Cluster',
        LogUri= f's3://emr-logs-{account_id}-{region}/logs/',
        ReleaseLabel='emr-6.15.0',
        Applications=[{'Name': 'Spark'}, {'Name': 'Hadoop'}],
        Instances={
            'InstanceFleets': [
                {
                    'Name': 'Master Fleet',
                    'InstanceFleetType': 'MASTER',
                    'TargetOnDemandCapacity': 1,  # Use On-Demand for the Master node
                    'InstanceTypeConfigs': [
                        {'InstanceType': 'm5.xlarge'}  # Cost-effective instance type
                    ]
                },
                {
                    'Name': 'Core Fleet',
                    'InstanceFleetType': 'CORE',
                    'TargetOnDemandCapacity': 1,  # Fallback to On-Demand if Spot is unavailable
                    'TargetSpotCapacity': 2,      # Use Spot Instances for cost savings
                    'InstanceTypeConfigs': [
                        {'InstanceType': 'm5.xlarge', 'WeightedCapacity': 1},
                        {'InstanceType': 'm5.2xlarge', 'WeightedCapacity': 2},
                        {'InstanceType': 'm5.4xlarge', 'WeightedCapacity': 4}
                    ],
                    'LaunchSpecifications': {
                        'SpotSpecification': {
                            'TimeoutDurationMinutes': 10,  # Wait up to 10 minutes for Spot capacity
                            'TimeoutAction': 'SWITCH_TO_ON_DEMAND'  # Fallback to On-Demand if Spot is unavailable
                        }
                    }
                }
            ],
            'Ec2KeyName': 'Default_Key',
            'KeepJobFlowAliveWhenNoSteps': False,  
            'TerminationProtected': False,
            'EmrManagedMasterSecurityGroup': sg_id,
            'EmrManagedSlaveSecurityGroup': sg_id,
            'Ec2SubnetIds': ["subnet-0a3367f66e3f5bf05","subnet-0f0bb40c3ae5cbf3e"]  # Specify multiple subnets for high availability
        },
        Steps=[{
            'Name': 'SampleSparkJob',
            'ActionOnFailure': 'TERMINATE_CLUSTER',  
            'HadoopJarStep': {
                'Jar': 'command-runner.jar',
                'Args': [
                    'spark-submit',
                    f's3://emr-scripts-{account_id}-{region}/script.py',
                    f's3://emr-input-{account_id}-{region}/meta_Kindle_Store.jsonl.7z',
                    f's3://emr-output-{account_id}-{region}/output/'
                ]
            }
        }],
        VisibleToAllUsers=True,
        JobFlowRole='EMR_EC2_DefaultRole',
        ServiceRole='EMR_DefaultRole',
        ScaleDownBehavior='TERMINATE_AT_TASK_COMPLETION',
        ManagedScalingPolicy={
            'ComputeLimits': {
                'MinimumCapacityUnits': 2,  # Minimum number of instances
                'MaximumCapacityUnits': 10,  # Maximum number of instances
                'UnitType': 'InstanceFleetUnits',  # Scale by number of instances
                'MaximumOnDemandCapacityUnits': 2  # Limit On-Demand usage
            }
        }
    )

    
    return cluster_id['JobFlowId']

if __name__ == "__main__":
    # Get security group ID from previous step
    sg_id = 'sg-xxxxxxxx'  # Replace with actual security group ID
    create_emr_cluster(sg_id)