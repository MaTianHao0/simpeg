"""
Test cases for CAD frame generation functionality.
"""

import unittest
import os
import tempfile
import numpy as np
from SimPEG.utils.cad import FrameGenerator, FrameTemplateManager, DWGReader


class TestFrameGenerator(unittest.TestCase):
    """Test cases for FrameGenerator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.generator = FrameGenerator()
    
    def test_initialization(self):
        """Test FrameGenerator initialization."""
        self.assertIsInstance(self.generator, FrameGenerator)
        self.assertIsInstance(self.generator.template_manager, FrameTemplateManager)
    
    def test_generate_default_frame(self):
        """Test generating a default frame without template files."""
        frame = self.generator.generate_frame('A4')
        
        self.assertIsInstance(frame, dict)
        self.assertIn('entities', frame)
        self.assertIn('bounds', frame)
        self.assertIn('reference_point', frame)
        self.assertIn('metadata', frame)
        
        # Check that frame has reasonable dimensions for A4
        self.assertEqual(frame['paper_size'], 'A4')
        self.assertTrue(len(frame['entities']) > 0)
    
    def test_generate_frame_with_reference_point(self):
        """Test generating frame with custom reference point."""
        ref_point = [100, 200]
        frame = self.generator.generate_frame('A4', reference_point=ref_point)
        
        self.assertEqual(frame['reference_point'], ref_point)
        
        # Check that entities are positioned relative to reference point
        for entity in frame['entities']:
            if entity['type'] == 'line':
                # Start and end points should be offset by reference point
                self.assertTrue(entity['start'][0] >= ref_point[0])
                self.assertTrue(entity['start'][1] >= ref_point[1])
    
    def test_generate_frame_with_scale(self):
        """Test generating frame with custom scale."""
        scale = 2.0
        frame = self.generator.generate_frame('A4', scale=scale)
        
        self.assertEqual(frame['scale'], scale)
        
        # Check that scaled size is correct
        expected_size = [210 * scale, 297 * scale]  # A4 size scaled
        actual_size = frame['metadata']['scaled_size']
        
        self.assertAlmostEqual(actual_size[0], expected_size[0], places=1)
        self.assertAlmostEqual(actual_size[1], expected_size[1], places=1)
    
    def test_generate_frame_with_rotation(self):
        """Test generating frame with rotation."""
        rotation = 45.0
        frame = self.generator.generate_frame('A4', rotation=rotation)
        
        self.assertEqual(frame['rotation'], rotation)
        
        # Check that entities are rotated (bounds should change)
        self.assertTrue(len(frame['entities']) > 0)
    
    def test_unit_conversion(self):
        """Test unit conversion functionality."""
        frame_mm = self.generator.generate_frame('A4', units='mm')
        frame_cm = self.generator.generate_frame('A4', units='cm')
        
        # cm frame should be 10x smaller than mm frame
        mm_size = frame_mm['metadata']['scaled_size']
        cm_size = frame_cm['metadata']['scaled_size']
        
        self.assertAlmostEqual(mm_size[0] / cm_size[0], 10.0, places=1)
        self.assertAlmostEqual(mm_size[1] / cm_size[1], 10.0, places=1)
    
    def test_get_rhino_geometry(self):
        """Test conversion to Rhino geometry format."""
        frame = self.generator.generate_frame('A4')
        rhino_geometry = self.generator.get_rhino_geometry(frame)
        
        self.assertIsInstance(rhino_geometry, list)
        self.assertTrue(len(rhino_geometry) > 0)
        
        # Check that all geometry items have proper type
        for geom in rhino_geometry:
            self.assertIn('type', geom)
            self.assertIn(geom['type'], ['Line', 'Polyline', 'Circle', 'Text'])
    
    def test_get_grasshopper_data(self):
        """Test conversion to Grasshopper data format."""
        frame = self.generator.generate_frame('A4')
        gh_data = self.generator.get_grasshopper_data(frame)
        
        self.assertIsInstance(gh_data, dict)
        self.assertIn('Lines', gh_data)
        self.assertIn('Polylines', gh_data)
        self.assertIn('Circles', gh_data)
        self.assertIn('Texts', gh_data)
        self.assertIn('Bounds', gh_data)
        self.assertIn('Metadata', gh_data)
    
    def test_list_available_sizes(self):
        """Test listing available paper sizes."""
        sizes = self.generator.list_available_sizes()
        
        self.assertIsInstance(sizes, list)
        self.assertIn('A0', sizes)
        self.assertIn('A1', sizes)
        self.assertIn('A2', sizes)
        self.assertIn('A3', sizes)
        self.assertIn('A4', sizes)
    
    def test_get_size_info(self):
        """Test getting paper size information."""
        info = self.generator.get_size_info('A4')
        
        self.assertIsInstance(info, dict)
        self.assertEqual(info['paper_size'], 'A4')
        self.assertEqual(info['width_mm'], 210)
        self.assertEqual(info['height_mm'], 297)


class TestFrameTemplateManager(unittest.TestCase):
    """Test cases for FrameTemplateManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.manager = FrameTemplateManager()
    
    def test_initialization(self):
        """Test FrameTemplateManager initialization."""
        self.assertIsInstance(self.manager, FrameTemplateManager)
        self.assertIn('A0', self.manager.PAPER_SIZES)
        self.assertIn('A4', self.manager.PAPER_SIZES)
    
    def test_get_default_template(self):
        """Test getting default template."""
        template = self.manager.get_template('A4')
        
        self.assertIsInstance(template, dict)
        self.assertIn('entities', template)
        self.assertIn('bounds', template)
        self.assertIn('size', template)
        self.assertEqual(template['paper_size'], 'A4')
        self.assertTrue(template.get('is_default', False))
    
    def test_paper_size_validation(self):
        """Test paper size validation."""
        # Valid paper size
        template = self.manager.get_template('A4')
        self.assertEqual(template['paper_size'], 'A4')
        
        # Invalid paper size
        with self.assertRaises(ValueError):
            self.manager.get_template('INVALID')
    
    def test_get_paper_size_info(self):
        """Test getting paper size information."""
        info = self.manager.get_paper_size_info('A4')
        
        self.assertEqual(info['paper_size'], 'A4')
        self.assertEqual(info['width_mm'], 210)
        self.assertEqual(info['height_mm'], 297)
        self.assertAlmostEqual(info['aspect_ratio'], 210/297, places=3)
    
    def test_validate_template(self):
        """Test template validation."""
        validation = self.manager.validate_template('A4')
        
        self.assertIsInstance(validation, dict)
        self.assertIn('is_valid', validation)
        self.assertIn('paper_size', validation)
        self.assertIn('template_size', validation)
        self.assertIn('standard_size', validation)


class TestDWGReader(unittest.TestCase):
    """Test cases for DWGReader class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.reader = DWGReader()
    
    def test_initialization(self):
        """Test DWGReader initialization."""
        self.assertIsInstance(self.reader, DWGReader)
        self.assertIn('.dwg', self.reader.supported_formats)
        self.assertIn('.dxf', self.reader.supported_formats)
    
    def test_file_not_found(self):
        """Test handling of non-existent files."""
        with self.assertRaises(FileNotFoundError):
            self.reader.read_frame_template('/nonexistent/file.dwg')
    
    def test_unsupported_format(self):
        """Test handling of unsupported file formats."""
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as tmp:
            tmp.write(b'test content')
            tmp_path = tmp.name
        
        try:
            with self.assertRaises(ValueError):
                self.reader.read_frame_template(tmp_path)
        finally:
            os.unlink(tmp_path)


if __name__ == '__main__':
    unittest.main()