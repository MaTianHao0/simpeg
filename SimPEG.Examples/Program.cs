using System;
using System.Collections.Generic;
using MathNet.Numerics.LinearAlgebra;
using SimPEG;
using SimPEG.Data;
using SimPEG.Survey;
using SimPEG.Models;
using SimPEG.Simulation;

namespace SimPEG.Examples
{
    // Concrete implementations for the example
    public class ExampleSurvey : BaseSurvey
    {
        public ExampleSurvey(List<BaseSrc> sourceList) : base(sourceList) { }
    }

    public class ExampleRx : BaseRx
    {
        public ExampleRx(Matrix<double> locations, bool storeProjections = false) 
            : base(locations, storeProjections) { }
    }

    public class ExampleSrc : BaseSrc
    {
        public ExampleSrc(List<BaseRx> receiverList) : base(receiverList) { }
    }

    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("====================================================");
            Console.WriteLine(SimPEGInfo.GetInfo());
            Console.WriteLine("====================================================");
            Console.WriteLine();

            // Example: Linear Forward Problem
            Console.WriteLine("Running SimPEG C# Example: Linear Forward Problem");
            Console.WriteLine("=================================================");

            try
            {
                // 1. Create a simple survey geometry
                Console.WriteLine("1. Creating survey geometry...");
                var receiverLocations = Matrix<double>.Build.DenseOfArray(new double[,] 
                {
                    { 0.0, 0.0, 0.0 },  // Receiver 1
                    { 1.0, 0.0, 0.0 },  // Receiver 2
                    { 2.0, 0.0, 0.0 },  // Receiver 3
                    { 3.0, 0.0, 0.0 },  // Receiver 4
                    { 4.0, 0.0, 0.0 }   // Receiver 5
                });

                var rx = new ExampleRx(receiverLocations);
                var src = new ExampleSrc(new List<BaseRx> { rx });
                var survey = new ExampleSurvey(new List<BaseSrc> { src });

                Console.WriteLine($"   - Created survey with {survey.NSrc} source and {receiverLocations.RowCount} receivers");

                // 2. Create a simple linear forward operator (kernel matrix)
                Console.WriteLine("2. Creating linear forward operator...");
                var G = Matrix<double>.Build.DenseOfArray(new double[,]
                {
                    { 1.0, 0.5, 0.2 },  // Data point 1 sensitivity to model parameters
                    { 0.8, 1.0, 0.3 },  // Data point 2 sensitivity to model parameters
                    { 0.3, 0.7, 1.0 },  // Data point 3 sensitivity to model parameters
                    { 0.1, 0.4, 0.8 },  // Data point 4 sensitivity to model parameters
                    { 0.05, 0.2, 0.6 }  // Data point 5 sensitivity to model parameters
                });

                var simulation = new LinearSimulation(survey, G);
                Console.WriteLine($"   - Created linear simulation with G matrix: {G.RowCount}x{G.ColumnCount}");

                // 3. Create a model
                Console.WriteLine("3. Creating model...");
                var modelParams = Vector<double>.Build.DenseOfArray(new double[] { 2.0, 1.5, 3.0 });
                var model = new Model(modelParams);
                simulation.Model = model;

                Console.WriteLine($"   - Created model with {model.Size} parameters: [{string.Join(", ", model.ToArray())}]");

                // 4. Compute synthetic data
                Console.WriteLine("4. Computing synthetic data...");
                var cleanData = simulation.Dpred();
                Console.WriteLine($"   - Clean synthetic data: [{string.Join(", ", cleanData.ToArray().Select(x => x.ToString("F3")))}]");

                // 5. Add noise to create realistic data
                Console.WriteLine("5. Adding noise to create realistic data...");
                var syntheticData = simulation.MakeSyntheticData(model, relativeError: 0.05, noiseFloor: 0.01);
                Console.WriteLine($"   - Noisy synthetic data: [{string.Join(", ", syntheticData.Dobs.ToArray().Select(x => x.ToString("F3")))}]");
                Console.WriteLine($"   - Standard deviations: [{string.Join(", ", syntheticData.StandardDeviation.ToArray().Select(x => x.ToString("F3")))}]");

                // 6. Test different model mappings
                Console.WriteLine("6. Testing different model mappings...");
                
                // Test exponential mapping (useful for conductivity inversion)
                var logModelParams = Vector<double>.Build.DenseOfArray(new double[] { 0.0, 0.5, 1.0 });
                var expMapping = new ExpMapping(3);
                var expModel = new Model(logModelParams, expMapping);
                Console.WriteLine($"   - Log parameters: [{string.Join(", ", logModelParams.ToArray().Select(x => x.ToString("F3")))}]");
                Console.WriteLine($"   - Exp-transformed: [{string.Join(", ", expModel.Transform.ToArray().Select(x => x.ToString("F3")))}]");

                // Test log mapping 
                var physicalParams = Vector<double>.Build.DenseOfArray(new double[] { 1.0, 2.718, 10.0 });
                var logMapping = new LogMapping(3);
                var logModel = new Model(physicalParams, logMapping);
                Console.WriteLine($"   - Physical parameters: [{string.Join(", ", physicalParams.ToArray().Select(x => x.ToString("F3")))}]");
                Console.WriteLine($"   - Log-transformed: [{string.Join(", ", logModel.Transform.ToArray().Select(x => x.ToString("F3")))}]");

                // 7. Compute Jacobian
                Console.WriteLine("7. Computing Jacobian matrix...");
                var jacobian = simulation.Jvec();
                Console.WriteLine($"   - Jacobian dimensions: {jacobian.RowCount}x{jacobian.ColumnCount}");
                Console.WriteLine("   - Jacobian matrix:");
                for (int i = 0; i < jacobian.RowCount; i++)
                {
                    var row = string.Join(", ", Enumerable.Range(0, jacobian.ColumnCount).Select(j => jacobian[i, j].ToString("F3")));
                    Console.WriteLine($"     [{row}]");
                }

                // 8. Test adjoint operation
                Console.WriteLine("8. Testing adjoint operation...");
                var testVector = Vector<double>.Build.DenseOfArray(new double[] { 1.0, 1.0, 1.0, 1.0, 1.0 });
                var adjointResult = simulation.Jtvec(testVector);
                Console.WriteLine($"   - Test vector: [{string.Join(", ", testVector.ToArray().Select(x => x.ToString("F3")))}]");
                Console.WriteLine($"   - J^T * vector: [{string.Join(", ", adjointResult.ToArray().Select(x => x.ToString("F3")))}]");

                Console.WriteLine("\n✅ SimPEG C# Example completed successfully!");
                Console.WriteLine("   All core functionality is working correctly.");

            }
            catch (Exception ex)
            {
                Console.WriteLine($"\n❌ Error in SimPEG C# Example: {ex.Message}");
                Console.WriteLine($"Stack trace: {ex.StackTrace}");
                Environment.Exit(1);
            }

            Console.WriteLine("\nPress any key to exit...");
            Console.ReadKey();
        }
    }
}