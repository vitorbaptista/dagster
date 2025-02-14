from dagster import In, Out, graph, op
from dagster.utils import file_relative_path
from dagster_pandas import DataFrame


def test_hello_world():
    @op(ins={"num_csv": In(DataFrame)}, out=Out(DataFrame))
    def hello_world_op(num_csv):
        num_csv["sum"] = num_csv["num1"] + num_csv["num2"]
        return num_csv

    @graph
    def hello_world():
        hello_world_op()

    result = hello_world.execute_in_process(
        config={
            "hello_world_op": {
                "inputs": {"num_csv": {"csv": {"path": file_relative_path(__file__, "num.csv")}}}
            }
        }
    )
    assert result.success
    assert result.result_for_node("hello_world_op").output_value().to_dict("list") == {
        "num1": [1, 3],
        "num2": [2, 4],
        "sum": [3, 7],
    }
