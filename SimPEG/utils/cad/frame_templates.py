"""
Frame template management for CAD frames.

This module manages frame templates for different paper sizes (A0, A1, A2, A3)
and provides methods to load and organize template files.
"""

import os
import json
from typing import Dict, List, Tuple, Optional, Any
from .dwg_reader import DWGReader


class FrameTemplateManager:
    """
    Manager for frame templates in various paper sizes.
    
    This class handles loading, caching, and organizing frame templates
    from DWG/DXF files for different paper formats.
    """
    
    # Standard ISO paper sizes in millimeters
    PAPER_SIZES = {
        'A0': [841, 1189],
        'A1': [594, 841], 
        'A2': [420, 594],
        'A3': [297, 420],
        'A4': [210, 297]
    }
    
    def __init__(self, template_directory: Optional[str] = None):
        """
        Initialize the frame template manager.
        
        Parameters
        ----------
        template_directory : str, optional
            Directory containing frame template files.
            If None, uses default template directory.
        """
        self.template_directory = template_directory
        self.dwg_reader = DWGReader()
        self._templates_cache = {}
        self._template_files = {}
        
        if template_directory and os.path.exists(template_directory):
            self._scan_template_directory()
    
    def set_template_directory(self, directory: str):
        """
        Set the template directory and scan for template files.
        
        Parameters
        ----------
        directory : str
            Path to directory containing template files
        """
        if not os.path.exists(directory):
            raise FileNotFoundError(f"Template directory not found: {directory}")
            
        self.template_directory = directory
        self._scan_template_directory()
    
    def _scan_template_directory(self):
        """Scan the template directory for DWG/DXF files."""
        if not self.template_directory:
            return
            
        self._template_files = {}
        
        for filename in os.listdir(self.template_directory):
            file_path = os.path.join(self.template_directory, filename)
            file_ext = os.path.splitext(filename)[1].lower()
            
            if file_ext in ['.dwg', '.dxf'] and os.path.isfile(file_path):
                # Try to determine paper size from filename
                paper_size = self._extract_paper_size_from_filename(filename)
                if paper_size:
                    self._template_files[paper_size] = file_path
    
    def _extract_paper_size_from_filename(self, filename: str) -> Optional[str]:
        """
        Extract paper size from filename.
        
        Parameters
        ----------
        filename : str
            The filename to analyze
            
        Returns
        -------
        str or None
            Paper size if found, None otherwise
        """
        filename_upper = filename.upper()
        for paper_size in self.PAPER_SIZES.keys():
            if paper_size in filename_upper:
                return paper_size
        return None
    
    def add_template(self, paper_size: str, file_path: str):
        """
        Add a template file for a specific paper size.
        
        Parameters
        ----------
        paper_size : str
            Paper size (e.g., 'A0', 'A1', 'A2', 'A3')
        file_path : str
            Path to the template file
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Template file not found: {file_path}")
            
        paper_size = paper_size.upper()
        if paper_size not in self.PAPER_SIZES:
            raise ValueError(f"Unsupported paper size: {paper_size}")
            
        self._template_files[paper_size] = file_path
        
        # Clear cache for this template
        if paper_size in self._templates_cache:
            del self._templates_cache[paper_size]
    
    def get_template(self, paper_size: str) -> Dict[str, Any]:
        """
        Get template data for a specific paper size.
        
        Parameters
        ----------
        paper_size : str
            Paper size (e.g., 'A0', 'A1', 'A2', 'A3')
            
        Returns
        -------
        dict
            Template data including geometry and metadata
        """
        paper_size = paper_size.upper()
        
        if paper_size not in self.PAPER_SIZES:
            raise ValueError(f"Unsupported paper size: {paper_size}")
        
        # Check cache first
        if paper_size in self._templates_cache:
            return self._templates_cache[paper_size]
        
        # Load from file if available
        if paper_size in self._template_files:
            template_data = self.dwg_reader.read_frame_template(self._template_files[paper_size])
            template_data['paper_size'] = paper_size
            template_data['standard_size'] = self.PAPER_SIZES[paper_size]
            
            # Cache the template
            self._templates_cache[paper_size] = template_data
            return template_data
        else:
            # Generate default template if no file available
            return self._generate_default_template(paper_size)
    
    def _generate_default_template(self, paper_size: str) -> Dict[str, Any]:
        """
        Generate a default template for a paper size.
        
        Parameters
        ----------
        paper_size : str
            Paper size to generate template for
            
        Returns
        -------
        dict
            Default template data
        """
        size = self.PAPER_SIZES[paper_size]
        margin = 20  # 20mm margin
        
        # Create a simple rectangular frame
        entities = [
            {
                'type': 'line',
                'start': [margin, margin],
                'end': [size[0] - margin, margin],
                'bounds': [margin, margin, size[0] - margin, margin]
            },
            {
                'type': 'line', 
                'start': [size[0] - margin, margin],
                'end': [size[0] - margin, size[1] - margin],
                'bounds': [size[0] - margin, margin, size[0] - margin, size[1] - margin]
            },
            {
                'type': 'line',
                'start': [size[0] - margin, size[1] - margin],
                'end': [margin, size[1] - margin],
                'bounds': [margin, size[1] - margin, size[0] - margin, size[1] - margin]
            },
            {
                'type': 'line',
                'start': [margin, size[1] - margin],
                'end': [margin, margin],
                'bounds': [margin, margin, margin, size[1] - margin]
            },
            {
                'type': 'text',
                'text': f'{paper_size} Frame',
                'insert_point': [margin + 10, size[1] - margin - 20],
                'height': 10,
                'bounds': [margin + 10, size[1] - margin - 20, margin + 100, size[1] - margin - 10]
            }
        ]
        
        return {
            'entities': entities,
            'bounds': [0, 0, size[0], size[1]],
            'size': size,
            'reference_point': [0, 0],
            'paper_size': paper_size,
            'standard_size': size,
            'file_path': None,
            'is_default': True
        }
    
    def list_available_templates(self) -> Dict[str, str]:
        """
        List all available templates.
        
        Returns
        -------
        dict
            Dictionary mapping paper sizes to file paths
        """
        return self._template_files.copy()
    
    def get_paper_size_info(self, paper_size: str) -> Dict[str, Any]:
        """
        Get information about a paper size.
        
        Parameters
        ----------
        paper_size : str
            Paper size to get info for
            
        Returns
        -------
        dict
            Paper size information
        """
        paper_size = paper_size.upper()
        if paper_size not in self.PAPER_SIZES:
            raise ValueError(f"Unsupported paper size: {paper_size}")
            
        size = self.PAPER_SIZES[paper_size]
        has_template = paper_size in self._template_files
        
        return {
            'paper_size': paper_size,
            'width_mm': size[0],
            'height_mm': size[1],
            'aspect_ratio': size[0] / size[1],
            'has_custom_template': has_template,
            'template_file': self._template_files.get(paper_size)
        }
    
    def validate_template(self, paper_size: str) -> Dict[str, Any]:
        """
        Validate a template and return validation results.
        
        Parameters
        ----------
        paper_size : str
            Paper size to validate
            
        Returns
        -------
        dict
            Validation results
        """
        try:
            template = self.get_template(paper_size)
            
            # Check if template has reasonable dimensions
            template_size = template['size']
            standard_size = self.PAPER_SIZES[paper_size.upper()]
            
            size_ratio_x = template_size[0] / standard_size[0] if standard_size[0] > 0 else 0
            size_ratio_y = template_size[1] / standard_size[1] if standard_size[1] > 0 else 0
            
            is_valid = (0.8 <= size_ratio_x <= 1.2) and (0.8 <= size_ratio_y <= 1.2)
            
            return {
                'is_valid': is_valid,
                'paper_size': paper_size,
                'template_size': template_size,
                'standard_size': standard_size,
                'size_ratio': [size_ratio_x, size_ratio_y],
                'entity_count': len(template['entities']),
                'has_file': not template.get('is_default', False)
            }
            
        except Exception as e:
            return {
                'is_valid': False,
                'error': str(e),
                'paper_size': paper_size
            }