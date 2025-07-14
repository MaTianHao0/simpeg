using System;
using MathNet.Numerics.LinearAlgebra;

namespace SimPEG.Models
{
    /// <summary>
    /// Model class for SimPEG, representing physical parameters
    /// </summary>
    public class Model
    {
        private Vector<double> _vector;
        private IMapping _mapping;

        /// <summary>
        /// Model parameter vector
        /// </summary>
        public Vector<double> Vector
        {
            get => _vector;
            set => _vector = value ?? throw new ArgumentNullException(nameof(value));
        }

        /// <summary>
        /// Mapping from model parameters to physical properties
        /// </summary>
        public IMapping Mapping
        {
            get => _mapping;
            set => _mapping = value ?? throw new ArgumentNullException(nameof(value));
        }

        /// <summary>
        /// Number of model parameters
        /// </summary>
        public int Size => Vector?.Count ?? 0;

        /// <summary>
        /// Number of parameters in the mapping
        /// </summary>
        public int NParam => Mapping?.NParam ?? Size;

        /// <summary>
        /// Initializes a new instance of the Model class.
        /// </summary>
        /// <param name="inputVector">Model parameter vector</param>
        /// <param name="mapping">Mapping object (optional, defaults to identity)</param>
        public Model(Vector<double> inputVector, IMapping mapping = null)
        {
            Vector = inputVector;
            Mapping = mapping ?? new IdentityMapping(inputVector.Count);

            if (Size != Mapping.NParam)
            {
                throw new ArgumentException($"Incorrect size for array. Expected {Mapping.NParam}, got {Size}");
            }
        }

        /// <summary>
        /// Transform the model using the mapping
        /// </summary>
        public Vector<double> Transform => Mapping.Transform(Vector);

        /// <summary>
        /// Compute the derivative of the transformation
        /// </summary>
        public Matrix<double> TransformDeriv => Mapping.Deriv(Vector);

        /// <summary>
        /// Access model parameters by index
        /// </summary>
        /// <param name="index">Parameter index</param>
        /// <returns>Parameter value</returns>
        public double this[int index]
        {
            get => Vector[index];
            set => Vector[index] = value;
        }

        /// <summary>
        /// Create a copy of the model
        /// </summary>
        /// <returns>Copy of the model</returns>
        public Model Clone()
        {
            return new Model(Vector.Clone(), Mapping);
        }

        /// <summary>
        /// Convert model to array
        /// </summary>
        /// <returns>Array representation</returns>
        public double[] ToArray()
        {
            return Vector.ToArray();
        }
    }

    /// <summary>
    /// Interface for model parameter mappings
    /// </summary>
    public interface IMapping
    {
        /// <summary>
        /// Number of parameters in the mapping
        /// </summary>
        int NParam { get; }

        /// <summary>
        /// Transform model parameters
        /// </summary>
        /// <param name="model">Model parameters</param>
        /// <returns>Transformed parameters</returns>
        Vector<double> Transform(Vector<double> model);

        /// <summary>
        /// Compute derivative of the transformation
        /// </summary>
        /// <param name="model">Model parameters</param>
        /// <returns>Derivative matrix</returns>
        Matrix<double> Deriv(Vector<double> model);
    }

    /// <summary>
    /// Identity mapping (no transformation)
    /// </summary>
    public class IdentityMapping : IMapping
    {
        /// <summary>
        /// Number of parameters
        /// </summary>
        public int NParam { get; }

        /// <summary>
        /// Initializes a new instance of the IdentityMapping class.
        /// </summary>
        /// <param name="nParam">Number of parameters</param>
        public IdentityMapping(int nParam)
        {
            NParam = nParam;
        }

        /// <summary>
        /// Transform model parameters (identity - no change)
        /// </summary>
        /// <param name="model">Model parameters</param>
        /// <returns>Same parameters</returns>
        public Vector<double> Transform(Vector<double> model)
        {
            return model.Clone();
        }

        /// <summary>
        /// Compute derivative (identity matrix)
        /// </summary>
        /// <param name="model">Model parameters</param>
        /// <returns>Identity matrix</returns>
        public Matrix<double> Deriv(Vector<double> model)
        {
            return Matrix<double>.Build.DenseIdentity(NParam);
        }
    }

    /// <summary>
    /// Exponential mapping (transforms log parameters to physical parameters)
    /// </summary>
    public class ExpMapping : IMapping
    {
        /// <summary>
        /// Number of parameters
        /// </summary>
        public int NParam { get; }

        /// <summary>
        /// Initializes a new instance of the ExpMapping class.
        /// </summary>
        /// <param name="nParam">Number of parameters</param>
        public ExpMapping(int nParam)
        {
            NParam = nParam;
        }

        /// <summary>
        /// Transform log parameters to physical parameters using exponential
        /// </summary>
        /// <param name="model">Log model parameters</param>
        /// <returns>Physical parameters</returns>
        public Vector<double> Transform(Vector<double> model)
        {
            var result = Vector<double>.Build.Dense(model.Count);
            for (int i = 0; i < model.Count; i++)
            {
                result[i] = Math.Exp(model[i]);
            }
            return result;
        }

        /// <summary>
        /// Compute derivative of exponential transformation
        /// </summary>
        /// <param name="model">Log model parameters</param>
        /// <returns>Diagonal matrix with exp(model) on diagonal</returns>
        public Matrix<double> Deriv(Vector<double> model)
        {
            var diagonal = Vector<double>.Build.Dense(model.Count);
            for (int i = 0; i < model.Count; i++)
            {
                diagonal[i] = Math.Exp(model[i]);
            }
            return Matrix<double>.Build.DenseOfDiagonalVector(diagonal);
        }
    }

    /// <summary>
    /// Log mapping (transforms physical parameters to log parameters)
    /// </summary>
    public class LogMapping : IMapping
    {
        /// <summary>
        /// Number of parameters
        /// </summary>
        public int NParam { get; }

        /// <summary>
        /// Initializes a new instance of the LogMapping class.
        /// </summary>
        /// <param name="nParam">Number of parameters</param>
        public LogMapping(int nParam)
        {
            NParam = nParam;
        }

        /// <summary>
        /// Transform physical parameters to log parameters
        /// </summary>
        /// <param name="model">Physical model parameters</param>
        /// <returns>Log parameters</returns>
        public Vector<double> Transform(Vector<double> model)
        {
            var result = Vector<double>.Build.Dense(model.Count);
            for (int i = 0; i < model.Count; i++)
            {
                if (model[i] <= 0)
                    throw new ArgumentException($"LogMapping requires positive values, got {model[i]} at index {i}");
                result[i] = Math.Log(model[i]);
            }
            return result;
        }

        /// <summary>
        /// Compute derivative of log transformation
        /// </summary>
        /// <param name="model">Physical model parameters</param>
        /// <returns>Diagonal matrix with 1/model on diagonal</returns>
        public Matrix<double> Deriv(Vector<double> model)
        {
            var diagonal = Vector<double>.Build.Dense(model.Count);
            for (int i = 0; i < model.Count; i++)
            {
                if (model[i] <= 0)
                    throw new ArgumentException($"LogMapping requires positive values, got {model[i]} at index {i}");
                diagonal[i] = 1.0 / model[i];
            }
            return Matrix<double>.Build.DenseOfDiagonalVector(diagonal);
        }
    }
}