using NUnit.Framework;
using MathNet.Numerics.LinearAlgebra;
using SimPEG.Models;

namespace SimPEG.Tests
{
    [TestFixture]
    public class ModelTests
    {
        [Test]
        public void TestModelCreation()
        {
            // Test basic model creation with identity mapping
            var vector = Vector<double>.Build.DenseOfArray(new double[] { 1.0, 2.0, 3.0 });
            var model = new Model(vector);
            
            Assert.AreEqual(3, model.Size);
            Assert.AreEqual(3, model.NParam);
            Assert.AreEqual(vector, model.Vector);
        }

        [Test]
        public void TestModelWithIdentityMapping()
        {
            // Test model with explicit identity mapping
            var vector = Vector<double>.Build.DenseOfArray(new double[] { 1.0, 2.0, 3.0 });
            var mapping = new IdentityMapping(3);
            var model = new Model(vector, mapping);
            
            Assert.AreEqual(mapping, model.Mapping);
            Assert.AreEqual(vector, model.Transform);
            
            var derivMatrix = model.TransformDeriv;
            Assert.AreEqual(3, derivMatrix.RowCount);
            Assert.AreEqual(3, derivMatrix.ColumnCount);
            
            // Check identity matrix
            for (int i = 0; i < 3; i++)
            {
                for (int j = 0; j < 3; j++)
                {
                    if (i == j)
                        Assert.AreEqual(1.0, derivMatrix[i, j], 1e-10);
                    else
                        Assert.AreEqual(0.0, derivMatrix[i, j], 1e-10);
                }
            }
        }

        [Test]
        public void TestModelWithExpMapping()
        {
            // Test model with exponential mapping
            var vector = Vector<double>.Build.DenseOfArray(new double[] { 0.0, 1.0, 2.0 });
            var mapping = new ExpMapping(3);
            var model = new Model(vector, mapping);
            
            var transformed = model.Transform;
            Assert.AreEqual(System.Math.Exp(0.0), transformed[0], 1e-10);
            Assert.AreEqual(System.Math.Exp(1.0), transformed[1], 1e-10);
            Assert.AreEqual(System.Math.Exp(2.0), transformed[2], 1e-10);
            
            var derivMatrix = model.TransformDeriv;
            Assert.AreEqual(System.Math.Exp(0.0), derivMatrix[0, 0], 1e-10);
            Assert.AreEqual(System.Math.Exp(1.0), derivMatrix[1, 1], 1e-10);
            Assert.AreEqual(System.Math.Exp(2.0), derivMatrix[2, 2], 1e-10);
        }

        [Test]
        public void TestModelWithLogMapping()
        {
            // Test model with log mapping
            var vector = Vector<double>.Build.DenseOfArray(new double[] { 1.0, System.Math.E, 10.0 });
            var mapping = new LogMapping(3);
            var model = new Model(vector, mapping);
            
            var transformed = model.Transform;
            Assert.AreEqual(System.Math.Log(1.0), transformed[0], 1e-10);
            Assert.AreEqual(System.Math.Log(System.Math.E), transformed[1], 1e-10);
            Assert.AreEqual(System.Math.Log(10.0), transformed[2], 1e-10);
            
            var derivMatrix = model.TransformDeriv;
            Assert.AreEqual(1.0 / 1.0, derivMatrix[0, 0], 1e-10);
            Assert.AreEqual(1.0 / System.Math.E, derivMatrix[1, 1], 1e-10);
            Assert.AreEqual(1.0 / 10.0, derivMatrix[2, 2], 1e-10);
        }

        [Test]
        public void TestModelIndexing()
        {
            // Test model parameter access by index
            var vector = Vector<double>.Build.DenseOfArray(new double[] { 1.0, 2.0, 3.0 });
            var model = new Model(vector);
            
            Assert.AreEqual(1.0, model[0]);
            Assert.AreEqual(2.0, model[1]);
            Assert.AreEqual(3.0, model[2]);
            
            model[1] = 5.0;
            Assert.AreEqual(5.0, model[1]);
        }

        [Test]
        public void TestModelClone()
        {
            // Test model cloning
            var vector = Vector<double>.Build.DenseOfArray(new double[] { 1.0, 2.0, 3.0 });
            var model = new Model(vector);
            var cloned = model.Clone();
            
            Assert.AreEqual(model.Size, cloned.Size);
            Assert.AreEqual(model.Vector, cloned.Vector);
            Assert.AreNotSame(model.Vector, cloned.Vector); // Should be different instances
        }

        [Test]
        public void TestInvalidModelSize()
        {
            // Test that model creation fails with incorrect size
            var vector = Vector<double>.Build.DenseOfArray(new double[] { 1.0, 2.0, 3.0 });
            var mapping = new IdentityMapping(5); // Wrong size
            
            Assert.Throws<System.ArgumentException>(() => new Model(vector, mapping));
        }
    }
}