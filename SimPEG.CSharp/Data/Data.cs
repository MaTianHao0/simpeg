using System;
using MathNet.Numerics.LinearAlgebra;
using SimPEG.Survey;
using SimPEG.Utils;

namespace SimPEG.Data
{
    /// <summary>
    /// Class for defining data in SimPEG.
    /// 
    /// The Data class is used to create an object which connects the survey geometry,
    /// observed data and data uncertainties.
    /// </summary>
    public class Data
    {
        private Vector<double> _dobs;
        private Vector<double> _standardDeviation;
        private BaseSurvey _survey;

        /// <summary>
        /// A SimPEG survey object. For each geophysical method, the survey object defines
        /// the survey geometry; i.e. sources, receivers, data type.
        /// </summary>
        public BaseSurvey Survey
        {
            get => _survey;
            set => _survey = value ?? throw new ArgumentNullException(nameof(value));
        }

        /// <summary>
        /// Observed data.
        /// </summary>
        public Vector<double> Dobs
        {
            get => _dobs;
            set => _dobs = value ?? throw new ArgumentNullException(nameof(value));
        }

        /// <summary>
        /// Standard deviations of the data uncertainties
        /// </summary>
        public Vector<double> StandardDeviation
        {
            get => _standardDeviation;
            set => _standardDeviation = value ?? throw new ArgumentNullException(nameof(value));
        }

        /// <summary>
        /// Number of data points
        /// </summary>
        public int Ndata => Dobs?.Count ?? 0;

        /// <summary>
        /// Initializes a new instance of the Data class.
        /// </summary>
        /// <param name="survey">A SimPEG survey object</param>
        /// <param name="dobs">Observed data</param>
        /// <param name="relativeError">Relative uncertainties to the data (optional)</param>
        /// <param name="noiseFloor">Floor/absolute uncertainties to the data (optional)</param>
        /// <param name="standardDeviation">Direct uncertainty specification (optional)</param>
        public Data(BaseSurvey survey, Vector<double> dobs, 
                   double? relativeError = null, double? noiseFloor = null, 
                   Vector<double>? standardDeviation = null)
        {
            Survey = survey;
            Dobs = dobs;

            if (standardDeviation != null)
            {
                StandardDeviation = standardDeviation;
            }
            else
            {
                StandardDeviation = CalculateStandardDeviation(dobs, relativeError, noiseFloor);
            }
        }

        /// <summary>
        /// Calculate standard deviation from relative error and noise floor
        /// </summary>
        private Vector<double> CalculateStandardDeviation(Vector<double> dobs, 
                                                         double? relativeError, 
                                                         double? noiseFloor)
        {
            var stdDev = Vector<double>.Build.Dense(dobs.Count);
            
            for (int i = 0; i < dobs.Count; i++)
            {
                double variance = 0.0;
                
                // Add noise floor contribution
                if (noiseFloor.HasValue)
                {
                    variance += noiseFloor.Value * noiseFloor.Value;
                }
                
                // Add relative error contribution
                if (relativeError.HasValue)
                {
                    var relativeContrib = relativeError.Value * Math.Abs(dobs[i]);
                    variance += relativeContrib * relativeContrib;
                }
                
                stdDev[i] = Math.Sqrt(variance);
            }
            
            return stdDev;
        }

        /// <summary>
        /// Create synthetic data with noise
        /// </summary>
        /// <param name="cleanData">Clean synthetic data</param>
        /// <param name="random">Random number generator for noise</param>
        /// <returns>Noisy synthetic data</returns>
        public Vector<double> AddNoise(Vector<double> cleanData, Random? random = null)
        {
            random ??= new Random();
            var noisyData = Vector<double>.Build.Dense(cleanData.Count);
            
            for (int i = 0; i < cleanData.Count; i++)
            {
                var noise = random.NextGaussian() * StandardDeviation[i];
                noisyData[i] = cleanData[i] + noise;
            }
            
            return noisyData;
        }
    }

    /// <summary>
    /// Synthetic data class for SimPEG
    /// </summary>
    public class SyntheticData : Data
    {
        /// <summary>
        /// Clean synthetic data (without noise)
        /// </summary>
        public Vector<double> DcleanVector { get; set; }

        /// <summary>
        /// Initializes a new instance of the SyntheticData class.
        /// </summary>
        public SyntheticData(BaseSurvey survey, Vector<double> dclean,
                           double? relativeError = null, double? noiseFloor = null,
                           Vector<double>? standardDeviation = null, Random? random = null)
            : base(survey, Vector<double>.Build.Dense(dclean.Count), relativeError, noiseFloor, standardDeviation)
        {
            DcleanVector = dclean;
            
            // Generate noisy observed data
            Dobs = AddNoise(dclean, random);
        }
    }
}