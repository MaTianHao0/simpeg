"""
Example demonstrating DWG/DXF template file usage.

This script shows how to use actual DWG/DXF template files with the frame generation system.
"""

import os
import sys

# Add SimPEG to path if running as script
if __name__ == '__main__':
    simpeg_path = os.path.join(os.path.dirname(__file__), '..', '..')
    if simpeg_path not in sys.path:
        sys.path.insert(0, simpeg_path)

from SimPEG.utils.cad import FrameGenerator, FrameTemplateManager


def test_template_loading():
    """Test loading templates from DXF files."""
    print("=== Testing Template File Loading ===")
    
    # Get template directory
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    
    # Create template manager with template directory
    manager = FrameTemplateManager(template_dir)
    
    # Check which templates were found
    available_templates = manager.list_available_templates()
    print(f"Found templates: {available_templates}")
    
    # Test loading each template
    for paper_size in ['A0', 'A1', 'A2', 'A3', 'A4']:
        if paper_size in available_templates:
            print(f"\nLoading {paper_size} template from file...")
            template = manager.get_template(paper_size)
            
            print(f"  Template file: {template['file_path']}")
            print(f"  Entity count: {len(template['entities'])}")
            print(f"  Template size: {template['size']}")
            print(f"  Template bounds: {template['bounds']}")
            
            # Show first few entities
            print(f"  First few entities:")
            for i, entity in enumerate(template['entities'][:3]):
                print(f"    {i+1}. {entity['type']}")
        else:
            print(f"\n{paper_size}: Using default template (no file found)")
    
    return manager


def test_frame_generation_with_templates():
    """Test frame generation using loaded templates."""
    print("\n=== Frame Generation with Templates ===")
    
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    generator = FrameGenerator(template_dir)
    
    # Generate frames using templates
    test_cases = [
        ('A4', [100, 150], 1.0, 0),
        ('A3', [200, 300], 0.8, 15),
        ('A2', [0, 0], 1.2, 30),
        ('A1', [500, 400], 0.5, 45),
        ('A0', [1000, 800], 0.7, 90)
    ]
    
    for paper_size, ref_point, scale, rotation in test_cases:
        print(f"\nGenerating {paper_size} frame:")
        print(f"  Reference point: {ref_point}")
        print(f"  Scale: {scale}")
        print(f"  Rotation: {rotation}°")
        
        frame = generator.generate_frame(
            paper_size=paper_size,
            reference_point=ref_point,
            scale=scale,
            rotation=rotation
        )
        
        print(f"  Result: {len(frame['entities'])} entities")
        print(f"  Final bounds: {frame['bounds']}")
        print(f"  Using template file: {not frame['metadata'].get('is_default_template', True)}")
        
        # Get Grasshopper-compatible output
        gh_data = generator.get_grasshopper_data(frame)
        print(f"  Grasshopper output: {len(gh_data['Lines'])} lines, {len(gh_data['Texts'])} texts")


def test_template_validation():
    """Test template validation functionality."""
    print("\n=== Template Validation ===")
    
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    manager = FrameTemplateManager(template_dir)
    
    for paper_size in ['A0', 'A1', 'A2', 'A3', 'A4']:
        validation = manager.validate_template(paper_size)
        
        print(f"\n{paper_size} Validation:")
        print(f"  Valid: {validation['is_valid']}")
        print(f"  Template size: {validation['template_size']}")
        print(f"  Standard size: {validation['standard_size']}")
        print(f"  Size ratio: [{validation['size_ratio'][0]:.3f}, {validation['size_ratio'][1]:.3f}]")
        print(f"  Entity count: {validation['entity_count']}")
        print(f"  Has custom file: {validation['has_file']}")


def test_rhino_output_with_templates():
    """Test Rhino geometry output with template files."""
    print("\n=== Rhino Output with Templates ===")
    
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    generator = FrameGenerator(template_dir)
    
    # Generate A3 frame with template
    frame = generator.generate_frame('A3', reference_point=[300, 200], scale=1.0)
    
    # Get Rhino geometry
    rhino_geometry = generator.get_rhino_geometry(frame)
    
    print(f"Generated {len(rhino_geometry)} Rhino geometry objects:")
    
    # Group by type
    geometry_types = {}
    for geom in rhino_geometry:
        geom_type = geom['type']
        if geom_type not in geometry_types:
            geometry_types[geom_type] = []
        geometry_types[geom_type].append(geom)
    
    # Display summary
    for geom_type, items in geometry_types.items():
        print(f"  {geom_type}: {len(items)} objects")
        
        # Show a sample
        if items:
            sample = items[0]
            print(f"    Sample: {list(sample.keys())}")


def test_grasshopper_battery_simulation():
    """Simulate complete Grasshopper battery workflow."""
    print("\n=== Grasshopper Battery Simulation ===")
    
    # This simulates the complete workflow as it would appear in Grasshopper
    
    print("1. Setting up template directory...")
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    generator = FrameGenerator(template_dir)
    
    print("2. Battery inputs (from Grasshopper user interface):")
    # These would be input parameters in Grasshopper
    paper_size = "A2"
    reference_point = [400, 500]  # Point from Grasshopper
    scale_factor = 0.9
    rotation_angle = 20.0
    units = "mm"
    
    print(f"   - Paper Size: {paper_size}")
    print(f"   - Reference Point: {reference_point}")
    print(f"   - Scale: {scale_factor}")
    print(f"   - Rotation: {rotation_angle}°")
    print(f"   - Units: {units}")
    
    print("3. Generating frame...")
    frame = generator.generate_frame(
        paper_size=paper_size,
        reference_point=reference_point,
        scale=scale_factor,
        rotation=rotation_angle,
        units=units
    )
    
    print("4. Processing outputs for Grasshopper...")
    gh_data = generator.get_grasshopper_data(frame)
    
    print("5. Battery outputs (to Grasshopper components):")
    print(f"   - Lines: {len(gh_data['Lines'])} objects -> Line output")
    print(f"   - Polylines: {len(gh_data['Polylines'])} objects -> Polyline output")
    print(f"   - Circles: {len(gh_data['Circles'])} objects -> Circle output")
    print(f"   - Texts: {len(gh_data['Texts'])} objects -> Text output")
    print(f"   - Bounds: {gh_data['Bounds']} -> Rectangle output")
    
    print("6. Metadata (for information panel):")
    metadata = gh_data['Metadata']
    print(f"   - Template file used: {metadata.get('template_file', 'Default')}")
    print(f"   - Original size: {metadata['original_size']}")
    print(f"   - Scaled size: {metadata['scaled_size']}")
    print(f"   - Total entities: {metadata['entity_count']}")
    
    print("\n✓ Battery processing complete - ready for Rhino bake operation")
    
    return gh_data


def main():
    """Run all tests with template files."""
    print("DWG/DXF Template Usage Examples")
    print("===============================")
    
    try:
        # Check if templates exist
        template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        if not os.path.exists(template_dir):
            print(f"Template directory not found: {template_dir}")
            print("Please run create_templates.py first to create sample templates.")
            return
        
        # Run tests
        test_template_loading()
        test_frame_generation_with_templates()
        test_template_validation()
        test_rhino_output_with_templates()
        test_grasshopper_battery_simulation()
        
        print("\n=== All Template Tests Completed Successfully ===")
        
    except Exception as e:
        print(f"\nError running template tests: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()