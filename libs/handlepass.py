import re
class HandlePassword():

    def passwordstrength(self,password):

        length_error = len(password) < 8
        digit_error = re.search(r"\d", password) is None
        uppercase_error = re.search(r"[A-Z]", password) is None
        lowercase_error = re.search(r"[a-z]", password) is None
        symbol_error = re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~]", password) is None

        score = 0
        if not length_error:
            score += 1
        if not digit_error:
            score += 1
        if not uppercase_error:
            score += 1
        if not lowercase_error:
            score += 1
        if not symbol_error:
            score += 1

        if score == 5 and len(password) >= 12:
            return '5'
        elif score >= 4:
            return '4'
        elif score >= 3:
            return '3'
        elif score >= 2:
            return '2'
        else:
            return '1'
