"""Contrôle la seule extension de grammaire nécessaire aux grands paquets."""
import json
import unittest
import lie_jugements_corriges_portables as adapter
from lie_jugements_corriges import BindingError

class PortableTests(unittest.TestCase):
    def setUp(self):
        self.args = {'cmd': "Get-Content -LiteralPath 'C:/paquet.json' -Raw", 'max_output_tokens': 55000}
        self.read = 'text(await tools.exec_command(' + json.dumps(self.args) + '));'

    def test_exact_read_pragma(self):
        self.assertEqual(adapter.arguments(adapter.READ_PRAGMA + self.read, 'exec_command'), self.args)

    def test_no_pragma_read_remains_valid(self):
        self.assertEqual(adapter.arguments(self.read, 'exec_command'), self.args)

    def test_other_pragmas_refused(self):
        for prefix in ('// @exec: {"max_output_tokens": 1000}\n', '// @exec: {"yield_time_ms": 55000}\n', adapter.READ_PRAGMA * 2):
            with self.subTest(prefix=prefix), self.assertRaises(BindingError):
                adapter.arguments(prefix + self.read, 'exec_command')

    def test_write_pragma_refused(self):
        with self.assertRaises(BindingError):
            adapter.arguments(adapter.READ_PRAGMA + 'text(await tools.apply_patch("patch"));', 'apply_patch')

    def test_extra_code_refused(self):
        with self.assertRaises(BindingError):
            adapter.arguments(adapter.READ_PRAGMA + self.read + 'text("autre");', 'exec_command')

if __name__ == '__main__':
    unittest.main()
