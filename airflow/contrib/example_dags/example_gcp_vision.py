# -*- coding: utf-8 -*-
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""
Example Airflow DAG that creates, gets, updates and deletes Products and Product Sets in the Google Cloud
Vision service in the Google Cloud Platform.

This DAG relies on the following OS environment variables

* GCP_VISION_LOCATION - Google Cloud Platform zone where the instance exists.
"""
import os

# [START howto_operator_vision_retry_import]
from google.api_core.retry import Retry
# [END howto_operator_vision_retry_import]
# [START howto_operator_vision_productset_import]
from google.cloud.vision_v1.proto.product_search_service_pb2 import ProductSet
# [END howto_operator_vision_productset_import]
# [START howto_operator_vision_product_import]
from google.cloud.vision_v1.proto.product_search_service_pb2 import Product
# [END howto_operator_vision_product_import]

import airflow
from airflow import models

from airflow.contrib.operators.gcp_vision_operator import (
    CloudVisionProductSetCreateOperator,
    CloudVisionProductSetGetOperator,
    CloudVisionProductSetUpdateOperator,
    CloudVisionProductSetDeleteOperator,
    CloudVisionProductCreateOperator,
    CloudVisionProductGetOperator,
    CloudVisionProductUpdateOperator,
    CloudVisionProductDeleteOperator,
)

default_args = {'start_date': airflow.utils.dates.days_ago(1)}

# [START howto_operator_vision_args_common]
GCP_VISION_LOCATION = os.environ.get('GCP_VISION_LOCATION', 'europe-west1')
# [END howto_operator_vision_args_common]

# [START howto_operator_vision_productset]
product_set = ProductSet(display_name='My Product Set 1')
# [END howto_operator_vision_productset]

# [START howto_operator_vision_product]
product = Product(display_name='My Product 1', product_category='toys')
# [END howto_operator_vision_product]

# [START howto_operator_vision_productset_explicit_id]
GCP_VISION_PRODUCT_SET_ID = os.environ.get('GCP_VISION_PRODUCT_SET_ID', 'product_set_explicit_id')
# [END howto_operator_vision_productset_explicit_id]

# [START howto_operator_vision_product_explicit_id]
GCP_VISION_PRODUCT_ID = os.environ.get('GCP_VISION_PRODUCT_ID', 'product_explicit_id')
# [END howto_operator_vision_product_explicit_id]

with models.DAG(
    'example_gcp_vision', default_args=default_args, schedule_interval=None  # Override to match your needs
) as dag:
    # ################################## #
    # ### Autogenerated IDs examples ### #
    # ################################## #

    # [START howto_operator_vision_product_set_create]
    product_set_create = CloudVisionProductSetCreateOperator(
        location=GCP_VISION_LOCATION,
        product_set=product_set,
        retry=Retry(maximum=10.0),
        timeout=5,
        task_id='product_set_create',
    )
    # [END howto_operator_vision_product_set_create]

    # [START howto_operator_vision_product_set_get]
    product_set_get = CloudVisionProductSetGetOperator(
        location=GCP_VISION_LOCATION,
        product_set_id="{{ task_instance.xcom_pull('product_set_create') }}",
        task_id='product_set_get',
    )
    # [END howto_operator_vision_product_set_get]

    # [START howto_operator_vision_product_set_update]
    product_set_update = CloudVisionProductSetUpdateOperator(
        location=GCP_VISION_LOCATION,
        product_set_id="{{ task_instance.xcom_pull('product_set_create') }}",
        product_set=ProductSet(display_name='My Product Set 2'),
        task_id='product_set_update',
    )
    # [END howto_operator_vision_product_set_update]

    # [START howto_operator_vision_product_set_delete]
    product_set_delete = CloudVisionProductSetDeleteOperator(
        location=GCP_VISION_LOCATION,
        product_set_id="{{ task_instance.xcom_pull('product_set_create') }}",
        task_id='product_set_delete',
    )
    # [END howto_operator_vision_product_set_delete]

    # [START howto_operator_vision_product_create]
    product_create = CloudVisionProductCreateOperator(
        location=GCP_VISION_LOCATION,
        product=product,
        retry=Retry(maximum=10.0),
        timeout=5,
        task_id='product_create',
    )
    # [END howto_operator_vision_product_create]

    # [START howto_operator_vision_product_get]
    product_get = CloudVisionProductGetOperator(
        location=GCP_VISION_LOCATION,
        product_id="{{ task_instance.xcom_pull('product_create') }}",
        task_id='product_get',
    )
    # [END howto_operator_vision_product_get]

    # [START howto_operator_vision_product_update]
    product_update = CloudVisionProductUpdateOperator(
        location=GCP_VISION_LOCATION,
        product_id="{{ task_instance.xcom_pull('product_create') }}",
        product=Product(display_name='My Product 2', description='My updated description'),
        task_id='product_update',
    )
    # [END howto_operator_vision_product_update]

    # [START howto_operator_vision_product_delete]
    product_delete = CloudVisionProductDeleteOperator(
        location=GCP_VISION_LOCATION,
        product_id="{{ task_instance.xcom_pull('product_create') }}",
        task_id='product_delete',
    )
    # [END howto_operator_vision_product_delete]

    product_set_create >> product_set_get >> product_set_update >> product_set_delete
    product_create >> product_get >> product_update >> product_delete

    # ############################# #
    # ### Explicit IDs examples ### #
    # ############################# #

    # [START howto_operator_vision_product_set_create_2]
    product_set_create_2 = CloudVisionProductSetCreateOperator(
        product_set_id=GCP_VISION_PRODUCT_SET_ID,
        location=GCP_VISION_LOCATION,
        product_set=product_set,
        retry=Retry(maximum=10.0),
        timeout=5,
        task_id='product_set_create_2',
    )
    # [END howto_operator_vision_product_set_create_2]

    # Second 'create' task with the same product_set_id to demonstrate idempotence
    product_set_create_2_idempotence = CloudVisionProductSetCreateOperator(
        product_set_id=GCP_VISION_PRODUCT_SET_ID,
        location=GCP_VISION_LOCATION,
        product_set=product_set,
        retry=Retry(maximum=10.0),
        timeout=5,
        task_id='product_set_create_2_idempotence',
    )

    # [START howto_operator_vision_product_set_get_2]
    product_set_get_2 = CloudVisionProductSetGetOperator(
        location=GCP_VISION_LOCATION, product_set_id=GCP_VISION_PRODUCT_SET_ID, task_id='product_set_get_2'
    )
    # [END howto_operator_vision_product_set_get_2]

    # [START howto_operator_vision_product_set_update_2]
    product_set_update_2 = CloudVisionProductSetUpdateOperator(
        location=GCP_VISION_LOCATION,
        product_set_id=GCP_VISION_PRODUCT_SET_ID,
        product_set=ProductSet(display_name='My Product Set 2'),
        task_id='product_set_update_2',
    )
    # [END howto_operator_vision_product_set_update_2]

    # [START howto_operator_vision_product_set_delete_2]
    product_set_delete_2 = CloudVisionProductSetDeleteOperator(
        location=GCP_VISION_LOCATION, product_set_id=GCP_VISION_PRODUCT_SET_ID, task_id='product_set_delete_2'
    )
    # [END howto_operator_vision_product_set_delete_2]

    # [START howto_operator_vision_product_create_2]
    product_create_2 = CloudVisionProductCreateOperator(
        product_id=GCP_VISION_PRODUCT_ID,
        location=GCP_VISION_LOCATION,
        product=product,
        retry=Retry(maximum=10.0),
        timeout=5,
        task_id='product_create_2',
    )
    # [END howto_operator_vision_product_create_2]

    # Second 'create' task with the same product_id to demonstrate idempotence
    product_create_2_idempotence = CloudVisionProductCreateOperator(
        product_id=GCP_VISION_PRODUCT_ID,
        location=GCP_VISION_LOCATION,
        product=product,
        retry=Retry(maximum=10.0),
        timeout=5,
        task_id='product_create_2_idempotence',
    )

    # [START howto_operator_vision_product_get_2]
    product_get_2 = CloudVisionProductGetOperator(
        location=GCP_VISION_LOCATION, product_id=GCP_VISION_PRODUCT_ID, task_id='product_get_2'
    )
    # [END howto_operator_vision_product_get_2]

    # [START howto_operator_vision_product_update_2]
    product_update_2 = CloudVisionProductUpdateOperator(
        location=GCP_VISION_LOCATION,
        product_id=GCP_VISION_PRODUCT_ID,
        product=Product(display_name='My Product 2', description='My updated description'),
        task_id='product_update_2',
    )
    # [END howto_operator_vision_product_update_2]

    # [START howto_operator_vision_product_delete_2]
    product_delete_2 = CloudVisionProductDeleteOperator(
        location=GCP_VISION_LOCATION, product_id=GCP_VISION_PRODUCT_ID, task_id='product_delete_2'
    )
    # [END howto_operator_vision_product_delete_2]

    product_set_create_2 >> product_set_get_2 >> product_set_update_2 >> product_set_delete_2
    product_create_2 >> product_get_2 >> product_update_2 >> product_delete_2
