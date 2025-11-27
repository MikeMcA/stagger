#!/usr/bin/env python3
#
# test_stringio_bug.py
# Test for io.StringIO bug in PIC._to_version()
#

import unittest
import io

import stagger
from stagger.id3 import PIC, APIC


class StringIOBugTestCase(unittest.TestCase):
    def test_pic_to_apic_with_gif_format(self):
        """Test that PIC frame with GIF format can be converted to APIC.

        This test previously exposed a bug where io.StringIO was used instead
        of the correct pattern imghdr.what(None, data[:32]) when converting
        PIC frames with non-PNG/JPG formats to APIC.

        Fixed in: id3.py:822
        """
        # Create a minimal GIF header (GIF89a)
        gif_data = b'GIF89a' + b'\x00' * 100

        # Create a PIC frame (ID3v2.2) with GIF format
        pic = PIC(
            encoding='latin-1',
            format='GIF',  # This triggers the else branch at line 821
            type=3,  # Cover (front)
            desc='Test GIF',
            data=gif_data
        )

        # Convert to ID3v2.3 (APIC frame)
        # This should now work correctly with the fix
        apic = pic._to_version(3)

        # Verify the conversion worked
        self.assertIsInstance(apic, APIC)
        self.assertEqual(apic.mime, 'image/gif')
        self.assertEqual(apic.type, 3)
        self.assertEqual(apic.desc, 'Test GIF')
        self.assertEqual(apic.data, gif_data)


suite = unittest.TestLoader().loadTestsFromTestCase(StringIOBugTestCase)

if __name__ == '__main__':
    unittest.main()
