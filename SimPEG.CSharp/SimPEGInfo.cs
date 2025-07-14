using System;
using System.Reflection;

namespace SimPEG
{
    /// <summary>
    /// SimPEG - Simulation and Parameter Estimation in Geophysics
    /// 
    /// SimPEG is a C# package for simulation and gradient based
    /// parameter estimation in the context of geophysical applications.
    /// 
    /// This is a C# port of the original Python SimPEG library.
    /// </summary>
    public static class SimPEGInfo
    {
        /// <summary>
        /// Version of SimPEG
        /// </summary>
        public const string Version = "0.18.1";

        /// <summary>
        /// Authors of SimPEG
        /// </summary>
        public const string Authors = "SimPEG Team (C# Port)";

        /// <summary>
        /// License information
        /// </summary>
        public const string License = "MIT";

        /// <summary>
        /// Copyright information
        /// </summary>
        public const string Copyright = "2013 - 2024, SimPEG Team, http://simpeg.xyz";

        /// <summary>
        /// Get version information
        /// </summary>
        /// <returns>Version string</returns>
        public static string GetVersion()
        {
            return $"SimPEG C# v{Version}";
        }

        /// <summary>
        /// Get full information about SimPEG
        /// </summary>
        /// <returns>Information string</returns>
        public static string GetInfo()
        {
            var assembly = Assembly.GetExecutingAssembly();
            var assemblyName = assembly.GetName();
            
            return $"""
                SimPEG - Simulation and Parameter Estimation in Geophysics
                Version: {Version}
                Authors: {Authors}
                License: {License}
                Copyright: {Copyright}
                
                Assembly: {assemblyName.Name}
                Assembly Version: {assemblyName.Version}
                Runtime: {Environment.Version}
                """;
        }
    }
}