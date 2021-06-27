"""
...module docstring here...
"""
import logging
from .acibaseobject import BaseACIObject
from .acitoolkit import EPG

log = logging.getLogger(__name__)


class AAEP_EPG(BaseACIObject):
    """ Represents a 'infraRsFuncToEpg' in APIC API (EPG attachment to AAEP)

    This object specifies an EPG with a certain encapsulation attached to an AAEP. Technically,
    a infraRsFuncToEpg is a relationship from a function to to an EPG. An AAEP has one automatic
    function of class 'infraGeneric' with name 'default'. The EPGs are attached to this object.
    """

    def __init__(self, parent, epg=None, encap=None):
        """ Constructor

        :param epg: the EPG this attachment is for
        :param parent: the AccessEntityProfile the EPG is attached to
        :param encap: the string representation of the encapsulation e.g. 'vlan-123'
        """
        if parent:
            if not isinstance(parent, AAEP):
                raise TypeError("Parent must be instance of AccessEntityProfile")
        if epg:
            if not isinstance(epg, EPG):
                raise TypeError("epg parameter must be instance of EPG class")
        super(AAEP_EPG, self).__init__('asdf', parent)
        self.dn = None
        self.lcOwn = None
        self.childAction = None
        self.epg = epg
        if epg:
            self.tDn = epg.dn
        else:
            self.tDn = None
        if encap:
            if not self.is_valid_encap(encap):
                raise ValueError("Invalid encapsulation string: " + str(encap)[:20])
        self.encap = encap

    @classmethod
    def _get_apic_classes(cls):
        """ Get the APIC classes used by this acitoolkit class.

        :returns: list of strings containing APIC class names
        """
        return ['infraRsFuncToEpg']

    @staticmethod
    def _get_parent_class():
        """ Gets the class of the parent object

        :returns: class of parent object
        """
        return AAEP

    def get_parent(self):
        """
        :returns: Parent of this object.
        """
        return self._parent

    def get_json(self):
        """ Returns json representation of the physDomP object

        :returns: A json dictionary of physical domain
        """
        attr = self._generate_attributes()
        return super(AAEP_EPG, self).get_json(self._get_apic_classes()[0], attributes=attr)

    @staticmethod
    def get_url(fmt='json'):
        """
        Get the URL used to push the configuration to the APIC
        if no format parameter is specified, the format will be 'json'
        otherwise it will return '/api/mo/uni.' with the format string
        appended.

        :param fmt: optional format string, default is 'json'
        :returns: URL string
        """
        return '/api/mo/uni.' + fmt

    def push_to_apic(self, session):
        """
        Push the appropriate configuration to the APIC for this Phys Domain.
        All of the subobject configuration will also be pushed.

        :param session: the instance of Session used for APIC communication
        :returns: Requests Response code
        """
        resp = session.push_to_apic(self.get_url(),
                                    self.get_json())
        return resp

    @classmethod
    def get(cls, session):
        """ Gets all the EPG Attachments from the APIC

        :param session: the instance of Session used for APIC communication
        :returns: List of EPGAttachment objects
        """
        toolkit_class = cls
        apic_class = cls._get_apic_classes()[0]
        parent = None
        log.debug('%s.get called', cls.__name__)
        return super(AAEP_EPG, cls).get(session, toolkit_class, apic_class, parent)

    def _generate_attributes(self):
        """
        Gets the attributes used in generating the JSON for the object
        """
        attributes = dict()
        if self.dn:
            attributes['dn'] = self.dn
        if self.lcOwn:
            attributes['lcOwn'] = self.lcOwn
        if self.childAction:
            attributes['childAction'] = self.childAction
        if self.tDn:
            attributes['tDn'] = self.tDn
        if self.encap:
            attributes['encap'] = self.encap
        return attributes

    def _populate_from_attributes(self, attributes):
        """ Fills in an object with the desired attributes from APIC API.

        :param attributes: dictionary of attributes of this object from APIC API
        """
        self.dn = self.get_dn_from_attributes(attributes)
        self.lcOwn = attributes.get('lcOwn')
        self.childAction = attributes.get('childAction')
        self.tDn = attributes.get('tDn')
        self.encap = attributes.get('encap')

    @staticmethod
    def is_valid_encap(encap):
        """ Return True if the encap argument is a valid encapsulation string. False otherwise.

        Currently only 802.1q encapsulation is supported. untagged is not supported.

        Examples of valid encaps:
        'vlan-123'
        'vlan-0001'
        'vlan-4094'

        :param encap: string specifying encapsulation
        :return: True or False
        """
        if not type(encap) is str:
            return False
        if encap[:5] != 'vlan-':
            return False
        try:
            vlan = int(encap[5:])
        except ValueError:
            return False
        if vlan < 1 or vlan > 4094:
            return False
        return True


class AAEP_PhysDomain(BaseACIObject):
    """ Represents a 'infraRsDomP' in APIC API (pdom attachment to AAEP)

    This object specifies a particular physical domain attached to a particular AAEP
    """

    @classmethod
    def _get_apic_classes(cls):
        """ Get the APIC classes used by this acitoolkit class.

        :returns: list of strings containing APIC class names
        """
        return ['infraRsDomP']

    @staticmethod
    def _get_parent_class():
        """ Gets the class of the parent object

        :returns: class of parent object
        """
        return AAEP

    def get_parent(self):
        """
        :returns: Parent of this object.
        """
        return self._parent


class AAEP(BaseACIObject):
    """ (Attachable) Access Entity Profile (AAEP)

    Represents an AAEP which has associations with physical domains and EPGs.
    Interface policy groups also refer to this object.
    """

    def __init__(self, name, parent=None):
        """
        :param name: String containing the AccessEntityProfile name
        :param parent: The logical model or None
        """
        self.dn = None
        self.lcOwn = None
        self.childAction = None
        self.descr = None
        self.name = name
        super(AAEP, self).__init__(name, parent)


    def get_json(self):
        """
        Returns json representation of the physDomP object

        :returns: A json dictionary of physical domain
        """
        attr = self._generate_attributes()
        children = []
        return super(AAEP, self).get_json(self._get_apic_classes()[0],
                                          attributes=attr,
                                          children=children)

    def _generate_attributes(self):
        """
        Gets the attributes used in generating the JSON for the object
        """
        attributes = dict()
        if self.name:
            attributes['name'] = self.name
        if self.descr:
            attributes['descr'] = self.descr
        if self.dn:
            attributes['dn'] = self.dn
        if self.lcOwn:
            attributes['lcOwn'] = self.lcOwn
        if self.childAction:
            attributes['childAction'] = self.childAction
        return attributes

    @classmethod
    def _get_apic_classes(cls):
        """
        Get the APIC classes used by this acitoolkit class.

        :returns: list of strings containing APIC class names
        """
        return ['infraAttEntityP']

    def get_parent(self):
        """
        :returns: Parent of this object.
        """
        return self._parent

    @staticmethod
    def get_url(fmt='json'):
        """
        Get the URL used to push the configuration to the APIC
        if no format parameter is specified, the format will be 'json'
        otherwise it will return '/api/mo/uni.' with the format string
        appended.

        :param fmt: optional format string, default is 'json'
        :returns: URL string
        """
        return '/api/mo/uni/infra.' + fmt

    def push_to_apic(self, session):
        """
        Push the appropriate configuration to the APIC for this Phys Domain.
        All of the subobject configuration will also be pushed.

        :param session: the instance of Session used for APIC communication
        :returns: Requests Response code
        """
        resp = session.push_to_apic(self.get_url(),
                                    self.get_json())
        return resp

    @classmethod
    def get(cls, session, parent=None):
        """
        Gets all of the Physical Domains from the APIC

        :param session: the instance of Session used for APIC communication
        :returns: List of AccessEntityProfile objects

        """
        toolkit_class = cls
        apic_class = cls._get_apic_classes()[0]
        log.debug('%s.get called', cls.__name__)
        query_url = (('/api/mo/uni.json?query-target=subtree&'
                      'target-subtree-class=') + str(apic_class))
        ret = session.get(query_url)
        data = ret.json()['imdata']

        log.debug('response returned %s', data)
        resp = []
        for object_data in data:
            name = str(object_data[apic_class]['attributes']['name'])
            obj = toolkit_class(name, parent)
            attribute_data = object_data[apic_class]['attributes']
            obj._populate_from_attributes(attribute_data)
            obj.dn = object_data[apic_class]['attributes']['dn']
            obj.lcOwn = object_data[apic_class]['attributes']['lcOwn']
            obj.childAction = object_data[apic_class]['attributes']['childAction']
            resp.append(obj)
        return resp

    def get_epg_attachments_from_apic(self, session):
        """
        Get the 'infraRsFuncToEpg'
        :param session:
        :return:
        """
        pass
        # todo

    @classmethod
    def get_by_name(cls, session, aaep_name):
        """
        Gets a particular AAEP from the APIC by name

        :param aaep_name:
        :param session: the instance of Session used for APIC communication
        :returns: List of AccessEntityProfile objects
        """
        toolkit_class = cls
        apic_class = cls._get_apic_classes()[0]
        parent = None
        log.debug('%s.get called', cls.__name__)
        query_url = (('/api/mo/uni.json?query-target=subtree&'
                      'target-subtree-class=') + str(apic_class))
        ret = session.get(query_url)
        data = ret.json()['imdata']
        log.debug('response returned %s', data)
        for object_data in data:
            name = str(object_data[apic_class]['attributes']['name'])
            obj = toolkit_class(name, parent)
            attribute_data = object_data[apic_class]['attributes']
            obj._populate_from_attributes(attribute_data)
            obj.dn = object_data[apic_class]['attributes']['dn']
            obj.lcOwn = object_data[apic_class]['attributes']['lcOwn']
            obj.childAction = object_data[apic_class]['attributes']['childAction']
            obj.descr = object_data[apic_class]['attributes']['descr']
            if name == aaep_name:
                return obj
        return None

    # @staticmethod
    # def _get_children_classes():
    #     return ['infraGeneric', 'infraRsDomP', 'infraRtAttEntP']
