from datetime import datetime

import ply.lex as lex

from .constants import *

class XmlLexer:
    def __init__(self):
        self._lexer = _Lexer()
        self._ply_lexer = self._lexer.build()
        self.tokens = self._lexer.tokens

    def __getattr__(self, name):
        return getattr(self._ply_lexer, name)

    def input(self, data):
        """Wrapper method for providing input to the lexer."""
        self._ply_lexer.input(data)

    def token(self):
        """Wrapper method to get the next token."""
        return self._ply_lexer.token()

class _Lexer:
    tokens = [
        'StartTagClose',
        'XmlDeclStartTag',
        'XmlDeclEndTag',
        'DocTypeDeclStartTag',
        'HealthTopicsStartTagOpen',
        'HealthTopicsEndTag',
        'HealthTopicStartTagOpen',
        'HealthTopicEndTag',
        'AlsoCalledStartTagOpen',
        'AlsoCalledEndTag',
        'FullSummaryStartTagOpen',
        'FullSummaryEndTag',
        'GroupStartTagOpen',
        'GroupEndTag',
        'LanguageMappedTopicStartTagOpen',
        'LanguageMappedTopicEndTag',
        'MeshHeadingStartTagOpen',
        'MeshHeadingEndTag',
        'DescriptorStartTagOpen',
        'DescriptorEndTag',
        'QualifierStartTagOpen',
        'QualifierEndTag',
        'OtherLanguageStartTagOpen',
        'OtherLanguageEndTag',
        'PrimaryInstituteStartTagOpen',
        'PrimaryInstituteEndTag',
        'SeeReferenceStartTagOpen',
        'SeeReferenceEndTag',
        'SiteStartTagOpen',
        'SiteEndTag',
        'InformationCategoryStartTagOpen',
        'InformationCategoryEndTag',
        'OrganizationStartTagOpen',
        'OrganizationEndTag',
        'StandardDescriptionStartTagOpen',
        'StandardDescriptionEndTag',
        'RelatedTopicStartTagOpen',
        'RelatedTopicEndTag',
        'DocTypeDeclName',
        'DocTypeDeclExternalId',
        'VersionKey',
        'EncodingKey',
        'DateGeneratedKey',
        'TotalKey',
        'IdKey',
        'DateCreatedKey',
        'LanguageKey',
        'TitleKey',
        'UrlKey',
        'MetaDescKey',
        'VernacularNameKey',
        'LanguageMappedUrlKey',
        'Timestamp',
        'Integer',
        'Date',
        'Language',
        'Uri',
        'String',
        'Line'
    ]

    # Regular expression rules for simple tokens
    t_HealthTopicsStartTagOpen = rf'<{HEALTH_TOPICS}'
    t_HealthTopicsEndTag = rf'</{HEALTH_TOPICS}>'
    t_HealthTopicStartTagOpen = rf'<{HEALTH_TOPIC}'
    t_HealthTopicEndTag = rf'</{HEALTH_TOPIC}>'
    t_AlsoCalledStartTagOpen = rf'<{ALSO_CALLED}'
    t_AlsoCalledEndTag = rf'</{ALSO_CALLED}>'
    t_FullSummaryStartTagOpen = rf'<{FULL_SUMMARY}'
    t_FullSummaryEndTag = rf'</{FULL_SUMMARY}>'
    t_GroupStartTagOpen = rf'<{GROUP}'
    t_GroupEndTag = rf'</{GROUP}>'
    t_LanguageMappedTopicStartTagOpen = rf'<{LANGUAGE_MAPPED_TOPIC}'
    t_LanguageMappedTopicEndTag = rf'</{LANGUAGE_MAPPED_TOPIC}>'
    t_MeshHeadingStartTagOpen = rf'<{MESH_HEADING}'
    t_MeshHeadingEndTag = rf'</{MESH_HEADING}>'
    t_DescriptorStartTagOpen = rf'<{DESCRIPTOR}'
    t_DescriptorEndTag = rf'</{DESCRIPTOR}>'
    t_QualifierStartTagOpen = rf'<{QUALIFIER}'
    t_QualifierEndTag = rf'</{QUALIFIER}>'
    t_OtherLanguageStartTagOpen = rf'<{OTHER_LANGUAGE}'
    t_OtherLanguageEndTag = rf'</{OTHER_LANGUAGE}>'
    t_PrimaryInstituteStartTagOpen = rf'<{PRIMARY_INSTITUTE}'
    t_PrimaryInstituteEndTag = rf'</{PRIMARY_INSTITUTE}>'
    t_SeeReferenceStartTagOpen = rf'<{SEE_REFERENCE}'
    t_SeeReferenceEndTag = rf'</{SEE_REFERENCE}>'
    t_SiteStartTagOpen = rf'<{SITE}'
    t_SiteEndTag = rf'</{SITE}>'
    t_InformationCategoryStartTagOpen = rf'<{INFORMATION_CATEGORY}'
    t_InformationCategoryEndTag = rf'</{INFORMATION_CATEGORY}>'
    t_OrganizationStartTagOpen = rf'<{ORGANIZATION}'
    t_OrganizationEndTag = rf'</{ORGANIZATION}>'
    t_StandardDescriptionStartTagOpen = rf'<{STANDARD_DESCRIPTION}'
    t_StandardDescriptionEndTag = rf'</{STANDARD_DESCRIPTION}>'
    t_RelatedTopicStartTagOpen = rf'<{RELATED_TOPIC}'
    t_RelatedTopicEndTag = rf'</{RELATED_TOPIC}>'

    # A string containing ignored characters (spaces and tabs)
    t_ignore = ' \t'

    _entity_replacements = {
        '&amp;': '&',
        '&quot;': '"',
        '&#39;': "'",
        '&lt;': '<',
        '&gt;': '>',
        '&apos;': "'"
    }

    # Prolog tags
    def __init__(self):
        self._lexer = None

    def t_XmlDeclStartTag(self, t):
        r'<\?xml'
        return t

    def t_XmlDeclEndTag(self, t):
        r'\?>'
        return t

    def t_StartTagClose(self, t):
        r'>'
        return t

    def t_DocTypeDeclStartTag(self, t):
        r'<!DOCTYPE'
        return t

    def t_DocTypeDeclName(self, t):
        r' health-topics'
        return t

    def t_DocTypeDeclExternalId(self, t):
        r'PUBLIC\s+"-//NLM//DTD\s+health-topics\s+//EN"\s+"https://medlineplus.gov/xml/mplus_topics.dtd"'
        return t

    # Keys of attributes
    def t_VersionKey(self, t):
        r'version='
        return t

    def t_EncodingKey(self, t):
        r'encoding='
        return t

    def t_DateGeneratedKey(self, t):
        r'date-generated='
        return t

    def t_TotalKey(self, t):
        r'total='
        return t

    def t_IdKey(self, t):
        r'id='
        return t

    def t_DateCreatedKey(self, t):
        r'date-created='
        return t

    def t_LanguageKey(self, t):
        r'language='
        return t

    def t_TitleKey(self, t):
        r'title='
        return t

    def t_UrlKey(self, t):
        r'url='
        return t

    def t_MetaDescKey(self, t):
        r'meta-desc='
        return t

    def t_VernacularNameKey(self, t):
        r'vernacular-name='
        return t

    def t_LanguageMappedUrlKey(self, t):
        r'language-mapped-url='
        return t

    # Value types of attributes
    def t_Date(self, t):
        r'"\d{2}/\d{2}/\d{4}"'
        value = t.value
        t.value = datetime.strptime(value.replace('"', ''), "%m/%d/%Y").date()
        return t

    def t_Timestamp(self, t):
        r'"\d{2}/\d{2}/\d{4}\s\d{2}:\d{2}:\d{2}"'
        value = t.value
        t.value = datetime.strptime(value.replace('"', ''), "%m/%d/%Y %H:%M:%S")
        return t

    def t_Integer(self, t):
        r'"\d+"'
        value = t.value
        t.value = int(value.replace('"', ''))
        return t

    def t_Language(self, t):
        r'"(English|Spanish)"'
        t.value = t.value.replace('"', '')
        return t

    def t_Uri(self, t):
        r'"(?:https?):\/\/[^\s/$.?#].[^\s"<>]*[^"<>]*"'
        t.value = self._replace_html_entities(t.value.replace('"', ''))
        return t

    def t_String(self, t):
        r'"[^"]+"'
        t.value = self._replace_html_entities(t.value.replace('"', ''))
        return t

    def t_Line(self, t):
        r'[\w ¿?¡!:;,#&=+°•\.\-\'\"%\*\{\}\[\]\(\)/\t]+'
        t.value = self._replace_html_entities(t.value)
        return t

    # Define a rule so we can track line numbers
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # Error handling rule
    def t_error(self, t):
        raise Exception(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")

    # Post processing function to replace html entities
    def _replace_html_entities(self, t_value):
        for entity, char in self._entity_replacements.items():
            t_value = t_value.replace(entity, char)
        return t_value

    def build(self, **kwargs):
        self._lexer = lex.lex(module=self, **kwargs)
        return self._lexer