{{
    config(
        materialized='incremental',
        strategy = 'append',
        unique_key = 'customer_sk',
        indexes= [{
            "columns":['customer_sk'],"union":true,
        }],
        target_schema = 'staging'
    )
}}

with valid_customers as (
    select 
        distinct "Customer ID" as customer_id,
        "Customer Name" as customer_name,
        Segment,
        'snow' as data_source
    from {{source ('ecommerce_oltp','ECOMMERCE')}}
    where 
        "Customer ID" is not null
)

select 
    md5(customer_id || data_source) as customer_sk,
    *
from  valid_customers