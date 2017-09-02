import ast

import translator


def h_arg(node, indent):
    return translator.get(node.arg)


def h_arguments(node, indent):
    arg_elements = []

    for arg in node.args[:(-len(node.defaults) or None)]:
        arg_elements.append(minify_node(arg))

    for arg, default in zip(node.args[-len(node.defaults):], node.defaults):
        arg_elements.append(f'{minify_node(arg)}={minify_node(default)}')

    if node.vararg:
        arg_elements.append(f'*{minify_node(node.vararg)}')

    for arg, default in zip(node.kwonlyargs, node.kw_defaults):
        arg_elements.append(f'{minify_node(arg)}={minify_node(default)}')

    if node.kwarg:
        arg_elements.append(f'**{minify_node(node.kwarg)}')

    return ','.join(arg_elements)


def h_assign(node, indent):
    return '{}={}'.format(
        minify_nodes(node.targets),
        minify_node(node.value)
    )


def h_call(node, indent):
    return '{}({})'.format(
        minify_node(node.func),
        minify_nodes(node.args)
    )


def h_expr(node, indent):
    return minify_node(node.value)


def h_lambda(node, indent):
    args = minify_node(node.args)
    body = minify_node(node.body)
    if args:
        return f'lambda {args}: {body}'
    else:
        return f'lambda: {body}'


def h_module(node, indent):
    return minify_nodes(node.body, separator='\n')


def h_name(node, indent):
    if node.id in __builtins__:
        return node.id
    return translator.get(node.id)


def h_num(node, indent):
    return str(node.n)


def h_str(node, indent):
    return repr(node.s)


def h_tuple(node, indent):
    return '({})'.format(minify_nodes(node.elts))


NODE_CLASS_TO_HANDLER = {
    ast.arg: h_arg,
    ast.arguments: h_arguments,
    ast.Assign: h_assign,
    ast.Call: h_call,
    ast.Expr: h_expr,
    ast.Lambda: h_lambda,
    ast.Module: h_module,
    ast.Name: h_name,
    ast.Num: h_num,
    ast.Str: h_str,
    ast.Tuple: h_tuple,
}


def minify_node(node, indent=0):
    handler = NODE_CLASS_TO_HANDLER.get(node.__class__)
    if handler is None:
        raise ValueError(node)
    minified_node = handler(node, indent=indent)
    output = '{}{}'.format(' ' * indent, minified_node)
    return output


def minify_nodes(nodes, separator=','):
    return separator.join(minify_node(node) for node in nodes)

