#include <cmath>
#include <vector>

extern "C" {
#include <Python.h>
}

namespace utils {	
    typedef std::vector<double>  row_t;
    typedef std::vector<row_t>   matrix_t;

    static bool is_less(float first, float second, float epsilon=1e-8) {
        return (second - first) > epsilon;
    }

    static matrix_t get_shortest_paths(const matrix_t &adjacency_matrix) {
        matrix_t result(adjacency_matrix);
        for (size_t node_index = 0; node_index < adjacency_matrix.size(); ++node_index) {
            for (size_t node_from_index = 0; node_from_index < adjacency_matrix.size(); ++node_from_index) {
                for (size_t node_to_index = 0; node_to_index < adjacency_matrix.size(); ++node_to_index) {
                    double new_value = result[node_from_index][node_index] + result[node_index][node_to_index];
                    if (is_less(new_value, result[node_from_index][node_to_index])) {
                        result[node_from_index][node_to_index] = new_value;
                    }
                }
            }
        }
        return result;
    }
}

static utils::matrix_t pyobject_to_cxx(PyObject * py_matrix) {
    utils::matrix_t result;
    result.resize(PyObject_Length(py_matrix));
    for (size_t i=0; i<result.size(); ++i) {
        PyObject * py_row = PyList_GetItem(py_matrix, i);
        utils::row_t & row = result[i];
        row.resize(PyObject_Length(py_row));
        for (size_t j=0; j<row.size(); ++j) {
            PyObject * py_elem = PyList_GetItem(py_row, j);
            const double elem = PyFloat_AsDouble(py_elem);
            row[j] = elem;
        }
    }
    return result;
}

static PyObject * cxx_to_pyobject(const utils::matrix_t &matrix)
{
    PyObject * result = PyList_New(matrix.size());
    for (size_t i=0; i<matrix.size(); ++i) {
        const utils::row_t & row = matrix[i];
        PyObject * py_row = PyList_New(row.size());
        PyList_SetItem(result, i, py_row);
        for (size_t j=0; j<row.size(); ++j) {
            const double elem = row[j];
            PyObject * py_elem = PyFloat_FromDouble(elem);
            PyList_SetItem(py_row, j, py_elem);
        }
    }
    return result;
}

static PyObject * get_shortest_paths(PyObject * module, PyObject * args) {
    PyObject * py_adjacency_matrix = PyTuple_GetItem(args, 0);

    /* Convert to C++ structure */
    const utils::matrix_t adjacency_matrix = pyobject_to_cxx(py_adjacency_matrix);

    /* Perform calculations */
    const utils::matrix_t result = utils::get_shortest_paths(adjacency_matrix);

    /* Convert back to Python object */
    PyObject * py_result = cxx_to_pyobject(result);
    return py_result;
}

PyMODINIT_FUNC PyInit_floydwarshall() {
    static PyMethodDef ModuleMethods[] = {
        { "get_shortest_paths", get_shortest_paths, METH_VARARGS, "Find shortest paths between all nodes" },
        { NULL, NULL, 0, NULL }
    };
    static PyModuleDef ModuleDef = {
        PyModuleDef_HEAD_INIT,
        "floydwarshall",
        "Find shortest paths between all nodes",
        -1, ModuleMethods, 
        NULL, NULL, NULL, NULL
    };
    PyObject * module = PyModule_Create(&ModuleDef);
    return module;
}