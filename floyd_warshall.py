'''Find shortest paths between all nodes of directed weighted multigraph with no negative cycles'''


import argparse
import csv
import math
import os.path
import time
from copy import deepcopy

import pygraphml

import floydwarshall


def get_weight(edge):
    return float(edge.attr['weight'].value)


def get_label(node):
    return node.attr['label'].value


def get_shortest_paths(adjacency_matrix):
    result = deepcopy(adjacency_matrix)
    for node_index in range(len(adjacency_matrix)):
        for node_from_index in range(len(adjacency_matrix)):
            for node_to_index in range(len(adjacency_matrix)):
                result[node_from_index][node_to_index] = min(
                    result[node_from_index][node_to_index],
                    result[node_from_index][node_index] + result[node_index][node_to_index],
                )
    return result

def main():
    # parse arguments of program
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '-f',
        '--file',
        help='graphml file of directed graph',
        metavar='FILE',
        required=True,
    )
    parser.add_argument(
        '-o',
        '--output',
        help='output csv file to write shortest paths between all nodes',
        metavar='OUTPUT',
    )
    arguments = parser.parse_args()

    # make filename of output csv file if is needed
    # if input graphml file was '<name>.graphml', the output csv file will be '<name>_paths.csv'
    if not arguments.output:
        arguments.output = '{}_paths.csv'.format(os.path.splitext(arguments.file)[0])

    # parse input graphml file and get the graph
    graph_parser = pygraphml.GraphMLParser()
    graph = graph_parser.parse(arguments.file)

    # make adjacency matrix of graph
    adjacency_matrix = [[math.inf for _ in range(len(graph._nodes))] for _ in range(len(graph._nodes))]
    for node_index in range(len(graph._nodes)):
        adjacency_matrix[node_index][node_index] = 0
    for edge in graph._edges:
        parent_index, child_index = graph._nodes.index(edge.parent()), graph._nodes.index(edge.child())
        if parent_index != child_index:
            adjacency_matrix[parent_index][child_index] = min(
                adjacency_matrix[parent_index][child_index],
                get_weight(edge),
            )

    # get shortest paths by python
    python_start = time.process_time()
    python_paths = get_shortest_paths(adjacency_matrix)
    python_end = time.process_time()
    python_time = python_end - python_start
    print("Python calculations time: {:.1f} sec".format(python_time))

    # get shortest paths by c++
    cxx_start = time.process_time()
    c_paths = floydwarshall.get_shortest_paths(adjacency_matrix)
    cxx_end = time.process_time()
    cxx_time = cxx_end - cxx_start
    print("Pure C++ calculations time: {:.1f} sec".format(cxx_time))
    
    # check results
    assert python_paths == c_paths

    # write result to csv file
    with open(arguments.output, 'w', newline='') as csvfile:
        paths_writer = csv.writer(csvfile, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
        paths_writer.writerow([''] + [get_label(node) for node in graph._nodes])
        for index, node in enumerate(graph._nodes):
           paths_writer.writerow([get_label(node)] + c_paths[index]) 

    
if __name__ == '__main__':
    main()