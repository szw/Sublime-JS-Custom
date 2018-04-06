import sublime

from unittest import TestCase

class TestJsxCloseTag(TestCase):

    def setUp(self):
        self.view = sublime.active_window().new_file()
        self.view.set_syntax_file('Packages/User/JS Custom/Tests/jsx/jsx.sublime-syntax')

    def tearDown(self):
        if self.view:
            self.view.set_scratch(True)
            self.view.window().focus_view(self.view)
            self.view.window().run_command("close_file")

    def _test_close_tag(self, before, after):
        self.view.run_command('insert', { 'characters': before })
        self.view.run_command('jsx_close_tag')
        result = self.view.substr(sublime.Region(0, self.view.size()))
        self.assertEqual(result, after)

    def test_1(self):
        self._test_close_tag('<foo>', '<foo></foo>')

    def test_2(self):
        self._test_close_tag('<foo>text', '<foo>text</foo>')

    def test_3(self):
        self._test_close_tag('<>text', '<>text</>')

    def test_4(self):
        self._test_close_tag('<foo.bar>text', '<foo.bar>text</foo.bar>')

    def test_5(self):
        self._test_close_tag('<foo><bar>text', '<foo><bar>text</bar>')

    def test_6(self):
        self._test_close_tag('<foo><bar>text</bar>', '<foo><bar>text</bar></foo>')

    def test_7(self):
        self._test_close_tag('<foo><bar/>text', '<foo><bar/>text</foo>')

    # def test_8(self):
    #     self._test_close_tag('<foo att=<xyzzy/>>text', '<foo att=<xyzzy/>>text</foo>')
