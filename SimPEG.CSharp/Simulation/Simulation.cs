using System;
using MathNet.Numerics.LinearAlgebra;
using SimPEG.Survey;
using SimPEG.Data;
using SimPEG.Models;

namespace SimPEG.Simulation
{
    /// <summary>
    /// BaseSimulation is the base class for all geophysical forward simulations in SimPEG.
    /// </summary>
    public abstract class BaseSimulation
    {
        private BaseSurvey _survey;
        private Model _model;
        
        /// <summary>
        /// The survey for the simulation
        /// </summary>
        public BaseSurvey Survey
        {
            get => _survey;
            set => _survey = value ?? throw new ArgumentNullException(nameof(value));
        }

        /// <summary>
        /// The model for the simulation
        /// </summary>
        public Model Model
        {
            get => _model;
            set => _model = value ?? throw new ArgumentNullException(nameof(value));
        }

        /// <summary>
        /// Initializes a new instance of the BaseSimulation class.
        /// </summary>
        /// <param name="survey">The survey object</param>
        protected BaseSimulation(BaseSurvey survey)
        {
            Survey = survey;
        }

        /// <summary>
        /// Compute synthetic data for the given model
        /// </summary>
        /// <param name="model">Model parameters</param>
        /// <returns>Predicted data</returns>
        public abstract Vector<double> Dpred(Model model = null);

        /// <summary>
        /// Compute the Jacobian matrix
        /// </summary>
        /// <param name="model">Model parameters</param>
        /// <returns>Jacobian matrix</returns>
        public abstract Matrix<double> Jvec(Model model = null);

        /// <summary>
        /// Compute Jacobian transpose times vector
        /// </summary>
        /// <param name="vector">Vector to multiply</param>
        /// <param name="model">Model parameters</param>
        /// <returns>Jt * vector</returns>
        public abstract Vector<double> Jtvec(Vector<double> vector, Model model = null);

        /// <summary>
        /// Create synthetic data with noise
        /// </summary>
        /// <param name="model">Model parameters</param>
        /// <param name="relativeError">Relative error for noise</param>
        /// <param name="noiseFloor">Noise floor</param>
        /// <param name="random">Random number generator</param>
        /// <returns>Synthetic data object</returns>
        public SyntheticData MakeSyntheticData(Model model, double? relativeError = null, 
                                              double? noiseFloor = null, Random random = null)
        {
            var dclean = Dpred(model);
            return new SyntheticData(Survey, dclean, relativeError, noiseFloor, random: random);
        }

        /// <summary>
        /// Number of data points
        /// </summary>
        public virtual int Ndata => Survey?.Ndata ?? 0;

        /// <summary>
        /// Number of model parameters
        /// </summary>
        public virtual int NParam => Model?.Size ?? 0;
    }

    /// <summary>
    /// Linear simulation class for problems with linear forward operators
    /// </summary>
    public class LinearSimulation : BaseSimulation
    {
        private Matrix<double> _G;

        /// <summary>
        /// Linear forward operator matrix
        /// </summary>
        public Matrix<double> G
        {
            get => _G;
            set => _G = value ?? throw new ArgumentNullException(nameof(value));
        }

        /// <summary>
        /// Initializes a new instance of the LinearSimulation class.
        /// </summary>
        /// <param name="survey">The survey object</param>
        /// <param name="G">Linear forward operator matrix</param>
        public LinearSimulation(BaseSurvey survey, Matrix<double> G) : base(survey)
        {
            this.G = G;
        }

        /// <summary>
        /// Compute synthetic data for the given model
        /// </summary>
        /// <param name="model">Model parameters</param>
        /// <returns>Predicted data</returns>
        public override Vector<double> Dpred(Model model = null)
        {
            model ??= Model;
            if (model == null)
                throw new InvalidOperationException("Model must be set before calling Dpred");

            return G * model.Vector;
        }

        /// <summary>
        /// Compute the Jacobian matrix (same as G for linear problems)
        /// </summary>
        /// <param name="model">Model parameters</param>
        /// <returns>Jacobian matrix</returns>
        public override Matrix<double> Jvec(Model model = null)
        {
            return G;
        }

        /// <summary>
        /// Compute Jacobian transpose times vector
        /// </summary>
        /// <param name="vector">Vector to multiply</param>
        /// <param name="model">Model parameters</param>
        /// <returns>Jt * vector</returns>
        public override Vector<double> Jtvec(Vector<double> vector, Model model = null)
        {
            return G.Transpose() * vector;
        }
    }

    /// <summary>
    /// Base time simulation class for time-domain problems
    /// </summary>
    public abstract class BaseTimeSimulation : BaseSimulation
    {
        private Vector<double> _timeSteps;

        /// <summary>
        /// Time stepping for time-domain simulations
        /// </summary>
        public Vector<double> TimeSteps
        {
            get => _timeSteps;
            set => _timeSteps = value ?? throw new ArgumentNullException(nameof(value));
        }

        /// <summary>
        /// Number of time steps
        /// </summary>
        public int NTime => TimeSteps?.Count ?? 0;

        /// <summary>
        /// Initializes a new instance of the BaseTimeSimulation class.
        /// </summary>
        /// <param name="survey">The survey object</param>
        /// <param name="timeSteps">Time stepping</param>
        protected BaseTimeSimulation(BaseSurvey survey, Vector<double> timeSteps) : base(survey)
        {
            TimeSteps = timeSteps;
        }

        /// <summary>
        /// Compute time-domain fields
        /// </summary>
        /// <param name="model">Model parameters</param>
        /// <returns>Time-domain fields</returns>
        public abstract Matrix<double> ComputeTimeFields(Model model);
    }
}