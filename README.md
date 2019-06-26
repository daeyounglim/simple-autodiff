# Simple Automatic Differentiation

This repo implements a simple, comically inefficient auto diff algorithm in python using a "define by run" methodology.  What that means is you can write more or less natural, native code to compute results (using basic operators, loops, ifs, function calls etc), and then compute the derivative/gradient/jacobian of that computation.

The ``Scalar`` type is a numeric type that supports normal numeric operators but performs tracking that allows one to later compute the derivatives.  In order to perform simple machine learning tasks I implement a comically inefficient Matrix class which gives you simple linear algebra operations.  However the Matrix is really just a 2D array of Scalars, so all computation and derivatives are done on each Scalar individually (so its slow).

### Forward vs Reverse Mode Autodiff

The package implements both forward and reverse mode autodiff (along with a slow finite difference for doublechecking).  Forward vs reverse mode refers to the order in which the derivative is computed, and based on the structure of the function one or the other (or a hybrid) may be more efficient.  Forward mode implies that the partial derivative are accumulated by working your way from the inputs to the outputs.  This means the computation is O(# of inputs).  Reverse mode accumulates the partial derivatives from the outputs backwards to the inputs, and is thus O(# outputs).  Machine learning problems are more amenable to reverse mode because the error function is a function of many (thousands, millions of) weights, but has a single scalar output.  Reverse mode autodifferentiation is the other name for "backpropagation."

### Simple Example

Consider a functon like this:

    def func(x):
      return 2*x**2 + 4*x + 3

Of course you can evalute it thusly:

    print(func(12))

But you can also compute the same result using a Scalar:

    x = Scalar(12)
    y = func(x)
    print(y)

This allows you to compute the derivative:

    x = Scalar(12)
	y = func(x)
	print(y)
	dydx = reverse_autodiff(y, x) # Take the deriv of y w.r.t. x
	print(dydx)

### MNIST

The 'mnist.py' file solves mnist (verrry slowly) using this package.  Note I actually don't even solve mnist as it is, I shrink the images from 28x28 to 7x7 to reduce the computation significantly.  It still takes 1-2 hours.  It will only get 88% accuracy (vs 91-92%) due to the reduced size images.

The ''linear_fit.py'' file is a simple optimizer that fits a line to a set of x,y points that were generated by sampling random points from the line y=.7x + 4 with some gaussian noise added to the y coordinates.  The optimization starts from a line of y=-2x + 0 and "quickly" converges to the correct line.

### References

The following references were useful in understanding practical implementation of auto diff, in particular reverse mode.

* [Wikipedia auto differentiation article](https://en.wikipedia.org/wiki/Automatic_differentiation)
* [Havard Berland's auto diff overview deck](http://www.robots.ox.ac.uk/~tvg/publications/talks/autodiff.pdf)
* [Auto differentiation blog post](http://www.columbia.edu/~ahd2125/post/2015/12/5/)
* [Rufflewind's reverse mode autodiff tutorial](https://rufflewind.com/2016-12-30/reverse-mode-automatic-differentiation)
