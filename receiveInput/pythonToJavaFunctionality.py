import re


def declarations(output, string, declared_variables):
    # grabs the variable name before the equal sign and strips unnecessary spaces
    var_name = string[0: string.index("=")].strip()
    # grabs the value after the equal sign and strips unnecessary spaces
    value = string[string.index("=") + 1: len(string)].strip()

    # checks if the variable has already been declared
    if var_name in declared_variables.keys() and not declared_variables[var_name] == 'ArrayList':
        return var_name + " = " + value + ";\n"
        # checks if the variable is a list

    # checks if the variable is a tuple, comments are the same as checking for list
    if '(' in value and ')' in value:
        declared_variables[var_name] = 'final array'
        try:
            first_element = value[1:value.index(',')]
        except ValueError:
            first_element = value[1:value.index(']')]
        new_string = f'None = {first_element}'
        type_of_array = declarations(new_string, {})
        type_of_array = type_of_array.split()[0]
        return f"final {type_of_array}[] " + var_name + ' = ' + value + ";\n"

    # checks if the value is a string
    if '"' in value or '\'' in value and 'System.out.print' not in value:
        print('Value is: ' + value)
        declared_variables[var_name] = 'String'
        return "String " + var_name + ' = "' + value[1:-1] + '";\n'

    # checks if the value is an int
    try:
        value = int(value)
        # print('In declarations method: ' + str(value))
        declared_variables[var_name] = 'int'
        return "int " + var_name + " = " + str(value) + ";\n"
    except ValueError:
        # print("not an int")
        pass

    # checks if the value is a double/float
    try:
        value = float(value)
        # print('In declarations method: ' + str(value))
        declared_variables[var_name] = 'double'
        return "double " + var_name + " = " + str(value) + ";\n"
    except ValueError:
        # print("not an double")
        pass

    # checks if the value is a boolean
    if value == "True" or value == "False":
        declared_variables[var_name] = 'boolean'
        return "boolean " + var_name + " = " + value.lower() + ";\n"

    # Checks if there's an operation on the right side of the equal sign
    if '+' in value or '-' in value or '*' in value or '/' in value or '%' in value:
        return operations(string, declared_variables)

    return "// Translation for this line isn't supported yet. \n"


def listDeclarations(string, output, declared_variables):
    """This function is called when the variable name before the opening square bracket hasn't been declared."""

    # grabs the variable name before the equal sign and strips unnecessary spaces
    var_name = string[0: string.index("=")].strip()
    # grabs the value after the equal sign and strips unnecessary spaces
    value = string[string.index("=") + 1: len(string)].strip()
    #
    # # checks if the variable has already been declared
    # if var_name in declared_variables.keys() and not declared_variables[var_name] == 'ArrayList':
    #     return var_name + " = " + value + ";\n"

    # checks if the variable is a list
    output = 'import java.util.ArrayList;\n\n' + output

    list_of_values = value[1:-1].split(',')
    to_return = f"ArrayList " + var_name + ' = new ArrayList();\n'
    for value in list_of_values:
        value = value.strip()
        to_return += f'{var_name}.add({value});\n'

    return output + to_return


def comments(string):
    if string == '# Hit translate below!':
        return '// Paste this code in a Java main method and run it!'
    string = string.strip()

    non_comment = string[0: string.index("#")]
    comment = string[string.index("#") + 1: len(string)]
    return non_comment + "//" + comment + "\n"


def concatenations(string):
    string = string.strip()
    if "str(" in string:
        string = string.replace("str", "")


def tryExcept(string):
    # NullPointerException
    # NumberFormatException
    # IllegalStateException
    # NoSuchMethodException
    # ClassCastException
    # ParseException
    # InvocationTargetException
    common_exceptions = {"ValueError": "IllegalArgumentException", "RuntimeError": "RuntimeException",
                         "IndexError": "IndexOutOfBoundsException", "NameError": "NoSuchFieldException",
                         }
    output = ""
    if "raise " in string:
        message = ""
        output += "throw new "
        if "(" and ")" in string:
            message = string[string.index("("):string.index(")") + 1]
        split_string = string.split(" ")
        if split_string[1] in common_exceptions:
            output += common_exceptions[split_string[1]] + message
        else:
            output += "Exception" + message

        return output + ";"

    elif "try:" in string:
        return "try {\n"

    elif "except " in string:
        split_string = string.split(" ")
        output += "catch"
        if split_string[1] in common_exceptions:
            output += common_exceptions[split_string[1]] + "e"
        else:
            output += "Exception"

        return output + "{\n"




def forLoops(string, declared_variables):
    output = ""
    # Find whether the for loop is looping through an element(list/string) or through a range of numbers
    # See if “range(“ is in the line or not
    if "range(" not in string:
        # If element:
        # Convert to a for each loop in java
        # Use Object as the element type for the for each loop
        # for (Object a: list){
        output += "for (Object "
        name = string[string.index("for ") + 4:string.index(" in")]
        output += name + ": "
        iterable = string[string.index("in ") + 3: string.index(":")]
        print(iterable)
        if iterable in declared_variables:
            if declared_variables[iterable] == "String":
                output = "for (int i = 0; i < " + iterable + ".length(); i++) {\n"
                output += "    " + name + " = " + iterable + ".charAt(i);\n"
                declared_variables[name] = 'String'
                return output
            elif declared_variables[iterable] == "ArrayList":
                output += iterable + "){"
        else:
            return "LIST NOT DECLARED"
    else:
        starting = "0"
        end = "0"
        increment = "1"
        # If range of numbers:
        # Find out the range of numbers
        # If it’s range of numbers or if length of something
        # See if “len(“ is in the line
        # Find out if there is a multiplier
        # Convert to standard for loop in java
        name = string[string.index("for ") + 4:string.index(" in ")]
        output += "for(int " + name

        splitt = string[string.index("range(") + 6: string.index(":") - 1]
        splitt = splitt.split(",")
        len_range = len(splitt)

        if len_range == 3:
            for number in range(len(splitt)):
                if number == 0:
                    if "len(" in splitt[number]:
                        starting = length(splitt[number], declared_variables)
                    else:
                        starting = splitt[number]
                if number == 1:
                    if "len(" in splitt[number]:
                        print(splitt[number])
                        print(declared_variables)
                        end = length(splitt[number], declared_variables)
                    else:
                        end = splitt[number]
                if number == 2:
                    if "len(" in splitt[number]:
                        increment = length(splitt[number], declared_variables)
                    else:
                        increment = splitt[number]
        elif len_range == 2:
            for number in range(len(splitt)):
                if number == 0:
                    if "len(" in splitt[number]:
                        starting = length(splitt[number], declared_variables)
                    else:
                        starting = splitt[number]
                if number == 1:
                    if "len(" in splitt[number]:
                        end = length(splitt[number], declared_variables)
                    else:
                        end = splitt[number]
        else:
            if "len(" in splitt[0]:
                end = length(splitt[0], declared_variables)
            else:
                end = splitt[0]

        output += " = " + starting + "; "

        if "length" not in increment and "size" not in increment:
            if int(increment) <= 0:
                output += name + " > " + end + "; "
            else:
                output += name + " < " + end + "; "
        else:
            output += name + " < " + end + "; "

        output += name + " += " + increment + "){"


    return output + "\n"



def brackets(string, declared_variables, existing):
    output = ""
    # copy both sides of the equal signs
    first = string[0:string.index("=")].strip()
    second = string[string.index("=") + 1: len(string)].strip()
    # split the right side of the equal sign by every "+"
    second = second.split("+")

    # run through all the values that were split
    for var in second:
        var = var.strip()
        if "[" in var:
            name = var[0:var.index("[")]
            # check if the split values are already declared
            if name in declared_variables:
                # convert code to java if the element is a string
                if declared_variables[name] == "String":
                    var = var.replace("[", ".substring(")
                    var = var.replace(":", ",")
                    var = var.replace("]", ")")
                elif declared_variables[name] == "ArrayList":
                    if ":" in var:
                        return
                    var = var.replace("[", ".get(")
                    var = var.replace("]", ")")
                output += var + " + "
                if first not in declared_variables:
                    first = "String " + first
                    declared_variables[first] = "String"
                    output = first + " = " + output
            else:
                existing = listDeclarations(string, existing, declared_variables)
                if first not in declared_variables:
                    declared_variables[first] = "ArrayList"
                return existing

    return existing + output[0:-3] + ";"


# if hello in object

def ifWhileStatements(output, string, declared_variables):
    string = string.strip()
    # check if the statement is and if or a while
    if string[0:2] == "if":
        to_return = "if"
        string = string[string.index("if ") + 3:string.index(":")]
    elif string[0:5] == "while":
        to_return = "while"
        string = string[string.index("while ") + 6:string.index(":")]
    else:
        to_return = "else if"
        string = string[string.index("elif ") + 5:string.index(":")]
    # check if there are parentheses in the string, and if there are, remove them
    string = string.replace("(", " ")
    string = string.replace(")", " ")
    # change the trues and falses to lowercases
    string = string.replace("True", "true")
    string = string.replace("False", "false")
    if string.strip() == "true" or string.strip() == "false":
        return to_return + " (" + string + ") {\n"
    # split the string on every space
    string_split = string.split(" ")
    and_ors = []
    and_ors_index = 0
    # find all of the ors and ands in the statement
    for word in string_split:
        if word == "and":
            and_ors.append("&&")
        if word == "or":
            and_ors.append("||")
    # split the string on ands or ors
    separate = re.split(' and | or ', string)
    # loop through each statement that was split
    for statement in separate:
        # check if "in" is in the statement and handle it
        if " in " in statement:
            if and_ors_index != len(and_ors):
                to_return += " (" + "FEAUTURE NOT YET SUPPORTED" + ") " + and_ors[and_ors_index]
            else:
                to_return += " (" + "FEAUTURE NOT YET SUPPORTED" + ") "
        # check for every other possibility
        elif "<=" in statement or "==" in statement or ">=" in statement or ">" in statement or "<" in statement:
            original = statement
            split_statement = re.split('<=|<|>=|>|==', statement)
            # check if the left half of the equation is an int
            try:
                split_statement[0] = int(split_statement[0].strip())
                if and_ors_index != len(and_ors):
                    to_return += " (" + original + ") " + and_ors[and_ors_index]
                else:
                    to_return += " (" + original + ") "
            except ValueError:
                # check if the left half of the equation is a double/float
                try:
                    split_statement[0] = float(split_statement[0].strip())
                    if and_ors_index != len(and_ors):
                        to_return += " (" + original + ") " + and_ors[and_ors_index]
                    else:
                        to_return += " (" + original + ") "
                except ValueError:
                    for variable in split_statement:
                        variable = variable.strip()
                        # check if the left half is a declared variable that is a boolean, int, or double
                        if variable in declared_variables.keys():
                            if declared_variables[variable] == "int" or declared_variables[variable] == "boolean" or \
                                    declared_variables[variable] == "double":
                                if and_ors_index != len(and_ors):
                                    to_return += " (" + original + ") " + and_ors[and_ors_index]
                                    break
                                else:
                                    to_return += " (" + original + ") "
                                    break
                        # handle the left half it is a string
                        else:
                            if "<=" in original:
                                if and_ors_index != len(and_ors):
                                    to_return += " (" + split_statement[0] + ".compareTo(" + split_statement[
                                        1] + ") <= 0" + ") " + and_ors[and_ors_index]
                                    break
                                else:
                                    to_return += " (" + split_statement[0] + ".compareTo(" + split_statement[
                                        1] + ") <= 0" + ") "
                                    break
                            elif "<" in original:
                                if and_ors_index != len(and_ors):
                                    to_return += " (" + split_statement[0] + ".compareTo(" + split_statement[
                                        1] + ") < 0" + ") " + and_ors[and_ors_index]
                                    break
                                else:
                                    to_return += " (" + split_statement[0] + ".compareTo(" + split_statement[
                                        1] + ") < 0" + ") "
                                    break
                            elif ">=" in original:
                                if and_ors_index != len(and_ors):
                                    to_return += " (" + split_statement[0] + ".compareTo(" + split_statement[
                                        1] + ") >= 0" + ") " + and_ors[and_ors_index]
                                    break
                                else:
                                    to_return += " (" + split_statement[0] + ".compareTo(" + split_statement[
                                        1] + ") >= 0" + ") "
                                    break
                            elif ">" in original:
                                if and_ors_index != len(and_ors):
                                    to_return += " (" + split_statement[0] + ".compareTo(" + split_statement[
                                        1] + ") > 0" + ") " + and_ors[and_ors_index]
                                    break
                                else:
                                    to_return += " (" + split_statement[0] + ".compareTo(" + split_statement[
                                        1] + ") > 0" + ") "
                                    break
                            elif "==" in original:
                                if and_ors_index != len(and_ors):
                                    to_return += " (" + split_statement[0] + ".equals(" + split_statement[
                                        1] + ")" + ") " + and_ors[and_ors_index]
                                    break
                                else:
                                    to_return += " (" + split_statement[0] + ".equals(" + split_statement[
                                        1] + ")" + ") "
                                    break
        # increment the index of the and or array
        and_ors_index += 1

    # return the string output with a curly brace
    return to_return[: -1] + " {\n"


def userInput(string, output, declared_variables):
    # check if the import statement has already been implemented
    if "import java.util.Scanner" not in output:
        output = "import java.util.Scanner;\n\n" + output

    # check if a scanner object has been created already
    if "= new Scanner(System.in);" not in output:
        output += "Scanner std = new Scanner(System.in);\n"

    # check if the element has already been declared and add the std.nextLine() instead of input()
    first = string[0:string.index("=")].strip()
    if first in declared_variables:
        output += first + " = std.nextLine();"
    else:
        output += "String " + first + " = std.nextLine();"
        declared_variables[first] = "String"

    return output


def translatePrint(string, declared_variables):
    string = string.strip()
    if string[-7:-1] == "end=''":
        output = 'System.out.print('
        string = string[:-9] + '0'
    elif len(string) == 7:
        return 'System.out.println();\n'
    else:
        output = 'System.out.println('
    string = string[6:-1]  # Splice out all of the contents of the print statement
    items = string.split('+')

    for item in items:
        item = item.strip()
        if (item[0] == '"' and item[-1] == '"') or (item[0] == "'" and item[-1] == "'"):
            item = '"' + item[1:-1] + '"'
            output += item + ' + '
        elif item in declared_variables.keys() and declared_variables[item] != 'String':
            output += 'str(' + item + ') + '
        else:
            output += item + ' + '
    output = output[:-3] + ');\n'
    return output


# if string[0] == "'" or string[0] == '"':  # This is if we're printing a String
    #     output += start + '"' + string[7:-2] + '");\n'
    # else:  # This is if we're printing other things in the print statement
    #     output += start + string[6:-1] + ');\n'

def operations(string, declared_variables):
    """This method is used when there's an operation on the right side of the equation. It splits the right side of
    the equation by the five operators and checks whether each term is an int or float"""

    # grabs the variable name before the equal sign and strips unnecessary spaces
    var_name = string[0: string.index("=")].strip()
    # grabs the value after the equal sign and strips unnecessary spaces
    right_side = string[string.index("=") + 1: len(string)]
    # take out all excess white space from right side of equation
    value = re.sub(r'\s+', '', right_side)
    # split the right side of the equation by the 5 operators
    value = re.split('\+|\-|\*|\/|\%', value)
    # go through each of the terms on the right side and make sure that they're ints
    for val in value:
        try:
            if declared_variables[val] != 'int':  # if this throws an error, check if it's a literal int
                # Also, if the variable exists but isn't an int, throw an error to trigger except clause
                raise TypeError
        except:
            try:
                int(val)  # if this throws an error, then it's neither a primitive int or a literal int
            except:
                declared_variables[var_name] = 'double'
                return "double " + var_name + " = " + re.sub(r'\s+', ' ', right_side) + ";\n"
    # if all of the terms on the right side are ints, then make the left side an int too
    declared_variables[var_name] = 'int'
    return "int " + var_name + " = " + re.sub(r'\s+', ' ', right_side) + ";\n"


# For lists' append and remove functionality
def listOperations(string):
    name = string[:string.index('.')]
    item_to_append = string[string.index('(') + 1: string.index(')')]
    print(item_to_append)
    if item_to_append[0] == "'" and item_to_append[-1] == "'":
        item_to_append = '"' + item_to_append[1:-1] + '"'
    if 'append' in string or 'insert' in string:
        return name + '.add(' + item_to_append + ');\n'
    # if 'insert' in string:
    #     return name + '.add(' + item_to_append + ');'
    if 'pop' in string or 'remove' in string:
        return name + '.remove(' + item_to_append + ');\n'
    return "// There's been an error on this line with this translator."


def length(string, declared_variables):
    output = ""
    # grabs the variable name before the equal sign and strips unnecessary spaces
    if '=' in string:
        var_name = string[0: string.index("=")].strip()
        # grabs the value after the equal sign and strips unnecessary spaces
        right_side = string[string.index("=") + 1: len(string)]

        # This is if the variable on the left needs to be declared as an int
        if var_name in declared_variables.keys():
            output = ""
        else:
            output = "int "
            declared_variables[var_name] = 'int'
        # This determines the type of the variable in the len() function
        name = right_side[right_side.index('len(') + 4:right_side.index(')')]
        if name in declared_variables.keys():
            if declared_variables[name] == 'ArrayList':
                return output + var_name + ' = ' + name + '.size();\n'
            if declared_variables[name] == 'String':
                return output + var_name + ' = ' + name + '.length();\n'
        else:
            return '// The string needs to be assigned to a variable first'
    elif 'print' in string:
        first_part = string[:string.index('len(')]
        len_part = string[string.index('len(') + 4:string.index(')')]
        last_part = string[string.index(')') + 1:]
        if declared_variables[len_part] == 'ArrayList':
            return first_part + len_part + '.size()' + last_part
        if declared_variables[len_part] == 'String':
            return first_part + len_part + '.length()' + last_part
        return string
    else:
        len_part = string[string.index('len(') + 4:string.index(')')]
        if declared_variables[len_part] == 'ArrayList':
            return len_part + '.size()'
        if declared_variables[len_part] == 'String':
            return len_part + '.length()'


