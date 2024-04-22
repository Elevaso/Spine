# pyright: reportMissingImports=false
# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring

# Python Standard Libraries
import context
import re
from io import StringIO
import unittest

# 3rd Party Libraries


# Code Repository Sub-Packages
from spine.fmt import sub


class SubValueBase(unittest.TestCase):
    pattern = re.compile(r"\${([\w\d\:]+)}")

    def call_function_for_log(
        self,
        log_level: str = "NOTSET",
        value: object = None,
        sub_values: object = {},
        default_val: object = None,
    ) -> context.Tuple[object, object]:
        if log_level == "NOTSET":
            output = sub.sub_value(
                pattern=self.pattern,
                value=value,
                sub_values=sub_values,
                default_val=default_val,
            )

            log = None
        else:
            with self.assertLogs(level=log_level) as log:
                output = sub.sub_value(
                    pattern=self.pattern,
                    value=value,
                    sub_values=sub_values,
                    default_val=default_val,
                )

        return output, log


class TestSubValue(SubValueBase):
    def test_none_value(self):
        value = None
        sub_values = {}

        output = sub.sub_value(
            pattern=self.pattern, value=value, sub_values=sub_values
        )

        self.assertIsNone(output)

    def test_invalid_value_type(self):
        value = b"${test}"
        sub_values = {"Hello": "World"}

        output, log = self.call_function_for_log(
            log_level="WARN", value=value, sub_values=sub_values
        )

        self.assertIn(
            "Value object type bytes does not support iteration, "
            "returning original value",
            log.output[0],
        )

    def test_invalid_sub_value_type(self):
        value = "${test}"
        sub_values = ("hello", "there")

        with self.assertRaises(TypeError) as cm:
            _ = sub.sub_value(
                pattern=self.pattern, value=value, sub_values=sub_values
            )

        self.assertEqual(
            "Invalid type of <class 'tuple'> for sub_values", str(cm.exception)
        )

    def test_child_list(self):
        value = [["${test}"], "there"]
        sub_values = {"test": "hello"}

        output = sub.sub_value(
            pattern=self.pattern, value=value, sub_values=sub_values
        )

        self.assertListEqual(output, [["hello"], "there"])

    def test_list_of_dict(self):
        value = [{"key": "${test}"}, "there"]
        sub_values = {"test": "hello"}

        output = sub.sub_value(
            pattern=self.pattern, value=value, sub_values=sub_values
        )

        self.assertListEqual(output, [{"key": "hello"}, "there"])

    def test_dict_with_list(self):
        value = {"key": ["${test}"], "key2": "there"}
        sub_values = {"test": "hello"}

        output = sub.sub_value(
            pattern=self.pattern, value=value, sub_values=sub_values
        )

        self.assertDictEqual(output, {"key": ["hello"], "key2": "there"})

    def test_multiple_groupings(self):
        value = "${test} ${test}"
        sub_values = {"test": "hello"}

        output = sub.sub_value(
            pattern=re.compile(r"(\${([\w\d\:]+)})"),
            value=value,
            sub_values=sub_values,
        )

        self.assertEqual(output, "hello hello")

    def test_case_sensitive(self):
        value = "${test}"
        sub_values = {"Test": 2}

        output, log = self.call_function_for_log(
            log_level="DEBUG", value=value, sub_values=sub_values
        )

        self.assertEqual(output, "")

        self.assertIn("Value test not found, returning None", log.output[0])

    def test_case_insensitive(self):
        value = "${Test}"
        sub_values = {"Test": 2}

        output = sub.sub_value(
            pattern=re.compile(r"\${([a-z\:]+)}", re.IGNORECASE),
            value=value,
            sub_values=sub_values,
        )

        self.assertEqual(output, "2")

    def test_default_val(self):
        value = "${test}"
        sub_values = {"Test": 2}

        output, log = self.call_function_for_log(
            log_level="DEBUG",
            value=value,
            sub_values=sub_values,
            default_val="Hello",
        )

        self.assertEqual(output, "Hello")

        self.assertIn(
            "Value test not found, returning Hello",
            log.output[0],
        )

    def test_error_not_exist(self):
        value = "${test}"
        sub_values = {"Test": 2}

        with self.assertRaises(KeyError) as log:
            _ = sub.sub_value(
                pattern=self.pattern,
                value=value,
                sub_values=sub_values,
                default_val="Hello",
                error_not_exist=True,
            )

        self.assertEqual(str(log.exception), "'Value test not found'")

    def test_int(self):
        value = 1
        sub_values = {"Test": 1}

        output, log = self.call_function_for_log(
            log_level="WARNING", value=value, sub_values=sub_values
        )

        self.assertEqual(output, value)

        self.assertIn(
            "Value object type int does not support iteration, "
            "returning original value",
            log.output[0],
        )

    def test_immutable_object(self):
        value = {"hello": StringIO(), "second": "${Test}"}
        sub_values = {"Test": 1}

        output = sub.sub_value(
            pattern=self.pattern,
            value=value,
            sub_values=sub_values,
            copy_val=False,
        )

        self.assertEqual(output["second"], str(sub_values["Test"]))
        self.assertEqual(output["hello"], value["hello"])


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
