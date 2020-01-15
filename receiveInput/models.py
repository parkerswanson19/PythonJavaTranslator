from django.db import models
from django.db.models import TextField

from .pythonToJavaFunctionality import *


# This is a model for the inputted code, it has an input and output field
class InputtedCode(models.Model):
    input = models.TextField()
    output = models.TextField()
    declared_variables = {}  # declared variables

    # This method takes the input and translates it, then assigns that result to the output field
    def translate(self):
        self.declared_variables = {}
        split_lines = TextField.to_python(self.input, self.input).splitlines()
        output = TextField.to_python(self.output, self.output)
        need_indentation = 0  # is the initial state, no loops have come by so we don't need a }
        # 0 means to add a curly brace and no longer need to indent # 1 or more means need to indent that many times
        need_to_import_array_list = True
        for line in split_lines:
            tab = ' ' * 4
            try:
                while True:
                    if line[0: (4 * need_indentation)] != tab * need_indentation:
                        need_indentation -= 1
                        self.output += f'{tab * need_indentation}' + '}\n'
                    else:
                        break
                unaltered_copy = line
                if need_indentation > 0:
                    self.output += (tab * need_indentation)
                if 'print' in line and '#' not in line:
                    # Just making sure the print line wasn't commented out, this may need to be removed
                    line = translatePrint(line, self.declared_variables)
                if 'append' in line or 'insert' in line or 'pop' in line or 'remove' in line:
                    self.output += listOperations(line, self.declared_variables)
                    continue
                if "for " in line:
                    need_indentation += 1
                    self.output += forLoops(line, self.declared_variables)
                    continue
                if 'len' in line:
                    self.output += length(line, self.declared_variables)
                    continue
                if 'try:' in line:
                    need_indentation += 1
                    self.output = tryExcept(line, self.output)
                if 'except ' in line:
                    need_indentation += 1
                    self.output = tryExcept(line, self.output)
                if "raise " in line:
                    self.output = tryExcept(line, self.output)
                if '#' in line:
                    self.output += comments(line)
                    continue
                if "=" in line and "[" in line and "]" in line:
                    self.output = brackets(line, self.declared_variables, self.output)
                    continue
                if "input(" in line:
                    self.output = userInput(line, self.output, self.declared_variables)
                    continue
                if '+=' in line or '-=' in line or '/=' in line or '*=' in line:
                    self.output += line.strip() + ';\n'
                if '=' in line and not '==' in line and not '<=' in line and not '>=' in line and not '<' in line and not \
                        '>' in line and not '+=' in line and not '-=' in line and not '/=' in line and not '*=' in line:
                    self.output += declarations(self.output, line, self.declared_variables)
                if "if" in line:
                    need_indentation += 1
                    self.output = ifWhileStatements(self.output, line, self.declared_variables)
                if 'while' in line:
                    need_indentation += 1
                    self.output = ifWhileStatements(self.output, line, self.declared_variables)
                if 'else' in line and not 'if' in line:
                    need_indentation += 1
                    self.output = self.output.strip() + " else {\n"
                # This line is necessary if there's only a string in the print statement that didn't need any further
                # processing, meaning there are no string concatenation going on
                if 'System.out.print' in line:
                    self.output += line
                if need_indentation > 0 and unaltered_copy == split_lines[-1]:
                    while True:
                        need_indentation -= 1
                        self.output += f'{tab * need_indentation}' + '}\n'
                        if need_indentation == 0:
                            break
            except:
                self.output += "// There's been an error with this line. Check for typos.\n"
