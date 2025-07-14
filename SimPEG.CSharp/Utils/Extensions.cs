using System;
using MathNet.Numerics.LinearAlgebra;

namespace SimPEG.Utils
{
    /// <summary>
    /// Utility extension methods for SimPEG
    /// </summary>
    public static class Extensions
    {
        /// <summary>
        /// Generate a normally distributed random number using Box-Muller transform
        /// </summary>
        /// <param name="random">Random number generator</param>
        /// <param name="mean">Mean of the distribution</param>
        /// <param name="standardDeviation">Standard deviation of the distribution</param>
        /// <returns>Normally distributed random number</returns>
        public static double NextGaussian(this Random random, double mean = 0.0, double standardDeviation = 1.0)
        {
            // Use Box-Muller transform
            static double GenerateStandardNormal(Random rng)
            {
                double u1 = 1.0 - rng.NextDouble(); // uniform(0,1] random doubles
                double u2 = 1.0 - rng.NextDouble();
                return Math.Sqrt(-2.0 * Math.Log(u1)) * Math.Cos(2.0 * Math.PI * u2);
            }

            return mean + standardDeviation * GenerateStandardNormal(random);
        }

        /// <summary>
        /// Convert array to vector format (equivalent to Python's mkvc)
        /// </summary>
        /// <param name="array">Input array</param>
        /// <returns>Flattened vector</returns>
        public static Vector<double> ToVector(this double[] array)
        {
            return Vector<double>.Build.DenseOfArray(array);
        }

        /// <summary>
        /// Convert 2D array to vector format
        /// </summary>
        /// <param name="array">Input 2D array</param>
        /// <returns>Flattened vector</returns>
        public static Vector<double> ToVector(this double[,] array)
        {
            int rows = array.GetLength(0);
            int cols = array.GetLength(1);
            var vector = Vector<double>.Build.Dense(rows * cols);
            
            int index = 0;
            for (int i = 0; i < rows; i++)
            {
                for (int j = 0; j < cols; j++)
                {
                    vector[index++] = array[i, j];
                }
            }
            
            return vector;
        }

        /// <summary>
        /// Validate that a vector has the expected shape
        /// </summary>
        /// <param name="vector">Vector to validate</param>
        /// <param name="expectedLength">Expected length</param>
        /// <param name="parameterName">Parameter name for error messages</param>
        public static void ValidateShape(this Vector<double> vector, int expectedLength, string parameterName = "vector")
        {
            if (vector.Count != expectedLength)
            {
                throw new ArgumentException($"{parameterName} must have length {expectedLength}, got {vector.Count}");
            }
        }

        /// <summary>
        /// Validate that a value is within acceptable range
        /// </summary>
        /// <param name="value">Value to validate</param>
        /// <param name="min">Minimum acceptable value</param>
        /// <param name="max">Maximum acceptable value</param>
        /// <param name="parameterName">Parameter name for error messages</param>
        public static void ValidateRange(this double value, double min, double max, string parameterName = "value")
        {
            if (value < min || value > max)
            {
                throw new ArgumentOutOfRangeException(parameterName, $"{parameterName} must be between {min} and {max}, got {value}");
            }
        }
    }
}