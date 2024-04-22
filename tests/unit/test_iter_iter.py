# pyright: reportMissingImports=false
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

# Python Standard Libraries
import context
import unittest

# 3rd Party Libraries


# Code Repository Sub-Packages
from spine.iter import iter


class TestIterate(unittest.TestCase):
    def call_function_for_log(
        self,
        log_level: str = "NOTSET",
        value: object = None,
        copy_val: bool = True,
        custom_type_map: dict = {},
    ) -> context.Tuple[object, object]:
        if log_level == "NOTSET":
            output = iter.iterate(value, copy_val, custom_type_map)

            log = None
        else:
            with self.assertLogs(level=log_level) as log:
                output = iter.iterate(value, copy_val, custom_type_map)

        return output, log

    def custom_func(self, val: object):
        return val

    def test_none_value(self):
        value = None

        output, log = self.call_function_for_log(log_level="WARN", value=value)

        self.assertIsNone(output)
        self.assertIn(
            "Value object type NoneType does not support iteration, returning "
            "original value",
            log.output[0],
        )

    def test_nested(self):
        value = [{"Test": [1]}]

        output, _ = self.call_function_for_log(
            log_level="NOTSET",
            value=value,
            custom_type_map={int: self.custom_func},
            copy_val=False,
        )

        self.assertEqual(output, value)

    def test_copy_val(self):
        value = [{"Test": 1}]

        output, _ = self.call_function_for_log(
            log_level="NOTSET", value=value, copy_val=True
        )

        self.assertEqual(output, value)

    def test_custom_type_map_int(self):
        value = 1

        output, log = self.call_function_for_log(
            log_level="NOTSET",
            value=value,
            custom_type_map={int: self.custom_func},
        )

        self.assertEqual(output, value)

    def test_custom_type_map_nested(self):
        value = [{"Test": 1}]

        output, log = self.call_function_for_log(
            log_level="NOTSET",
            value=value,
            custom_type_map={int: self.custom_func},
        )

        self.assertEqual(output, value)


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
