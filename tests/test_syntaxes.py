import sublime

import sublime
import sublime_plugin
import sublime_api

import os
from os import path
from unittest import TestCase

from JSCustom.src.build import build_configuration
from JSCustom.src.paths import resource_path, system_path, clean_tests, TEST_PATH

class TestSyntaxes(TestCase):
    def run_syntax_tests(self, tests):
        total_assertions = 0
        failed_assertions = 0

        for t in tests:
            assertions, test_output_lines = sublime_api.run_syntax_test(t)
            total_assertions += assertions
            if len(test_output_lines) > 0:
                failed_assertions += len(test_output_lines)
                for line in test_output_lines:
                    print(line)

        if failed_assertions > 0:
            self.fail('FAILED: {} of {} assertions in {} files failed'.format(failed_assertions, total_assertions, len(tests)))

        # print()

    def run_tests_for_configuration(self, name, configuration, tests):
        p = system_path(TEST_PATH, name)

        os.makedirs(p)

        build_configuration(name, configuration, p)

        syntax_path = resource_path(TEST_PATH, name, name+'.sublime-syntax')

        for test in tests:
            with open(system_path(TEST_PATH, name, test['filename']), 'w') as file:
                file.write('// SYNTAX TEST "%s"\n' % syntax_path)
                file.write(test['contents'])

        test_paths = [
            resource_path(TEST_PATH, name, test['filename'])
            for test in tests
        ]

        self.run_syntax_tests(test_paths)

    def test_syntaxes(self):
        clean_tests()

        cases = sublime.decode_value(sublime.load_resource('Packages/JSCustom/tests/tests.json'));

        syntax_tests = [
            {
                'filename': path.basename(file_path),
                'contents': sublime.load_resource(file_path),
                'suite': path.basename(path.dirname(file_path)),
            }
            for file_path in sublime.find_resources('syntax_test*')
            if file_path.startswith('Packages/JSCustom/tests')
        ]

        for name, case in cases.items():
            tests = [
                test
                for test in syntax_tests
                if test['suite'] in case['tests']
            ]

            self.run_tests_for_configuration(name, case['configuration'], tests)
