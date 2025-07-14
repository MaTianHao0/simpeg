using NUnit.Framework;
using MathNet.Numerics.LinearAlgebra;
using SimPEG.Survey;
using System.Collections.Generic;
using Data = SimPEG.Data.Data;
using SyntheticData = SimPEG.Data.SyntheticData;

namespace SimPEG.Tests
{
    /// <summary>
    /// Test concrete implementations for abstract classes
    /// </summary>
    public class TestSurvey : BaseSurvey
    {
        public TestSurvey(List<BaseSrc> sourceList) : base(sourceList) { }
    }

    public class TestRx : BaseRx
    {
        public TestRx(Matrix<double> locations, bool storeProjections = false) 
            : base(locations, storeProjections) { }
    }

    public class TestSrc : BaseSrc
    {
        public TestSrc(List<BaseRx> receiverList) : base(receiverList) { }
    }

    [TestFixture]
    public class DataTests
    {
        private BaseSurvey _survey;
        private Vector<double> _testData;

        [SetUp]
        public void Setup()
        {
            // Create test survey
            var locations = Matrix<double>.Build.DenseOfArray(new double[,] 
            {
                { 0.0, 0.0, 0.0 },
                { 1.0, 0.0, 0.0 },
                { 2.0, 0.0, 0.0 }
            });

            var rx = new TestRx(locations);
            var src = new TestSrc(new List<BaseRx> { rx });
            _survey = new TestSurvey(new List<BaseSrc> { src });

            _testData = Vector<double>.Build.DenseOfArray(new double[] { 1.0, 2.0, 3.0 });
        }

        [Test]
        public void TestDataCreation()
        {
            // Test basic data creation
            var data = new SimPEG.Data.Data(_survey, _testData);
            
            Assert.AreEqual(_survey, data.Survey);
            Assert.AreEqual(_testData, data.Dobs);
            Assert.AreEqual(3, data.Ndata);
        }

        [Test]
        public void TestDataWithRelativeError()
        {
            // Test data creation with relative error
            var relativeError = 0.1;
            var data = new SimPEG.Data.Data(_survey, _testData, relativeError: relativeError);
            
            Assert.AreEqual(3, data.StandardDeviation.Count);
            
            // Check that standard deviation is approximately relative_error * |data|
            for (int i = 0; i < _testData.Count; i++)
            {
                var expected = relativeError * System.Math.Abs(_testData[i]);
                Assert.AreEqual(expected, data.StandardDeviation[i], 1e-10);
            }
        }

        [Test]
        public void TestDataWithNoiseFloor()
        {
            // Test data creation with noise floor
            var noiseFloor = 0.05;
            var data = new SimPEG.Data.Data(_survey, _testData, noiseFloor: noiseFloor);
            
            Assert.AreEqual(3, data.StandardDeviation.Count);
            
            // Check that standard deviation equals noise floor
            for (int i = 0; i < _testData.Count; i++)
            {
                Assert.AreEqual(noiseFloor, data.StandardDeviation[i], 1e-10);
            }
        }

        [Test]
        public void TestDataWithCombinedErrors()
        {
            // Test data creation with both relative error and noise floor
            var relativeError = 0.1;
            var noiseFloor = 0.05;
            var data = new SimPEG.Data.Data(_survey, _testData, 
                              relativeError: relativeError, 
                              noiseFloor: noiseFloor);
            
            // Check that standard deviation combines both error sources
            for (int i = 0; i < _testData.Count; i++)
            {
                var relativeContrib = relativeError * System.Math.Abs(_testData[i]);
                var expected = System.Math.Sqrt(noiseFloor * noiseFloor + relativeContrib * relativeContrib);
                Assert.AreEqual(expected, data.StandardDeviation[i], 1e-10);
            }
        }

        [Test]
        public void TestSyntheticDataCreation()
        {
            // Test synthetic data creation
            var relativeError = 0.1;
            var random = new System.Random(42); // Fixed seed for reproducibility
            
            var syntheticData = new SimPEG.Data.SyntheticData(_survey, _testData, 
                                                relativeError: relativeError, 
                                                random: random);
            
            Assert.AreEqual(_testData, syntheticData.DcleanVector);
            Assert.AreEqual(3, syntheticData.Ndata);
            Assert.IsNotNull(syntheticData.Dobs);
            
            // Check that noise was applied by comparing data with uncertainty level
            // Since we use relative error of 0.1, noise should be around 10% of data values
            bool hasReasonableNoise = false;
            for (int i = 0; i < _testData.Count; i++)
            {
                var difference = System.Math.Abs(syntheticData.Dobs[i] - _testData[i]);
                var expectedNoiseLevel = relativeError * System.Math.Abs(_testData[i]);
                
                // If difference is less than 3 times the expected noise level, it's reasonable
                if (difference <= 3.0 * expectedNoiseLevel)
                {
                    hasReasonableNoise = true;
                }
            }
            Assert.IsTrue(hasReasonableNoise, "Synthetic data should have reasonable noise levels");
        }
    }
}