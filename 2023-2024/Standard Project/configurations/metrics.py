from sklearn.metrics import f1_score

from cinnamon_core.core.registry import Registry, register, RegistrationKey
from cinnamon_generic.components.metrics import LambdaMetric, MetricPipeline
from cinnamon_generic.configurations.metrics import LambdaMetricConfig
from cinnamon_generic.configurations.pipeline import PipelineConfig


class SequenceF1MetricConfig(LambdaMetricConfig):

    @classmethod
    def get_default(
            cls
    ):
        config = super().get_default()
        config.method = f1_score
        config.method_args = {'average': 'macro'}
        return config

    @classmethod
    def get_emotion_config(
            cls
    ):
        config = cls.get_default()
        config.name = 'emotion_F1'
        return config

    @classmethod
    def get_triggers_config(
            cls
    ):
        config = cls.get_default()
        config.name = 'triggers_F1'
        return config


@register
def register_metrics_configurations():
    Registry.add_and_bind(config_class=SequenceF1MetricConfig,
                          config_constructor=SequenceF1MetricConfig.get_emotion_config,
                          component_class=LambdaMetric,
                          name='metrics',
                          tags={'emotions_f1'},
                          namespace='sp')

    Registry.add_and_bind(config_class=SequenceF1MetricConfig,
                          config_constructor=SequenceF1MetricConfig.get_triggers_config,
                          component_class=LambdaMetric,
                          name='metrics',
                          tags={'triggers_f1'},
                          namespace='sp')

    Registry.add_and_bind(config_class=PipelineConfig,
                          config_constructor=PipelineConfig.from_keys,
                          config_kwargs={
                              'keys': [
                                  RegistrationKey(name='metrics', tags={'emotions_f1'}, namespace='sp'),
                                  RegistrationKey(name='metrics', tags={'triggers_f1'}, namespace='sp'),
                              ],
                              'names': [
                                  'emotions_f1',
                                  'triggers_f1',
                              ]
                          },
                          component_class=MetricPipeline,
                          name='metrics',
                          tags={'emotions_f1', 'triggers_f1'},
                          namespace='sp')
