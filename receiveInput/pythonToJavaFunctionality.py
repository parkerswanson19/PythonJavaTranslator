import re
# from .models import InputtedCode


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

    # Checks if there's an operation on the right side of the equal sign
    if '+' in value or '-' in value or '*' in value or '/' in value or '%' in value:
        return operations(string, declared_variables)

    return "// Translation for this line isn't supported yet. \n"


def comments(string):
    if "#" not in string:
        return "No comment found"
    string = string.strip()

    non_comment = string[0: string.index("#")]
    comment = string[string.index("#") + 1: len(string)]
    return non_comment + "//" + comment + ";\n"

# if x in hello or y in yes or y in hello
#if hello in object

def ifWhileStatements(string, declared_variables):
    if string[0:2] == "if":
        toReturn = "if"
        string = string[string.index("if ") + 3:string.index(":")]
    else:
        toReturn = "while"
        string = string[string.index("while ") + 3:string.index(":")]
    string = string.replace("(", " ")
    string = string.replace(")", " ")
    string = string.replace("True", "true")
    string = string.replace("False", "false")
    stringSplit = string.split(" ")
    andOrs = []
    andOrsIndex = 0
    for word in stringSplit:
        if word == "and":
            andOrs.append("&&")
        if word == "or":
            andOrs.append("||")

    string = string.replace(" and ", " ---- ")
    string = string.replace(" or ", " ---- ")

    separate = string.split(" ---- ")
    for statement in separate:
        print(statement)
        if " in " in statement:
            if andOrsIndex != len(andOrs):
                toReturn += " (" + statement + ") " + andOrs[andOrsIndex]
            else:
                toReturn += " (" + statement + ") "
        elif "<=" in statement or "=="  in statement or ">=" in statement or ">" in statement or "<" in statement:
            original = statement
            statement  = statement.replace("<=", "+++++")
            statement = statement.replace("<", "+++++")
            statement = statement.replace(">=", "+++++")
            statement = statement.replace(">", "+++++")
            statement = statement.replace("==", "+++++")
            split_statement = statement.split("+++++")
            try:
                split_statement[0] = int(split_statement[0].strip())
                if andOrsIndex != len(andOrs):
                    toReturn += " (" + original + ") " + andOrs[andOrsIndex]
                else:
                    toReturn += " (" + original + ") "
            except ValueError:
                try:
                    split_statement[0] = float(split_statement[0].strip())
                    if andOrsIndex != len(andOrs):
                        toReturn += " (" + original + ") " + andOrs[andOrsIndex]
                    else:
                        toReturn += " (" + original + ") "
                except ValueError:
                    for variable in split_statement:
                        variable = variable.strip()
                        if variable in declared_variables.keys():
                            if declared_variables[variable] == "int" or declared_variables[variable] == "boolean" or declared_variables[variable] == "double":
                                if andOrsIndex != len(andOrs):
                                    toReturn += " (" + original + ") " + andOrs[andOrsIndex]
                                    break
                                else:
                                    toReturn += " (" + original + ") "
                                    break
                        else:
                            if "<=" in original:
                                if andOrsIndex != len(andOrs):
                                    toReturn += " (" + split_statement[0] + ".compareTo(" + split_statement[1] + ") <= 0" + ") " + andOrs[andOrsIndex]
                                    break
                                else:
                                    toReturn += " (" + split_statement[0] + ".compareTo(" + split_statement[1] + ") <= 0" + ") "
                                    break
                            elif "<" in original:
                                if andOrsIndex != len(andOrs):
                                    toReturn += " (" + split_statement[0] + ".compareTo(" + split_statement[1] + ") < 0" + ") " + andOrs[andOrsIndex]
                                    break
                                else:
                                    toReturn += " (" + split_statement[0] + ".compareTo(" + split_statement[1] + ") < 0" + ") "
                                    break
                            elif ">=" in original:
                                if andOrsIndex != len(andOrs):
                                    toReturn += " (" + split_statement[0] + ".compareTo(" + split_statement[1] + ") >= 0" + ") " + andOrs[andOrsIndex]
                                    break
                                else:
                                    toReturn += " (" + split_statement[0] + ".compareTo(" + split_statement[1] + ") >= 0" + ") "
                                    break
                            elif ">" in original:
                                if andOrsIndex != len(andOrs):
                                    toReturn += " (" + split_statement[0] + ".compareTo(" + split_statement[1] + ") > 0" + ") " + andOrs[andOrsIndex]
                                    break
                                else:
                                    toReturn += " (" + split_statement[0] + ".compareTo(" + split_statement[1] + ") > 0" + ") "
                                    break
                            elif "==" in original:
                                if andOrsIndex != len(andOrs):
                                    toReturn += " (" + split_statement[0] + ".equals(" + split_statement[1] + ")" + ") " + andOrs[andOrsIndex]
                                    break
                                else:
                                    toReturn += " (" + split_statement[0] + ".equals(" + split_statement[1] + ")" + ") "
                                    break




        andOrsIndex += 1

    return toReturn[: -1] + "{\n"


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


def whileLoops(string):
    string = string.strip()
    string = string.replace('True', 'true')
    string = string.replace('False', 'false')

    output = 'while (' + string[6: -1] + ') {\n'
    return output
