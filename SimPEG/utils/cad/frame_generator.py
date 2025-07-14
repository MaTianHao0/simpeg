"""
Frame generator for CAD frames in Rhino/Grasshopper.

This module provides the main frame generation functionality, allowing users
to generate frames based on templates and reference points.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Any, Union
from .frame_templates import FrameTemplateManager
from .dwg_reader import DWGReader


class FrameGenerator:
    """
    Generator for CAD frames based on templates and reference points.
    
    This class provides the main functionality for generating frames
    that can be used in Rhino/Grasshopper environments.
    """
    
    def __init__(self, template_directory: Optional[str] = None):
        """
        Initialize the frame generator.
        
        Parameters
        ----------
        template_directory : str, optional
            Directory containing frame template files
        """
        self.template_manager = FrameTemplateManager(template_directory)
        self.last_generated_frame = None
    
    def set_template_directory(self, directory: str):
        """
        Set the template directory.
        
        Parameters
        ----------
        directory : str
            Path to template directory
        """
        self.template_manager.set_template_directory(directory)
    
    def generate_frame(self, 
                      paper_size: str, 
                      reference_point: List[float] = [0, 0],
                      scale: float = 1.0,
                      rotation: float = 0.0,
                      units: str = 'mm') -> Dict[str, Any]:
        """
        Generate a frame based on template and reference point.
        
        Parameters
        ----------
        paper_size : str
            Paper size (A0, A1, A2, A3, A4)
        reference_point : list of float, optional
            Reference point for frame placement [x, y], default [0, 0]
        scale : float, optional
            Scale factor for the frame, default 1.0
        rotation : float, optional
            Rotation angle in degrees, default 0.0
        units : str, optional
            Units for the frame ('mm', 'cm', 'm'), default 'mm'
            
        Returns
        -------
        dict
            Generated frame data including:
            - 'entities': Transformed geometric entities
            - 'bounds': Bounding box of the generated frame
            - 'reference_point': Applied reference point
            - 'metadata': Generation metadata
        """
        # Get template
        template = self.template_manager.get_template(paper_size)
        
        # Apply unit conversion
        unit_scale = self._get_unit_scale(units)
        effective_scale = scale * unit_scale
        
        # Transform entities
        transformed_entities = []
        for entity in template['entities']:
            transformed_entity = self._transform_entity(
                entity, reference_point, effective_scale, rotation
            )
            transformed_entities.append(transformed_entity)
        
        # Calculate new bounds
        new_bounds = self._calculate_bounds(transformed_entities)
        
        # Prepare frame data
        frame_data = {
            'entities': transformed_entities,
            'bounds': new_bounds,
            'reference_point': reference_point,
            'paper_size': paper_size,
            'scale': scale,
            'rotation': rotation,
            'units': units,
            'metadata': {
                'template_file': template.get('file_path'),
                'is_default_template': template.get('is_default', False),
                'original_size': template['size'],
                'scaled_size': [
                    template['size'][0] * effective_scale,
                    template['size'][1] * effective_scale
                ],
                'entity_count': len(transformed_entities),
                'generation_params': {
                    'reference_point': reference_point,
                    'scale': scale,
                    'rotation': rotation,
                    'units': units
                }
            }
        }
        
        self.last_generated_frame = frame_data
        return frame_data
    
    def _get_unit_scale(self, units: str) -> float:
        """
        Get scale factor for unit conversion from mm.
        
        Parameters
        ----------
        units : str
            Target units
            
        Returns
        -------
        float
            Scale factor
        """
        unit_scales = {
            'mm': 1.0,
            'cm': 0.1,
            'm': 0.001,
            'in': 1.0 / 25.4,  # inches
            'ft': 1.0 / 304.8   # feet
        }
        
        return unit_scales.get(units.lower(), 1.0)
    
    def _transform_entity(self, 
                         entity: Dict[str, Any],
                         reference_point: List[float],
                         scale: float,
                         rotation: float) -> Dict[str, Any]:
        """
        Transform a single entity based on reference point, scale, and rotation.
        
        Parameters
        ----------
        entity : dict
            Entity to transform
        reference_point : list
            Reference point [x, y]
        scale : float
            Scale factor
        rotation : float
            Rotation angle in degrees
            
        Returns
        -------
        dict
            Transformed entity
        """
        transformed_entity = entity.copy()
        rotation_rad = np.radians(rotation)
        
        if entity['type'] == 'line':
            start = self._transform_point(entity['start'], reference_point, scale, rotation_rad)
            end = self._transform_point(entity['end'], reference_point, scale, rotation_rad)
            transformed_entity['start'] = start
            transformed_entity['end'] = end
            transformed_entity['bounds'] = [
                min(start[0], end[0]), min(start[1], end[1]),
                max(start[0], end[0]), max(start[1], end[1])
            ]
            
        elif entity['type'] == 'polyline':
            points = []
            for point in entity['points']:
                transformed_point = self._transform_point(point, reference_point, scale, rotation_rad)
                points.append(transformed_point)
            
            transformed_entity['points'] = points
            if points:
                x_coords = [p[0] for p in points]
                y_coords = [p[1] for p in points]
                transformed_entity['bounds'] = [min(x_coords), min(y_coords), max(x_coords), max(y_coords)]
            
        elif entity['type'] == 'circle':
            center = self._transform_point(entity['center'], reference_point, scale, rotation_rad)
            radius = entity['radius'] * scale
            transformed_entity['center'] = center
            transformed_entity['radius'] = radius
            transformed_entity['bounds'] = [
                center[0] - radius, center[1] - radius,
                center[0] + radius, center[1] + radius
            ]
            
        elif entity['type'] == 'text':
            insert_point = self._transform_point(entity['insert_point'], reference_point, scale, rotation_rad)
            height = entity['height'] * scale
            transformed_entity['insert_point'] = insert_point
            transformed_entity['height'] = height
            # Simplified bounds calculation for text
            text_width = len(entity['text']) * height * 0.6
            transformed_entity['bounds'] = [
                insert_point[0], insert_point[1],
                insert_point[0] + text_width, insert_point[1] + height
            ]
            
        elif entity['type'] == 'block':
            insert_point = self._transform_point(entity['insert_point'], reference_point, scale, rotation_rad)
            transformed_entity['insert_point'] = insert_point
            transformed_entity['scale'] = [s * scale for s in entity['scale']]
            transformed_entity['rotation'] = entity['rotation'] + rotation
            # Simplified bounds for blocks
            transformed_entity['bounds'] = insert_point + insert_point
        
        return transformed_entity
    
    def _transform_point(self, 
                        point: List[float],
                        reference_point: List[float],
                        scale: float,
                        rotation_rad: float) -> List[float]:
        """
        Transform a point with scale, rotation, and translation.
        
        Parameters
        ----------
        point : list
            Original point [x, y]
        reference_point : list
            Reference point for translation [x, y]
        scale : float
            Scale factor
        rotation_rad : float
            Rotation angle in radians
            
        Returns
        -------
        list
            Transformed point [x, y]
        """
        # Scale
        x = point[0] * scale
        y = point[1] * scale
        
        # Rotate around origin
        if rotation_rad != 0:
            cos_r = np.cos(rotation_rad)
            sin_r = np.sin(rotation_rad)
            x_rot = x * cos_r - y * sin_r
            y_rot = x * sin_r + y * cos_r
            x, y = x_rot, y_rot
        
        # Translate
        x += reference_point[0]
        y += reference_point[1]
        
        return [x, y]
    
    def _calculate_bounds(self, entities: List[Dict[str, Any]]) -> List[float]:
        """
        Calculate bounding box for a list of entities.
        
        Parameters
        ----------
        entities : list
            List of entities
            
        Returns
        -------
        list
            Bounding box [min_x, min_y, max_x, max_y]
        """
        if not entities:
            return [0, 0, 0, 0]
        
        bounds = [float('inf'), float('inf'), float('-inf'), float('-inf')]
        
        for entity in entities:
            if 'bounds' in entity:
                entity_bounds = entity['bounds']
                bounds[0] = min(bounds[0], entity_bounds[0])  # min_x
                bounds[1] = min(bounds[1], entity_bounds[1])  # min_y
                bounds[2] = max(bounds[2], entity_bounds[2])  # max_x
                bounds[3] = max(bounds[3], entity_bounds[3])  # max_y
        
        return bounds if bounds[0] != float('inf') else [0, 0, 0, 0]
    
    def get_rhino_geometry(self, frame_data: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Convert frame data to Rhino-compatible geometry definitions.
        
        Parameters
        ----------
        frame_data : dict, optional
            Frame data to convert. If None, uses last generated frame.
            
        Returns
        -------
        list
            List of Rhino geometry definitions
        """
        if frame_data is None:
            frame_data = self.last_generated_frame
            
        if frame_data is None:
            raise ValueError("No frame data available. Generate a frame first.")
        
        rhino_geometry = []
        
        for entity in frame_data['entities']:
            if entity['type'] == 'line':
                rhino_geometry.append({
                    'type': 'Line',
                    'start': entity['start'],
                    'end': entity['end']
                })
                
            elif entity['type'] == 'polyline':
                rhino_geometry.append({
                    'type': 'Polyline',
                    'points': entity['points'],
                    'closed': entity.get('closed', False)
                })
                
            elif entity['type'] == 'circle':
                rhino_geometry.append({
                    'type': 'Circle',
                    'center': entity['center'],
                    'radius': entity['radius']
                })
                
            elif entity['type'] == 'text':
                rhino_geometry.append({
                    'type': 'Text',
                    'text': entity['text'],
                    'location': entity['insert_point'],
                    'height': entity['height']
                })
        
        return rhino_geometry
    
    def get_grasshopper_data(self, frame_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Convert frame data to Grasshopper-compatible data structure.
        
        Parameters
        ----------
        frame_data : dict, optional
            Frame data to convert. If None, uses last generated frame.
            
        Returns
        -------
        dict
            Grasshopper-compatible data structure
        """
        if frame_data is None:
            frame_data = self.last_generated_frame
            
        if frame_data is None:
            raise ValueError("No frame data available. Generate a frame first.")
        
        # Separate geometry by type for Grasshopper
        lines = []
        polylines = []
        circles = []
        texts = []
        
        for entity in frame_data['entities']:
            if entity['type'] == 'line':
                lines.append({
                    'start': entity['start'],
                    'end': entity['end']
                })
            elif entity['type'] == 'polyline':
                polylines.append({
                    'points': entity['points'],
                    'closed': entity.get('closed', False)
                })
            elif entity['type'] == 'circle':
                circles.append({
                    'center': entity['center'],
                    'radius': entity['radius']
                })
            elif entity['type'] == 'text':
                texts.append({
                    'text': entity['text'],
                    'location': entity['insert_point'],
                    'height': entity['height']
                })
        
        return {
            'Lines': lines,
            'Polylines': polylines,
            'Circles': circles,
            'Texts': texts,
            'Bounds': frame_data['bounds'],
            'Metadata': frame_data['metadata']
        }
    
    def list_available_sizes(self) -> List[str]:
        """
        List available paper sizes.
        
        Returns
        -------
        list
            List of available paper sizes
        """
        return list(self.template_manager.PAPER_SIZES.keys())
    
    def get_size_info(self, paper_size: str) -> Dict[str, Any]:
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
        return self.template_manager.get_paper_size_info(paper_size)