import sublime, sublime_plugin, re

class SimplestDebuggerCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    selections = []
    for region in self.view.sel():
      if region.empty():
        line = self.view.line(region)
        content = re.compile("([\s\t]*)(.*)[\s\t]*").split(self.view.substr(line))
        if content[2] == 'debugger;':
          # remove debugger line
          # taken from "delete line" macros
          self.view.run_command("expand_selection", {"to": 'line'})
          self.view.run_command("add_to_kill_ring", {"forward": 'true'})
          self.view.run_command("left_delete")
        else:
          # add debugger line
          self.view.insert(edit, line.begin(), content[1]+'debugger;\n')
        # save start of debugger line for later selections
        point = line.begin() + content[1].__len__()
        selections.append(sublime.Region(point, point))
    # set selections to start of lines
    self.view.sel().clear()
    for sel in selections:
      self.view.sel().add(sel)
