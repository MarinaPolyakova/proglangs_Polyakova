import random


NODES_COUNT = 300
EDGES_COUNT = 5000
GRAPH_FILENAME = 'my_big_graph.graphml'
WEIGHT_MAX = 50


def main():
    with open(GRAPH_FILENAME, 'w') as graphml_file:
        graphml_file.write(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<graphml xmlns="http://graphml.graphdrawing.org/xmlns"\n'  
            '    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n'
            '    xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns\n'
            '     http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">\n'
            '  <key id="weight" for="edge" attr.name="weight" attr.type="double"/>\n'
            '  <graph id="G" edgedefault="directed">\n'
        )

        # write nodes
        for node_index in range(NODES_COUNT):
             graphml_file.write('    <node id="n{}"/>\n'.format(node_index))

        # write edges
        random.seed(293)
        for _ in range(EDGES_COUNT):
            node_from_index, node_to_index = random.randint(0, NODES_COUNT - 1), random.randint(0, NODES_COUNT - 1)
            weight = random.random() * WEIGHT_MAX
            graphml_file.write('    <edge source="n{}" target="n{}">\n'.format(node_from_index, node_to_index))
            graphml_file.write('      <data key="weight">{}</data>\n'.format(weight))
            graphml_file.write('    </edge>\n')

        graphml_file.write(
            '  </graph>\n'
            '</graphml>'
        )


if __name__ == '__main__':
    main()