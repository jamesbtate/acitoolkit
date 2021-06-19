"""
...module docstring here...
"""
from .acisession import Session
from .aciphysobject import Fabric
from .acibaseobject import BaseACIObject


class LogicalModel(BaseACIObject):
    """
    This is the root class for the logical part of the network.
    Its corollary is the PhysicalModel class.
    It is a container that can hold all of logical model instances such as Tenants.

    From this class, you can populate all of the children classes.
    """

    def __init__(self, session=None, parent=None):
        """
        Initialization method that sets up the Fabric.
        :return:
        """
        if session:
            assert isinstance(session, Session)

        # if parent:
        #     assert isinstance(parent, Fabric)

        super(LogicalModel, self).__init__(name='', parent=parent)

        self._session = session
        self.dn = 'logical'

    @staticmethod
    def _get_parent_class():
        """
        Gets the class of the parent object

        :returns: class of parent object
        """
        return Fabric

    @classmethod
    def _get_name_from_dn(cls, dn):
        """
        Parse the name out of a dn string.
        Meant to be overridden by inheriting classes.
        Raises exception if not overridden.

        :returns: string containing name
        """
        return None

    @staticmethod
    def _get_parent_dn(dn):
        """
        Gets the dn of the parent object
        Meant to be overridden by inheriting classes.
        Raises exception if not overridden.

        :returns: string containing dn
        """
        return None

    @classmethod
    def get(cls, session=None, parent=None):
        """
        Method to get all of the LogicalModels.  It will get one and return it in a list.

        :param session:
        :param parent:
        :return: list of LogicalModel
        """
        logical_model = LogicalModel(session=session, parent=parent)
        return [logical_model]

    @staticmethod
    def _get_children_classes():
        """
        Get the acitoolkit class of the children of this object.
        This is meant to be overridden by any inheriting classes that have children.
        If they don't have children, this will return an empty list.
        :return: list of classes
        """
        # need to put these imports here instead of top of file to prevent circular import.
        # this goofy project has "parent" classes that reference "child" classes.
        #   (parent and child used in reference to APIC API, not Python classes)
        # this explains why acitoolit.py is a mega file with all the classes...
        from .aaep import AAEP
        from .acitoolkit import PhysDomain, Tenant
        return [Tenant, PhysDomain, AAEP]

    @classmethod
    def _get_apic_classes(cls):
        """
        Get the APIC classes used by the acitoolkit class.
        Meant to be overridden by inheriting classes.
        Raises exception if not overridden.

        :returns: list of strings containing APIC class names
        """
        return []

    def populate_children(self, deep=False, include_concrete=False):
        """
        Populates all of the children and then calls populate_children\
        of those children if deep is True.  This method should be\
        overridden by any object that does have children.

        If include_concrete is True, then if the object has concrete objects
        below it, i.e. is a switch, then also populate those conrete object.

        :param include_concrete: True or False. Default is False
        :param deep: True or False.  Default is False.
        """
        for child_class in self._get_children_classes():
            if deep:
                child_class.get_deep(self._session, parent=self)
            else:
                child_class.get(self._session, self)

        return self._children

    def _define_searchables(self):
        """
        Create all of the searchable terms

        """
        results = super(LogicalModel, self)._define_searchables()
        results[0].add_term('model', 'logical')

        return results
