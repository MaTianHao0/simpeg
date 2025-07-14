"""
Script to create sample DWG/DXF template files for demonstration purposes.

This script creates basic frame templates in DXF format that can be used
to demonstrate the DWG reading functionality.
"""

import os
import ezdxf
from ezdxf import units


def create_a4_template(output_path):
    """Create a basic A4 template."""
    doc = ezdxf.new('R2010', units=units.MM)
    msp = doc.modelspace()
    
    # A4 dimensions in mm
    width, height = 210, 297
    margin = 20
    
    # Border rectangle
    msp.add_lwpolyline([
        (margin, margin),
        (width - margin, margin),
        (width - margin, height - margin),
        (margin, height - margin),
        (margin, margin)
    ])
    
    # Title block
    title_width = 150
    title_height = 50
    title_x = width - margin - title_width
    title_y = margin
    
    # Title block border
    msp.add_lwpolyline([
        (title_x, title_y),
        (width - margin, title_y),
        (width - margin, title_y + title_height),
        (title_x, title_y + title_height),
        (title_x, title_y)
    ])
    
    # Title text
    msp.add_text("A4 DRAWING FRAME", 
                 dxfattribs={'insert': (title_x + 10, title_y + title_height - 15),
                            'height': 10})
    
    # Scale text
    msp.add_text("SCALE: 1:1",
                 dxfattribs={'insert': (title_x + 10, title_y + 25),
                            'height': 7})
    
    # Drawing number
    msp.add_text("DWG NO: A4-001",
                 dxfattribs={'insert': (title_x + 10, title_y + 10),
                            'height': 7})
    
    doc.saveas(output_path)
    print(f"Created A4 template: {output_path}")


def create_a3_template(output_path):
    """Create a basic A3 template."""
    doc = ezdxf.new('R2010', units=units.MM)
    msp = doc.modelspace()
    
    # A3 dimensions in mm
    width, height = 420, 297
    margin = 25
    
    # Border rectangle
    msp.add_lwpolyline([
        (margin, margin),
        (width - margin, margin),
        (width - margin, height - margin),
        (margin, height - margin),
        (margin, margin)
    ])
    
    # Inner border
    inner_margin = margin + 5
    msp.add_lwpolyline([
        (inner_margin, inner_margin),
        (width - inner_margin, inner_margin),
        (width - inner_margin, height - inner_margin),
        (inner_margin, height - inner_margin),
        (inner_margin, inner_margin)
    ])
    
    # Title block
    title_width = 180
    title_height = 60
    title_x = width - margin - title_width
    title_y = margin
    
    # Title block border
    msp.add_lwpolyline([
        (title_x, title_y),
        (width - margin, title_y),
        (width - margin, title_y + title_height),
        (title_x, title_y + title_height),
        (title_x, title_y)
    ])
    
    # Divide title block
    msp.add_line((title_x, title_y + 40), (width - margin, title_y + 40))
    msp.add_line((title_x + 90, title_y), (title_x + 90, title_y + title_height))
    
    # Title text
    msp.add_text("A3 DRAWING FRAME", 
                 dxfattribs={'insert': (title_x + 10, title_y + 45),
                            'height': 12})
    
    # Project info
    msp.add_text("PROJECT:",
                 dxfattribs={'insert': (title_x + 10, title_y + 30),
                            'height': 6})
    
    msp.add_text("DRAWN BY:",
                 dxfattribs={'insert': (title_x + 10, title_y + 20),
                            'height': 6})
    
    msp.add_text("DATE:",
                 dxfattribs={'insert': (title_x + 10, title_y + 10),
                            'height': 6})
    
    # Scale and drawing number
    msp.add_text("SCALE: 1:1",
                 dxfattribs={'insert': (title_x + 100, title_y + 30),
                            'height': 8})
    
    msp.add_text("DWG NO:",
                 dxfattribs={'insert': (title_x + 100, title_y + 20),
                            'height': 6})
    
    msp.add_text("A3-001",
                 dxfattribs={'insert': (title_x + 100, title_y + 10),
                            'height': 8})
    
    doc.saveas(output_path)
    print(f"Created A3 template: {output_path}")


def create_a2_template(output_path):
    """Create a basic A2 template."""
    doc = ezdxf.new('R2010', units=units.MM)
    msp = doc.modelspace()
    
    # A2 dimensions in mm
    width, height = 594, 420
    margin = 30
    
    # Border rectangle with rounded corners (approximated with lines)
    msp.add_lwpolyline([
        (margin, margin),
        (width - margin, margin),
        (width - margin, height - margin),
        (margin, height - margin),
        (margin, margin)
    ])
    
    # Grid lines for reference
    grid_spacing = 50
    for x in range(margin + grid_spacing, width - margin, grid_spacing):
        msp.add_line((x, margin + 5), (x, height - margin - 5),
                     dxfattribs={'linetype': 'DASHED'})
    
    for y in range(margin + grid_spacing, height - margin, grid_spacing):
        msp.add_line((margin + 5, y), (width - margin - 5, y),
                     dxfattribs={'linetype': 'DASHED'})
    
    # Title block
    title_width = 200
    title_height = 80
    title_x = width - margin - title_width
    title_y = margin
    
    # Title block border
    msp.add_lwpolyline([
        (title_x, title_y),
        (width - margin, title_y),
        (width - margin, title_y + title_height),
        (title_x, title_y + title_height),
        (title_x, title_y)
    ])
    
    # Complex title block divisions
    msp.add_line((title_x, title_y + 50), (width - margin, title_y + 50))
    msp.add_line((title_x, title_y + 30), (width - margin, title_y + 30))
    msp.add_line((title_x + 100, title_y), (title_x + 100, title_y + 50))
    
    # Title text
    msp.add_text("A2 TECHNICAL DRAWING", 
                 dxfattribs={'insert': (title_x + 10, title_y + 60),
                            'height': 14})
    
    # Company info
    msp.add_text("COMPANY NAME",
                 dxfattribs={'insert': (title_x + 10, title_y + 40),
                            'height': 8})
    
    # Drawing details
    fields = [
        ("PROJECT:", title_x + 10, title_y + 20),
        ("DRAWN BY:", title_x + 10, title_y + 10),
        ("CHECKED BY:", title_x + 10, title_y + 2),
        ("SCALE:", title_x + 110, title_y + 20),
        ("DATE:", title_x + 110, title_y + 10),
        ("DWG NO: A2-001", title_x + 110, title_y + 2)
    ]
    
    for text, x, y in fields:
        msp.add_text(text, dxfattribs={'insert': (x, y), 'height': 6})
    
    doc.saveas(output_path)
    print(f"Created A2 template: {output_path}")


def create_a1_template(output_path):
    """Create a basic A1 template."""
    doc = ezdxf.new('R2010', units=units.MM)
    msp = doc.modelspace()
    
    # A1 dimensions in mm
    width, height = 841, 594
    margin = 40
    
    # Double border
    msp.add_lwpolyline([
        (margin, margin),
        (width - margin, margin),
        (width - margin, height - margin),
        (margin, height - margin),
        (margin, margin)
    ])
    
    inner_margin = margin + 10
    msp.add_lwpolyline([
        (inner_margin, inner_margin),
        (width - inner_margin, inner_margin),
        (width - inner_margin, height - inner_margin),
        (inner_margin, height - inner_margin),
        (inner_margin, inner_margin)
    ])
    
    # Reference grid
    grid_spacing = 100
    for x in range(margin + grid_spacing, width - margin, grid_spacing):
        msp.add_line((x, margin + 10), (x, height - margin - 10),
                     dxfattribs={'linetype': 'CENTER'})
    
    for y in range(margin + grid_spacing, height - margin, grid_spacing):
        msp.add_line((margin + 10, y), (width - margin - 10, y),
                     dxfattribs={'linetype': 'CENTER'})
    
    # Large title block
    title_width = 250
    title_height = 100
    title_x = width - margin - title_width
    title_y = margin
    
    # Title block border
    msp.add_lwpolyline([
        (title_x, title_y),
        (width - margin, title_y),
        (width - margin, title_y + title_height),
        (title_x, title_y + title_height),
        (title_x, title_y)
    ])
    
    # Title block divisions
    msp.add_line((title_x, title_y + 70), (width - margin, title_y + 70))
    msp.add_line((title_x, title_y + 50), (width - margin, title_y + 50))
    msp.add_line((title_x, title_y + 30), (width - margin, title_y + 30))
    msp.add_line((title_x + 125, title_y), (title_x + 125, title_y + 70))
    
    # Main title
    msp.add_text("A1 ENGINEERING DRAWING", 
                 dxfattribs={'insert': (title_x + 20, title_y + 80),
                            'height': 16})
    
    # Detailed information
    info_fields = [
        ("PROJECT TITLE:", title_x + 10, title_y + 60),
        ("DRAWING TITLE:", title_x + 10, title_y + 40),
        ("DRAWN BY:", title_x + 10, title_y + 20),
        ("CHECKED BY:", title_x + 10, title_y + 10),
        ("APPROVED BY:", title_x + 10, title_y + 2),
        ("SCALE: 1:50", title_x + 135, title_y + 40),
        ("DATE:", title_x + 135, title_y + 30),
        ("REVISION:", title_x + 135, title_y + 20),
        ("SHEET:", title_x + 135, title_y + 10),
        ("DWG NO: A1-001", title_x + 135, title_y + 2)
    ]
    
    for text, x, y in info_fields:
        msp.add_text(text, dxfattribs={'insert': (x, y), 'height': 7})
    
    doc.saveas(output_path)
    print(f"Created A1 template: {output_path}")


def create_a0_template(output_path):
    """Create a basic A0 template."""
    doc = ezdxf.new('R2010', units=units.MM)
    msp = doc.modelspace()
    
    # A0 dimensions in mm
    width, height = 1189, 841
    margin = 50
    
    # Triple border system
    msp.add_lwpolyline([
        (margin, margin),
        (width - margin, margin),
        (width - margin, height - margin),
        (margin, height - margin),
        (margin, margin)
    ])
    
    mid_margin = margin + 15
    msp.add_lwpolyline([
        (mid_margin, mid_margin),
        (width - mid_margin, mid_margin),
        (width - mid_margin, height - mid_margin),
        (mid_margin, height - mid_margin),
        (mid_margin, mid_margin)
    ])
    
    inner_margin = margin + 25
    msp.add_lwpolyline([
        (inner_margin, inner_margin),
        (width - inner_margin, inner_margin),
        (width - inner_margin, height - inner_margin),
        (inner_margin, height - inner_margin),
        (inner_margin, inner_margin)
    ])
    
    # Comprehensive grid system
    grid_spacing = 100
    for x in range(margin + grid_spacing, width - margin, grid_spacing):
        msp.add_line((x, margin + 25), (x, height - margin - 25),
                     dxfattribs={'linetype': 'CENTER'})
    
    for y in range(margin + grid_spacing, height - margin, grid_spacing):
        msp.add_line((margin + 25, y), (width - margin - 25, y),
                     dxfattribs={'linetype': 'CENTER'})
    
    # Professional title block
    title_width = 300
    title_height = 120
    title_x = width - margin - title_width
    title_y = margin
    
    # Title block border
    msp.add_lwpolyline([
        (title_x, title_y),
        (width - margin, title_y),
        (width - margin, title_y + title_height),
        (title_x, title_y + title_height),
        (title_x, title_y)
    ])
    
    # Complex title block layout
    msp.add_line((title_x, title_y + 90), (width - margin, title_y + 90))
    msp.add_line((title_x, title_y + 70), (width - margin, title_y + 70))
    msp.add_line((title_x, title_y + 50), (width - margin, title_y + 50))
    msp.add_line((title_x, title_y + 30), (width - margin, title_y + 30))
    msp.add_line((title_x + 150, title_y), (title_x + 150, title_y + 90))
    
    # Company logo area
    msp.add_circle((title_x + 50, title_y + 105), 10)
    msp.add_text("LOGO", dxfattribs={'insert': (title_x + 45, title_y + 100), 'height': 6})
    
    # Main title
    msp.add_text("A0 MASTER DRAWING", 
                 dxfattribs={'insert': (title_x + 80, title_y + 100),
                            'height': 18})
    
    # Professional fields
    fields = [
        ("PROJECT:", title_x + 10, title_y + 80),
        ("DRAWING TITLE:", title_x + 10, title_y + 60),
        ("DESCRIPTION:", title_x + 10, title_y + 40),
        ("DRAWN BY:", title_x + 10, title_y + 20),
        ("DESIGNED BY:", title_x + 10, title_y + 10),
        ("CHECKED BY:", title_x + 10, title_y + 2),
        ("SCALE:", title_x + 160, title_y + 60),
        ("DATE:", title_x + 160, title_y + 50),
        ("REVISION:", title_x + 160, title_y + 40),
        ("SHEET NO:", title_x + 160, title_y + 30),
        ("TOTAL SHEETS:", title_x + 160, title_y + 20),
        ("DWG NO:", title_x + 160, title_y + 10),
        ("A0-001", title_x + 160, title_y + 2)
    ]
    
    for text, x, y in fields:
        msp.add_text(text, dxfattribs={'insert': (x, y), 'height': 8})
    
    doc.saveas(output_path)
    print(f"Created A0 template: {output_path}")


def main():
    """Create all template files."""
    template_dir = "/home/runner/work/simpeg/simpeg/examples/cad/templates"
    
    templates = [
        ("A4_template.dxf", create_a4_template),
        ("A3_template.dxf", create_a3_template),
        ("A2_template.dxf", create_a2_template),
        ("A1_template.dxf", create_a1_template),
        ("A0_template.dxf", create_a0_template)
    ]
    
    print("Creating DXF template files...")
    for filename, create_func in templates:
        file_path = os.path.join(template_dir, filename)
        create_func(file_path)
    
    print(f"\nAll templates created in: {template_dir}")
    print("Files created:")
    for filename, _ in templates:
        print(f"  - {filename}")


if __name__ == "__main__":
    main()