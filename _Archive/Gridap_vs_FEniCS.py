from dolfinx import *
from ufl import (FacetNormal, Measure, SpatialCoordinate, TestFunction, TrialFunction, 
                 div, dot, dx, grad, inner, lhs, rhs, system)

import numpy as np
import time
from mpi4py import MPI
from dolfinx.mesh import * 
from dolfinx.fem import *
from dolfinx.fem import Expression, FunctionSpace, Function, Constant, DirichletBC
from dolfinx.fem.petsc import LinearProblem
from dolfinx.io import VTKFile

start = time.time()

n = 1000
domain = mesh.create_unit_square(comm=MPI.COMM_WORLD, nx=n, ny=n)

tdim = domain.topology.dim
fdim = tdim - 1
domain.topology.create_connectivity(fdim, tdim)
boundary_facets = mesh.exterior_facet_indices(domain.topology)

V = fem.functionspace(domain, ("Lagrange", 1))
uD = fem.Function(V)

boundary_dofs = fem.locate_dofs_topological(V, fdim, boundary_facets)
bc = fem.dirichletbc(uD, boundary_dofs)


class Source(Expression):
    def eval(self, values, x):
        values[0] = np.sin(np.pi * x[0]) * np.sin(np.pi * x[1])
        
    def value_shape(self):
        return ()
f = Source(degree=2)

u = TrialFunction(V)
v = TestFunction(V)
a = dot(grad(u), grad(v)) * dx
L = f * v * dx

u_h = Function(V)
LinearProblem.solve(a == L, u_h, bc)

vtkfile = VTKFile("poisson_unitsquare.pvd")
vtkfile << u_h

end = time.time()
print(f"Execution time: {end - start:.4f} seconds")