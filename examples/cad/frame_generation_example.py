"""
Example usage of the CAD frame generation system.

This script demonstrates how to use the frame generation functionality
for creating CAD frames that can be used in Rhino/Grasshopper.
"""

import os
import sys
import numpy as np

# Add SimPEG to path if running as script
if __name__ == '__main__':
    simpeg_path = os.path.join(os.path.dirname(__file__), '..', '..')
    if simpeg_path not in sys.path:
        sys.path.insert(0, simpeg_path)

from SimPEG.utils.cad import FrameGenerator, FrameTemplateManager


def basic_frame_generation_example():
    """
    Example: Basic frame generation with default templates.
    """
    print("=== Basic Frame Generation Example ===")
    
    # Create frame generator
    generator = FrameGenerator()
    
    # Generate A4 frame at origin
    frame = generator.generate_frame('A4')
    print(f"Generated A4 frame with {len(frame['entities'])} entities")
    print(f"Frame bounds: {frame['bounds']}")
    print(f"Frame size: {frame['metadata']['scaled_size']}")
    
    # Generate A3 frame with custom reference point
    frame_a3 = generator.generate_frame('A3', reference_point=[300, 400])
    print(f"Generated A3 frame at reference point [300, 400]")
    print(f"A3 Frame bounds: {frame_a3['bounds']}")
    
    return frame, frame_a3


def scaled_and_rotated_frame_example():
    """
    Example: Generate frames with scaling and rotation.
    """
    print("\n=== Scaled and Rotated Frame Example ===")
    
    generator = FrameGenerator()
    
    # Generate scaled frame
    scaled_frame = generator.generate_frame(
        'A2', 
        reference_point=[0, 0],
        scale=0.5,
        units='mm'
    )
    print(f"Generated half-scale A2 frame")
    print(f"Original A2 size: {generator.get_size_info('A2')['width_mm']}x{generator.get_size_info('A2')['height_mm']}mm")
    print(f"Scaled size: {scaled_frame['metadata']['scaled_size']}")
    
    # Generate rotated frame
    rotated_frame = generator.generate_frame(
        'A4',
        reference_point=[100, 100], 
        rotation=45.0
    )
    print(f"Generated A4 frame rotated 45 degrees")
    print(f"Rotated frame bounds: {rotated_frame['bounds']}")
    
    return scaled_frame, rotated_frame


def unit_conversion_example():
    """
    Example: Generate frames in different units.
    """
    print("\n=== Unit Conversion Example ===")
    
    generator = FrameGenerator()
    
    # Generate frames in different units
    frame_mm = generator.generate_frame('A4', units='mm')
    frame_cm = generator.generate_frame('A4', units='cm') 
    frame_m = generator.generate_frame('A4', units='m')
    
    print("A4 frame in different units:")
    print(f"  Millimeters: {frame_mm['metadata']['scaled_size']}")
    print(f"  Centimeters: {frame_cm['metadata']['scaled_size']}")
    print(f"  Meters: {frame_m['metadata']['scaled_size']}")
    
    return frame_mm, frame_cm, frame_m


def rhino_grasshopper_export_example():
    """
    Example: Export frame data for Rhino/Grasshopper.
    """
    print("\n=== Rhino/Grasshopper Export Example ===")
    
    generator = FrameGenerator()
    
    # Generate a frame
    frame = generator.generate_frame(
        'A1',
        reference_point=[200, 300],
        scale=1.2,
        rotation=30.0
    )
    
    # Get Rhino-compatible geometry
    rhino_geometry = generator.get_rhino_geometry(frame)
    print(f"Generated {len(rhino_geometry)} Rhino geometry objects:")
    for i, geom in enumerate(rhino_geometry[:3]):  # Show first 3
        print(f"  {i+1}. {geom['type']}: {list(geom.keys())}")
    
    # Get Grasshopper-compatible data structure
    gh_data = generator.get_grasshopper_data(frame)
    print(f"\nGrasshopper data structure:")
    print(f"  Lines: {len(gh_data['Lines'])}")
    print(f"  Polylines: {len(gh_data['Polylines'])}")
    print(f"  Circles: {len(gh_data['Circles'])}")
    print(f"  Texts: {len(gh_data['Texts'])}")
    
    return rhino_geometry, gh_data


def template_management_example():
    """
    Example: Template management and validation.
    """
    print("\n=== Template Management Example ===")
    
    manager = FrameTemplateManager()
    
    # List available paper sizes
    sizes = manager.list_available_templates()
    print(f"Available template files: {sizes}")
    
    # Get information about different paper sizes
    for paper_size in ['A0', 'A1', 'A2', 'A3', 'A4']:
        info = manager.get_paper_size_info(paper_size)
        print(f"{paper_size}: {info['width_mm']}x{info['height_mm']}mm, "
              f"aspect ratio: {info['aspect_ratio']:.3f}")
    
    # Validate templates
    for paper_size in ['A3', 'A4']:
        validation = manager.validate_template(paper_size)
        print(f"{paper_size} validation: valid={validation['is_valid']}, "
              f"entities={validation.get('entity_count', 0)}")
    
    return manager


def frame_comparison_example():
    """
    Example: Compare different frame sizes and orientations.
    """
    print("\n=== Frame Comparison Example ===")
    
    generator = FrameGenerator()
    
    # Generate frames of different sizes at same reference point
    ref_point = [0, 0]
    frames = {}
    
    for size in ['A4', 'A3', 'A2', 'A1', 'A0']:
        frame = generator.generate_frame(size, reference_point=ref_point)
        frames[size] = frame
        
        width, height = frame['metadata']['scaled_size']
        area = width * height
        
        print(f"{size}: {width:.1f}x{height:.1f}mm, area: {area:.0f}mm²")
    
    # Compare portrait vs landscape A4
    portrait = generator.generate_frame('A4', rotation=0)
    landscape = generator.generate_frame('A4', rotation=90)
    
    print(f"\nA4 Portrait bounds: {portrait['bounds']}")
    print(f"A4 Landscape bounds: {landscape['bounds']}")
    
    return frames


def grasshopper_plugin_simulation():
    """
    Example: Simulate how this would work in a Grasshopper plugin.
    """
    print("\n=== Grasshopper Plugin Simulation ===")
    
    # This simulates the workflow of a Grasshopper battery/component
    
    # Input parameters (would come from Grasshopper inputs)
    paper_size = 'A3'
    reference_point = [500, 600]  # User-defined reference point
    scale_factor = 0.8
    rotation_angle = 15.0
    
    print(f"Input parameters:")
    print(f"  Paper size: {paper_size}")
    print(f"  Reference point: {reference_point}")
    print(f"  Scale: {scale_factor}")
    print(f"  Rotation: {rotation_angle}°")
    
    # Generate frame (main computation)
    generator = FrameGenerator()
    frame = generator.generate_frame(
        paper_size=paper_size,
        reference_point=reference_point,
        scale=scale_factor,
        rotation=rotation_angle
    )
    
    # Output for Grasshopper (would be connected to output parameters)
    gh_data = generator.get_grasshopper_data(frame)
    
    print(f"\nOutput for Grasshopper:")
    print(f"  Generated {len(frame['entities'])} entities")
    print(f"  Frame bounds: {frame['bounds']}")
    print(f"  Lines output: {len(gh_data['Lines'])} lines")
    print(f"  Text output: {len(gh_data['Texts'])} text objects")
    
    # This data would be passed to Grasshopper outputs:
    # - Lines -> Line geometry output
    # - Polylines -> Polyline geometry output  
    # - Circles -> Circle geometry output
    # - Texts -> Text geometry output
    # - Bounds -> Rectangle for bounding box
    
    return gh_data


def main():
    """
    Run all examples.
    """
    print("CAD Frame Generation Examples")
    print("============================")
    
    try:
        # Run examples
        basic_frame_generation_example()
        scaled_and_rotated_frame_example()
        unit_conversion_example()
        rhino_grasshopper_export_example()
        template_management_example()
        frame_comparison_example()
        grasshopper_plugin_simulation()
        
        print("\n=== All Examples Completed Successfully ===")
        
    except Exception as e:
        print(f"\nError running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()