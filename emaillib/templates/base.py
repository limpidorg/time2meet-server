# TEMPLATE

from sendgrid.helpers.mail.email import Email


class EmailTemplate:
    def __init__(self) -> None:
        'Additional settings, getting inputs while initialising & determining GetRequiredArguments and GetOptionalArguments'
        raise Exception("Not Implemented")

    def _GenerateEmail(self, **keywords) -> str:
        'Internal Method - called by Generate(). Generates the email here by reading input keywords'
        raise Exception("Not Implemented")

    def GetRequiredArguments(self) -> list:
        'Returns a list of arguments that are required.'
        raise Exception("Not Implemented")
    
    def GetOptionalArguments(self) -> list:
        'Returns a list of optional arguments.'
        raise Exception("Not Implemented")
    
    def Generate(self, **keywords) -> str:
        'External function. Do not override this function if unneccessary.'
        for key in self.GetRequiredArguments():
            if key not in keywords:
                raise KeyError(f"Email generation failure: Non-optional key {key} was not found.")
        return self._GenerateEmail(**keywords)

    @staticmethod
    def KeywordSubstitution(text: str, **keywords) -> str:
        '''
        Substitutes keywords within text with a given value, defined within **keywords.
        All input values will be casted as string.
        
        The keyword must be in the format of {{key}}.

        For example, KeywordSubstitution("Hello {{world}}", world="developer") ==> Hello developer
        '''
        for word in keywords:
            text = text.replace(f"{{{{{word}}}}}", keywords[word])
        
        return text
