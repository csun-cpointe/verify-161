allow_k8s_contexts('local')
docker_prune_settings(num_builds=1, keep_recent=1)

aissemble_version = '1.6.1'

build_args = { 'DOCKER_BASELINE_REPO_ID': 'aiops-docker-internal.nexus.boozallencsn.com/aiops/',
               'VERSION_AISSEMBLE': aissemble_version}

# Kafka

yaml = helm(
    'verify-161-deploy/src/main/resources/apps/kafka-cluster',
    values=['verify-161-deploy/src/main/resources/apps/kafka-cluster/values.yaml',
        'verify-161-deploy/src/main/resources/apps/kafka-cluster/values-dev.yaml']
)
k8s_yaml(yaml)

# python-pipeline-compiler
local_resource(
    name='compile-python-pipeline',
    cmd='cd verify-161-pipelines/python-pipeline && poetry run behave tests/features && poetry build && cd - && \
    cp -r verify-161-pipelines/python-pipeline/dist/* verify-161-docker/verify-161-spark-worker-docker/target/dockerbuild/python-pipeline && \
    cp verify-161-pipelines/python-pipeline/dist/requirements.txt verify-161-docker/verify-161-spark-worker-docker/target/dockerbuild/requirements/python-pipeline',
    deps=['verify-161-pipelines/python-pipeline'],
    auto_init=False,
    ignore=['**/dist/']
)

yaml = helm(
   'verify-161-deploy/src/main/resources/apps/policy-decision-point',
   name='policy-decision-point',
   values=['verify-161-deploy/src/main/resources/apps/policy-decision-point/values.yaml',
       'verify-161-deploy/src/main/resources/apps/policy-decision-point/values-dev.yaml']
)
k8s_yaml(yaml)
k8s_kind('SparkApplication', image_json_path='{.spec.image}')

# spark-worker-image
docker_build(
    ref='boozallen/verify-161-spark-worker-docker',
    context='verify-161-docker/verify-161-spark-worker-docker',
    build_args=build_args,
    extra_tag='boozallen/verify-161-spark-worker-docker:latest',
    dockerfile='verify-161-docker/verify-161-spark-worker-docker/src/main/resources/docker/Dockerfile'
)


yaml = helm(
   'verify-161-deploy/src/main/resources/apps/spark-infrastructure',
   name='spark-infrastructure',
   values=['verify-161-deploy/src/main/resources/apps/spark-infrastructure/values.yaml',
       'verify-161-deploy/src/main/resources/apps/spark-infrastructure/values-dev.yaml']
)
k8s_yaml(yaml)
yaml = helm(
   'verify-161-deploy/src/main/resources/apps/pipeline-invocation-service',
   name='pipeline-invocation-service',
   values=['verify-161-deploy/src/main/resources/apps/pipeline-invocation-service/values.yaml',
       'verify-161-deploy/src/main/resources/apps/pipeline-invocation-service/values-dev.yaml']
)
k8s_yaml(yaml)
k8s_yaml('verify-161-deploy/src/main/resources/apps/spark-worker-image/spark-worker-image.yaml')


yaml = helm(
   'verify-161-deploy/src/main/resources/apps/s3-local',
   name='s3-local',
   values=['verify-161-deploy/src/main/resources/apps/s3-local/values.yaml',
       'verify-161-deploy/src/main/resources/apps/s3-local/values-dev.yaml']
)
k8s_yaml(yaml)
yaml = helm(
   'verify-161-deploy/src/main/resources/apps/hive-metastore-db',
   name='hive-metastore-db',
   values=['verify-161-deploy/src/main/resources/apps/hive-metastore-db/values.yaml',
       'verify-161-deploy/src/main/resources/apps/hive-metastore-db/values-dev.yaml']
)
k8s_yaml(yaml)
yaml = helm(
   'verify-161-deploy/src/main/resources/apps/metadata',
   name='metadata',
   values=['verify-161-deploy/src/main/resources/apps/metadata/values.yaml',
       'verify-161-deploy/src/main/resources/apps/metadata/values-dev.yaml']
)
k8s_yaml(yaml)
yaml = helm(
   'verify-161-deploy/src/main/resources/apps/hive-metastore-service',
   name='hive-metastore-service',
   values=['verify-161-deploy/src/main/resources/apps/hive-metastore-service/values.yaml',
       'verify-161-deploy/src/main/resources/apps/hive-metastore-service/values-dev.yaml']
)
k8s_yaml(yaml)
yaml = helm(
   'verify-161-deploy/src/main/resources/apps/spark-operator',
   name='spark-operator',
   values=['verify-161-deploy/src/main/resources/apps/spark-operator/values.yaml',
       'verify-161-deploy/src/main/resources/apps/spark-operator/values-dev.yaml']
)
k8s_yaml(yaml)

k8s_resource('hive-metastore-service', resource_deps=['hive-metastore-db'])

# policy-decision-point
docker_build(
    ref='boozallen/verify-161-policy-decision-point-docker',
    context='verify-161-docker/verify-161-policy-decision-point-docker',
    build_args=build_args,
    dockerfile='verify-161-docker/verify-161-policy-decision-point-docker/src/main/resources/docker/Dockerfile'
)



yaml = local('helm template aissemble-spark-application --version %s --values verify-161-pipelines/python-pipeline/src/python_pipeline/resources/apps/python-pipeline-base-values.yaml,verify-161-pipelines/python-pipeline/src/python_pipeline/resources/apps/python-pipeline-dev-values.yaml --repo https://nexus.boozallencsn.com/repository/aiops-helm-internal' % aissemble_version)
k8s_yaml(yaml)
k8s_resource('python-pipeline', port_forwards=[port_forward(4747, 4747, 'debug')], auto_init=False, trigger_mode=TRIGGER_MODE_MANUAL)
# Add deployment resources here