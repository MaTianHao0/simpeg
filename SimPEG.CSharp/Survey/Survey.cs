using System;
using MathNet.Numerics.LinearAlgebra;
using System.Collections.Generic;

namespace SimPEG.Survey
{
    /// <summary>
    /// Base SimPEG receiver class.
    /// </summary>
    public abstract class BaseRx
    {
        private Matrix<double> _locations;
        private Dictionary<string, object> _projections;
        private bool _storeProjections;
        private Guid _uid;

        /// <summary>
        /// Receiver locations
        /// </summary>
        public Matrix<double> Locations
        {
            get => _locations;
            set => _locations = value ?? throw new ArgumentNullException(nameof(value));
        }

        /// <summary>
        /// Store projections from the mesh to receiver
        /// </summary>
        public bool StoreProjections
        {
            get => _storeProjections;
            set => _storeProjections = value;
        }

        /// <summary>
        /// Number of receiver locations
        /// </summary>
        public int NLoc => Locations?.RowCount ?? 0;

        /// <summary>
        /// Number of spatial dimensions
        /// </summary>
        public int NDim => Locations?.ColumnCount ?? 0;

        /// <summary>
        /// Unique identifier for this receiver
        /// </summary>
        public Guid Uid => _uid;

        /// <summary>
        /// Initializes a new instance of the BaseRx class.
        /// </summary>
        /// <param name="locations">Locations associated with a given receiver</param>
        /// <param name="storeProjections">Store projections from the mesh to receiver</param>
        protected BaseRx(Matrix<double> locations, bool storeProjections = false)
        {
            Locations = locations;
            StoreProjections = storeProjections;
            _projections = new Dictionary<string, object>();
            _uid = Guid.NewGuid();
        }

        /// <summary>
        /// Get projection for a specific key
        /// </summary>
        /// <param name="key">Projection key</param>
        /// <returns>Projection object</returns>
        public object GetProjection(string key)
        {
            return _projections.TryGetValue(key, out var projection) ? projection : null;
        }

        /// <summary>
        /// Set projection for a specific key
        /// </summary>
        /// <param name="key">Projection key</param>
        /// <param name="projection">Projection object</param>
        public void SetProjection(string key, object projection)
        {
            _projections[key] = projection;
        }
    }

    /// <summary>
    /// Base SimPEG source class.
    /// </summary>
    public abstract class BaseSrc
    {
        private List<BaseRx> _receiverList;
        private Guid _uid;

        /// <summary>
        /// List of receivers associated with this source
        /// </summary>
        public List<BaseRx> ReceiverList
        {
            get => _receiverList;
            set => _receiverList = value ?? throw new ArgumentNullException(nameof(value));
        }

        /// <summary>
        /// Number of receivers
        /// </summary>
        public int NRx => ReceiverList?.Count ?? 0;

        /// <summary>
        /// Unique identifier for this source
        /// </summary>
        public Guid Uid => _uid;

        /// <summary>
        /// Initializes a new instance of the BaseSrc class.
        /// </summary>
        /// <param name="receiverList">List of receivers</param>
        protected BaseSrc(List<BaseRx> receiverList)
        {
            ReceiverList = receiverList;
            _uid = Guid.NewGuid();
        }

        /// <summary>
        /// Total number of data points from all receivers
        /// </summary>
        public virtual int Ndata
        {
            get
            {
                int total = 0;
                foreach (var rx in ReceiverList)
                {
                    total += rx.NLoc;
                }
                return total;
            }
        }
    }

    /// <summary>
    /// Base SimPEG survey class.
    /// </summary>
    public abstract class BaseSurvey
    {
        private List<BaseSrc> _sourceList;

        /// <summary>
        /// List of sources in the survey
        /// </summary>
        public List<BaseSrc> SourceList
        {
            get => _sourceList;
            set => _sourceList = value ?? throw new ArgumentNullException(nameof(value));
        }

        /// <summary>
        /// Number of sources
        /// </summary>
        public int NSrc => SourceList?.Count ?? 0;

        /// <summary>
        /// Initializes a new instance of the BaseSurvey class.
        /// </summary>
        /// <param name="sourceList">List of sources</param>
        protected BaseSurvey(List<BaseSrc> sourceList)
        {
            SourceList = sourceList;
        }

        /// <summary>
        /// Total number of data points in the survey
        /// </summary>
        public virtual int Ndata
        {
            get
            {
                int total = 0;
                foreach (var src in SourceList)
                {
                    total += src.Ndata;
                }
                return total;
            }
        }

        /// <summary>
        /// Get all receivers from all sources
        /// </summary>
        /// <returns>List of all receivers</returns>
        public List<BaseRx> GetAllReceivers()
        {
            var allReceivers = new List<BaseRx>();
            foreach (var src in SourceList)
            {
                allReceivers.AddRange(src.ReceiverList);
            }
            return allReceivers;
        }
    }

    /// <summary>
    /// Time-domain survey base class
    /// </summary>
    public abstract class BaseTimeSurvey : BaseSurvey
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
        /// Initializes a new instance of the BaseTimeSurvey class.
        /// </summary>
        /// <param name="sourceList">List of sources</param>
        /// <param name="timeSteps">Time stepping</param>
        protected BaseTimeSurvey(List<BaseSrc> sourceList, Vector<double> timeSteps) 
            : base(sourceList)
        {
            TimeSteps = timeSteps;
        }
    }
}