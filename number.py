import math

# TODO
#
# 1. Move auto diff code into autodiff.py
# 2. Handle jacobians as well
# 3. Centralize finite diff code (into autodiff?)
# 4. Support for exp(Number) which means fixing pow's autodiff.  The full monty is
#   https://math.stackexchange.com/questions/210915/derivative-of-a-function-raised-to-the-power-of-x

class Number:
  opcount = 0

  def __init__(self, value):
    self.value = value
    self.parents = []
    self.children = []
    self.grad_value = None
  
  def _do_forward_autodiff(self):
    # Strictly speaking forward pass doesn't need caching since
    # we are executing in a non repetitive order
    if self.grad_value is None:
      Number.opcount += 1
      self.grad_value = 0
      for partial, parent in self.parents:
        self.grad_value += partial * parent._do_forward_autodiff()
    
    return self.grad_value
    
  def _do_reverse_autodiff(self):
    if self.grad_value is None:
      Number.opcount += 1
      self.grad_value = 0
      for partial, child in self.children:
        self.grad_value += partial * child._do_reverse_autodiff()
  
    return self.grad_value

  def _reset_grad(self):
    self.grad_value = None
    for partial, parent in self.parents:
      parent._reset_grad()
  
  def add(self, other):
    z = Number(self.value + other.value)
    z.parents.append((1.0, self))
    z.parents.append((1.0, other))
    self.children.append((1.0, z))
    other.children.append((1.0, z))
    return z

  def sub(self, other):
    z = Number(self.value - other.value)
    z.parents.append((1.0, self))
    z.parents.append((-1.0, other))
    self.children.append((1.0, z))
    other.children.append((-1.0, z))
    return z

  def mul(self, other):
    z = Number(self.value * other.value)
    z.parents.append((other.value, self))
    z.parents.append((self.value, other))
    self.children.append((other.value, z))
    other.children.append((self.value, z))
    return z
    
  def truediv(self, other):
    z = Number(self.value / other.value)
    partial_z_wrt_self = 1 / other.value
    partial_z_wrt_other = -self.value / other.value**2
    z.parents.append((partial_z_wrt_self, self))
    z.parents.append((partial_z_wrt_other, other))
    self.children.append((partial_z_wrt_self, z))
    other.children.append((partial_z_wrt_other, z))
    return z
    
  def pow(self, other, is_constant_exponent = True):
    z = Number(self.value ** other.value)

    # Attempt #1 - Didn't allow non constants (e.g. variables of interest)
    # in the exponent e.g. no e^x
    #partial_z_wrt_self = other.value * self.value ** (other.value - 1)
    #z.parents.append((partial_z_wrt_self, self))
    #self.children.append((partial_z_wrt_self, z))

    # Attempt #2
    # Reference material
    # https://github.com/JuliaDiff/ForwardDiff.jl/blob/master/src/dual.jl
    # https://math.stackexchange.com/questions/210915/derivative-of-a-function-raised-to-the-power-of-x
    partial_z_wrt_self = other.value * self.value ** (other.value - 1)
    # This is super hokey.
    if is_constant_exponent:
      partial_z_wrt_other = 1
    else:
      partial_z_wrt_other = z.value * math.log(self.value)
    
    z.parents.append((partial_z_wrt_self, self))
    z.parents.append((partial_z_wrt_other, other))
    self.children.append((partial_z_wrt_self, z))
    other.children.append((partial_z_wrt_other, z))
    
    return z
    
  def neg(self):
    z = Number(-self.value)
    z.parents.append((-1.0, self))
    self.children.append((-1.0, z))
    return z
    
  def abs(self):
    return self if self.value >= 0 else self.neg()
    
  def __add__(self, other):
    other = other if isinstance(other, Number) else Number(other)
    return self.add(other)

  def __radd__(self, other):
    other = other if isinstance(other, Number) else Number(other)
    return other.add(self)

  def __sub__(self, other):
    other = other if isinstance(other, Number) else Number(other)
    return self.sub(other)

  def __rsub__(self, other):
    other = other if isinstance(other, Number) else Number(other)
    return other.sub(self)

  def __mul__(self, other):
    other = other if isinstance(other, Number) else Number(other)
    return self.mul(other)

  def __rmul__(self, other):
    other = other if isinstance(other, Number) else Number(other)
    return other.mul(self)

  def __truediv__(self, other):
    other = other if isinstance(other, Number) else Number(other)
    return self.truediv(other)

  def __rtruediv__(self, other):
    other = other if isinstance(other, Number) else Number(other)
    return other.truediv(self)

  def __pow__(self, other):
    other = other if isinstance(other, Number) else Number(other)
    return self.pow(other)

  def __rpow__(self, other):
    other = other if isinstance(other, Number) else Number(other)
    return other.pow(self, False)

  def __neg__(self):
    return self.neg()
  
  def __abs__(self):
    return self.abs()

  def __eq__(self, other):
    return self.value == other.value
  
  def __lt__(self, other):
    other = other.value if isinstance(other, Number) else other
    return self.value < other
      
  def __le__(self, other):
    other = other.value if isinstance(other, Number) else other
    return self.value <= other
  
  def __gt__(self, other):
    other = other.value if isinstance(other, Number) else other
    return self.value > other
      
  def __ge__(self, other):
    other = other.value if isinstance(other, Number) else other
    return self.value >= other
      
  def __str__(self):
    return str(self.value) + 'n'
