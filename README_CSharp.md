# SimPEG C# Port

This directory contains a C# port of the SimPEG (Simulation and Parameter Estimation in Geophysics) library for Visual Studio 2022.

## Overview

SimPEG has been converted from Python to C# to enable geophysical simulations and parameter estimation in the .NET ecosystem. This port maintains the core functionality and design patterns of the original Python library while leveraging C#'s strong typing and performance benefits.

## Project Structure

```
SimPEG.sln                  # Visual Studio 2022 Solution File
├── SimPEG.CSharp/          # Main SimPEG library (C#)
│   ├── Data/               # Data handling classes
│   ├── Survey/             # Survey geometry classes  
│   ├── Models/             # Model parameter classes
│   ├── Simulation/         # Forward simulation classes
│   ├── Utils/              # Utility functions and extensions
│   └── SimPEGInfo.cs       # Version and assembly information
├── SimPEG.Tests/           # Unit tests (NUnit framework)
├── SimPEG.Examples/        # Example applications
└── README_CSharp.md        # This file
```

## Key Features Implemented

### Core Classes
- **Data**: Handles observed data and uncertainties
- **SyntheticData**: Generates synthetic data with noise
- **Model**: Represents physical model parameters with mappings
- **BaseSurvey**: Survey geometry with sources and receivers
- **BaseSimulation**: Abstract simulation base class
- **LinearSimulation**: Linear forward operator simulations

### Model Mappings
- **IdentityMapping**: No transformation (1:1)
- **ExpMapping**: Exponential transformation (log → physical)
- **LogMapping**: Logarithmic transformation (physical → log)

### Mathematical Support
- Uses **MathNet.Numerics** for linear algebra operations
- Vector and Matrix operations compatible with scientific computing
- Gaussian noise generation for synthetic data

## Requirements

- **.NET 8.0** or later
- **Visual Studio 2022** (recommended IDE)
- **MathNet.Numerics** package (automatically installed via NuGet)

## Building and Running

### Building the Solution
```bash
dotnet restore
dotnet build
```

### Running Tests
```bash
dotnet test
```

### Running Examples
```bash
dotnet run --project SimPEG.Examples
```

## Usage Example

```csharp
using MathNet.Numerics.LinearAlgebra;
using SimPEG.Data;
using SimPEG.Survey;
using SimPEG.Models;
using SimPEG.Simulation;

// Create survey geometry
var receiverLocations = Matrix<double>.Build.DenseOfArray(new double[,] {
    { 0.0, 0.0, 0.0 },
    { 1.0, 0.0, 0.0 },
    { 2.0, 0.0, 0.0 }
});

var rx = new ExampleRx(receiverLocations);
var src = new ExampleSrc(new List<BaseRx> { rx });
var survey = new ExampleSurvey(new List<BaseSrc> { src });

// Create linear forward operator
var G = Matrix<double>.Build.DenseOfArray(new double[,] {
    { 1.0, 0.5, 0.2 },
    { 0.8, 1.0, 0.3 },
    { 0.3, 0.7, 1.0 }
});

var simulation = new LinearSimulation(survey, G);

// Create model
var modelParams = Vector<double>.Build.DenseOfArray(new double[] { 2.0, 1.5, 3.0 });
var model = new Model(modelParams);
simulation.Model = model;

// Compute synthetic data
var cleanData = simulation.Dpred();
var syntheticData = simulation.MakeSyntheticData(model, relativeError: 0.05);

Console.WriteLine($"Clean data: [{string.Join(", ", cleanData.ToArray())}]");
Console.WriteLine($"Noisy data: [{string.Join(", ", syntheticData.Dobs.ToArray())}]");
```

## Key Differences from Python Version

### Type Safety
- Strong typing for all model parameters, data, and matrices
- Compile-time error checking
- Nullable reference types for better null safety

### Performance
- No interpreter overhead
- Compiled to native code
- Efficient memory management

### Ecosystem Integration
- Native Windows integration with Visual Studio
- NuGet package management
- MSBuild compilation system

### Mathematical Libraries
- **MathNet.Numerics** replaces NumPy/SciPy
- Strongly-typed linear algebra operations
- Integration with .NET numerical computing ecosystem

## Testing

The solution includes comprehensive unit tests covering:
- Data creation and noise handling
- Model parameter transformations
- Survey geometry validation
- Linear simulation operations
- Mapping transformations (Identity, Exp, Log)

All tests use the NUnit framework and can be run in Visual Studio or via command line.

## Future Enhancements

This initial port focuses on core linear simulation functionality. Future enhancements could include:

1. **Advanced Simulations**: Electromagnetics, potential fields, seismic
2. **Inversion Algorithms**: Gradient-based optimization routines
3. **Mesh Support**: Integration with discretization libraries
4. **Visualization**: Plotting and visualization components
5. **Parallel Computing**: Multi-threading and GPU acceleration

## Contributing

This C# port maintains compatibility with the original SimPEG API design while adapting to C# conventions and .NET ecosystem best practices.

## License

MIT License - Same as the original SimPEG project.

## Acknowledgments

- Original SimPEG Team for the Python implementation
- MathNet.Numerics contributors for numerical computing support
- .NET community for the excellent development ecosystem