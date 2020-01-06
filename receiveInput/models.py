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
            while True:
                if line[0: (4 * need_indentation)] != tab * need_indentation:
                    need_indentation -= 1
                    self.output += f'{tab * need_indentation}' + '}\n'
                else:
                    break
            if need_indentation > 0:
                self.output += (tab * need_indentation)
            if 'append' in line or 'insert' in line or 'pop' in line or 'remove' in line:
                # print(str(need_to_import_array_list))
                # if need_to_import_array_list:
                #     self.output = 'import java.util.ArrayList;\n' + self.output
                #     need_to_import_array_list = False
                # print(output)
                self.output += lists(line)
                continue
            if '#' in line:
                self.output += comments(line)
                continue
            if "=" in line and "[" in line and ":" in line and "]" in line:
                self.output += substrings(line, self.declared_variables)
                continue
            if '+=' in line or '-=' in line or '/=' in line or '*=' in line:
                self.output += line.strip() + ';\n'
                continue
            if '=' in line and not '==' in line and not '<=' in line and not '>=' in line and not '<' in line and not '>' in line:
                self.output += declarations(self.output, line, self.declared_variables)
            if 'print' in line:
                self.output += translatePrint(line)
            # if "elif" in line:
            #     need_indentation += 1
            #     self.output += ifWhileStatements(line, self.declared_variables)
            if "if" in line:
                need_indentation += 1
                self.output += ifWhileStatements(line, self.declared_variables)
            if 'while' in line:
                need_indentation += 1
                self.output += ifWhileStatements(line, self.declared_variables)
            if 'else' in line:
                need_indentation += 1
                self.output += "else {\n"

            if need_indentation > 0 and split_lines[-1] == line:
                while True:
                    need_indentation -= 1
                    self.output += f'{tab * need_indentation}' + '}\n'
                    if need_indentation == 0:
                        break
