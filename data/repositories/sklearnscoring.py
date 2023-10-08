from sklearn.metrics import f1_score, precision_score
from domain.entities.scoring import Scoring


class SklearnScoring(Scoring):
    def score(self, validations, actuals):
        print('fscore: {}'.format(f1_score(validations, actuals, average="macro")))
        print('precision: {}'.format(precision_score(
            validations, actuals, average="macro")))
