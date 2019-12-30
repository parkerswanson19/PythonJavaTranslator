import re


def declarations(string, declared_variables):
    # grabs the variable name before the equal sign and strips unnecessary spaces
    var_name = string[0: string.index("=")].strip()
    # grabs the value after the equal sign and strips unnecessary spaces 
    value = string[string.index("=") + 1: len(string)].strip()

    if var_name in declared_variables.keys():
        return var_name + " = " + value + ";\n"

    # checks if the value is a string
    if '"' in value:
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

    # checks if the variable is a list
    if '[' in value and ']' in value:
        declared_variables[var_name] = 'array'
        first_element = value[1:value.index(',')]
        print('first element is: ' + str(first_element))
        new_string = f'None = {first_element}'
        type_of_array = declarations(new_string, {})
        type_of_array = type_of_array.split()[0]
        return f"{type_of_array}[] " + var_name + ' = ' + value + ";\n"

    # Checks if there's an operation on the right side of the equal sign
    if '+' in value or '-' in value or '*' in value or '/' in value or '%' in value:
        return operations(string, declared_variables)

    return "// Translation for this line isn't supported yet. \n"


def comments(string):
    string = string.strip()

    non_comment = string[0: string.index("#")]
    comment = string[string.index("#") + 1: len(string)]
    return non_comment + "//" + comment + ";\n"


# if x in hello or y in yes or y in hello
# if hello in object

def ifWhileStatements(string, declared_variables):
    #check if the statement is and if or a while
    if string[0:2] == "if":
        to_return = "if"
        string = string[string.index("if ") + 3:string.index(":")]
    else:
        to_return = "while"
        string = string[string.index("while ") + 6:string.index(":")]
    #check if there are parentheses in the string, and if there are, remove them
    string = string.replace("(", " ")
    string = string.replace(")", " ")
    #change the trues and falses to lowercases
    string = string.replace("True", "true")
    string = string.replace("False", "false")
    #split the string on every space
    string_split = string.split(" ")
    and_ors = []
    and_ors_index = 0
    #find all of the ors and ands in the statement
    for word in string_split:
        if word == "and":
            and_ors.append("&&")
        if word == "or":
            and_ors.append("||")
    separate = re.split(' and | or ', string)
    for statement in separate:
        print(statement)
        if " in " in statement:
            if and_ors_index != len(and_ors):
                to_return += " (" + statement + ") " + and_ors[and_ors_index]
            else:
                to_return += " (" + statement + ") "
        elif "<=" in statement or "==" in statement or ">=" in statement or ">" in statement or "<" in statement:
            original = statement
            split_statement = re.split('<=|<|>=|>|==', statement)
            try:
                split_statement[0] = int(split_statement[0].strip())
                if and_ors_index != len(and_ors):
                    to_return += " (" + original + ") " + and_ors[and_ors_index]
                else:
                    to_return += " (" + original + ") "
            except ValueError:
                try:
                    split_statement[0] = float(split_statement[0].strip())
                    if and_ors_index != len(and_ors):
                        to_return += " (" + original + ") " + and_ors[and_ors_index]
                    else:
                        to_return += " (" + original + ") "
                except ValueError:
                    for variable in split_statement:
                        variable = variable.strip()
                        if variable in declared_variables.keys():
                            if declared_variables[variable] == "int" or declared_variables[variable] == "boolean" or \
                                    declared_variables[variable] == "double":
                                if and_ors_index != len(and_ors):
                                    to_return += " (" + original + ") " + and_ors[and_ors_index]
                                    break
                                else:
                                    to_return += " (" + original + ") "
                                    break
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
        #increment the index of the and or array
        and_ors_index += 1

    #return the string output with a curly brace
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

    # print(declared_variables)
    # if all of the terms on the right side are ints, then make the left side an int too
    declared_variables[var_name] = 'int'
    return "int " + var_name + " = " + re.sub(r'\s+', ' ', right_side) + ";\n"
