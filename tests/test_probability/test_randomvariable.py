"""Tests for the random variable implementation."""

import unittest
from tests.custom_assertions import NumpyAssertions

import itertools
import numpy as np

from probnum import probability
from probnum.linalg import linear_operators

# Random variable instantiation
scalars = [0, int(1), .1, np.nan, np.inf]
arrays = [np.empty(2), np.zeros(4), np.array([]), np.array([1, 2])]

# Random variable arithmetic
arrays2d = [np.empty(2), np.zeros(2), np.array([np.inf, 1]), np.array([1, -2.5])]
matrices2d = [np.array([[1, 2], [3, 2]]), np.array([[0, 0], [1.0, -4.3]])]
linops2d = [linear_operators.MatrixMult(A=np.array([[1, 2], [4, 5]]))]
randvars2d = [
    probability.RandomVariable(distribution=probability.Normal(mean=np.array([1, 2]), cov=np.array([[2, 0], [0, 5]])))]
randvars2x2 = [
    probability.RandomVariable(shape=(2, 2),
                               distribution=probability.Normal(mean=np.array([[-2, .3], [0, 1]]),
                                                               cov=linear_operators.SymmetricKronecker(
                                                                   A=np.eye(2), B=np.ones((2, 2)))))
]


class TestRandomVariable(unittest.TestCase, NumpyAssertions):
    """Test random variable properties."""

    # Instantiation
    def test_rv_dtype(self):
        """Check the random variable types."""
        pass

    def test_rv_from_number(self):
        """Create a random variable from a number."""
        for x in scalars:
            with self.subTest():
                probability.asrandvar(x)

    def test_rv_from_ndarray(self):
        """Create a random variable from an array."""
        for arr in scalars:
            with self.subTest():
                probability.asrandvar(arr)

    # def test_rv_from_linearoperator(self):
    #     """Create a random variable from a linear operator."""
    #     for linop in linops:
    #       with self.suTest():
    #           probability.asrandvar(A)

    # Arithmetic
    def test_rv_addition(self):
        """Addition with random variables."""
        for (x, rv) in list(itertools.product(arrays2d, randvars2d)):
            with self.subTest():
                z1 = x + rv
                z2 = rv + x
                self.assertEqual(z1.shape, rv.shape)
                self.assertEqual(z2.shape, rv.shape)
                self.assertIsInstance(z1, probability.RandomVariable)
                self.assertIsInstance(z2, probability.RandomVariable)

    def test_rv_scalarmult(self):
        """Multiplication of random variables with scalar constants."""
        for (alpha, rv) in list(itertools.product(scalars, randvars2d)):
            with self.subTest():
                z = alpha * rv
                self.assertEqual(z.shape, rv.shape)
                self.assertIsInstance(z, probability.RandomVariable)

    def test_rv_broadcasting(self):
        """Broadcasting for arrays and random variables."""
        for alpha, rv in list(itertools.product(scalars, randvars2d)):
            with self.subTest():
                z = alpha + rv
                z = rv - alpha
                self.assertEqual(z.shape, rv.shape)

    def test_rv_dotproduct(self):
        """Dot product of random variables with constant vectors."""
        for x, rv in list(itertools.product([np.array([1, 2]), np.array([0, -1.4])], randvars2d)):
            with self.subTest():
                # z1 = np.dot(x, rv)
                # z2 = np.dot(rv, x)
                z1 = rv @ x[:, None]
                z2 = x @ rv
                self.assertEqual(z1.shape, ())
                self.assertEqual(z2.shape, ())
                self.assertIsInstance(z1, probability.RandomVariable)
                self.assertIsInstance(z2, probability.RandomVariable)

    def test_rv_matmul(self):
        """Multiplication of random variables with constant matrices."""
        for A, rv in list(itertools.product(matrices2d, randvars2d)):
            with self.subTest():
                y2 = A @ rv
                self.assertEqual(y2.shape[0], A.shape[0])
                self.assertIsInstance(y2, probability.RandomVariable)

    def test_rv_linop_matmul(self):
        """Linear operator applied to a random variable."""
        for A, rv in list(itertools.product(linops2d, randvars2d)):
            with self.subTest():
                y = A @ rv + np.array([-1, 1.1])
                self.assertEqual(y.shape[0], A.shape[0])

    def test_rv_vector_product(self):
        """Matrix-variate random variable applied to vector."""
        for rv in randvars2x2:
            with self.subTest():
                x = np.array([[1], [-4]])
                y = rv @ x
                X = np.kron(np.eye(rv.shape[0]), x)
                truemean = rv.mean() @ x
                truecov = X.T @ rv.cov().todense() @ X
                self.assertIsInstance(y, probability.RandomVariable, "The variable y does not have the correct type.")
                self.assertEqual(y.shape, (2, 1), "Shape of resulting random variable incorrect.")
                self.assertAllClose(y.mean(), truemean,
                                    msg="Means of random variables do not match.")
                self.assertAllClose(y.cov().todense(), truecov,
                                    msg="Covariances of random variables do not match.")

    # Random seed
    def test_different_rv_seeds(self):
        """Arithmetic operation between two random variables with different seeds."""
        pass


if __name__ == "__main__":
    unittest.main()
