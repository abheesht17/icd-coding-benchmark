"""Metrics."""
import numpy as np
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)

from src.utils.configuration import Config
from src.utils.mapper import ConfigMapper
from src.utils.text_loggers import get_logger

logger = get_logger(__name__)


def to_np_array(array):
    # Keep None as it is, and convert others into Numpy array
    if array is not None and not isinstance(array, np.ndarray):
        array = np.array(array)
    return array


class Metric:
    def __init__(self, config):
        if isinstance(config, dict):
            config = Config(dic=config)
        self.config = config

    def __call__(self, y_true, y_pred=None, p_pred=None):
        y_true = to_np_array(y_true)
        y_pred = to_np_array(y_pred)
        p_pred = to_np_array(p_pred)
        return self.forward(y_true, y_pred, p_pred)

    def forward(self, y_true, y_pred=None, p_pred=None):
        raise NotImplementedError("This is the base class for metrics")


def load_metric(config_dict):
    metric_params = config_dict.get("params", None)
    metric_class = config_dict.get("class", config_dict.get("name"))
    logger.debug(
        f"Loading metric {metric_class} with the following config: "
        f"{metric_params}"
    )
    return ConfigMapper.get_object("metrics", metric_class)(metric_params)


#########################################################################
# Macro Metrics: computes metrics for each label, and average over labels
#########################################################################


@ConfigMapper.map("metrics", "macro_prec")
class MacroPrecision(Metric):
    def forward(self, y_true, y_pred=None, p_pred=None):
        y_pred = y_pred if y_pred is not None else p_pred.round()
        return precision_score(y_true=y_true, y_pred=y_pred, average="macro")


@ConfigMapper.map("metrics", "macro_rec")
class MacroRecall(Metric):
    def forward(self, y_true, y_pred=None, p_pred=None):
        y_pred = y_pred if y_pred is not None else p_pred.round()
        return recall_score(y_true=y_true, y_pred=y_pred, average="macro")


@ConfigMapper.map("metrics", "macro_f1")
class MacroF1(Metric):
    def forward(self, y_true, y_pred=None, p_pred=None):
        y_pred = y_pred if y_pred is not None else p_pred.round()
        return f1_score(y_true=y_true, y_pred=y_pred, average="macro")


@ConfigMapper.map("metrics", "macro_auc")
class MacroAUC(Metric):
    def forward(self, y_true, y_pred=None, p_pred=None):
        assert p_pred is not None
        # Filter out the class without positive examples
        pos_flag = y_true.sum(axis=0) > 0
        y_true = y_true[:, pos_flag]
        p_pred = p_pred[:, pos_flag]
        return roc_auc_score(y_true, p_pred, average="macro")


##########################################################################
# Micro Metrics: treat all predictions as in the same label
##########################################################################


@ConfigMapper.map("metrics", "micro_prec")
class MicroPrecision(Metric):
    def forward(self, y_true, y_pred=None, p_pred=None):
        y_pred = y_pred if y_pred is not None else p_pred.round()
        return precision_score(y_true=y_true, y_pred=y_pred, average="micro")


@ConfigMapper.map("metrics", "micro_rec")
class MicroRecall(Metric):
    def forward(self, y_true, y_pred=None, p_pred=None):
        y_pred = y_pred if y_pred is not None else p_pred.round()
        return recall_score(y_true=y_true, y_pred=y_pred, average="micro")


@ConfigMapper.map("metrics", "micro_f1")
class MicroF1(Metric):
    def forward(self, y_true, y_pred=None, p_pred=None):
        y_pred = y_pred if y_pred is not None else p_pred.round()
        return f1_score(y_true=y_true, y_pred=y_pred, average="micro")


@ConfigMapper.map("metrics", "micro_auc")
class MicroAUC(Metric):
    def forward(self, y_true, y_pred=None, p_pred=None):
        assert p_pred is not None
        return roc_auc_score(y_true, p_pred, average="micro")


##########################################################################
# Metrics@K
##########################################################################


@ConfigMapper.map("metrics", "recall_at_k")
class RecallAtK(Metric):
    def __init__(self, config):
        super().__init__(config)
        self.k = self.config.k

    def forward(self, y_true, y_pred=None, p_pred=None):
        # We need scores
        assert p_pred is not None

        # Get the top-k predictons
        top_k = np.argsort(p_pred)[:, : -(self.k + 1) : -1]

        # Compute precision
        precs = []
        for y, t in zip(y_true, top_k):
            correct = y[t].sum()
            total = y.sum()
            prec = correct / total if total else 0.0
            precs.append(prec)

        return np.mean(precs)


@ConfigMapper.map("metrics", "prec_at_k")
class PrecAtK(Metric):
    def __init__(self, config):
        super().__init__(config)
        self.k = self.config.k

    def forward(self, y_true, y_pred=None, p_pred=None):
        # We need scores
        assert p_pred is not None

        # Get the top-k predictons
        top_k = np.argsort(p_pred)[:, : -(self.k + 1) : -1]

        # Compute precision
        precs = []
        for y, t in zip(y_true, top_k):
            correct = y[t].sum()
            prec = correct / self.k
            precs.append(prec)

        return np.mean(precs)


##########################################################################
# Others
##########################################################################


@ConfigMapper.map("metrics", "accuracy")
class Accuracy(Metric):
    def forward(self, y_true, y_pred=None, p_pred=None):
        y_pred = y_pred if y_pred is not None else p_pred.round()
        return accuracy_score(y_true=y_true.ravel(), y_pred=y_pred.ravel())
