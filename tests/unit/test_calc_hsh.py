# pyright: reportMissingImports=false

# Python Standard Libraries
import context
import hashlib
import os
import unittest
import uuid

# 3rd Party Libraries


# Code Repository Sub-Packages
from spine.calc import hsh


def hash_file(path: os.path) -> uuid.uuid4:
    """Simplified file hash function to compare results dynamically"""
    hasher = hashlib.md5()

    path = os.path.expanduser(path)

    with open(path, "rb") as file_obj:
        buf = file_obj.read()
        hasher.update(buf)

    return str(uuid.UUID(hasher.hexdigest()))


class TestHashContent(unittest.TestCase):
    def test_dict(self):
        output = hsh.hash_content({"hello": "world"})

        self.assertEqual(output, "49dfdd54-b01c-bcd2-d2ab-5e9e5ee6b9b9")

    def test_bytes(self):
        output = hsh.hash_content("Hello World".encode("utf-8"))

        self.assertEqual(output, "b10a8db1-64e0-7541-05b7-a99be72e3fe5")

    def test_not_implemented(self):
        with self.assertRaises(NotImplementedError) as cm:
            _ = hsh.hash_content(("Hello", "World"))

        self.assertEqual(
            str(cm.exception), "Hashing for <class 'tuple'> Not Supported"
        )


class TestHashFile(unittest.TestCase):
    def test_file(self):
        file_obj = os.path.join(os.path.dirname(__file__), "context.py")

        output = hsh.hash_file(file_obj)

        self.assertEqual(output, hash_file(file_obj))


class TestHashString(unittest.TestCase):
    def test_str(self):
        output = hsh.hash_string("Hello World")

        self.assertEqual(output, "b10a8db1-64e0-7541-05b7-a99be72e3fe5")


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
