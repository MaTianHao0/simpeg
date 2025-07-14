"""
CAD utilities for SimPEG - Computer Aided Design functionality.

This module provides CAD-related utilities including:
- DWG file reading and processing
- Frame template management  
- Geometric frame generation
- Reference point-based positioning

Example usage:
    from SimPEG.utils.cad import FrameGenerator
    
    generator = FrameGenerator()
    frame = generator.generate_frame('A0', reference_point=[0, 0])
"""

from .frame_generator import FrameGenerator
from .dwg_reader import DWGReader  
from .frame_templates import FrameTemplateManager

__all__ = ['FrameGenerator', 'DWGReader', 'FrameTemplateManager']