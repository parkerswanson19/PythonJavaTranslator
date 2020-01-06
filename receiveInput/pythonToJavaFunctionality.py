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

    if '[' in value and ']' in value and not ':' in value:
        if not 'ArrayList' in declared_variables.values():
            output = 'import java.util.ArrayList;\n\n' + output
        declared_variables[var_name] = 'ArrayList'

        # # grabs the first element in the array and checks its type
        # try:
        #     # if there are no commas in the value string, then there's only one element in the array
        #     first_element = value[1:value.index(',')]
        # except ValueError:
        #     # a ValueError will be raised if no commas are found
        #     first_element = value[1:value.index(']')]
        # new_string = f'None = {first_element}'  # Need to find the type of variables the list is holding
        # type_of_array = declarations(new_string, {})  # recursively call this function
        # type_of_array = type_of_array.split()[0]  # splice the variable type and store it

        list_of_values = value[1:-1].split(',')
        to_return = f"ArrayList " + var_name + ' = new ArrayList();\n'
        for value in list_of_values:
            value = value.strip()
            to_return += f'{var_name}.add({value});\n'

        return to_return

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
    if '"' in value or '\'' in value:
        declared_variables[var_name] = 'String'
        return "String " + var_name + " = " + value + ";\n"

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


def comments(string):
    string = string.strip()

    non_comment = string[0: string.index("#")]
    comment = string[string.index("#") + 1: len(string)]
    return non_comment + "//" + comment + "\n"


def concatenations(string):
    string = string.strip()
    if "str(" in string:
        string = string.replace("str", "")


def substrings(string, declared_variables):
    output = ""
    first = string[0:string.index("=")].strip()
    second = string[string.index("=") + 1: len(string)].strip()
    second = second.split("+")

    if first not in declared_variables:
        first = "String " + first

    output += first + " = "

    for var in second:
        var = var.strip()
        if "[" in var:
            name = var[0:var.index("[")]
            print(name)
            if name in declared_variables:
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


    return output[0:-3] + ";"

# if hello in object

def ifWhileStatements(string, declared_variables):
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


def translatePrint(string):
    output = ""
    string = string.strip()
    start = 'System.out.println('
    if string[0:5] == 'print':
        if string[6] == "'" or string[6] == '"':  # This is if we're printing a String
            output += start + '"' + string[7:-2] + '");\n'
        else:  # This is if we're printing other things in the print statement
            output += start + string[6:-1] + ');\n'
    return output


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
def lists(string):
    name = string[:string.index('.')]
    item_to_append = string[string.index('(') + 1: string.index(')')]
    if 'append' in string or 'insert' in string:
        return name + '.add(' + item_to_append + ');\n'
    # if 'insert' in string:
    #     return name + '.add(' + item_to_append + ');'
    if 'pop' in string or 'remove':
        return 'Object ' + name + '.remove(' + item_to_append + ');\n'
    return "// There's been an error on this line with this translator."


def length(string, declared_variables):
    # grabs the variable name before the equal sign and strips unnecessary spaces
    var_name = string[0: string.index("=")].strip()
    # grabs the value after the equal sign and strips unnecessary spaces
    right_side = string[string.index("=") + 1: len(string)]

    # This is if the variable on the left needs to be declared as an int
    if var_name in declared_variables.keys():
        output = ""
    else:
        output = "int "
        declared_variables[var_name] = 'int'
    name = right_side[right_side.index('(') + 1:right_side.index(')')]
    if name in declared_variables.keys():
        return output + var_name + ' = ' + name + '.length();\n'
