# CAD Frame Generation System for SimPEG

This module provides Computer Aided Design (CAD) functionality for generating frame templates that can be used in Rhino/Grasshopper environments. It allows users to input a reference point and automatically generate standardized drawing frames (A0, A1, A2, A3, A4) based on DWG/DXF template files.

## Features

- **Multi-format Support**: Read DWG and DXF template files
- **Standard Paper Sizes**: Support for A0, A1, A2, A3, A4 formats
- **Reference Point Positioning**: Generate frames relative to user-defined reference points
- **Flexible Transformations**: Scale, rotate, and position frames as needed
- **Unit Conversion**: Support for mm, cm, m, inches, and feet
- **Rhino/Grasshopper Integration**: Export geometry in formats compatible with Rhino and Grasshopper
- **Template Management**: Organize and validate frame templates
- **Default Templates**: Fallback to generated templates when DWG files are not available

## Installation

The CAD module is part of SimPEG and requires the `ezdxf` package for DWG/DXF file reading:

```bash
pip install ezdxf
```

## Quick Start

### Basic Frame Generation

```python
from SimPEG.utils.cad import FrameGenerator

# Create frame generator
generator = FrameGenerator()

# Generate A4 frame at origin
frame = generator.generate_frame('A4')

# Generate A3 frame with custom reference point
frame_a3 = generator.generate_frame('A3', reference_point=[300, 400])

# Generate scaled and rotated frame
frame_scaled = generator.generate_frame(
    'A2', 
    reference_point=[100, 200],
    scale=0.8,
    rotation=45.0,
    units='mm'
)
```

### Using Template Files

```python
from SimPEG.utils.cad import FrameGenerator

# Set up generator with template directory
template_dir = '/path/to/your/templates'
generator = FrameGenerator(template_dir)

# Generate frame using template file
frame = generator.generate_frame('A3', reference_point=[0, 0])

# The system will automatically use A3_template.dxf if available
```

### Rhino/Grasshopper Integration

```python
# Generate frame
frame = generator.generate_frame('A1', reference_point=[500, 300])

# Get Rhino-compatible geometry
rhino_geometry = generator.get_rhino_geometry(frame)

# Get Grasshopper-compatible data structure
gh_data = generator.get_grasshopper_data(frame)

# Use the outputs in Grasshopper:
# - gh_data['Lines'] -> Line geometry components
# - gh_data['Polylines'] -> Polyline geometry components  
# - gh_data['Circles'] -> Circle geometry components
# - gh_data['Texts'] -> Text geometry components
# - gh_data['Bounds'] -> Bounding rectangle
```

## Template File Management

### Organizing Template Files

The system automatically detects template files based on naming conventions:

```
templates/
├── A0_template.dxf
├── A1_template.dxf  
├── A2_template.dxf
├── A3_template.dxf
└── A4_template.dxf
```

### Template File Requirements

- **Supported formats**: .dwg, .dxf
- **Naming convention**: Files should contain the paper size (A0, A1, A2, A3, A4) in the filename
- **Units**: Templates should be drawn in millimeters
- **Content**: Can include lines, polylines, circles, text, and blocks

### Creating Template Files

You can create template files using any CAD software that exports DWG/DXF:

1. **AutoCAD**: File → Export → DXF
2. **QCAD**: File → Export → DXF  
3. **LibreCAD**: File → Export → DXF
4. **FreeCAD**: File → Export → DXF

## API Reference

### FrameGenerator

Main class for generating frames.

#### Methods

- `generate_frame(paper_size, reference_point=[0,0], scale=1.0, rotation=0.0, units='mm')`: Generate a frame
- `get_rhino_geometry(frame_data=None)`: Convert frame to Rhino geometry
- `get_grasshopper_data(frame_data=None)`: Convert frame to Grasshopper data structure
- `list_available_sizes()`: Get list of supported paper sizes
- `get_size_info(paper_size)`: Get information about a paper size

### FrameTemplateManager

Class for managing frame templates.

#### Methods

- `set_template_directory(directory)`: Set template file directory
- `add_template(paper_size, file_path)`: Add a template file
- `get_template(paper_size)`: Load template data
- `validate_template(paper_size)`: Validate template dimensions
- `list_available_templates()`: List available template files

### DWGReader

Class for reading DWG/DXF files.

#### Methods

- `read_frame_template(file_path)`: Read template from DWG/DXF file
- `get_frame_info(file_path)`: Get basic template information

## Grasshopper Battery/Component Usage

This system is designed to work as a Grasshopper battery (component) with the following workflow:

### Input Parameters
- **Paper Size** (Text): "A0", "A1", "A2", "A3", or "A4"
- **Reference Point** (Point): User-defined reference point in Rhino
- **Scale** (Number): Scale factor (default: 1.0)
- **Rotation** (Number): Rotation angle in degrees (default: 0.0)
- **Units** (Text): "mm", "cm", "m", "in", or "ft" (default: "mm")
- **Template Directory** (Text): Path to template files (optional)

### Output Parameters
- **Lines** (Line): Line geometry from the frame
- **Polylines** (Polyline): Polyline geometry from the frame
- **Circles** (Circle): Circle geometry from the frame
- **Texts** (Text): Text objects from the frame
- **Bounds** (Rectangle): Bounding box of the frame
- **Info** (Text): Generation metadata and information

### Example Grasshopper Component Implementation

```python
# In Grasshopper Python component:

import sys
sys.path.append(r'C:\path\to\simpeg')  # Adjust path as needed

from SimPEG.utils.cad import FrameGenerator

# Get inputs from Grasshopper
paper_size = paper_size if 'paper_size' in locals() else 'A4'
ref_point = ref_point if 'ref_point' in locals() else [0, 0]
scale = scale if 'scale' in locals() else 1.0
rotation = rotation if 'rotation' in locals() else 0.0
units = units if 'units' in locals() else 'mm'

# Convert Rhino point to list
if hasattr(ref_point, 'X'):
    ref_point = [ref_point.X, ref_point.Y]

# Generate frame
generator = FrameGenerator(template_directory)
frame = generator.generate_frame(
    paper_size=paper_size,
    reference_point=ref_point,
    scale=scale,
    rotation=rotation,
    units=units
)

# Get Grasshopper outputs
gh_data = generator.get_grasshopper_data(frame)

# Set outputs
Lines = [Rhino.Geometry.Line(Rhino.Geometry.Point3d(*line['start']), 
                            Rhino.Geometry.Point3d(*line['end'])) 
         for line in gh_data['Lines']]

Polylines = [Rhino.Geometry.Polyline([Rhino.Geometry.Point3d(*pt) 
                                     for pt in pline['points']]) 
            for pline in gh_data['Polylines']]

Circles = [Rhino.Geometry.Circle(Rhino.Geometry.Point3d(*circle['center']), 
                                circle['radius'])
          for circle in gh_data['Circles']]

# Text objects would need additional processing based on Rhino's text handling

# Bounding box
bounds = gh_data['Bounds']
Bounds = Rhino.Geometry.Rectangle3d(
    Rhino.Geometry.Plane.WorldXY,
    bounds[2] - bounds[0],  # width
    bounds[3] - bounds[1]   # height
)
Bounds.Transform(Rhino.Geometry.Transform.Translation(bounds[0], bounds[1], 0))

# Information
Info = f"Paper: {paper_size}, Entities: {len(frame['entities'])}, Template: {frame['metadata'].get('template_file', 'Default')}"
```

## Examples

See the `examples/cad/` directory for comprehensive examples:

- `frame_generation_example.py`: Basic usage examples
- `template_usage_example.py`: Working with DXF template files
- `create_templates.py`: Script to create sample template files

## Paper Size Specifications

| Size | Width (mm) | Height (mm) | Aspect Ratio |
|------|------------|-------------|--------------|
| A0   | 841        | 1189        | 0.707        |
| A1   | 594        | 841         | 0.706        |
| A2   | 420        | 594         | 0.707        |
| A3   | 297        | 420         | 0.707        |
| A4   | 210        | 297         | 0.707        |

## Troubleshooting

### Common Issues

1. **"ezdxf package not available"**
   - Install ezdxf: `pip install ezdxf`

2. **Template file not found**
   - Check file path and naming convention
   - Ensure file has .dwg or .dxf extension
   - Verify template directory is set correctly

3. **Template validation fails**
   - Check that template dimensions are reasonable
   - Ensure template is drawn in millimeters
   - Verify template contains geometric entities

4. **Empty geometry output**
   - Check that template file contains supported entities (lines, polylines, circles, text)
   - Verify template is not corrupted
   - Try using default templates first

### Debug Mode

Enable verbose output for troubleshooting:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Your frame generation code here
```

## Contributing

To contribute to the CAD module:

1. Add new features in the appropriate module file
2. Write comprehensive tests in `tests/cad/`
3. Update documentation and examples
4. Ensure compatibility with existing Rhino/Grasshopper workflows

## License

This module is part of SimPEG and follows the same MIT license terms.