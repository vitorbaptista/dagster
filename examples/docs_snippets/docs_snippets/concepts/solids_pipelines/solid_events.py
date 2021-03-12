# pylint: disable=unused-argument
from dagster import (
    AssetMaterialization,
    EventMetadataEntry,
    ExpectationResult,
    Failure,
    Output,
    OutputDefinition,
    RetryRequested,
    solid,
)


def do_some_transform(_):
    return []


def calculate_bytes(_):
    return 0.0


def get_some_data():
    return []


def some_calculation(_):
    return 0


def get_files():
    return []


def store_to_s3(_):
    return


def flaky_operation():
    return 0


# start_solid_output_0


@solid
def my_simple_yield_solid(context):
    yield Output(1)


# end_solid_output_0

# start_solid_output_1


@solid
def my_simple_return_solid(context):
    return 1


# end_solid_output_1

# start_solid_output_2


@solid(
    output_defs=[
        OutputDefinition(name="my_output"),
    ]
)
def my_named_yield_solid(context):
    yield Output(1, output_name="my_output")


# end_solid_output_2

# start_solid_output_3


@solid
def my_metadata_output(context):
    df = get_some_data()
    yield Output(
        df,
        metadata_entries=[
            EventMetadataEntry.text("Text-based metadata for this event", label="text_metadata"),
            EventMetadataEntry.url("http://mycoolsite.com/url_for_my_data", label="dashboard_url"),
            EventMetadataEntry.int(len(df), "row count"),
            EventMetadataEntry.float(calculate_bytes(df), "size (bytes)"),
        ],
    )


# end_solid_output_3

# start_metadata_expectation_solid


@solid
def my_metadata_expectation_solid(context, df):
    df = do_some_transform(df)
    yield ExpectationResult(
        success=len(df) > 0,
        description="ensure dataframe has rows",
        metadata_entries=[
            EventMetadataEntry.text("Text-based metadata for this event", label="text_metadata"),
            EventMetadataEntry.url("http://mycoolsite.com/url_for_my_data", label="dashboard_url"),
            EventMetadataEntry.int(len(df), "row count"),
            EventMetadataEntry.float(calculate_bytes(df), "size (bytes)"),
        ],
    )
    yield Output(df)


# end_metadata_expectation_solid

# start_failure_solid


@solid
def my_failure_solid(_):
    my_files = get_files()
    if len(my_files) == 0:
        raise Failure("No files to process")
    return some_calculation(my_files)


# end_failure_solid

# start_retry_solid


@solid
def my_retry_solid(_):
    try:
        result = flaky_operation()
    except:
        raise RetryRequested(max_retries=3)
    return result


# end_retry_solid

# start_asset_solid


@solid
def my_asset_solid(context):
    df = get_some_data()
    store_to_s3(df)
    yield AssetMaterialization(
        asset_key="s3.my_asset",
        description="A df I stored in s3",
    )

    result = do_some_transform(df)
    yield Output(result)


# end_asset_solid
