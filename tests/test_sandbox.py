import unittest
from src.security.sandbox import SandboxedEnvironment, SecurityPolicy, SecurityError

class TestSandboxedEnvironment(unittest.TestCase):
    def setUp(self):
        self.sandbox = SandboxedEnvironment()

    def test_binary_operations(self):
        self.assertEqual(self.sandbox.call_binop('+', 1, 2), 3)
        self.assertEqual(self.sandbox.call_binop('*', 2, 3), 6)
        with self.assertRaises(SecurityError):
            self.sandbox.call_binop('@', 1, 2)

    def test_unary_operations(self):
        self.assertEqual(self.sandbox.call_unop('-', 5), -5)
        with self.assertRaises(SecurityError):
            self.sandbox.call_unop('!', 5)

    def test_attribute_access(self):
        self.assertTrue(self.sandbox.check_attribute_access("test", "upper"))
        with self.assertRaises(SecurityError):
            self.sandbox.check_attribute_access("test", "dangerous_method")

    def test_module_import(self):
        self.assertTrue(self.sandbox.check_module_import("math"))
        with self.assertRaises(SecurityError):
            self.sandbox.check_module_import("os")

    def test_custom_policy(self):
        policy = SecurityPolicy(
            allowed_builtins={'len'},
            allowed_attributes={'title'},
            allowed_modules={'decimal'}
        )
        sandbox = SandboxedEnvironment(policy)
        self.assertTrue(sandbox.check_attribute_access("test", "title"))
        with self.assertRaises(SecurityError):
            sandbox.check_attribute_access("test", "upper")
