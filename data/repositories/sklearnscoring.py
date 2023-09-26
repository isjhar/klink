from sklearn.metrics import precision_recall_fscore_support as score

from domain.entities.scoring import Scoring


class SklearnScoring(Scoring):
    def score(self, validations, actuals):
        precision, recall, fscore, support = score(validations, actuals)

        print('precision: {}'.format(precision))
        print('recall: {}'.format(recall))
        print('fscore: {}'.format(fscore))
        print('support: {}'.format(support))
