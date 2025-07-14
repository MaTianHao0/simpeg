"""
DWG file reader for CAD frame templates.

This module provides functionality to read DWG files containing frame templates
and extract geometric data for frame generation.
"""

import os
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
import warnings

try:
    import ezdxf
    EZDXF_AVAILABLE = True
except ImportError:
    EZDXF_AVAILABLE = False
    warnings.warn("ezdxf package not available. DWG/DXF reading functionality will be limited.")


class DWGReader:
    """
    Reader for DWG/DXF files containing frame templates.
    
    This class provides methods to read CAD files and extract frame geometry
    that can be used for generating frames in Rhino/Grasshopper.
    """
    
    def __init__(self):
        """Initialize the DWG reader."""
        self.supported_formats = ['.dwg', '.dxf']
        if not EZDXF_AVAILABLE:
            warnings.warn("ezdxf not available - install with: pip install ezdxf")
    
    def read_frame_template(self, file_path: str) -> Dict[str, Any]:
        """
        Read a frame template from a DWG/DXF file.
        
        Parameters
        ----------
        file_path : str
            Path to the DWG/DXF file containing the frame template
            
        Returns
        -------
        dict
            Dictionary containing frame geometry data including:
            - 'entities': List of geometric entities (lines, rectangles, text, etc.)
            - 'bounds': Bounding box of the frame
            - 'size': Frame size (width, height)
            - 'reference_point': Default reference point
        """
        if not EZDXF_AVAILABLE:
            raise ImportError("ezdxf package is required for DWG/DXF reading")
            
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        file_ext = os.path.splitext(file_path)[1].lower()
        if file_ext not in self.supported_formats:
            raise ValueError(f"Unsupported file format: {file_ext}")
        
        try:
            # Read the DXF/DWG file
            doc = ezdxf.readfile(file_path)
            modelspace = doc.modelspace()
            
            # Extract entities
            entities = []
            bounds = [float('inf'), float('inf'), float('-inf'), float('-inf')]  # min_x, min_y, max_x, max_y
            
            for entity in modelspace:
                entity_data = self._extract_entity_data(entity)
                if entity_data:
                    entities.append(entity_data)
                    
                    # Update bounds
                    if 'bounds' in entity_data:
                        entity_bounds = entity_data['bounds']
                        bounds[0] = min(bounds[0], entity_bounds[0])  # min_x
                        bounds[1] = min(bounds[1], entity_bounds[1])  # min_y
                        bounds[2] = max(bounds[2], entity_bounds[2])  # max_x
                        bounds[3] = max(bounds[3], entity_bounds[3])  # max_y
            
            # Calculate frame size
            width = bounds[2] - bounds[0] if bounds[0] != float('inf') else 0
            height = bounds[3] - bounds[1] if bounds[1] != float('inf') else 0
            
            # Set reference point at bottom-left corner
            reference_point = [bounds[0], bounds[1]] if bounds[0] != float('inf') else [0, 0]
            
            return {
                'entities': entities,
                'bounds': bounds,
                'size': [width, height],
                'reference_point': reference_point,
                'file_path': file_path
            }
            
        except Exception as e:
            raise RuntimeError(f"Error reading file {file_path}: {str(e)}")
    
    def _extract_entity_data(self, entity) -> Optional[Dict[str, Any]]:
        """
        Extract data from a DXF entity.
        
        Parameters
        ----------
        entity
            DXF entity from ezdxf
            
        Returns
        -------
        dict or None
            Entity data dictionary or None if entity type not supported
        """
        if not EZDXF_AVAILABLE:
            return None
            
        entity_type = entity.dxftype()
        
        if entity_type == 'LINE':
            start = [entity.dxf.start.x, entity.dxf.start.y]
            end = [entity.dxf.end.x, entity.dxf.end.y]
            return {
                'type': 'line',
                'start': start,
                'end': end,
                'bounds': [
                    min(start[0], end[0]), min(start[1], end[1]),
                    max(start[0], end[0]), max(start[1], end[1])
                ]
            }
            
        elif entity_type == 'LWPOLYLINE':
            points = []
            for point in entity.get_points():
                points.append([point[0], point[1]])
            
            if points:
                x_coords = [p[0] for p in points]
                y_coords = [p[1] for p in points]
                bounds = [min(x_coords), min(y_coords), max(x_coords), max(y_coords)]
            else:
                bounds = [0, 0, 0, 0]
                
            return {
                'type': 'polyline',
                'points': points,
                'closed': entity.closed,
                'bounds': bounds
            }
            
        elif entity_type == 'CIRCLE':
            center = [entity.dxf.center.x, entity.dxf.center.y]
            radius = entity.dxf.radius
            return {
                'type': 'circle',
                'center': center,
                'radius': radius,
                'bounds': [
                    center[0] - radius, center[1] - radius,
                    center[0] + radius, center[1] + radius
                ]
            }
            
        elif entity_type == 'TEXT':
            insert_point = [entity.dxf.insert.x, entity.dxf.insert.y]
            return {
                'type': 'text',
                'text': entity.dxf.text,
                'insert_point': insert_point,
                'height': entity.dxf.height,
                'bounds': [
                    insert_point[0], insert_point[1],
                    insert_point[0] + len(entity.dxf.text) * entity.dxf.height * 0.6,
                    insert_point[1] + entity.dxf.height
                ]
            }
            
        elif entity_type == 'INSERT':
            # Block reference (useful for title blocks)
            insert_point = [entity.dxf.insert.x, entity.dxf.insert.y]
            return {
                'type': 'block',
                'name': entity.dxf.name,
                'insert_point': insert_point,
                'scale': [entity.dxf.xscale, entity.dxf.yscale],
                'rotation': entity.dxf.rotation,
                'bounds': insert_point + insert_point  # Simplified bounds
            }
        
        return None
    
    def get_frame_info(self, file_path: str) -> Dict[str, Any]:
        """
        Get basic information about a frame template file.
        
        Parameters
        ----------
        file_path : str
            Path to the frame template file
            
        Returns
        -------
        dict
            Basic frame information
        """
        template_data = self.read_frame_template(file_path)
        return {
            'file_path': file_path,
            'size': template_data['size'],
            'entity_count': len(template_data['entities']),
            'bounds': template_data['bounds']
        }