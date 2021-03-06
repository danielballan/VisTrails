###############################################################################
##
## Copyright (C) 2014-2015, New York University.
## All rights reserved.
## Contact: contact@vistrails.org
##
## This file is part of VisTrails.
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are met:
##
##  - Redistributions of source code must retain the above copyright notice,
##    this list of conditions and the following disclaimer.
##  - Redistributions in binary form must reproduce the above copyright
##    notice, this list of conditions and the following disclaimer in the
##    documentation and/or other materials provided with the distribution.
##  - Neither the name of the New York University nor the names of its
##    contributors may be used to endorse or promote products derived from
##    this software without specific prior written permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
## AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
## THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
## PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
## CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
## EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
## PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
## OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
## WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
## OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
## ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
##
###############################################################################

from __future__ import division

import numpy as np
import unittest
from vistrails.tests.utils import execute, intercept_results

from vistrails.packages.sklearn.init import (Digits, Iris, TrainTestSplit,
                                             Predict, Score, Transform,
                                             CrossValScore, _modules,
                                             GridSearchCV)
from vistrails.packages.sklearn import identifier

from sklearn.metrics import f1_score


def class_by_name(name):
    """Returns an autogenerated class from _modules from a string name."""
    for module in _modules:
        if module.__name__ == name:
            return module


class TestSklearn(unittest.TestCase):
    def test_digits(self):
        # check that the digits dataset can be loaded
        with intercept_results(Digits, 'data', Digits, 'target') as (data, target):
            self.assertFalse(execute([
                ('datasets|Digits', identifier, [])
            ]))
        data = np.vstack(data)
        target = np.hstack(target)
        self.assertEqual(data.shape, (1797, 64))
        self.assertEqual(target.shape, (1797,))

    def test_iris(self):
        # check that the iris dataset can be loaded
        with intercept_results(Iris, 'data', Iris, 'target') as (data, target):
            self.assertFalse(execute([
                ('datasets|Iris', identifier, [])
            ]))
        data = np.vstack(data)
        target = np.hstack(target)
        self.assertEqual(data.shape, (150, 4))
        self.assertEqual(target.shape, (150,))

    def test_train_test_split(self):
        # check that we can split the iris dataset
        with intercept_results(TrainTestSplit, 'training_data', TrainTestSplit,
                               'training_target', TrainTestSplit, 'test_data',
                               TrainTestSplit, 'test_target') as results:
            X_train, y_train, X_test, y_test = results
            self.assertFalse(execute(
                [
                    ('datasets|Iris', identifier, []),
                    ('cross-validation|TrainTestSplit', identifier,
                     [('test_size', [('Integer', '50')])])
                ],
                [
                    (0, 'data', 1, 'data'),
                    (0, 'target', 1, 'target')
                ]
            ))
        X_train = np.vstack(X_train)
        X_test = np.vstack(X_test)
        y_train = np.hstack(y_train)
        y_test = np.hstack(y_test)
        self.assertEqual(X_train.shape, (100, 4))
        self.assertEqual(X_test.shape, (50, 4))
        self.assertEqual(y_train.shape, (100,))
        self.assertEqual(y_test.shape, (50,))

    def test_classifier_training_predict(self):
        with intercept_results(Predict, 'prediction', Predict,
                               'decision_function', TrainTestSplit, 'test_target',
                               Score, 'score') as results:
            y_pred, decision_function, y_test, score = results
            self.assertFalse(execute(
                [
                    ('datasets|Iris', identifier, []),
                    ('cross-validation|TrainTestSplit', identifier,
                     [('test_size', [('Integer', '50')])]),
                    ('classifiers|LinearSVC', identifier, []),
                    ('Predict', identifier, []),
                    ('Score', identifier, []),
                    # use custom metric
                    ('Score', identifier,
                     [('metric', [('String', 'f1')])]),

                ],
                [
                    # train test split
                    (0, 'data', 1, 'data'),
                    (0, 'target', 1, 'target'),
                    # fit LinearSVC on training data
                    (1, 'training_data', 2, 'training_data'),
                    (1, 'training_target', 2, 'training_target'),
                    # predict on test data
                    (2, 'model', 3, 'model'),
                    (1, 'test_data', 3, 'data'),
                    # score test data
                    (2, 'model', 4, 'model'),
                    (1, 'test_data', 4, 'data'),
                    (1, 'test_target', 4, 'target'),
                    # f1 scorer
                    (2, 'model', 5, 'model'),
                    (1, 'test_data', 5, 'data'),
                    (1, 'test_target', 5, 'target')
                ]
            ))
        y_pred = np.hstack(y_pred)
        decision_function = np.vstack(decision_function)
        y_test = np.hstack(y_test)
        # unpack the results from the two scorers
        score_acc, score_f1 = score
        self.assertEqual(y_pred.shape, (50,))
        self.assertTrue(np.all(np.unique(y_pred) == np.array([0, 1, 2])))
        self.assertEqual(decision_function.shape, (50, 3))
        # some accuracy
        self.assertTrue(np.mean(y_test == y_pred) > .8)
        # score is actually the accuracy
        self.assertEqual(np.mean(y_test == y_pred), score_acc)
        # f1 score is actually f1 score
        self.assertEqual(f1_score(y_test, y_pred), score_f1)

    def test_transformer_supervised_transform(self):
        # test feature selection
        with intercept_results(Transform, 'transformed_data') as (transformed_data,):
            self.assertFalse(execute(
                [
                    ('datasets|Iris', identifier, []),
                    ('feature_selection|SelectKBest', identifier,
                        [('k', [('Integer', '2')])]),
                    ('Transform', identifier, [])
                ],
                [
                    (0, 'data', 1, 'training_data'),
                    (0, 'target', 1, 'training_target'),
                    (1, 'model', 2, 'model'),
                    (0, 'data', 2, 'data')
                ]
            ))
        transformed_data = np.vstack(transformed_data)
        self.assertEqual(transformed_data.shape, (150, 2))

    def test_transformer_unsupervised_transform(self):
        # test PCA
        with intercept_results(Transform, 'transformed_data') as (transformed_data,):
            self.assertFalse(execute(
                [
                    ('datasets|Iris', identifier, []),
                    ('decomposition|PCA', identifier,
                        [('n_components', [('Integer', '2')])]),
                    ('Transform', identifier, [])
                ],
                [
                    (0, 'data', 1, 'training_data'),
                    (1, 'model', 2, 'model'),
                    (0, 'data', 2, 'data')
                ]
            ))
        transformed_data = np.vstack(transformed_data)
        self.assertEqual(transformed_data.shape, (150, 2))

    def test_manifold_learning(self):
        # test Isomap
        with intercept_results(class_by_name("Isomap"), 'transformed_data') as (transformed_data,):
            self.assertFalse(execute(
                [
                    ('datasets|Iris', identifier, []),
                    ('manifold|Isomap', identifier, []),
                ],
                [
                    (0, 'data', 1, 'training_data'),
                ]
            ))
        transformed_data = np.vstack(transformed_data)
        self.assertEqual(transformed_data.shape, (150, 2))

    def test_cross_val_score(self):
        # chech that cross_val score of LinearSVC has the right length
        with intercept_results(CrossValScore, 'scores') as (scores,):
            self.assertFalse(execute(
                [
                    ('datasets|Iris', identifier, []),
                    ('classifiers|LinearSVC', identifier, []),
                    ('cross-validation|CrossValScore', identifier, []),
                ],
                [
                    (0, 'data', 2, 'data'),
                    (0, 'target', 2, 'target'),
                    (1, 'model', 2, 'model')
                ]
            ))
        scores = np.hstack(scores)
        self.assertEqual(scores.shape, (3,))
        self.assertTrue(np.mean(scores) > .8)

    def test_gridsearchcv(self):
        # check that gridsearch on DecisionTreeClassifier does the right number of runs
        # and gives the correct result.
        with intercept_results(GridSearchCV, 'scores', GridSearchCV,
                               'best_parameters') as (scores, parameters):
            self.assertFalse(execute(
                [
                    ('datasets|Iris', identifier, []),
                    ('classifiers|DecisionTreeClassifier', identifier, []),
                    ('GridSearchCV', identifier,
                     [('parameters', [('Dictionary', "{'max_depth': [1, 2, 3, 4]}")])]),
                ],
                [
                    (0, 'data', 2, 'data'),
                    (0, 'target', 2, 'target'),
                    (1, 'model', 2, 'model')
                ]
            ))
        self.assertEqual(len(scores[0]), 4)
        self.assertTrue(parameters[0]['max_depth'], 2)

    def test_pipeline(self):
        with intercept_results(Iris, 'target', Predict, 'prediction') as (y_true, y_pred):
            self.assertFalse(execute(
                [
                    ('datasets|Iris', identifier, []),
                    ('preprocessing|StandardScaler', identifier, []),
                    ('feature_selection|SelectKBest', identifier,
                        [('k', [('Integer', '2')])]),
                    ('classifiers|LinearSVC', identifier, []),
                    ('Pipeline', identifier, []),
                    ('Predict', identifier, [])
                ],
                [
                    # feed data to pipeline
                    (0, 'data', 4, 'training_data'),
                    (0, 'target', 4, 'training_target'),
                    # put models in pipeline
                    (1, 'model', 4, 'model1'),
                    (2, 'model', 4, 'model2'),
                    (3, 'model', 4, 'model3'),
                    # predict using pipeline
                    (4, 'model', 5, 'model'),
                    (0, 'data', 5, 'data')
                ]
            ))
            y_true, y_pred = np.array(y_true[0]), np.array(y_pred[0])
            self.assertEqual(y_true.shape, y_pred.shape)
            self.assertTrue(np.mean(y_true == y_pred) > .8)

    def test_nested_cross_validation(self):
        with intercept_results(CrossValScore, 'scores') as (scores, ):
            self.assertFalse(execute(
                [
                    ('datasets|Iris', identifier, []),
                    ('classifiers|DecisionTreeClassifier', identifier, []),
                    ('GridSearchCV', identifier,
                     [('parameters', [('Dictionary', "{'max_depth': [1, 2, 3, 4]}")])]),
                    ('cross-validation|CrossValScore', identifier, [])
                ],
                [
                    (0, 'data', 3, 'data'),
                    (0, 'target', 3, 'target'),
                    (1, 'model', 2, 'model'),
                    (2, 'model', 3, 'model')
                ]
            ))
        self.assertEqual(len(scores[0]), 3)
        self.assertTrue(np.mean(scores[0]) > .8)
