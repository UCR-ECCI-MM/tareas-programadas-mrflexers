import os
from io import BytesIO

import ply.yacc as yacc

from .constants import *
from .lexing import XmlLexer

class XmlParser:

    @staticmethod
    def parse_file(file: BytesIO) -> dict:
        """Parses the XML file and returns the parsed data."""
        data = file.read().decode('utf-8')
        return _Parser().parse(data)

class _Parser:
    _OUTPUT_FOLDER = './xml_parser'
    _TAB_MODULE = 'parser.parsetab'

    _token_to_key = {
        'AlsoCalled': ALSO_CALLED,
        'AlsoCalledList': ALSO_CALLED,
        'DateCreatedKey': DATE_CREATED,
        'DateGeneratedKey': DATE_GENERATED,
        'Descriptor': DESCRIPTOR,
        'DocTypeDeclExternalId': EXTERNAL_ID,
        'DocTypeDeclName': NAME,
        'EncodingKey': ENCODING,
        'FullSummary': FULL_SUMMARY,
        'Group': GROUP,
        'GroupList': GROUP,
        'HealthTopicList': HEALTH_TOPIC,
        'HealthTopics': HEALTH_TOPICS,
        'IdKey': ID,
        'InformationCategoryList': INFORMATION_CATEGORY,
        'LanguageKey': LANGUAGE,
        'LanguageMappedTopic': LANGUAGE_MAPPED_TOPIC,
        'LanguageMappedTopicOpt': LANGUAGE_MAPPED_TOPIC,
        'LanguageMappedUrlKey': LANGUAGE_MAPPED_URL,
        'MeshHeading': MESH_HEADING,
        'MeshHeadingList': MESH_HEADING,
        'MetaDescKey': META_DESC,
        'OrganizationList': ORGANIZATION,
        'OtherLanguage': OTHER_LANGUAGE,
        'OtherLanguageList': OTHER_LANGUAGE,
        'PrimaryInstitute': PRIMARY_INSTITUTE,
        'PrimaryInstituteOpt': PRIMARY_INSTITUTE,
        'QualifierList': QUALIFIER,
        'QualifierListOpt': QUALIFIER,
        'RelatedTopic': RELATED_TOPIC,
        'RelatedTopicList': RELATED_TOPIC,
        'SeeReference': SEE_REFERENCE,
        'SeeReferenceList': SEE_REFERENCE,
        'Site': SITE,
        'SiteList': SITE,
        'StandardDescriptionList': STANDARD_DESCRIPTION,
        'Text': TEXT,
        'TitleKey': TITLE,
        'TotalKey': TOTAL,
        'UrlKey': URL,
        'VernacularNameKey': VERNACULAR_NAME,
        'VersionKey': VERSION
    }

    @classmethod
    def _parse_child_tokens(cls, rule):
        return rule.split(':')[1].strip().split()

    @classmethod
    def _handle_element(cls, rule, p):
        child_tokens = cls._parse_child_tokens(rule)

        children = p[1:]

        attr_idx = next((i for i, string in enumerate(child_tokens) if 'Attributes' in string), -1)
        content_idx = next((i for i, string in enumerate(child_tokens) if 'Content' in string), -1)
        text_idx = child_tokens.index('Text') if 'Text' in child_tokens else -1

        parent = {}

        if attr_idx != -1:
            parent.update(children[attr_idx])

        if content_idx != -1:
            parent.update(children[content_idx])

        if text_idx != -1:
            text = children[text_idx].rstrip()

            if parent:
                parent[cls._token_to_key['Text']] = text
            else:
                parent = text

        return parent

    @classmethod
    def _handle_content(cls, rule, p):
        child_tokens = cls._parse_child_tokens(rule)

        children = p[1:]

        existing_children_indices = [i for i, child in enumerate(children) if child is not None]

        parent = {cls._token_to_key[child_tokens[i]]: children[i] for i in existing_children_indices}

        return parent

    @classmethod
    def _handle_attributes(cls, rule, p):
        child_tokens = cls._parse_child_tokens(rule)

        children = p[1:]

        parent = {cls._token_to_key[child_tokens[i]]: children[i + 1] for i in range(0, len(child_tokens), 2)}

        return parent

    @classmethod
    def _handle_list(cls, p):
        if len(p) == 3:
            parent = [p[1]] + p[2] if isinstance(p[2], list) else [p[1], p[2]]
        else:
            parent = p[1]  # Cant be empty

        return parent

    @classmethod
    def _handle_optional_list(cls, p):
        parent = None

        if len(p) == 3:
            if p[2] is None:
                parent = p[1]
            else:
                parent = [p[1]] + p[2] if isinstance(p[2], list) else [p[1], p[2]]

        return parent

    def __init__(self):
        if not os.path.exists(self._OUTPUT_FOLDER):
            os.makedirs(self._OUTPUT_FOLDER)

        self.lexer = XmlLexer()
        self.tokens = self.lexer.tokens
        self.parser = yacc.yacc(module=self, outputdir=self._OUTPUT_FOLDER, tabmodule=self._TAB_MODULE)

    # Parsing rules
    def p_Document(self, p):
        'Document : Prolog HealthTopics'
        p[0] = {
            **p[1],
            self._token_to_key['HealthTopics']: p[2]
        }

    def p_Prolog(self, p):
        'Prolog : XmlDeclStartTag XmlDeclAttributes XmlDeclEndTag DocTypeDeclStartTag DocTypeDeclName DocTypeDeclExternalId StartTagClose'
        p[0] = {
            **p[2],
            'doctype': {
                self._token_to_key['DocTypeDeclName']: p[5],
                self._token_to_key['DocTypeDeclExternalId']: p[6]
            }
        }

    def p_XmlDeclAttributes(self, p):
        'XmlDeclAttributes : VersionKey String EncodingKey String'
        p[0] = self._handle_attributes(self.p_XmlDeclAttributes.__doc__, p)

    def p_HealthTopics(self, p):
        'HealthTopics : HealthTopicsStartTagOpen HealthTopicsAttributes StartTagClose HealthTopicsContent HealthTopicsEndTag'
        p[0] = self._handle_element(self.p_HealthTopics.__doc__, p)

    def p_HealthTopicsContent(self, p):
        'HealthTopicsContent : HealthTopicList'
        p[0] = self._handle_content(self.p_HealthTopicsContent.__doc__, p)

    def p_HealthTopicsAttributes(self, p):
        'HealthTopicsAttributes : TotalKey Integer DateGeneratedKey Timestamp'
        p[0] = self._handle_attributes(self.p_HealthTopicsAttributes.__doc__, p)

    def p_HealthTopicList(self, p):
        '''HealthTopicList : HealthTopic HealthTopicList
        | HealthTopic'''
        p[0] = self._handle_list(p)

    def p_HealthTopic(self, p):
        'HealthTopic : HealthTopicStartTagOpen HealthTopicAttributes StartTagClose HealthTopicContent HealthTopicEndTag'
        p[0] = self._handle_element(self.p_HealthTopic.__doc__, p)

    def p_HealthTopicAttributes(self, p):
        'HealthTopicAttributes : MetaDescKey String TitleKey String UrlKey Uri IdKey Integer LanguageKey Language DateCreatedKey Date'
        p[0] = self._handle_attributes(self.p_HealthTopicAttributes.__doc__, p)

    def p_HealthTopicContent(self, p):
        'HealthTopicContent : AlsoCalledList FullSummary GroupList LanguageMappedTopicOpt MeshHeadingList OtherLanguageList PrimaryInstituteOpt RelatedTopicList SeeReferenceList SiteList'
        p[0] = self._handle_content(self.p_HealthTopicContent.__doc__, p)

    def p_AlsoCalledList(self, p):
        '''AlsoCalledList : AlsoCalled AlsoCalledList
        | empty'''
        p[0] = self._handle_optional_list(p)

    def p_GroupList(self, p):
        '''GroupList : Group GroupList
        | empty'''
        p[0] = self._handle_optional_list(p)

    def p_LanguageMappedTopicOpt(self, p):
        '''LanguageMappedTopicOpt : LanguageMappedTopic
        | empty'''
        p[0] = p[1]

    def p_MeshHeadingList(self, p):
        '''MeshHeadingList : MeshHeading MeshHeadingList
        | empty'''
        p[0] = self._handle_optional_list(p)

    def p_OtherLanguageList(self, p):
        '''OtherLanguageList : OtherLanguage OtherLanguageList
        | empty'''
        p[0] = self._handle_optional_list(p)

    def p_PrimaryInstituteOpt(self, p):
        '''PrimaryInstituteOpt : PrimaryInstitute
        | empty'''
        p[0] = p[1]

    def p_RelatedTopicList(self, p):
        '''RelatedTopicList : RelatedTopic RelatedTopicList
        | empty'''
        p[0] = self._handle_optional_list(p)

    def p_SeeReferenceList(self, p):
        '''SeeReferenceList : SeeReference SeeReferenceList
        | empty'''
        p[0] = self._handle_optional_list(p)

    def p_SiteList(self, p):
        '''SiteList : Site SiteList
        | empty'''
        p[0] = self._handle_optional_list(p)

    def p_FullSummary(self, p):
        'FullSummary : FullSummaryStartTagOpen StartTagClose Text FullSummaryEndTag'
        p[0] = self._handle_element(self.p_FullSummary.__doc__, p)

    def p_Group(self, p):
        'Group : GroupStartTagOpen GroupAttributes StartTagClose Text GroupEndTag'
        p[0] = self._handle_element(self.p_Group.__doc__, p)

    def p_GroupAttributes(self, p):
        'GroupAttributes : UrlKey Uri IdKey Integer'
        p[0] = self._handle_attributes(self.p_GroupAttributes.__doc__, p)

    def p_LanguageMappedTopic(self, p):
        'LanguageMappedTopic : LanguageMappedTopicStartTagOpen LanguageMappedTopicAttributes StartTagClose Text LanguageMappedTopicEndTag'
        p[0] = self._handle_element(self.p_LanguageMappedTopic.__doc__, p)

    def p_LanguageMappedTopicAttributes(self, p):
        'LanguageMappedTopicAttributes : UrlKey Uri IdKey Integer LanguageKey Language'
        p[0] = self._handle_attributes(self.p_LanguageMappedTopicAttributes.__doc__, p)

    def p_MeshHeading(self, p):
        'MeshHeading : MeshHeadingStartTagOpen StartTagClose MeshHeadingContent MeshHeadingEndTag'
        p[0] = self._handle_element(self.p_MeshHeading.__doc__, p)

    def p_MeshHeadingContent(self, p):
        'MeshHeadingContent : Descriptor QualifierListOpt'
        p[0] = self._handle_content(self.p_MeshHeadingContent.__doc__, p)

    def p_QualifierListOpt(self, p):
        '''QualifierListOpt : QualifierList
        | empty'''
        p[0] = p[1]

    def p_QualifierList(self, p):
        '''QualifierList : Qualifier QualifierList
        | empty'''
        p[0] = self._handle_optional_list(p)

    def p_OtherLanguage(self, p):
        'OtherLanguage : OtherLanguageStartTagOpen OtherLanguageAttributes StartTagClose Text OtherLanguageEndTag'
        p[0] = self._handle_element(self.p_OtherLanguage.__doc__, p)

    def p_OtherLanguageAttributes(self, p):
        'OtherLanguageAttributes : VernacularNameKey String UrlKey Uri'
        p[0] = self._handle_attributes(self.p_OtherLanguageAttributes.__doc__, p)

    def p_PrimaryInstitute(self, p):
        'PrimaryInstitute : PrimaryInstituteStartTagOpen PrimaryInstituteAttributes StartTagClose Text PrimaryInstituteEndTag'
        p[0] = self._handle_element(self.p_PrimaryInstitute.__doc__, p)

    def p_PrimaryInstituteAttributes(self, p):
        'PrimaryInstituteAttributes : UrlKey Uri'
        p[0] = self._handle_attributes(self.p_PrimaryInstituteAttributes.__doc__, p)

    def p_RelatedTopic(self, p):
        'RelatedTopic : RelatedTopicStartTagOpen RelatedTopicAttributes StartTagClose Text RelatedTopicEndTag'
        p[0] = self._handle_element(self.p_RelatedTopic.__doc__, p)

    def p_RelatedTopicAttributes(self, p):
        'RelatedTopicAttributes : UrlKey Uri IdKey Integer'
        p[0] = self._handle_attributes(self.p_RelatedTopicAttributes.__doc__, p)

    def p_SeeReference(self, p):
        'SeeReference : SeeReferenceStartTagOpen StartTagClose Text SeeReferenceEndTag'
        p[0] = self._handle_element(self.p_SeeReference.__doc__, p)

    def p_Site(self, p):
        'Site : SiteStartTagOpen SiteAttributes StartTagClose SiteContent SiteEndTag'
        p[0] = self._handle_element(self.p_Site.__doc__, p)

    def p_SiteContent(self, p):
        'SiteContent : InformationCategoryList OrganizationList StandardDescriptionList'
        p[0] = self._handle_content(self.p_SiteContent.__doc__, p)

    def p_InformationCategoryList(self, p):
        '''InformationCategoryList : InformationCategory InformationCategoryList
        | InformationCategory'''
        p[0] = self._handle_list(p)

    def p_OrganizationList(self, p):
        '''OrganizationList : Organization OrganizationList
        | empty'''
        p[0] = self._handle_optional_list(p)

    def p_StandardDescriptionList(self, p):
        '''StandardDescriptionList : StandardDescription StandardDescriptionList
        | empty'''
        p[0] = self._handle_optional_list(p)

    def p_SiteAttributes_full(self, p):
        '''SiteAttributes : TitleKey String UrlKey Uri LanguageMappedUrlKey Uri'''
        p[0] = self._handle_attributes(self.p_SiteAttributes_full.__doc__, p)

    def p_SiteAttributes_partial(self, p):
        '''SiteAttributes : TitleKey String UrlKey Uri'''
        p[0] = self._handle_attributes(self.p_SiteAttributes_partial.__doc__, p)

    def p_AlsoCalled(self, p):
        'AlsoCalled : AlsoCalledStartTagOpen StartTagClose Text AlsoCalledEndTag'
        p[0] = self._handle_element(self.p_AlsoCalled.__doc__, p)

    def p_Descriptor(self, p):
        'Descriptor : DescriptorStartTagOpen DescriptorAttributes StartTagClose Text DescriptorEndTag'
        p[0] = self._handle_element(self.p_Descriptor.__doc__, p)

    def p_DescriptorAttributes(self, p):
        'DescriptorAttributes : IdKey String'
        p[0] = self._handle_attributes(self.p_DescriptorAttributes.__doc__, p)

    def p_Qualifier(self, p):
        'Qualifier : QualifierStartTagOpen QualifierAttributes StartTagClose Text QualifierEndTag'
        p[0] = self._handle_element(self.p_Qualifier.__doc__, p)

    def p_QualifierAttributes(self, p):
        'QualifierAttributes : IdKey String'
        p[0] = self._handle_attributes(self.p_QualifierAttributes.__doc__, p)

    def p_InformationCategory(self, p):
        'InformationCategory : InformationCategoryStartTagOpen StartTagClose Text InformationCategoryEndTag'
        p[0] = self._handle_element(self.p_InformationCategory.__doc__, p)

    def p_Organization(self, p):
        'Organization : OrganizationStartTagOpen StartTagClose Text OrganizationEndTag'
        p[0] = self._handle_element(self.p_Organization.__doc__, p)

    def p_StandardDescription(self, p):
        'StandardDescription : StandardDescriptionStartTagOpen StartTagClose Text StandardDescriptionEndTag'
        p[0] = self._handle_element(self.p_StandardDescription.__doc__, p)

    def p_Text(self, p):
        '''Text : Text Line
        | Text String
        | Line'''
        # Set the content of the element
        p[0] = p[1] + p[2] if len(p) == 3 else p[1]

    def p_empty(self, p):
        'empty : '
        p[0] = None

    def p_error(self, p):
        if p:
            raise Exception(f"Syntax error at '{p.value}' on line {p.lineno}")
        else:
            raise Exception("Syntax error at EOF")

    def parse(self, data):
        """Parses the input data."""
        result = self.parser.parse(data, lexer=self.lexer)

        if result is None:
            raise ValueError("Input data is invalid.")

        return result