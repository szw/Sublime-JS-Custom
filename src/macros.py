import sublime

from yamlmacros.lib.extend import apply
from yamlmacros.lib.syntax import rule as _rule

from yamlmacros.lib.include import include_resource

from yamlmacros import process_macros
from yamlmacros.src.util import merge

import sublime
from os import path

def foo(resource, arguments):
    return process_macros(
        sublime.load_resource(resource),
        arguments=merge(arguments, { "file_path": resource }),
    )

def get_extensions(node, loader, **rest):
    arguments = loader.context
    return [
        foo(file_path, arguments)
        for file_path in sublime.find_resources('*.yaml')
        if path.dirname(file_path).endswith('Packages/JSCustom/extensions')
        and arguments.get(path.splitext(path.basename(file_path))[0], None)
    ]

get_extensions.raw = True
