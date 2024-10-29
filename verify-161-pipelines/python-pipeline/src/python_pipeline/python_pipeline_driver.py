###
# #%L
# Verify 161::Pipelines::Python Pipeline
# %%
# Copyright (C) 2021 Booz Allen
# %%
# All Rights Reserved. You may not copy, reproduce, distribute, publish, display,
# execute, modify, create derivative works of, transmit, sell or offer for resale,
# or in any way exploit any part of this solution without Booz Allen Hamilton’s
# express written permission.
# #L%
###
from python_pipeline.step.step1 import Step1
from python_pipeline.step.step2 import Step2
import asyncio
from krausening.logging import LogManager
from python_pipeline.generated.pipeline.pipeline_base import PipelineBase
import os
import sys
from py4j.version import __version__
import time

"""
Driver to run the PythonPipeline.

GENERATED STUB CODE - PLEASE ***DO*** MODIFY

Originally generated from: templates/data-delivery-pyspark/pipeline.driver.py.vm
"""

logger = LogManager.get_instance().get_logger("PythonPipeline")


def find_jar_path():
    """Tries to find the path where the py4j jar is located."""
    paths = []
    jar_file = "py4j{0}.jar".format(__version__)
    maven_jar_file = "py4j-{0}.jar".format(__version__)
    print("------------- jar file is : {}".format(jar_file))
    paths.append(jar_file)
    # ant
    paths.append(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "../../../py4j-java/" + jar_file,
        )
    )
    # maven
    paths.append(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "../../../py4j-java/target/" + maven_jar_file,
        )
    )
    paths.append(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "../share/py4j/" + jar_file
        )
    )
    paths.append("../../../current-release/" + jar_file)

    print("------------------- sys.prefix: {}".format(sys.prefix))
    paths.append(os.path.join(sys.prefix, "share/py4j/" + jar_file))
    # pip install py4j # On Ubuntu 16.04, where virtualenvepath=/usr/local
    #   this file is here:
    #     virtualenvpath/lib/pythonX/dist-packages/py4j/java_gateway.py
    #   the jar file is here: virtualenvpath/share/py4j/py4j.jar
    # pip install --user py4j # On Ubuntu 16.04, where virtualenvepath=~/.local
    #   this file is here:
    #     virtualenvpath/lib/pythonX/site-packages/py4j/java_gateway.py
    #   the jar file is here: virtualenvpath/share/py4j/py4j.jar
    paths.append(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "../../../../share/py4j/" + jar_file,
        )
    )

    for path in paths:
        print("-------------path: {}".format(path))
        if os.path.exists(path):
            return path
    return ""


if __name__ == "__main__":
    logger.info("STARTED: PythonPipeline driver")
    java_home = os.environ.get("JAVA_HOME")
    print("---------------------- helloworld: java_home {}".format(java_home))
    print("find jar path ------------------ {}".format(find_jar_path()))
    PipelineBase().record_pipeline_lineage_start_event()
    time.sleep(60000)

    # TODO: Execute steps in desired order and handle any inbound and outbound types
    Step1().execute_step()
    asyncio.run(Step2().execute_step())
    PipelineBase().record_pipeline_lineage_complete_event()
