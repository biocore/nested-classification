from q2_sample_classifier import Classifier
from qiime2 import MetadataColumn
from qiime2.plugin import Plugin, Metadata, Categorical, Str
from qiime2.plugin import (
    Int, Str, Float, Range, Bool, Plugin, Metadata, Choices, MetadataColumn,
    Numeric, Categorical, Citations, Visualization, TypeMatch)
from q2_types.feature_table import (
    FeatureTable, Frequency, RelativeFrequency, PresenceAbsence, Balance,
    PercentileNormalized, Design)

from q2_sample_classifier._type import (ClassifierPredictions, RegressorPredictions,
                    SampleEstimator, BooleanSeries, Importance,
                    Classifier, Regressor, Probabilities,
                    TrueTargets)
from qiime2.plugin import (
    Int, Str, Float, Range, Bool, Plugin, Metadata, Choices, MetadataColumn,
    Numeric, Categorical, Citations, Visualization, TypeMatch)


from qiime2.plugins import sample_classifier
from q2_types.sample_data import SampleData, AlphaDiversity
import q2_nc
from q2_nc import *
import _training 
from _predict_samples import predict_samples



plugin = Plugin(
    name='nested-classification',
    version=q2_nc.__version__,
    website='https://github.com/biocore/weneedtomakethis',
    package='q2_nc',
    description="QIIME2 package meant for nested-classification in a taxonomic hierachy tree. Utilizing q2-sample-classifiers, classifiers are trained with metadata-subsets at every unique node in the taxonomic tree. New feature-table can be inserted to predict evolutionary classification if the metadata is identical. ",
    short_description="This trains and predicts classifiers nested in a vertebrate taxonomic tree based on the animal samples."
)

#Variables
pipeline_outputs = [
    ('model_summary', Visualization),
    ('accuracy_results', Visualization)]

output_descriptions = {
    'model_summary': 'Summarized parameter and (if enabled) feature '
                     'selection information for the trained estimator.',
    'accuracy_results': 'Accuracy results visualization.'
}

# THIS IS EXAMPLE
# The semantic type SampleData requires a property.
# The only one available by default is AlphaDiversity
# so let's "use" that for now, and worry about defining
# our own property later
plugin.methods.register_function(
    function=q2_nc.samples_of_interest,
    inputs={},
    parameters={'metadata': Metadata},
    outputs=[('samples_of_interest', SampleData[AlphaDiversity])],
    input_descriptions={},
    parameter_descriptions={'metadata': 'our sample metadata'},
    output_descriptions={
        'samples_of_interest': 'sampsasdles meeting a specific criteria',
    },
    name='do stuff',
    description="do some super crazy complex",
    citations=[]
)

plugin.methods.register_function(
    function=_training.training_samples,
    inputs={'table': FeatureTable[Frequency]},
    parameters={'output_directory': Str, 'metadata': Metadata},
    outputs=[('sample_estimators', SampleEstimator[Classifier])],
    input_descriptions={'table': 'Feature table containing all features that '
                               'should be used for target prediction.'},
    parameter_descriptions={'output_directory': 'Folder to hold all trained estimators','metadata': 'Categorical metadata column to use as prediction target.'},
    output_descriptions={'sample_estimators': 'Trained sample estimator.'},
    name='Train classifiers ',
    description='Train and test many nested supervised learning classifiers in taxonomic tree formed with metadata.',
    citations=[]
)

plugin.methods.register_function(
    function=predict_samples,
    inputs={'table': FeatureTable[Frequency]},
    parameters={'input_directory': Str, 'metadata': Metadata},
    outputs=[#('predictions', SampleData[ClassifierPredictions])],
             ('probabilities', SampleData[Probabilities])],
    input_descriptions={'table': 'Feature table containing all features that '
                               'should be used for target prediction.'},
    parameter_descriptions={'input_directory': 'Folder with all trained estimators','metadata': 'Categorical metadata column to use as prediction target.'},
    output_descriptions={#'predictions': 'Predicted target values for each input sample.', 
                        'probabilities': 'Predicted class probabilities for each input sample.'},
    name='Predict classifications from trained classifiers',
    description='Use trained classifiers in taxonomic tree to predict classifications',
    citations=[]
)



