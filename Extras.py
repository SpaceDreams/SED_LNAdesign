"""
Created on Wed Jun  7 05:05:13 PM HST 2023

by: Charles White
My two main Methodologies are:
DRY code and KISS code:
DRY: Do not Repeat Yourself
KISS: Keep it Short and Simple
"""
from SLiCAP import *
### Function for converting schematic to a netlist and pdf to svg
def Cre8schAsvg4(fileName,title):
    makeNetlist(fileName + '.sch',title)
    #Add here convert pdf to svg
    Cre8svg4Pdf(fileName)
def Cre8svg4Pdf(fileName):
    #Add here convert pdf to svg
    os.system('pdf2svg '+ini.imgPath+fileName+'.pdf '+ini.imgPath+fileName+'.svg')

specFileName = "designData.csv"

def fullSubsRev(valExpr, parDefs):
    """
    Returns 'valExpr' after all parameters of 'parDefs' have been substituted
    into it recursively until no changes occur or until the maximum number of
    substitutions is achieved.

    The maximum number opf recursive substitutions is set by ini.maxRexSubst.

    :param valExpr: Eympy expression in which the parameters should be substituted.
    :type valExpr: sympy.Expr, sympy.Symbol, int, float

    :param parDefs: Dictionary with key-value pairs:

                    - key (*sympy.Symbol*): parameter name
                    - value (*sympy object, int, float*): value of the parameter

    :return: Expression or value obtained from recursive substitutions of
             parameter definitions into 'valExpr'.
    :rtype: sympy object, int, float
    """

    strValExpr = str(valExpr)
    i = 0
    newvalExpr = 0
    while valExpr != newvalExpr and i < ini.maxRecSubst and isinstance(valExpr, sp.Basic):
        # create a substitution dictionary with the smallest number of entries (this speeds up the substitution)
        substDict = {}
        params = list(valExpr.atoms(sp.Symbol))
        for param in params:
            if param.name in list(parDefs.keys()):
                if parDefs[param.name].minValue != '':
                    substDict[param] = parDefs[param.name].minValue
                elif parDefs[param.name].typValue != '':
                    substDict[param] = parDefs[param.name].typValue
                elif parDefs[param.name].maxValue != '':
                    substDict[param] = parDefs[param.name].maxValue
        # perform the substitution
        newvalExpr = valExpr
        valExpr = newvalExpr.xreplace(substDict)
        i += 1
    if i == ini.maxRecSubst:
        print("Warning: reached maximum number of substitutions for expression '{0}'".format(strValExpr))
    return valExpr
